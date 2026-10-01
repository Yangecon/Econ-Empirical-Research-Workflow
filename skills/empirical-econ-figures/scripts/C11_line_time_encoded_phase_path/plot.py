"""Draw a dated two-variable path using supplied transformed coordinates."""
import argparse
import csv
import json
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import is_color_like

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_shared"))
from line_geometry import draw_trace

PHASES = ("early", "middle", "late")
COLOR = {"early": "#636363", "middle": "#bcbcbc", "late": "#111111"}
TEXT = {
    "en": {"early": "Early", "middle": "Middle", "late": "Late",
           "x": "Log population", "y": "Log real wage", "title": "Real wages and population over time"},
    "zh": {"early": "早期", "middle": "中期", "late": "后期",
           "x": "人口的对数", "y": "实际工资的对数", "title": "实际工资与人口的时间轨迹"},
}


def load_config(path):
    spec = json.loads(Path(path).read_text(encoding="utf-8"))
    phases = spec.get("phases")
    if not isinstance(phases, list) or not phases:
        raise ValueError("config.phases must be a nonempty list")
    ids = []
    for row in phases:
        if not isinstance(row, dict) or any(not str(row.get(k, "")).strip() for k in ("id", "label_en", "label_zh")):
            raise ValueError("Each phase needs nonblank id, label_en and label_zh")
        if not is_color_like(row.get("color")) or row.get("linestyle", "-") not in ("-", "--", ":", "-."):
            raise ValueError("Phase color or linestyle is invalid")
        ids.append(row["id"])
    if len(set(ids)) != len(ids):
        raise ValueError("Phase IDs must be unique")
    axes = spec.get("axes", {})
    for lang in ("en", "zh"):
        if not isinstance(axes.get(lang), dict) or any(not str(axes[lang].get(k, "")).strip() for k in ("x", "y", "title")):
            raise ValueError(f"config.axes.{lang} needs nonblank x, y, title")
    return spec


def configured_phases(config=None):
    if config is None:
        return [{"id": p, "label_en": TEXT["en"][p], "label_zh": TEXT["zh"][p],
                 "color": COLOR[p], "linestyle": "-"} for p in PHASES]
    return config["phases"]


def load(path, config=None):
    cols = ("year", "x", "y", "phase", "year_label")
    with path.open(encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        if not set(cols).issubset(rd.fieldnames or []):
            raise ValueError(f"Required columns: {cols}")
        rows = list(rd)
    phase_order = [p["id"] for p in configured_phases(config)]
    if len(rows) < 2 * len(phase_order):
        raise ValueError("At least two dated points per configured phase required")
    years = np.array([float(r["year"]) for r in rows])
    x = np.array([float(r["x"]) for r in rows])
    y = np.array([float(r["y"]) for r in rows])
    if not all(np.isfinite(v).all() for v in (years, x, y)) or np.any(np.diff(years) <= 0):
        raise ValueError("Finite, strictly increasing years and finite coordinates required")
    phases = [r["phase"] for r in rows]
    if set(phases) != set(phase_order) or list(dict.fromkeys(phases)) != phase_order:
        raise ValueError("All configured phases required in order")
    for p in phase_order:
        ix = [i for i, v in enumerate(phases) if v == p]
        if ix != list(range(ix[0], ix[-1] + 1)) or len(ix) < 2:
            raise ValueError("Each phase must have at least two contiguous observations")
    for i, r in enumerate(rows):
        if r["year_label"] and (years[i] != int(years[i]) or r["year_label"] != str(int(years[i]))):
            raise ValueError("year_label must equal its integer year or be blank")
    return rows, years, x, y, phases


def draw(data, output, lang, title, config=None):
    output.parent.mkdir(parents=True, exist_ok=True)
    rows, years, x, y, phases = data
    plt.rcParams.update({"font.family": "Microsoft YaHei" if lang == "zh" else "DejaVu Sans",
                         "axes.unicode_minus": False, "pdf.fonttype": 42})
    specs = configured_phases(config)
    axes_text = TEXT if config is None else config["axes"]
    fig, ax = plt.subplots(figsize=(8.2, 5.5))
    for spec in specs:
        p = spec["id"]
        ix = np.array([i for i, v in enumerate(phases) if v == p])
        first = max(ix[0] - 1, 0)
        path = np.column_stack([x[first:ix[-1]+1], y[first:ix[-1]+1]])
        draw_trace(ax, path[:, 0], path[:, 1], linewidth=1.6, color=spec["color"],
                   linestyle=spec.get("linestyle", "-"), zorder=2,
                   label=spec["label_en"] if lang == "en" else spec["label_zh"])
        ax.scatter(x[ix], y[ix], s=32, color=spec["color"], zorder=3)
    xr, yr = np.ptp(x), np.ptp(y)
    for i, r in enumerate(rows):
        if r["year_label"]:
            ax.annotate(r["year_label"], (x[i], y[i]), xytext=(5, 5),
                        textcoords="offset points", fontsize=8.5)
    ax.set_xlim(x.min() - xr * .075, x.max() + xr * .10)
    ax.set_ylim(y.min() - yr * .10, y.max() + yr * .12)
    ax.set_xlabel(axes_text[lang]["x"])
    ax.set_ylabel(axes_text[lang]["y"])
    if title:
        ax.set_title(axes_text[lang]["title"], pad=11)
    ax.grid(color="#e6e6e6", lw=.7)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="lower right", frameon=False, ncol=min(len(specs), 3), fontsize=8.5)
    fig.tight_layout()
    fig.savefig(output, dpi=220)
    fig.savefig(output.with_suffix(".pdf"))
    plt.close(fig)
    with output.with_name(output.stem + "_checked.csv").open("w", encoding="utf-8", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=("year", "x", "y", "phase", "year_label"))
        wr.writeheader()
        wr.writerows({k: row[k] for k in wr.fieldnames} for row in rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--lang", choices=("en", "zh"), required=True)
    ap.add_argument("--title", action="store_true")
    ap.add_argument("--config", type=Path, help="Optional ordered phases and labels JSON")
    args = ap.parse_args()
    config = load_config(args.config) if args.config else None
    draw(load(args.input, config), args.output, args.lang, args.title, config)
