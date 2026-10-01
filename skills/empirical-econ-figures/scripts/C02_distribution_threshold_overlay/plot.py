"""Weighted binned-density overlay with explicit thresholds and tail shares."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont

# Edit series/threshold IDs, labels, and axes together for another study.
SERIES = (
    ("earlier", "Earlier", "早期", "#b1b1b1", "absolute"),
    ("later", "Later", "后期", "#4d4d4d", "comparison"),
)
THRESHOLDS = (
    ("absolute", 20000.0, "Common threshold", "共同阈值", "#777777"),
    ("comparison", 30000.0, "Comparison threshold", "比较阈值", "#242424"),
)
TEXT = {
    "en": {"x": "Value (synthetic units)", "y": "Weighted share per bin (%)",
           "title": "Distributions and thresholds"},
    "zh": {"x": "数值（合成单位）", "y": "每组距的加权比例（%）",
           "title": "分布与阈值"},
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
    if not {"id", "series", "value", "weight"}.issubset(df):
        raise ValueError("missing id, series, value, or weight")
    if df[["id", "series", "value", "weight"]].eq("").any().any() or df.id.duplicated().any():
        raise ValueError("blank field or duplicate id")
    if set(df.series) != {row[0] for row in SERIES}:
        raise ValueError("series IDs must match SERIES configuration")
    for col in ("value", "weight"):
        df[col] = pd.to_numeric(df[col], errors="raise")
        if not np.isfinite(df[col]).all():
            raise ValueError(f"nonfinite {col}")
    if (df.value < 0).any() or (df.weight < 0).any():
        raise ValueError("value and weight must be nonnegative")
    if (df.groupby("series").weight.sum() <= 0).any():
        raise ValueError("each series needs positive total weight")
    return df

def calculate(df: pd.DataFrame, xmin: float, xmax: float, width: float) -> tuple[np.ndarray, dict, pd.DataFrame]:
    if not np.isfinite([xmin, xmax, width]).all() or not (xmin == 0 and xmin < xmax and width > 0):
        raise ValueError("bins must start at zero, with positive xmax and width")
    n = (xmax-xmin)/width
    if abs(n-round(n)) > 1e-8:
        raise ValueError("bin width must divide plotting range exactly")
    edges = np.linspace(xmin, xmax, round(n)+1)
    for _tid, threshold, *_ in THRESHOLDS:
        if not (xmin <= threshold <= xmax) or np.min(np.abs(edges-threshold)) > 1e-8:
            raise ValueError("each threshold must coincide with a bin edge")
    curves, rows = {}, []
    for sid, *_ in SERIES:
        part = df[df.series == sid]
        denominator = float(part.weight.sum())
        # np.histogram includes the final right edge; explicitly exclude xmax
        # so every visible bin is half-open while retaining its weight below.
        visible = part[part.value < xmax]
        counts, _ = np.histogram(visible.value, bins=edges, weights=visible.weight)
        # Percentage mass per bin, including full-series weights above the displayed xmax in the denominator.
        mass = counts/denominator*100
        curves[sid] = mass
        for tid, threshold, *_ in THRESHOLDS:
            below = float(part.loc[part.value < threshold, "weight"].sum())
            rows.append({"series": sid, "threshold_id": tid, "threshold": threshold,
                         "weight_total": denominator, "weight_below": below,
                         "share_below": below/denominator})
    return edges, curves, pd.DataFrame(rows)

def draw(edges: np.ndarray, curves: dict, shares: pd.DataFrame, lang: str, output: Path, title: bool) -> None:
    font(lang)
    fig, ax = plt.subplots(figsize=(9.8, 5.5), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    centers = (edges[:-1]+edges[1:])/2
    height = max(float(np.max(m)) for m in curves.values())
    threshold_map = {r[0]: r[1] for r in THRESHOLDS}
    for sid, label_en, label_zh, color, shade_id in SERIES:
        mass = curves[sid]
        threshold = threshold_map[shade_id]
        cut = int(np.searchsorted(edges, threshold))
        if cut:
            ax.stairs(mass[:cut], edges[:cut+1], baseline=0, fill=True,
                      color=color, alpha=.5, zorder=1)
        ax.plot(centers, mass, color=color, linewidth=2.0,
                label=label_en if lang == "en" else label_zh)
        row = shares[(shares.series == sid) & (shares.threshold_id == shade_id)].iloc[0]
        xann = min(threshold*.52, threshold-edges[1])
        annotation_color = "#4a4a4a" if sid == SERIES[0][0] else "#242424"
        ax.text(xann, height*(.72 if sid == SERIES[0][0] else .24),
                f"{row.share_below:.1%}", color=annotation_color, fontsize=11, fontweight="bold")
    for tid, threshold, en, zh, color in THRESHOLDS:
        ax.axvline(threshold, color=color, linestyle="--", linewidth=1.2)
        ax.text(threshold+edges[1]*.5, height*.96, en if lang == "en" else zh,
                rotation=90, va="top", ha="left", color=color, fontsize=9)
    ax.set_xlim(edges[0], edges[-1])
    ax.set_ylim(0, height*1.08)
    ax.set_xlabel(TEXT[lang]["x"], fontsize=11)
    ax.set_ylabel(TEXT[lang]["y"], fontsize=11)
    if title:
        ax.set_title(TEXT[lang]["title"], fontsize=12)
    ax.grid(axis="y", color="#e6e6e6", linewidth=.65)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, loc="upper right", fontsize=10)
    fig.tight_layout()
    fig.savefig(output, dpi=240)
    fig.savefig(output.with_suffix(".pdf"))
    plt.close(fig)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, default=Path(__file__).with_name("demo.csv"))
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--lang", choices=TEXT, default="en")
    p.add_argument("--xmin", type=float, default=0)
    p.add_argument("--xmax", type=float, default=120000)
    p.add_argument("--binwidth", type=float, default=1000)
    p.add_argument("--title", action="store_true")
    a = p.parse_args()
    df = read(a.input)
    edges, curves, shares = calculate(df, a.xmin, a.xmax, a.binwidth)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    shares.to_csv(a.output.with_name(f"{a.output.stem}_shares.csv"), index=False, float_format="%.12g")
    draw(edges, curves, shares, a.lang, a.output, a.title)
    print(f"PYTHON_COMPLETE rows={len(df)} series={len(SERIES)} thresholds={len(THRESHOLDS)} output={a.output}")

if __name__ == "__main__":
    main()
