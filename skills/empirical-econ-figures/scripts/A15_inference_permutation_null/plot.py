"""Plot supplied null draws and compute finite-permutation tail counts."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont

TEXT = {
    "en": {"x": "Statistic", "y": "Share of permutations", "title": "Permutation null distribution"},
    "zh": {"x": "统计量", "y": "置换所占比例", "title": "置换零分布"},
}

def font(lang: str) -> None:
    if lang == "zh":
        for family in ("Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "Source Han Sans SC"):
            try:
                findfont(FontProperties(family=family), fallback_to_default=False)
                plt.rcParams["font.family"] = family
                break
            except ValueError:
                continue
        else:
            raise RuntimeError("A CJK font is required")
    else:
        plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False

def read(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    required = {"panel", "panel_order", "panel_label_en", "panel_label_zh", "draw_id", "null_stat", "observed_stat"}
    if not required.issubset(df):
        raise ValueError(f"missing columns: {sorted(required-set(df))}")
    if df[list(required)].eq("").any().any():
        raise ValueError("blank required field")
    for col in ("panel_order", "null_stat", "observed_stat"):
        df[col] = pd.to_numeric(df[col], errors="raise")
        if not np.isfinite(df[col]).all():
            raise ValueError(f"nonfinite {col}")
    if df.duplicated(["panel", "draw_id"]).any():
        raise ValueError("duplicate panel/draw_id")
    meta = df[["panel", "panel_order", "panel_label_en", "panel_label_zh", "observed_stat"]].drop_duplicates()
    if meta.panel.duplicated().any() or meta.panel_order.duplicated().any():
        raise ValueError("inconsistent panel metadata or observed statistic")
    if sorted(meta.panel_order.tolist()) != list(range(1, len(meta)+1)):
        raise ValueError("panel_order must be consecutive from 1")
    if not 1 <= len(meta) <= 4:
        raise ValueError("one to four panels required")
    return df.sort_values(["panel_order", "draw_id"])

def infer(df: pd.DataFrame, tail: str, center: float | None) -> pd.DataFrame:
    if tail == "two-sided" and (center is None or not np.isfinite(center)):
        raise ValueError("two-sided tail requires an explicit finite --null-center")
    rows = []
    for order, part in df.groupby("panel_order", sort=True):
        observed = float(part.observed_stat.iloc[0])
        draws = part.null_stat.to_numpy(float)
        if tail == "right":
            extreme = int(np.count_nonzero(draws >= observed))
        elif tail == "left":
            extreme = int(np.count_nonzero(draws <= observed))
        else:
            extreme = int(np.count_nonzero(np.abs(draws-center) >= abs(observed-center)))
        rows.append({"panel": part.panel.iloc[0], "panel_order": int(order), "draws": len(draws),
                     "extreme": extreme, "observed_stat": observed, "tail": tail,
                     "null_center": "" if center is None else center,
                     "p_finite": (extreme+1)/(len(draws)+1)})
    return pd.DataFrame(rows)

def draw(df: pd.DataFrame, results: pd.DataFrame, lang: str, output: Path, title: bool,
         xmin: float, xmax: float, width: float) -> None:
    if not np.isfinite([xmin, xmax, width]).all() or not (xmin < xmax and width > 0):
        raise ValueError("invalid axis or bin width")
    n_bins = (xmax-xmin)/width
    if abs(n_bins-round(n_bins)) > 1e-8:
        raise ValueError("bin width must divide the plotted range exactly")
    if df.null_stat.min() < xmin or df.null_stat.max() > xmax or df.observed_stat.min() < xmin or df.observed_stat.max() > xmax:
        raise ValueError("axis must contain all draws and observed statistics")
    font(lang)
    count = len(results)
    fig, axes = plt.subplots(1, count, figsize=(4.4*count+1.0, 4.4), sharey=False, squeeze=False, dpi=160)
    axes = axes[0]
    edges = np.linspace(xmin, xmax, round(n_bins)+1)
    for ax, row in zip(axes, results.itertuples()):
        part = df[df.panel_order == row.panel_order]
        ax.hist(part.null_stat, bins=edges, weights=np.full(len(part), 1/len(part)),
                color="#9c9c9c", edgecolor="#888888", linewidth=.2)
        ax.axvline(row.observed_stat, color="#d44b52", linestyle=(0, (5, 3)), linewidth=1.6)
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(bottom=0)
        ax.set_xlabel(TEXT[lang]["x"], fontsize=10)
        ax.set_ylabel(TEXT[lang]["y"], fontsize=10)
        if count > 1:
            ax.set_title(part[f"panel_label_{lang}"].iloc[0], fontsize=11)
        ax.grid(axis="y", color="#e5e5e5", linewidth=.55, zorder=0)
        ax.spines[["top", "right"]].set_visible(False)
    if title:
        fig.suptitle(TEXT[lang]["title"], fontsize=12)
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=240)
    fig.savefig(output.with_suffix(".pdf"))
    plt.close(fig)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, default=Path(__file__).with_name("demo.csv"))
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--lang", choices=TEXT, default="en")
    p.add_argument("--tail", choices=("right", "left", "two-sided"), default="right")
    p.add_argument("--null-center", type=float)
    p.add_argument("--xmin", type=float, default=0.0)
    p.add_argument("--xmax", type=float, default=1.0)
    p.add_argument("--binwidth", type=float, default=.01)
    p.add_argument("--title", action="store_true")
    a = p.parse_args()
    df = read(a.input)
    results = infer(df, a.tail, a.null_center)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(a.output.with_name(f"{a.output.stem}_results.csv"), index=False, float_format="%.12g")
    draw(df, results, a.lang, a.output, a.title, a.xmin, a.xmax, a.binwidth)
    print(f"PYTHON_COMPLETE rows={len(df)} panels={len(results)} tail={a.tail} output={a.output}")

if __name__ == "__main__":
    main()
