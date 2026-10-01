"""Two orientations of a grouped coefficient-and-confidence-interval plot.

Edit CONFIG to adapt the two source-inspired examples to another study.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

# Exactly 1–4 ordered panels per variant. Units can differ across panels.
# CSV panel/group IDs must match; term order/labels come from the CSV.
CONFIG = {
    "robustness": {
        "panels": ("mortality", "difficulty", "transfer", "employment"),
        "groups": ("main",), "preferred_term": "preferred",
        "en": {
            "panels": ("Log mortality", "Ambulatory difficulty", "Disability transfer", "Annual employment"),
            "units": ("Log-point effect", "Index-point effect", "Transfer effect", "Percentage-point effect"),
            "groups": ("Estimate",), "title": "Specification sensitivity",
        },
        "zh": {
            "panels": ("死亡率对数", "行动困难", "残障补助", "年度就业"),
            "units": ("对数点效应", "指数点效应", "补助效应", "百分点效应"),
            "groups": ("估计值",), "title": "不同规格的估计结果",
        },
    },
    "subgroup": {
        "panels": ("education",),
        "groups": ("group_a", "group_b"), "preferred_term": None,
        "en": {
            "panels": ("Educational attainment",), "units": ("Estimated effect",),
            "groups": ("Group A", "Group B"), "title": "Effects by group",
        },
        "zh": {
            "panels": ("教育结果",), "units": ("估计效应",),
            "groups": ("甲组", "乙组"), "title": "分组效应",
        },
    },
}

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

def load(path: Path, variant: str, multiplier: float) -> pd.DataFrame:
    required = {"variant", "panel", "panel_order", "term", "term_order", "term_label_en",
                "term_label_zh", "group", "group_order", "estimate", "ci_low", "ci_high"}
    df = pd.read_csv(path, dtype=str, encoding="utf-8-sig", keep_default_na=False)
    if not required.issubset(df):
        raise ValueError(f"CSV missing columns: {sorted(required-set(df))}")
    df = df.loc[df.variant == variant].copy()
    if df.empty:
        raise ValueError(f"variant {variant!r} has no rows")
    for col in ("panel_order", "term_order", "group_order", "estimate", "ci_low", "ci_high"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    if "se" in df:
        df["se"] = pd.to_numeric(df["se"], errors="coerce")
    else:
        df["se"] = np.nan
    missing_ci = df.ci_low.isna() & df.ci_high.isna() & df.se.notna() & (df.se >= 0)
    df.loc[missing_ci, "ci_low"] = df.loc[missing_ci, "estimate"] - multiplier*df.loc[missing_ci, "se"]
    df.loc[missing_ci, "ci_high"] = df.loc[missing_ci, "estimate"] + multiplier*df.loc[missing_ci, "se"]
    if df[list(("panel_order", "term_order", "group_order", "estimate", "ci_low", "ci_high"))].isna().any().any():
        raise ValueError("orders, estimates and both CI limits must be numeric; SE may replace both CI limits")
    if not ((df.ci_low <= df.estimate) & (df.estimate <= df.ci_high)).all():
        raise ValueError("each interval must contain its estimate")
    if df.duplicated(["panel", "term", "group"]).any():
        raise ValueError("duplicate panel/term/group")
    config = CONFIG[variant]
    panels, groups = config["panels"], config["groups"]
    if not 1 <= len(panels) <= 4 or not 1 <= len(groups) <= 3:
        raise ValueError("configuration supports 1–4 panels and 1–3 groups")
    if set(df.panel) != set(panels) or set(df.group) != set(groups):
        raise ValueError("CSV panel/group IDs must match CONFIG")
    for i, panel in enumerate(panels, 1):
        part = df[df.panel == panel]
        if set(part.panel_order) != {i}:
            raise ValueError(f"panel_order for {panel} must be {i}")
        terms = part[["term", "term_order"]].drop_duplicates()
        if terms.term.nunique() != len(terms) or sorted(terms.term_order) != list(range(1, len(terms)+1)):
            raise ValueError(f"{panel}: term_order must be unique and consecutive from 1")
        for j, group in enumerate(groups, 1):
            g = part[part.group == group]
            if len(g) != len(terms) or set(g.group_order) != {j} or set(g.term) != set(terms.term):
                raise ValueError(f"{panel}: each configured group must cover every ordered term")
    return df.sort_values(["panel_order", "term_order", "group_order"])

def draw(df: pd.DataFrame, variant: str, orientation: str, lang: str, output: Path, title: bool) -> None:
    setup_font(lang)
    cfg = CONFIG[variant]
    panels, groups = cfg["panels"], cfg["groups"]
    labels = cfg[lang]
    n = len(panels)
    if orientation == "horizontal":
        # Common row sequence permits compact 4-column source-style display.
        sequences = [tuple(df[df.panel == p].drop_duplicates("term").sort_values("term_order").term) for p in panels]
        if len(set(sequences)) != 1:
            raise ValueError("horizontal multi-panel view requires the same ordered terms in each panel")
        fig, axes = plt.subplots(1, n, figsize=(max(7.5, 2.9*n+2.8), 5.3), squeeze=False)
        axes = axes[0]
    else:
        fig, axes = plt.subplots(1, n, figsize=(max(7.5, 3.2*n), 4.6), squeeze=False)
        axes = axes[0]
    markers = ("o", "^", "s")
    colors = ("#1c1c1c", "#777777", "#2c608a")
    for pi, (ax, panel) in enumerate(zip(axes, panels)):
        part = df[df.panel == panel]
        terms = part.drop_duplicates("term").sort_values("term_order")
        count = len(terms)
        pos = {t: k for k, t in enumerate(terms.term)}
        lows = part.ci_low.to_numpy(float); highs = part.ci_high.to_numpy(float)
        effect_min, effect_max = min(0.0, lows.min()), max(0.0, highs.max())
        pad = max((effect_max-effect_min)*.12, .001)
        if orientation == "horizontal":
            ax.axvline(0, color="#333333", lw=1, zorder=0)
            if cfg["preferred_term"]:
                pref = part[part.term == cfg["preferred_term"]]
                if not pref.empty and len(groups) == 1:
                    ax.axvline(float(pref.estimate.iloc[0]), color="#777777", lw=.9, ls="--", zorder=0)
            for gi, group in enumerate(groups):
                gdata = part[part.group == group]
                offset = (gi-(len(groups)-1)/2)*.18
                for row in gdata.itertuples():
                    y = count-1-pos[row.term]+offset
                    preferred = row.term == cfg["preferred_term"] and len(groups) == 1
                    c = "#c93b3b" if preferred else colors[gi]
                    ax.hlines(y, row.ci_low, row.ci_high, color=c, lw=1.7, zorder=2)
                    ax.vlines([row.ci_low, row.ci_high], y-.045, y+.045, color=c, lw=1.0, zorder=2)
                    ax.plot(row.estimate, y, marker=markers[gi], ms=6.3,
                            mfc=c if preferred or len(groups)>1 else "white", mec=c, mew=1.3, zorder=3)
            ax.set_xlim(effect_min-pad, effect_max+pad)
            ax.set_ylim(-.6, count-.4)
            ax.set_yticks(range(count), list(reversed(terms[f"term_label_{lang}"].tolist())))
            if pi > 0:
                ax.tick_params(labelleft=False)
            ax.set_xlabel(labels["units"][pi], fontsize=9)
            ax.grid(axis="x", color="#e6e6e6", lw=.6)
        else:
            ax.axhline(0, color="#333333", lw=1, zorder=0)
            for gi, group in enumerate(groups):
                gdata = part[part.group == group]
                offset = (gi-(len(groups)-1)/2)*.22
                for row in gdata.itertuples():
                    x = pos[row.term]+offset
                    c = colors[gi]
                    ax.vlines(x, row.ci_low, row.ci_high, color="#9d9d9d", lw=1.35, zorder=2)
                    ax.hlines([row.ci_low, row.ci_high], x-.045, x+.045, color="#9d9d9d", lw=1.0, zorder=2)
                    ax.plot(x, row.estimate, marker=markers[gi], ms=7, mfc=c if gi==0 else "white",
                            mec=c, mew=1.3, zorder=3)
            ax.set_xlim(-.55, count-.45)
            ax.set_ylim(effect_min-pad, effect_max+pad)
            ax.set_xticks(range(count), terms[f"term_label_{lang}"].tolist(), fontsize=9)
            ax.set_ylabel(labels["units"][pi], fontsize=9)
            ax.grid(axis="y", color="#e6e6e6", lw=.6)
        if n > 1:
            ax.set_title(labels["panels"][pi], fontsize=10.5, pad=10)
        ax.tick_params(labelsize=8.5)
        ax.spines[["top", "right"]].set_visible(False)
        ax.set_axisbelow(True)
    if len(groups) > 1:
        handles = [Line2D([0], [0], color=colors[i], marker=markers[i], lw=0,
                          markerfacecolor=colors[i] if i==0 else "white", markeredgewidth=1.3,
                          markersize=7, label=labels["groups"][i]) for i in range(len(groups))]
        fig.legend(handles=handles, loc="lower center", ncol=len(groups), frameon=True,
                   bbox_to_anchor=(.5, .01), fontsize=9)
    if title:
        fig.suptitle(labels["title"], y=.99, fontsize=12)
    fig.subplots_adjust(left=.27 if orientation=="horizontal" else .09,
                        right=.98, bottom=.20 if len(groups)>1 else .14,
                        top=.86 if title else .91, wspace=.20)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=220, facecolor="white")
    fig.savefig(output.with_suffix(".pdf"), facecolor="white")
    plt.close(fig)

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--variant", choices=CONFIG, required=True)
    p.add_argument("--orientation", choices=("horizontal", "vertical"), required=True)
    p.add_argument("--lang", choices=("en", "zh"), default="en")
    p.add_argument("--ci-multiplier", type=float, default=1.96,
                   help="Used only when both CI limits are blank and se is supplied")
    p.add_argument("--title", action="store_true")
    args = p.parse_args()
    if args.ci_multiplier <= 0:
        p.error("--ci-multiplier must be positive")
    df = load(args.input, args.variant, args.ci_multiplier)
    draw(df, args.variant, args.orientation, args.lang, args.output, args.title)
    print(f"PYTHON_COMPLETE variant={args.variant} orientation={args.orientation} lang={args.lang} "
          f"rows={len(df)} panels={df.panel.nunique()} output={args.output.resolve()}")

if __name__ == "__main__":
    main()
