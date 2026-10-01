"""Plot supplied quantile-specific estimates and confidence intervals."""
import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

LABEL = {
    "en": {"x": "Quantile of outcome distribution", "y": "Coefficient", "title": "Coefficient across quantiles"},
    "zh": {"x": "结果分布分位数", "y": "回归系数", "title": "不同分位数的回归系数"},
}


def load(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        needed = {"quantile_percent", "estimate", "ci_low", "ci_high"}
        if not needed.issubset(reader.fieldnames or []):
            raise ValueError(f"Required columns: {sorted(needed)}")
        rows = list(reader)
    if len(rows) < 3:
        raise ValueError("At least three quantiles are required")
    values = np.empty((len(rows), 4), float)
    for i, row in enumerate(rows):
        for j, col in enumerate(("quantile_percent", "estimate", "ci_low", "ci_high")):
            try:
                values[i, j] = float(row[col])
            except (TypeError, ValueError):
                raise ValueError(f"Non-numeric {col} in row {i+2}") from None
    if not np.isfinite(values).all():
        raise ValueError("All numeric fields must be finite")
    if np.any((values[:, 0] <= 0) | (values[:, 0] >= 100)):
        raise ValueError("Quantiles must lie strictly between 0 and 100")
    if np.any(np.diff(values[:, 0]) <= 0):
        raise ValueError("Quantile rows must be strictly increasing and unique")
    if np.any((values[:, 2] > values[:, 1]) | (values[:, 1] > values[:, 3])):
        raise ValueError("Each confidence interval must contain its estimate")
    return values


def draw(values, output: Path, lang: str, title: bool):
    output.parent.mkdir(parents=True, exist_ok=True)
    font = "Microsoft YaHei" if lang == "zh" else "DejaVu Sans"
    plt.rcParams.update({"font.family": font, "axes.unicode_minus": False, "pdf.fonttype": 42})
    q, estimate, low, high = values.T
    fig, ax = plt.subplots(figsize=(7.1, 4.8))
    ax.errorbar(q, estimate, yerr=np.vstack((estimate-low, high-estimate)), fmt="o-",
                color="#252525", ecolor="#858585", lw=1.5, elinewidth=1.4,
                capsize=3, markersize=6.5, markerfacecolor="#5d5d5d", zorder=3)
    if low.min() <= 0 <= high.max():
        ax.axhline(0, color="#b5b5b5", lw=0.9, zorder=0)
    ax.set_xlim(max(0, q.min()-5), min(100, q.max()+5))
    pad = max((high.max()-low.min())*0.065, 0.015)
    ax.set_ylim(low.min()-pad, high.max()+pad)
    ax.set_xticks(q if len(q) <= 10 else np.linspace(q.min(), q.max(), 5))
    ax.set_xlabel(LABEL[lang]["x"])
    ax.set_ylabel(LABEL[lang]["y"])
    if title:
        ax.set_title(LABEL[lang]["title"], pad=11)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#ebebeb", lw=0.7)
    fig.tight_layout()
    fig.savefig(output, dpi=220)
    fig.savefig(output.with_suffix(".pdf"))
    plt.close(fig)
    with output.with_name(output.stem + "_checked.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(("quantile_percent", "estimate", "ci_low", "ci_high"))
        writer.writerows(values)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--lang", choices=("en", "zh"), required=True)
    p.add_argument("--title", action="store_true")
    a = p.parse_args()
    draw(load(a.input), a.output, a.lang, a.title)


if __name__ == "__main__":
    main()
