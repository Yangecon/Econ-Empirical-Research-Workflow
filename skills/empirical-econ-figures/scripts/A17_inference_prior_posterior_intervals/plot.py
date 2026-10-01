"""Compare supplied prior/posterior medians and frequentist ITT estimates."""
import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Panel identifiers, display labels and units are editable together.
PANELS = [
    ("export_2019", "Exporting, 2019", "出口参与，2019", "Probability-point effect", "概率差"),
    ("variety_2019", "Product-country varieties, 2019", "产品—国家种类，2019", "Count effect", "数量差"),
    ("export_2020", "Exporting, 2020", "出口参与，2020", "Probability-point effect", "概率差"),
    ("variety_2020", "Product-country varieties, 2020", "产品—国家种类，2020", "Count effect", "数量差"),
]
ROWS = [
    ("diffuse", "posterior", 10), ("literature", "posterior", 9), ("literature", "prior", 8),
    ("firm", "posterior", 7), ("firm", "prior", 6),
    ("policymaker", "posterior", 5), ("policymaker", "prior", 4),
    ("academic", "posterior", 3), ("academic", "prior", 2), ("itt", "itt", 1),
]
NAME = {"en": {"diffuse": "Diffuse", "literature": "Literature", "firm": "Firm",
               "policymaker": "Policymaker", "academic": "Academic", "itt": "ITT"},
        "zh": {"diffuse": "弥散", "literature": "文献", "firm": "企业",
               "policymaker": "政策制定者", "academic": "学者", "itt": "ITT"}}
TYPE = {"en": {"prior": "prior: median / 95% prior interval", "posterior": "posterior: median / 95% posterior interval", "itt": "ITT: estimate / 95% CI"},
        "zh": {"prior": "先验：中位数 / 95%先验区间", "posterior": "后验：中位数 / 95%后验区间", "itt": "ITT：估计值 / 95%置信区间"}}


def load(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        required = {"panel", "source", "kind", "median", "low", "high"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"Required columns: {sorted(required)}")
        rows = list(reader)
    expected = {(p[0], source, kind) for p in PANELS for source, kind, _ in ROWS}
    actual = set()
    for i, r in enumerate(rows):
        key = (r["panel"], r["source"], r["kind"])
        if key not in expected or key in actual:
            raise ValueError(f"Unknown or duplicate panel/source/kind in row {i+2}: {key}")
        actual.add(key)
        for col in ("median", "low", "high"):
            try:
                r[col] = float(r[col])
            except (TypeError, ValueError):
                raise ValueError(f"Non-numeric {col} in row {i+2}") from None
        if not np.isfinite([r["median"], r["low"], r["high"]]).all() or not r["low"] <= r["median"] <= r["high"]:
            raise ValueError(f"Invalid interval in row {i+2}")
    if actual != expected or len(rows) != len(expected):
        raise ValueError(f"Expected exactly {len(expected)} configured panel/source/kind rows")
    return {(r["panel"], r["source"], r["kind"]): r for r in rows}


def draw(data, output, lang, title):
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "Microsoft YaHei" if lang == "zh" else "DejaVu Sans",
                         "axes.unicode_minus": False, "pdf.fonttype": 42})
    fig, axes = plt.subplots(2, 2, figsize=(15, 10.2))
    colors = {"prior": "#1595bf", "posterior": "#425e72", "itt": "#be232e"}
    for ax, panel in zip(axes.flat, PANELS):
        pid = panel[0]
        values = [data[(pid, source, kind)] for source, kind, _ in ROWS]
        allends = [v[z] for v in values for z in ("low", "high")]
        spread = max(allends) - min(allends)
        pad = max(spread * .07, .02 if pid.startswith("export") else .4)
        ax.set_xlim(min(allends)-pad, max(allends)+pad)
        for source, kind, y in ROWS:
            r = data[(pid, source, kind)]
            ax.plot((r["low"], r["high"]), (y, y), color=colors[kind], lw=2.5 if kind == "itt" else 1.35,
                    ls="--" if kind == "prior" else "-", solid_capstyle="butt")
            ax.plot(r["median"], y, "o", ms=5.5 if kind == "itt" else 4.2,
                    color="#161616", zorder=4)
        ax.axvline(0, color="#c5c5c5", lw=.8, zorder=0)
        ax.set_ylim(.4, 10.6)
        ax.set_yticks([r[2] for r in ROWS],
                      ["ITT" if s == "itt" else f"{NAME[lang][s]} {k if lang == 'en' else {'prior':'先验','posterior':'后验'}[k]}"
                       for s, k, _ in ROWS], fontsize=8.5)
        ax.set_title(panel[1] if lang == "en" else panel[2], fontsize=11, pad=8)
        ax.set_xlabel(panel[3] if lang == "en" else panel[4], fontsize=9)
        ax.grid(axis="x", color="#eaeaea", ls="--", lw=.7)
        ax.spines[["top", "right", "left"]].set_visible(False)
        ax.tick_params(axis="y", length=0)
    handles = [plt.Line2D([0], [0], color=colors[k], ls="--" if k == "prior" else "-", lw=2.4) for k in ("prior", "posterior", "itt")]
    fig.legend(handles, [TYPE[lang][k] for k in ("prior", "posterior", "itt")],
               loc="lower center", bbox_to_anchor=(.5, .005), ncol=3, frameon=False, fontsize=9)
    if title:
        fig.suptitle("Prior, posterior and frequentist estimates" if lang == "en" else "先验、后验与频率派估计比较", y=.997, fontsize=15)
    fig.tight_layout(rect=(0, .05, 1, .965 if title else 1), h_pad=2.5, w_pad=2.7)
    fig.savefig(output, dpi=200)
    fig.savefig(output.with_suffix(".pdf"))
    plt.close(fig)
    with output.with_name(output.stem + "_checked.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(("panel", "source", "kind", "median", "low", "high"))
        for panel in PANELS:
            for source, kind, _ in ROWS:
                r = data[(panel[0], source, kind)]
                w.writerow((panel[0], source, kind, r["median"], r["low"], r["high"]))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--lang", choices=("en", "zh"), required=True)
    p.add_argument("--title", action="store_true")
    a = p.parse_args()
    draw(load(a.input), a.output, a.lang, a.title)
