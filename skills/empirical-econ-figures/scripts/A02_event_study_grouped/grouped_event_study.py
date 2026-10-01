"""Draw grouped event-study estimates from an explicit long CSV.

The reference period is normalized, never interpreted as an estimate.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from statistics import NormalDist

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D


HERE = Path(__file__).resolve().parent
COLORS = ("#008837", "#C51B2B", "#2B6CB0", "#8E44AD", "#B36B00", "#007D8A")
MARKERS = ("D", "o", "s", "^", "v", "P", "X")


def load_rows(path: Path, reference: float, level: float):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        required = {"event_time", "group", "estimate"}
        if not required <= columns:
            raise ValueError(f"Missing required columns: {sorted(required - columns)}")
        has_ci = {"ci_low", "ci_high"} <= columns
        if not has_ci and "se" not in columns:
            raise ValueError("Supply se or both ci_low and ci_high")
        rows = []
        seen = set()
        z = NormalDist().inv_cdf(0.5 + level / 200)
        for raw in reader:
            group = raw["group"].strip()
            if not group:
                raise ValueError("Group names must be nonempty")
            t = float(raw["event_time"])
            if not math.isfinite(t):
                raise ValueError("event_time must be finite")
            key = (group, t)
            if key in seen:
                raise ValueError(f"Duplicate group/event_time: {key}")
            seen.add(key)
            if t == reference:
                continue  # supplied normalization rows never enter inference
            b = float(raw["estimate"])
            if has_ci:
                lo, hi = float(raw["ci_low"]), float(raw["ci_high"])
            else:
                se = float(raw["se"])
                if not math.isfinite(se) or se < 0:
                    raise ValueError(f"Invalid se for {key}")
                lo, hi = b - z * se, b + z * se
            if not all(map(math.isfinite, (b, lo, hi))) or not lo <= b <= hi:
                raise ValueError(f"Invalid estimate or CI for {key}")
            rows.append(dict(event_time=t, group=group, estimate=b,
                             ci_low=lo, ci_high=hi, significant=(lo > 0 or hi < 0)))
    groups = list(dict.fromkeys(row["group"] for row in rows))
    if len(groups) < 2:
        raise ValueError("At least two groups with non-reference estimates are required")
    return rows, groups


def draw(rows, groups, output: Path, basename: str, reference: float,
         level: float, language: str, title: str | None,
         policy_time: float = 0):
    if language == "zh":
        available = {font.name for font in font_manager.fontManager.ttflist}
        choices = ("Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "Source Han Sans SC")
        selected = next((name for name in choices if name in available), None)
        if selected is None:
            raise RuntimeError("Chinese labels require a CJK font (Microsoft YaHei, SimHei, or Noto Sans CJK SC)")
        plt.rcParams["font.sans-serif"] = [selected]
        plt.rcParams["axes.unicode_minus"] = False
    times = sorted({reference, *(row["event_time"] for row in rows)})
    gaps = [b - a for a, b in zip(times, times[1:])]
    gap = min(gaps) if gaps else 1.0
    span = 0.26 * gap
    offsets = {g: (i / (len(groups) - 1) - 0.5) * span
               for i, g in enumerate(groups)}
    fig, ax = plt.subplots(figsize=(9.2, 5.3))
    for i, group in enumerate(groups):
        color, marker = COLORS[i % len(COLORS)], MARKERS[i % len(MARKERS)]
        for row in sorted((r for r in rows if r["group"] == group),
                          key=lambda r: r["event_time"]):
            x, b = row["event_time"] + offsets[group], row["estimate"]
            ax.vlines(x, row["ci_low"], row["ci_high"], color=color,
                      linewidth=1.3, zorder=2)
            cap = 0.035 * gap
            ax.hlines((row["ci_low"], row["ci_high"]), x-cap, x+cap,
                      color=color, linewidth=1.1, zorder=2)
            ax.scatter(x, b, marker=marker, s=38, edgecolors=color,
                       facecolors=color if row["significant"] else "white",
                       linewidths=1.3, zorder=3)
    ax.scatter(reference, 0, marker="o", s=38, facecolors="white",
               edgecolors="#555555", linewidths=1.3, zorder=4)
    ax.axhline(0, color="#858585", linewidth=0.9, zorder=0)
    pre_times = [t for t in times if t < policy_time]
    policy_boundary = (max(pre_times) + policy_time) / 2 if pre_times else policy_time
    ax.axvline(policy_boundary, color="#999999",
               linestyle="--", linewidth=1.0, zorder=0)
    ax.grid(axis="y", color="#E7EAED", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.set_xticks(times)
    ax.set_xlim(min(times) - 0.55 * gap, max(times) + 0.55 * gap)
    if language == "zh":
        ax.set_xlabel("相对政策时点")
        ax.set_ylabel(f"估计效应（{level:g}% 置信区间）")
        ref_label = "归一化参考期"
    else:
        ax.set_xlabel("Event time relative to intervention")
        ax.set_ylabel(f"Estimated effect ({level:g}% CI)")
        ref_label = "Normalized reference"
    if title:
        ax.set_title(title)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    handles = [Line2D([0], [0], color=COLORS[i % len(COLORS)],
                      marker=MARKERS[i % len(MARKERS)], linestyle="None",
                      markersize=6, label=g) for i, g in enumerate(groups)]
    handles.append(Line2D([0], [0], marker="o", color="#555555",
                          markerfacecolor="white", linestyle="None",
                          markersize=6, label=ref_label))
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.14),
              ncol=min(len(handles), 4), frameon=False)
    fig.tight_layout()
    output.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "pdf"):
        fig.savefig(output / f"{basename}.{ext}", dpi=300,
                    bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return {"rows": len(rows), "groups": len(groups),
            "significant": sum(r["significant"] for r in rows)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=HERE / "demo_estimates.csv")
    parser.add_argument("--output-dir", type=Path, default=HERE)
    parser.add_argument("--basename", default="grouped_event_study_python")
    parser.add_argument("--reference", type=float, default=-1)
    parser.add_argument("--policy-time", type=float, default=0,
                        help="First treated event time; divider is midway from preceding displayed time")
    parser.add_argument("--level", type=float, default=95)
    parser.add_argument("--language", choices=("en", "zh"), default="en")
    parser.add_argument("--title", default=None)
    args = parser.parse_args()
    if not 0 < args.level < 100:
        parser.error("--level must be between 0 and 100")
    rows, groups = load_rows(args.input, args.reference, args.level)
    result = draw(rows, groups, args.output_dir, args.basename,
                  args.reference, args.level, args.language, args.title,
                  args.policy_time)
    print(f"GROUPED_EVENT_STUDY_PYTHON_OK {result}")


if __name__ == "__main__":
    main()
