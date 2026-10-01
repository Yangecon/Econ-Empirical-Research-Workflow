"""Render supplied binned observed counts and counterfactual counts near a notch."""
import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Edit these three positions and axis wording for a new policy setting.
NOTCH = 1000.0
EXCLUSION_LOW = 880.0
EXCLUSION_HIGH = 1200.0
LABEL = {
    "en": {"x": "Running variable", "y": "Number of observations", "observed": "Observed count",
           "counterfactual": "Supplied counterfactual", "notch": "Notch", "bounds": "Exclusion bounds", "title": "Distribution around a notch"},
    "zh": {"x": "运行变量", "y": "样本数", "observed": "实际人数",
           "counterfactual": "给定的反事实", "notch": "税收跳跃门槛", "bounds": "排除区间边界", "title": "门槛附近的分布"},
}


def load(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        need = ("bin_center", "observed_count", "counterfactual_count")
        if not set(need).issubset(reader.fieldnames or []):
            raise ValueError(f"Required columns: {need}")
        rows = list(reader)
    if len(rows) < 10:
        raise ValueError("At least 10 bins are needed")
    a = np.empty((len(rows), 3), float)
    for i, row in enumerate(rows):
        for j, col in enumerate(need):
            try:
                a[i, j] = float(row[col])
            except (TypeError, ValueError):
                raise ValueError(f"Non-numeric {col} in row {i+2}") from None
    if not np.isfinite(a).all() or np.any(a[:, 1:] < 0):
        raise ValueError("Counts must be finite and nonnegative")
    d = np.diff(a[:, 0])
    if np.any(d <= 0) or not np.allclose(d, d[0], atol=1e-9, rtol=1e-9):
        raise ValueError("Bin centers must be strictly increasing and equally spaced")
    if not (a[0, 0] < EXCLUSION_LOW < NOTCH < EXCLUSION_HIGH < a[-1, 0]):
        raise ValueError("Exclusion bounds and notch must be ordered inside the plotted bins")
    if not np.any(a[:, 0] < EXCLUSION_LOW) or not np.any(a[:, 0] > EXCLUSION_HIGH):
        raise ValueError("Need bins outside each side of the exclusion window")
    return a


def draw(a, output: Path, lang: str, title: bool):
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "Microsoft YaHei" if lang == "zh" else "DejaVu Sans",
                         "axes.unicode_minus": False, "pdf.fonttype": 42})
    x, observed, counterfactual = a.T
    l = LABEL[lang]
    fig, ax = plt.subplots(figsize=(8, 4.9))
    ax.plot(x, counterfactual, color="#858585", lw=1.7, label=l["counterfactual"], zorder=2)
    ax.plot(x, observed, color="#24547d", lw=1.15, marker="o", ms=2.4,
            label=l["observed"], zorder=3)
    for i, bound in enumerate((EXCLUSION_LOW, EXCLUSION_HIGH)):
        ax.axvline(bound, color="#757575", ls="--", lw=1.0,
                   label=l["bounds"] if i == 0 else "_nolegend_")
    ax.axvline(NOTCH, color="#c72535", ls=":", lw=1.7, label=l["notch"])
    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(0, max(observed.max(), counterfactual.max())*1.08)
    ax.set_xlabel(l["x"])
    ax.set_ylabel(l["y"])
    if title:
        ax.set_title(l["title"], pad=10)
    ax.grid(color="#e5e5e5", ls=":", lw=.7)
    ax.spines[["top", "right"]].set_visible(False)
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, frameon=False, ncol=4, loc="lower center",
               bbox_to_anchor=(.5, .005), fontsize=8)
    fig.tight_layout(rect=(0, .075, 1, 1))
    fig.savefig(output, dpi=220)
    fig.savefig(output.with_suffix(".pdf"))
    plt.close(fig)
    with output.with_name(output.stem + "_checked.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(("bin_center", "observed_count", "counterfactual_count"))
        w.writerows(a)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--lang", choices=("en", "zh"), required=True)
    p.add_argument("--title", action="store_true")
    args = p.parse_args()
    draw(load(args.input), args.output, args.lang, args.title)
