"""Plot supplied admissible response bounds and representative response sequences."""
import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

LABEL = {
    "en": {"x": "Quarter (shock in period 1)", "y": "GDP growth response (pp)",
           "bounds": "Admissible bounds", "median": "Pointwise median", "maxg": "Supplied maxG path",
           "title": "Set-identified response to an uncertainty shock"},
    "zh": {"x": "季度（冲击发生于第1期）", "y": "GDP同比增速响应（百分点）",
           "bounds": "可容许响应上下界", "median": "逐期中位数", "maxg": "给定的maxG路径",
           "title": "不确定性冲击的集合识别响应"},
}


def load(path):
    fields = ("horizon", "admissible_low", "admissible_high", "pointwise_median", "maxg_response")
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not set(fields).issubset(reader.fieldnames or []):
            raise ValueError(f"Required columns: {fields}")
        rows = list(reader)
    if len(rows) < 3:
        raise ValueError("At least three horizons required")
    a = np.empty((len(rows), len(fields)), float)
    for i, r in enumerate(rows):
        for j, field in enumerate(fields):
            try:
                a[i, j] = float(r[field])
            except (TypeError, ValueError):
                raise ValueError(f"Non-numeric {field} at row {i+2}") from None
    if not np.isfinite(a).all() or np.any(a[:, 0] < 0) or np.any(np.diff(a[:, 0]) <= 0):
        raise ValueError("Horizons must be finite, nonnegative, strictly increasing, and unique")
    lo, hi, med, maxg = a[:, 1:].T
    if np.any((lo > hi) | (med < lo) | (med > hi) | (maxg < lo) | (maxg > hi)):
        raise ValueError("Bounds must contain each pointwise median and each maxG-path response")
    return a


def draw(a, output, lang, title):
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "Microsoft YaHei" if lang == "zh" else "DejaVu Sans",
                         "axes.unicode_minus": False, "pdf.fonttype": 42})
    h, lo, hi, med, maxg = a.T
    l = LABEL[lang]
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    ax.plot(h, lo, color="#26449b", lw=1.7, label=l["bounds"])
    ax.plot(h, hi, color="#26449b", lw=1.7)
    ax.plot(h, med, color="#238a4b", lw=1.55, marker="x", ms=5.4, mew=1.6, label=l["median"])
    ax.plot(h, maxg, color="#be3035", lw=1.55, marker="o", ms=4.4, mfc="white", mew=1.2, label=l["maxg"])
    ax.axhline(0, color="#4c4c4c", ls="--", lw=1.0, zorder=0)
    pad = max((hi.max()-lo.min())*.07, .08)
    ax.set_ylim(lo.min()-pad, hi.max()+pad)
    ax.set_xlim(h.min(), h.max())
    ax.set_xticks(h if len(h) <= 16 else np.linspace(h.min(), h.max(), 8))
    ax.set_xlabel(l["x"])
    ax.set_ylabel(l["y"])
    if title:
        ax.set_title(l["title"], pad=11)
    ax.grid(axis="y", color="#e7e7e7", lw=.65)
    ax.spines[["top", "right"]].set_visible(False)
    fig.legend(*ax.get_legend_handles_labels(), loc="lower center", bbox_to_anchor=(.5, .005),
               ncol=3, frameon=False, fontsize=8.5)
    fig.tight_layout(rect=(0, .075, 1, 1))
    fig.savefig(output, dpi=220)
    fig.savefig(output.with_suffix(".pdf"))
    plt.close(fig)
    with output.with_name(output.stem + "_checked.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(("horizon", "admissible_low", "admissible_high", "pointwise_median", "maxg_response"))
        w.writerows(a)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--lang", choices=("en", "zh"), required=True)
    p.add_argument("--title", action="store_true")
    arg = p.parse_args()
    draw(load(arg.input), arg.output, arg.lang, arg.title)
