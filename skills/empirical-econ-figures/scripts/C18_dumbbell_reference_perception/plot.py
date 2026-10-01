#!/usr/bin/env python3
"""Actual-versus-perceived dumbbells from supplied country-level values.

Descriptive drawing-method demonstration of Figure 2's left panel only.
No standard errors or confidence intervals are estimated here.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import pandas as pd

DEMO = [
    ("US", "美国", 10, 36, 34, 38),
    ("UK", "英国", 13, 31, 29, 33),
    ("Sweden", "瑞典", 18, 15, 13, 17),  # Synthetic underestimation.
    ("Italy", "意大利", 10, 26, 24, 28),
    ("Germany", "德国", 15, 30, 28, 32),
    ("France", "法国", 12, 12, 10, 14),  # Synthetic equality.
]


def make_demo() -> pd.DataFrame:
    return pd.DataFrame(DEMO, columns=[
        "category", "category_zh", "actual_pct", "perceived_pct",
        "perceived_ci_low_pct", "perceived_ci_high_pct",
    ])


def prepare(frame: pd.DataFrame) -> tuple[pd.DataFrame, bool]:
    required = {"category", "actual_pct", "perceived_pct"}
    if not required.issubset(frame):
        raise ValueError(f"Missing columns: {sorted(required - set(frame))}")
    data = frame.copy().reset_index(drop=True)  # Preserve supplied row order.
    if data.empty or data["category"].isna().any() or data["category"].duplicated().any():
        raise ValueError("Provide at least one unique nonblank category")
    if data["category"].astype(str).str.strip().eq("").any():
        raise ValueError("category cannot be blank")
    if "category_zh" in data and data["category_zh"].isna().any():
        raise ValueError("category_zh must be complete when supplied")
    has_low = "perceived_ci_low_pct" in data
    has_high = "perceived_ci_high_pct" in data
    if has_low != has_high:
        raise ValueError("Supply both perceived CI columns or neither")
    cols = ["actual_pct", "perceived_pct"]
    if has_low:
        cols += ["perceived_ci_low_pct", "perceived_ci_high_pct"]
    for col in cols:
        data[col] = pd.to_numeric(data[col], errors="raise")
        if data[col].isna().any() or not np.isfinite(data[col].to_numpy(dtype=float)).all():
            raise ValueError(f"{col} must be finite and complete")
        if not data[col].between(0, 100).all():
            raise ValueError(f"{col} must be a percentage in [0,100]")
    if has_low and not ((data.perceived_ci_low_pct <= data.perceived_pct) &
                        (data.perceived_pct <= data.perceived_ci_high_pct)).all():
        raise ValueError("Every supplied CI must contain its perceived mean")
    data["gap_pct_points"] = data.perceived_pct - data.actual_pct
    return data, has_low


def chinese_font() -> str:
    names = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in ("Microsoft YaHei", "SimHei", "Noto Sans CJK SC",
                      "Source Han Sans SC", "Arial Unicode MS"):
        if candidate in names:
            return candidate
    raise RuntimeError("No installed Chinese font available")


def render(data: pd.DataFrame, has_ci: bool, out: Path,
           language: str, title: str | None) -> None:
    if language == "zh":
        plt.rcParams["font.family"] = chinese_font()
        plt.rcParams["axes.unicode_minus"] = False
        categories = data["category_zh"] if "category_zh" in data else data["category"]
        actual_label, perceived_label = "实际份额", "感知均值"
        x_label = "移民占比（%）"
    else:
        plt.rcParams["font.family"] = "DejaVu Sans"
        categories = data["category"]
        actual_label, perceived_label = "Actual", "Perceived mean"
        x_label = "Share of immigrants (%)"
    y = np.arange(len(data))
    fig, ax = plt.subplots(figsize=(8.1, max(4.1, 0.57 * len(data) + 1.3)))
    ax.set_axisbelow(True)
    ax.grid(axis="x", color="#D2D2D2", linestyle=(0, (3, 4)), linewidth=0.8)
    for i, row in data.iterrows():
        if has_ci:
            ax.fill_betweenx([i - 0.11, i + 0.11],
                             row.perceived_ci_low_pct, row.perceived_ci_high_pct,
                             color="#D94830", alpha=0.19, linewidth=0, zorder=1)
        ax.plot([row.actual_pct, row.perceived_pct], [i, i],
                color="#323232", linewidth=1.3, zorder=2)
    ax.scatter(data.actual_pct, y, marker="D", s=62, color="#1F77B4",
               edgecolors="white", linewidths=0.4, label=actual_label, zorder=4)
    ax.scatter(data.perceived_pct, y, marker="s", s=64, color="#D94830",
               edgecolors="white", linewidths=0.4, label=perceived_label, zorder=5)
    max_value = max(data.actual_pct.max(), data.perceived_pct.max(),
                    data.perceived_ci_high_pct.max() if has_ci else 0)
    right = min(100, max(20, np.ceil((max_value + 3) / 5) * 5))
    ax.set_xlim(0, right)
    ax.set_xticks(np.arange(0, right + 1, 10))
    ax.set_yticks(y, categories)
    ax.invert_yaxis()  # First CSV row appears at the top.
    ax.set_xlabel(x_label, labelpad=8)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0, pad=8)
    if title:
        ax.set_title(title, fontsize=12, pad=12)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15),
              ncol=2, frameon=False, fontsize=10)
    fig.subplots_adjust(left=0.19, right=0.97, top=0.87 if title else 0.95,
                        bottom=0.23 if not title else 0.24)
    for extension in ("png", "pdf"):
        fig.savefig(out / f"reference_perception_dumbbell_{language}.{extension}",
                    dpi=300, facecolor="white")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="Country-level values CSV; omitted for synthetic demo")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "figures")
    parser.add_argument("--title-en", help="Optional English title")
    parser.add_argument("--title-zh", help="Optional Chinese title")
    parser.add_argument("--lang", choices=("en", "zh"), default="en")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    if args.input:
        frame = pd.read_csv(args.input)
        status = "user-supplied aggregate input"
    else:
        frame = make_demo()
        frame.to_csv(args.output / "demo_values.csv", index=False)
        status = "synthetic aggregate values"
    data, has_ci = prepare(frame)
    data.to_csv(args.output / "reference_perception_values.csv", index=False)
    render(data, has_ci, args.output, args.lang, args.title_en if args.lang == "en" else args.title_zh)
    print(data[["category", "actual_pct", "perceived_pct", "gap_pct_points"]].to_string(index=False))
    print(f"Input status: {status}; supplied perceived CI: {has_ci}")
    print("REFERENCE_PERCEPTION_DUMBBELL_COMPLETE")


if __name__ == "__main__":
    main()
