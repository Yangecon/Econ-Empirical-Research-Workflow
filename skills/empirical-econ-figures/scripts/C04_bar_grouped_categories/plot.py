"""Ordered grouped category rates with explicit numerator/denominator inputs."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont

# Change category/group IDs and bilingual labels here for another comparison.
CATEGORIES = (
    ("small", "Below 10k", "低于1万"),
    ("lower_middle", "10k–30k", "1万至3万"),
    ("middle", "30k–100k", "3万至10万"),
    ("upper_middle", "100k–300k", "10万至30万"),
    ("large", "300k–1m", "30万至100万"),
    ("very_large", "Above 1m", "高于100万"),
)
GROUPS = (
    ("before", "Before milestone", "节点前", "#282828", True),
    ("after", "After milestone", "节点后", "#282828", False),
)
TEXT = {
    "en": {"x": "Outcome proportion", "title": "Outcome by category and timing"},
    "zh": {"x": "结果比例", "title": "按类别与时间划分的结果"},
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

def calculate(path: Path) -> pd.DataFrame:
    if len(GROUPS) != 2:
        raise ValueError("this paired-bar layout requires exactly two configured groups")
    df = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    cols = ["category", "group", "numerator", "denominator"]
    if not set(cols).issubset(df) or df[cols].eq("").any().any():
        raise ValueError(f"required nonblank columns: {cols}")
    if df.duplicated(["category", "group"]).any():
        raise ValueError("duplicate category-group")
    required = {(c[0], g[0]) for c in CATEGORIES for g in GROUPS}
    if set(zip(df.category, df.group)) != required:
        raise ValueError("input must contain every configured category-group pair exactly once")
    for col in ("numerator", "denominator"):
        df[col] = pd.to_numeric(df[col], errors="raise")
        if not np.isfinite(df[col]).all() or not (df[col] == np.floor(df[col])).all():
            raise ValueError(f"{col} must be a finite nonnegative integer count")
    if (df.denominator <= 0).any() or (df.numerator < 0).any() or (df.numerator > df.denominator).any():
        raise ValueError("require 0 <= numerator <= positive denominator")
    df["proportion"] = df.numerator/df.denominator
    df["category_order"] = df.category.map({c[0]: i for i, c in enumerate(CATEGORIES)})
    df["group_order"] = df.group.map({g[0]: i for i, g in enumerate(GROUPS)})
    return df.sort_values(["category_order", "group_order"]).reset_index(drop=True)

def draw(df: pd.DataFrame, lang: str, output: Path, title: bool) -> None:
    set_font(lang)
    fig, ax = plt.subplots(figsize=(8.8, 5.8), dpi=160)
    y = np.arange(len(CATEGORIES))
    h = .27
    for i, (gid, en, zh, color, filled) in enumerate(GROUPS):
        p = df[df.group == gid].sort_values("category_order")
        ax.barh(y + (-h/2 if i == 0 else h/2), p.proportion.to_numpy(), height=h,
                facecolor=color if filled else "white", edgecolor=color, linewidth=1.4,
                label=en if lang == "en" else zh)
    ax.set_yticks(y, [c[1] if lang == "en" else c[2] for c in CATEGORIES])
    ax.invert_yaxis()
    ax.set_xlim(0, max(.6, float(df.proportion.max())*1.15))
    ax.set_xlabel(TEXT[lang]["x"])
    ax.set_ylabel("")
    ax.grid(axis="x", color="#e7e7e7", lw=.6)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    if title:
        ax.set_title(TEXT[lang]["title"])
    ax.legend(frameon=True, edgecolor="#888888", facecolor="white", ncol=2,
              loc="upper center", bbox_to_anchor=(.5, -.13), fontsize=9)
    fig.tight_layout()
    fig.savefig(output, dpi=240); fig.savefig(output.with_suffix(".pdf")); plt.close(fig)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--lang", choices=TEXT, default="en")
    p.add_argument("--title", action="store_true")
    a = p.parse_args()
    df = calculate(a.input)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(a.output.with_name(a.output.stem+"_rates.csv"), index=False, float_format="%.12g")
    draw(df, a.lang, a.output, a.title)
    print(f"PYTHON_COMPLETE rows={len(df)} categories={len(CATEGORIES)} groups={len(GROUPS)} output={a.output}")

if __name__ == "__main__":
    main()
