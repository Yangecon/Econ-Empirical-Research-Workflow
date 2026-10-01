"""Bilingual two-panel residualized scatter plot from already-residualized CSV.

Usage: python plot.py --input demo.csv --lang en --output residual_scatter_en.png
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont
import numpy as np

# Edit this block to reuse the template with another two-panel study. Each
# panel has two or three groups, listed in legend order with background last.
PANEL_GROUPS = {
    "all_fields": ("medicine", "other"),
    "computer_science": ("ai_late", "ai_early", "other"),
}
GROUP_STYLES = {
    "medicine": dict(color="#963c46", s=17, linewidths=.8, alpha=.83),
    "ai_late": dict(color="#d13b35", s=26, linewidths=1.0, alpha=1),
    "ai_early": dict(color="#202020", s=24, linewidths=.9, alpha=.90),
    "other": dict(color="#c8c8c8", s=17, linewidths=.65, alpha=.75),
}
TEXT = {
    "en": {
        "x": "Residualized X", "y": "Residualized Y",
        "panels": {"all_fields": "(a) Sample A", "computer_science": "(b) Sample B"},
        "groups": {"medicine": "Group A", "other": "Other groups",
                   "ai_early": "Group B", "ai_late": "Group A"},
        "title": "Residualized X and Y",
    },
    "zh": {
        "x": "X 的残差", "y": "Y 的残差",
        "panels": {"all_fields": "(a) 样本 A", "computer_science": "(b) 样本 B"},
        "groups": {"medicine": "组 A", "other": "其他组",
                   "ai_early": "组 B", "ai_late": "组 A"},
        "title": "X 与 Y 的残差关系",
    },
}
PANELS = tuple(PANEL_GROUPS)

def check_config() -> None:
    if len(PANELS) != 2 or any(len(groups) not in (2, 3) for groups in PANEL_GROUPS.values()):
        raise ValueError("configure exactly two panels with two or three groups each")
    for p, groups in PANEL_GROUPS.items():
        if len(groups) != len(set(groups)) or any(g not in GROUP_STYLES for g in groups):
            raise ValueError(f"panel {p}: group IDs must be distinct and have styles")
    for lang, labels in TEXT.items():
        if set(PANELS) != set(labels["panels"]) or not set(sum(PANEL_GROUPS.values(), ())).issubset(labels["groups"]):
            raise ValueError(f"{lang}: missing panel or group display labels")

def read_data(path: Path) -> dict[str, dict[str, np.ndarray]]:
    data: dict[str, dict[str, list[tuple[float, float]]]] = {
        p: {g: [] for g in PANEL_GROUPS[p]} for p in PANELS
    }
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not {"panel", "group", "rx", "ry"}.issubset(reader.fieldnames or []):
            raise ValueError("CSV requires panel,group,rx,ry columns")
        for n, row in enumerate(reader, 2):
            p, g = row["panel"].strip(), row["group"].strip()
            if p not in data or g not in data[p]:
                raise ValueError(f"line {n}: unsupported panel/group {p}/{g}")
            try:
                x, y = float(row["rx"]), float(row["ry"])
            except ValueError as e:
                raise ValueError(f"line {n}: rx and ry must be numeric") from e
            if not np.isfinite([x, y]).all():
                raise ValueError(f"line {n}: rx and ry must be finite")
            data[p][g].append((x, y))
    out = {}
    for p in PANELS:
        out[p] = {}
        for g in PANEL_GROUPS[p]:
            if not data[p][g]:
                raise ValueError(f"panel/group {p}/{g} has no observations")
            out[p][g] = np.array(data[p][g], dtype=float)
        xy = np.vstack(list(out[p].values()))
        if len(xy) < 3 or np.ptp(xy[:, 0]) == 0:
            raise ValueError(f"panel {p} needs >=3 observations and varying rx")
    return out

def setup_font(lang: str) -> None:
    if lang == "zh":
        candidates = ("Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "Source Han Sans SC")
        for name in candidates:
            try:
                findfont(FontProperties(family=name), fallback_to_default=False)
                plt.rcParams["font.family"] = name
                break
            except ValueError:
                continue
        else:
            raise RuntimeError("No Chinese font found; install Microsoft YaHei, SimHei, or Noto Sans CJK SC")
    else:
        plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False

def plot(data, lang: str, output: Path, title: bool) -> dict:
    setup_font(lang)
    labels = TEXT[lang]
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 5.2), dpi=160)
    stats = {}
    for ax, p in zip(axes, PANELS):
        xy = np.vstack(list(data[p].values()))
        x, y = xy[:, 0], xy[:, 1]
        # OLS with intercept, using every observation shown in this panel.
        slope, intercept = np.polyfit(x, y, 1)
        line_x = np.linspace(x.min(), x.max(), 150)
        ax.plot(line_x, intercept + slope * line_x,
                color="#a9a9a9", linestyle=(0, (5, 3)), linewidth=1.3, zorder=1)
        for g in reversed(PANEL_GROUPS[p]):
            points = data[p][g]
            ax.scatter(points[:, 0], points[:, 1], marker="+", zorder=2,
                       label=labels["groups"][g], **GROUP_STYLES[g])
        handles, legends = ax.get_legend_handles_labels()
        order = [legends.index(labels["groups"][g]) for g in PANEL_GROUPS[p]]
        ax.legend([handles[i] for i in order], [legends[i] for i in order],
                  loc="upper center", bbox_to_anchor=(.5, -.15), ncol=len(order),
                  fontsize=8.5, frameon=True, fancybox=False, edgecolor="#555555",
                  borderpad=.45, handletextpad=.35, columnspacing=1.0)
        ax.set_xlabel(labels["x"], fontsize=10, labelpad=5)
        ax.set_ylabel(labels["y"], fontsize=10, labelpad=5)
        ax.set_title(labels["panels"][p], y=-.37, fontsize=11)
        ax.tick_params(labelsize=8.5, direction="out", length=4, color="#777777")
        for spine in ax.spines.values():
            spine.set_color("#555555")
        xpad, ypad = max(np.ptp(x) * .035, .04), max(np.ptp(y) * .08, .06)
        ax.set_xlim(x.min() - xpad, x.max() + xpad)
        ax.set_ylim(y.min() - ypad, y.max() + ypad)
        # Equation is computed from the same visible data as the dashed fit.
        ax.text(.06, .96, f"y = {intercept:+.3f} {slope:+.3f}x",
                transform=ax.transAxes, va="top", fontsize=9.5,
                bbox=dict(facecolor="white", edgecolor="none", alpha=.88, pad=1.5))
        stats[p] = {"n": int(len(x)), "intercept": float(intercept), "slope": float(slope)}
    if title:
        fig.suptitle(labels["title"], fontsize=13, y=.98)
    fig.subplots_adjust(left=.08, right=.985, top=.90 if title else .95,
                        bottom=.30, wspace=.22)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=200, facecolor="white")
    fig.savefig(output.with_suffix(".pdf"), facecolor="white")
    plt.close(fig)
    return stats

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--lang", choices=TEXT, default="en")
    parser.add_argument("--title", action="store_true")
    args = parser.parse_args()
    check_config()
    stats = plot(read_data(args.input), args.lang, args.output, args.title)
    for panel, v in stats.items():
        print(f"PANEL {panel} N={v['n']} intercept={v['intercept']:.6f} slope={v['slope']:.6f}")
    print(f"PYTHON_COMPLETE output={args.output.resolve()}")

if __name__ == "__main__":
    main()
