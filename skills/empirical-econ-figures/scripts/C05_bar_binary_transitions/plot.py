#!/usr/bin/env python3
"""Four-state 100% stacks from matched binary observations.

This is a descriptive drawing-method demonstration of Figure 7's bar layer.
It does not reproduce the paper's data or its tests.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import pandas as pd

STATES = ["both_0", "zero_to_one", "one_to_zero", "both_1"]
COLORS = ["#999999", "#5C5C5C", "#FFFFFF", "#E3E3E3"]
DEMO = {
    "ELLS": (14, 5, 13, 6, 2),
    "CC ALLAIS": (18, 5, 7, 9, 1),
    "AUCT": (30, 0, 6, 4, 0),
    "ELECT": (8, 2, 17, 11, 2),
    "CR ALLAIS": (0, 0, 11, 28, 1),
}


def make_demo() -> pd.DataFrame:
    """Deterministic synthetic paired rows; tuple order 11,10,01,00,missing."""
    rows = []
    for task, (n11, n10, n01, n00, n_missing) in DEMO.items():
        pairs = ([(1, 1)] * n11 + [(1, 0)] * n10 +
                 [(0, 1)] * n01 + [(0, 0)] * n00)
        # Deliberately include missing first and second statuses.
        pairs += [(np.nan, 1) if j % 2 == 0 else (0, np.nan)
                  for j in range(n_missing)]
        assert len(pairs) == 40
        for subject, (first, second) in enumerate(pairs, start=1):
            rows.append((f"S{subject:03d}", task, first, second))
    return pd.DataFrame(rows, columns=["subject_id", "task", "first", "second"])


def summarize(frame: pd.DataFrame, task_order: list[str] | None = None) -> pd.DataFrame:
    required = {"subject_id", "task", "first", "second"}
    if not required.issubset(frame):
        raise ValueError(f"Missing columns: {sorted(required - set(frame))}")
    data = frame.copy()
    if data["subject_id"].isna().any() or data["task"].isna().any():
        raise ValueError("subject_id and task cannot be missing")
    if data.duplicated(["subject_id", "task"]).any():
        raise ValueError("Each subject_id/task pair must occur once")
    for col in ("first", "second"):
        parsed = pd.to_numeric(data[col], errors="raise")
        if not parsed.dropna().isin([0, 1]).all():
            raise ValueError(f"{col} must be 0, 1, or missing")
        data[col] = parsed
    tasks = task_order or list(dict.fromkeys(data["task"].astype(str)))
    if set(tasks) != set(data["task"].astype(str)) or len(tasks) != len(set(tasks)):
        raise ValueError("task_order must contain every task exactly once")
    rows = []
    for task in tasks:
        part = data.loc[data["task"].astype(str).eq(task)]
        missing_first = part["first"].isna()
        missing_second = part["second"].isna()
        complete = part.loc[~(missing_first | missing_second)]
        n = len(complete)
        if n == 0:
            raise ValueError(f"{task}: no complete pairs")
        n11 = int(((complete["first"] == 1) & (complete["second"] == 1)).sum())
        n10 = int(((complete["first"] == 1) & (complete["second"] == 0)).sum())
        n01 = int(((complete["first"] == 0) & (complete["second"] == 1)).sum())
        n00 = int(((complete["first"] == 0) & (complete["second"] == 0)).sum())
        assert n11 + n10 + n01 + n00 == n
        counts = {"both_1": n11, "one_to_zero": n10,
                  "zero_to_one": n01, "both_0": n00}
        start_one, start_zero = n11 + n10, n01 + n00
        row = {
            "task": task, "n_rows": len(part), "n_complete": n,
            "n_excluded_unpaired": len(part) - n,
            "n_missing_first": int(missing_first.sum()),
            "n_missing_second": int(missing_second.sum()),
            "n_missing_both": int((missing_first & missing_second).sum()),
            "n_start_1": start_one, "n_start_0": start_zero,
            "p_one_to_zero_given_start_1": n10 / start_one if start_one else np.nan,
            "p_zero_to_one_given_start_0": n01 / start_zero if start_zero else np.nan,
        }
        for state, count in counts.items():
            row[f"n_{state}"] = count
            row[f"pct_{state}"] = 100 * count / n
        rows.append(row)
    result = pd.DataFrame(rows)
    if not np.allclose(result[[f"pct_{s}" for s in STATES]].sum(axis=1), 100):
        raise AssertionError("Each complete-pair stack must total 100%")
    return result


def pick_chinese_font() -> str:
    names = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in ("Microsoft YaHei", "SimHei", "Noto Sans CJK SC",
                      "Source Han Sans SC", "Arial Unicode MS"):
        if candidate in names:
            return candidate
    raise RuntimeError("No installed Chinese font found for ZH export")


def render(summary: pd.DataFrame, output: Path, language: str, title: str | None) -> None:
    if language == "zh":
        plt.rcParams["font.family"] = pick_chinese_font()
        plt.rcParams["axes.unicode_minus"] = False
        labels = ["两次均为0", "0→1", "1→0", "两次均为1"]
        y_label, x_label = "完整配对占比（%）", "任务"
    else:
        plt.rcParams["font.family"] = "DejaVu Sans"
        labels = ["Both 0", "0→1", "1→0", "Both 1"]
        y_label, x_label = "Share of complete pairs (%)", "Task"
    fig, ax = plt.subplots(figsize=(9.0, 5.0))
    x = np.arange(len(summary))
    bottom = np.zeros(len(summary), dtype=float)
    for state, color, label in zip(STATES, COLORS, labels):
        values = summary[f"pct_{state}"].to_numpy(dtype=float)
        ax.bar(x, values, width=0.68, bottom=bottom,
               color=color, edgecolor="#333333", linewidth=0.7, label=label)
        for xi, value, floor in zip(x, values, bottom):
            if value >= 8.0:  # Small and zero components remain visible without cramped text.
                ink = "white" if state == "zero_to_one" else "#222222"
                ax.text(xi, floor + value / 2, f"{value:.1f}",
                        ha="center", va="center", fontsize=9, color=ink)
        bottom += values
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_xticks(x, [f"{row.task}\nn={row.n_complete}"
                      for row in summary.itertuples(index=False)])
    ax.yaxis.grid(True, color="#DDDDDD", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="x", length=0, pad=8)
    if title:
        ax.set_title(title, fontsize=12, pad=12)
    handles, legend_labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], legend_labels[::-1], loc="center left",
              bbox_to_anchor=(1.01, 0.5), frameon=False, fontsize=9)
    fig.subplots_adjust(left=0.09, right=0.77, bottom=0.18, top=0.87 if title else 0.95)
    for extension in ("png", "pdf"):
        fig.savefig(output / f"paired_binary_transition_stacks_{language}.{extension}",
                    dpi=300, facecolor="white")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="Paired subject-task CSV; omitted for synthetic demo")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "figures")
    parser.add_argument("--title-en", help="Optional English title")
    parser.add_argument("--title-zh", help="Optional Chinese title")
    parser.add_argument("--lang", choices=("en", "zh"), default="en")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    if args.input:
        frame = pd.read_csv(args.input, dtype={"subject_id": str, "task": str})
        status = "user-provided paired input"
    else:
        frame = make_demo()
        frame.to_csv(args.output / "demo_pairs.csv", index=False)
        status = "synthetic paired demonstration"
    summary = summarize(frame)
    summary.to_csv(args.output / "paired_binary_transition_summary.csv", index=False)
    render(summary, args.output, args.lang, args.title_en if args.lang == "en" else args.title_zh)
    print(summary[["task", "n_rows", "n_complete", "n_excluded_unpaired",
                   "p_one_to_zero_given_start_1", "p_zero_to_one_given_start_0"]].to_string(index=False))
    print(f"Input status: {status}")
    print("PAIRED_BINARY_TRANSITION_STACKS_COMPLETE")


if __name__ == "__main__":
    main()
