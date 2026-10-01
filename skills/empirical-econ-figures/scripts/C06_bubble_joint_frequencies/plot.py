"""Two-panel joint-frequency bubbles with one global area scale."""
import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PANELS = ("r1", "r200")
LABEL = {
    "en": {"r1": "Round 1", "r200": "Round 200", "x": "Belief conditional on negative signal (%)",
           "y": "Belief conditional on positive signal (%)", "title": "Joint belief frequencies"},
    "zh": {"r1": "第1轮", "r200": "第200轮", "x": "负信号条件下的信念（%）",
           "y": "正信号条件下的信念（%）", "title": "二维信念联合频数"},
}
REFERENCE = {"en": {"bayesian": "Bayesian", "perfect_brn": "Perfect BRN"},
             "zh": {"bayesian": "贝叶斯基准", "perfect_brn": "完全基率忽略"}}


def load(path):
    fields = ("panel", "kind", "x", "y", "count", "reference_label")
    with path.open(encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        if not set(fields).issubset(rd.fieldnames or []):
            raise ValueError(f"Required columns: {fields}")
        rows = list(rd)
    if not rows or set(r["panel"] for r in rows) != set(PANELS):
        raise ValueError("Both configured panels required")
    seen = set()
    for i, r in enumerate(rows):
        if r["kind"] not in ("bubble", "benchmark"):
            raise ValueError(f"Unknown kind at row {i+2}")
        try:
            x, y = float(r["x"]), float(r["y"])
        except (ValueError, TypeError):
            raise ValueError(f"Invalid coordinate at row {i+2}") from None
        if not np.isfinite([x, y]).all() or not (0 <= x <= 100 and 0 <= y <= 100):
            raise ValueError("Beliefs must lie in [0,100]")
        if r["kind"] == "bubble":
            try:
                count = int(r["count"])
            except (ValueError, TypeError):
                raise ValueError("Bubble count must be a nonnegative integer") from None
            if count < 0 or str(count) != r["count"].strip() or r["reference_label"]:
                raise ValueError("Bubble rows require an integer count and no reference label")
            key = (r["panel"], x, y)
            if key in seen:
                raise ValueError("Duplicate bubble coordinate within panel")
            seen.add(key)
        elif r["count"].strip() or r["reference_label"] not in REFERENCE["en"]:
            raise ValueError("Benchmark needs a configured reference ID and blank count")
    for p in PANELS:
        if not any(r["panel"] == p and r["kind"] == "bubble" and int(r["count"]) > 0 for r in rows):
            raise ValueError("Each panel needs a positive-frequency bubble")
    return rows


def draw(rows, output, lang, title):
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "Microsoft YaHei" if lang == "zh" else "DejaVu Sans",
                         "axes.unicode_minus": False, "pdf.fonttype": 42})
    max_count = max(int(r["count"]) for r in rows if r["kind"] == "bubble")
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.8), sharex=True, sharey=True)
    for ax, panel in zip(axes, PANELS):
        bubbles = [r for r in rows if r["panel"] == panel and r["kind"] == "bubble" and int(r["count"]) > 0]
        counts = np.array([int(r["count"]) for r in bubbles])
        diameters_pt = 27 * np.sqrt(counts / max_count)
        ax.scatter([float(r["x"]) for r in bubbles], [float(r["y"]) for r in bubbles],
                   s=diameters_pt**2, color="#ed6769", alpha=.76, edgecolors="none", zorder=2)
        for r in rows:
            if r["panel"] == panel and r["kind"] == "benchmark":
                x, y = float(r["x"]), float(r["y"])
                ax.scatter([x], [y], s=86, marker="^", color="#222222", zorder=4)
                ax.annotate(REFERENCE[lang][r["reference_label"]], (x, y), xytext=(8, 0),
                            textcoords="offset points", va="center", fontsize=8.5)
        ax.set_title(LABEL[lang][panel], fontsize=11)
        ax.set_xlim(-3, 105)
        ax.set_ylim(-3, 105)
        ax.set_xticks(np.arange(0, 101, 20))
        ax.set_yticks(np.arange(0, 101, 20))
        ax.grid(color="#ececec", lw=.6, zorder=0)
        ax.spines[["top", "right"]].set_visible(False)
    fig.supxlabel(LABEL[lang]["x"])
    fig.supylabel(LABEL[lang]["y"])
    if title:
        fig.suptitle(LABEL[lang]["title"], y=.99)
    fig.tight_layout(rect=(.02, .035, 1, .96 if title else 1))
    fig.savefig(output, dpi=220)
    fig.savefig(output.with_suffix(".pdf"))
    plt.close(fig)
    with output.with_name(output.stem + "_checked.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=("panel", "kind", "x", "y", "count", "reference_label", "bubble_area_ratio"))
        w.writeheader()
        for r in rows:
            w.writerow({k: (int(r["count"]) / max_count if k == "bubble_area_ratio" and r["kind"] == "bubble" else "" if k == "bubble_area_ratio" else r[k]) for k in w.fieldnames})


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--lang", required=True, choices=("en", "zh"))
    ap.add_argument("--title", action="store_true")
    a = ap.parse_args()
    draw(load(a.input), a.output, a.lang, a.title)
