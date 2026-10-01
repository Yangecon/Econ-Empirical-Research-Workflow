"""Weighted concentration curves by a common rank, or ordinary Lorenz curves."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_shared"))
from line_geometry import draw_trace
from matplotlib.font_manager import FontProperties, findfont

# Change IDs, labels, and colors together to adapt this two-resource example.
CURVES = (
    ("expenditure", "Total expenditure", "总支出", "#2778ac", 1.8),
    ("fuel", "Fuel purchases", "燃料购买", "#075995", 3.1),
)
TEXT = {
    "en": {"x": "Cumulative population share (%)", "y": "Cumulative resource share (%)",
           "equality": "Line of equality", "concentration_title": "Concentration curves",
           "lorenz_title": "Lorenz curves"},
    "zh": {"x": "人口累计比例（%）", "y": "资源累计比例（%）",
           "equality": "完全平等线", "concentration_title": "集中曲线",
           "lorenz_title": "洛伦兹曲线"},
}

def set_font(lang: str) -> None:
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
    cols = ["id", "rank_value", "weight", *(c[0] for c in CURVES)]
    if not set(cols).issubset(df):
        raise ValueError(f"required columns: {cols}")
    if df[cols].eq("").any().any() or df.id.duplicated().any():
        raise ValueError("blank required field or duplicate id")
    for c in cols[1:]:
        df[c] = pd.to_numeric(df[c], errors="raise")
        if not np.isfinite(df[c]).all() or (df[c] < 0).any():
            raise ValueError(f"{c} must be finite and nonnegative")
    if df.weight.sum() <= 0:
        raise ValueError("positive total population weight required")
    for c, *_ in CURVES:
        if (df.weight*df[c]).sum() <= 0:
            raise ValueError(f"positive weighted total required for {c}")
    return df

def calculate(df: pd.DataFrame, mode: str) -> pd.DataFrame:
    if mode not in ("concentration", "lorenz"):
        raise ValueError("mode must be concentration or lorenz")
    rows = []
    for resource, *_ in CURVES:
        rank = "rank_value" if mode == "concentration" else resource
        # Aggregate exact rank ties before cumulative sums: no arbitrary within-tie order.
        grouped = (df.assign(resource_mass=df.weight*df[resource])
                     .groupby(rank, sort=True, as_index=False)[["weight", "resource_mass"]].sum())
        total_w, total_r = grouped.weight.sum(), grouped.resource_mass.sum()
        rows.append({"curve": resource, "mode": mode, "rank_value": np.nan,
                     "population_pct": 0.0, "resource_pct": 0.0})
        cum_w = grouped.weight.cumsum().to_numpy()
        cum_r = grouped.resource_mass.cumsum().to_numpy()
        for i, row in grouped.iterrows():
            rows.append({"curve": resource, "mode": mode, "rank_value": row[rank],
                         "population_pct": 100*cum_w[i]/total_w,
                         "resource_pct": 100*cum_r[i]/total_r})
    out = pd.DataFrame(rows)
    for _, part in out.groupby("curve", sort=False):
        if not np.all(np.diff(part.population_pct) >= -1e-10) or not np.all(np.diff(part.resource_pct) >= -1e-10):
            raise AssertionError("cumulative curve decreased")
        if not np.allclose(part[["population_pct", "resource_pct"]].iloc[-1], 100):
            raise AssertionError("curve does not finish at (100,100)")
    return out

def draw(points: pd.DataFrame, lang: str, output: Path, title: bool) -> None:
    set_font(lang)
    fig, ax = plt.subplots(figsize=(7.8, 6.5), dpi=160)
    draw_trace(ax, [0, 100], [0, 100], color="#303030", linewidth=1.3, label=TEXT[lang]["equality"])
    for cid, en, zh, color, width in CURVES:
        p = points[points.curve == cid]
        draw_trace(ax, p.population_pct, p.resource_pct, color=color, linewidth=width,
                   label=en if lang == "en" else zh)
    ax.set(xlim=(0, 100), ylim=(0, 100), xlabel=TEXT[lang]["x"], ylabel=TEXT[lang]["y"])
    ax.set_xticks(np.arange(0, 101, 20)); ax.set_yticks(np.arange(0, 101, 20))
    ax.grid(color="#e8e8e8", lw=.6)
    ax.spines[["top", "right"]].set_visible(False)
    if title:
        mode = points["mode"].iloc[0]
        ax.set_title(TEXT[lang][mode+"_title"])
    ax.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="#999999")
    fig.tight_layout()
    fig.savefig(output, dpi=240)
    fig.savefig(output.with_suffix(".pdf"))
    plt.close(fig)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--lang", choices=TEXT, default="en")
    p.add_argument("--mode", choices=("concentration", "lorenz"), default="concentration")
    p.add_argument("--title", action="store_true")
    a = p.parse_args()
    df = read(a.input)
    points = calculate(df, a.mode)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    points.to_csv(a.output.with_name(a.output.stem+"_points.csv"), index=False, float_format="%.12g")
    draw(points, a.lang, a.output, a.title)
    print(f"PYTHON_COMPLETE rows={len(df)} mode={a.mode} output={a.output}")

if __name__ == "__main__":
    main()
