"""Two-panel comparison of three supplied cumulative distribution functions."""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont
import numpy as np
import pandas as pd

# Edit IDs and bilingual labels here to apply the template to other scenarios.
PANELS = ("forced_attention", "no_switching_costs")
GROUPS = ("low", "medium", "high")
TEXT = {
    "en": {
        "panels": ("Panel A. Forced attention", "Panel B. No switching costs"),
        "groups": ("Low acuity", "Medium acuity", "High acuity"),
        "legend": "Acuity level", "x": "Reduction in overspending ($)",
        "y": "Cumulative share (CDF)",
        "title": "Counterfactual reductions in overspending",
    },
    "zh": {
        "panels": ("面板A：强制关注", "面板B：无转换成本"),
        "groups": ("低需求", "中需求", "高需求"),
        "legend": "健康需求程度", "x": "超额支出减少额（美元）",
        "y": "累计比例（CDF）",
        "title": "反事实情景下的超额支出减少额",
    },
}
STYLES = (
    {"color": "#202020", "linestyle": "-", "linewidth": 1.9},
    {"color": "#777777", "linestyle": "--", "linewidth": 1.8},
    {"color": "#b0b0b0", "linestyle": (0, (4, 2, 1, 2)), "linewidth": 1.8},
)

def setup_font(lang: str) -> None:
    if lang == "zh":
        for family in ("Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "Source Han Sans SC"):
            try:
                findfont(FontProperties(family=family), fallback_to_default=False)
                plt.rcParams["font.family"] = family
                break
            except ValueError:
                continue
        else:
            raise RuntimeError("A CJK font is required for Chinese labels")
    else:
        plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False

def load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str, encoding="utf-8-sig", keep_default_na=False)
    required = {"panel", "panel_order", "group", "group_order", "x_reduction", "cdf"}
    if not required.issubset(df):
        raise ValueError(f"CSV missing columns: {sorted(required-set(df))}")
    if set(df.panel) != set(PANELS) or set(df.group) != set(GROUPS):
        raise ValueError("CSV panel/group IDs must match configuration")
    for col in ("panel_order", "group_order", "x_reduction", "cdf"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    if not np.isfinite(df[["panel_order", "group_order", "x_reduction", "cdf"]].to_numpy(float)).all():
        raise ValueError("orders, x_reduction and cdf must be finite numeric values")
    if not df.cdf.between(0, 1).all():
        raise ValueError("cdf must be in [0, 1]")
    for pi, panel in enumerate(PANELS, 1):
        part = df[df.panel == panel]
        if set(part.panel_order) != {pi}:
            raise ValueError(f"panel_order for {panel} must be {pi}")
        for gi, group in enumerate(GROUPS, 1):
            curve = part[part.group == group].sort_values("x_reduction")
            if len(curve) < 2 or set(curve.group_order) != {gi}:
                raise ValueError(f"{panel}/{group} needs >=2 rows and group_order {gi}")
            if (np.diff(curve.x_reduction) <= 0).any():
                raise ValueError(f"{panel}/{group}: x_reduction must be unique and increasing")
            if (np.diff(curve.cdf) < -1e-9).any():
                raise ValueError(f"{panel}/{group}: CDF decreases with x_reduction")
    return df

def draw(df: pd.DataFrame, lang: str, output: Path, title: bool) -> None:
    setup_font(lang)
    labels = TEXT[lang]
    fig, axes = plt.subplots(2, 1, figsize=(8.5, 7.0), sharex=True, sharey=True)
    xmin, xmax = float(df.x_reduction.min()), float(df.x_reduction.max())
    for pi, (panel, ax) in enumerate(zip(PANELS, axes)):
        for gi, group in enumerate(GROUPS):
            curve = df[(df.panel == panel) & (df.group == group)].sort_values("x_reduction")
            ax.plot(curve.x_reduction, curve.cdf, label=labels["groups"][gi], **STYLES[gi])
        ax.set_title(labels["panels"][pi], loc="left", fontsize=11, pad=9)
        ax.set_ylabel(labels["y"], fontsize=9.5)
        ax.set_ylim(-.015, 1.02)
        ax.set_yticks([0, .25, .5, .75, 1])
        ax.set_xlim(xmin, xmax)
        ax.grid(color="#e7e7e7", lw=.65)
        ax.set_axisbelow(True)
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=8.5)
        ax.legend(title=labels["legend"], loc="lower right", fontsize=8.5,
                  title_fontsize=8.5, frameon=True, fancybox=False,
                  facecolor="white", edgecolor="#555555", framealpha=.96)
        ax.set_xlabel(labels["x"], fontsize=9.5)
    if title:
        fig.suptitle(labels["title"], fontsize=12, y=.99)
    fig.subplots_adjust(left=.13, right=.98, top=.91 if title else .95,
                        bottom=.09, hspace=.36)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=220, facecolor="white")
    fig.savefig(output.with_suffix(".pdf"), facecolor="white")
    plt.close(fig)

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--lang", choices=TEXT, default="en")
    p.add_argument("--title", action="store_true")
    args = p.parse_args()
    df = load(args.input)
    draw(df, args.lang, args.output, args.title)
    print(f"PYTHON_COMPLETE lang={args.lang} panels={df.panel.nunique()} "
          f"curves={df.groupby(['panel','group']).ngroups} rows={len(df)} output={args.output.resolve()}")

if __name__ == "__main__":
    main()
