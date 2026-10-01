"""Contour two supplied policy-counterfactual surfaces on a complete rectangular grid."""
import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PAYMENT_LEVELS = (-20, -15, -10, -5, 0, 5, 10, 15, 20)  # dollars per visit, editable
LABEL = {
    "en": {"x": "Change in fee (%)", "y": "Relative change in denial probability (%)",
           "payment": "Payment change ($/visit)", "accept": "Constant acceptance", "base": "Observed baseline",
           "title": "Policy counterfactuals: fees and denials"},
    "zh": {"x": "费用变化（%）", "y": "拒付概率相对变化（%）",
           "payment": "每次就诊支付变化（美元）", "accept": "接受率不变", "base": "观测基准",
           "title": "费用与拒付的政策反事实"},
}


def load(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        need = {"fee_change_pct", "denial_change_pct", "acceptance_change", "payment_change_usd"}
        if not need.issubset(reader.fieldnames or []):
            raise ValueError(f"Required columns: {sorted(need)}")
        rows = list(reader)
    vals = {}
    for i, r in enumerate(rows):
        try:
            x, y, a, pay = (float(r[c]) for c in ("fee_change_pct", "denial_change_pct", "acceptance_change", "payment_change_usd"))
        except (TypeError, ValueError):
            raise ValueError(f"Nonnumeric grid value in row {i+2}") from None
        if not np.isfinite((x, y, a, pay)).all() or (x, y) in vals:
            raise ValueError(f"Nonfinite or duplicate grid point in row {i+2}")
        vals[(x, y)] = (a, pay)
    xs = np.array(sorted({x for x, _ in vals}), float)
    ys = np.array(sorted({y for _, y in vals}), float)
    if len(xs) < 5 or len(ys) < 5 or len(vals) != len(xs)*len(ys):
        raise ValueError("Need a complete rectangular grid with at least five unique values per axis")
    if 0 not in xs or 0 not in ys or not np.allclose(vals[(0., 0.)], (0., 0.), atol=1e-9):
        raise ValueError("Origin (0,0) must be present and normalized to zero on both surfaces")
    acceptance = np.array([[vals[(x, y)][0] for x in xs] for y in ys])
    payment = np.array([[vals[(x, y)][1] for x in xs] for y in ys])
    if not (acceptance.min() < 0 < acceptance.max() and payment.min() < min(PAYMENT_LEVELS) < max(PAYMENT_LEVELS) < payment.max()):
        raise ValueError("Surfaces must span the configured contour levels")
    return xs, ys, acceptance, payment


def draw(data, output, lang, title):
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "Microsoft YaHei" if lang == "zh" else "DejaVu Sans",
                         "axes.unicode_minus": False, "pdf.fonttype": 42})
    x, y, a, p = data
    fig, ax = plt.subplots(figsize=(7.7, 6.1))
    cp = ax.contour(x, y, p, levels=PAYMENT_LEVELS, colors="#6a6a6a", linewidths=1.0, linestyles="--")
    ca = ax.contour(x, y, a, levels=[0], colors="#171717", linewidths=2.1)
    black = np.concatenate(ca.allsegs[0])
    positions = []
    for level, parts in zip(cp.levels, cp.allsegs):
        candidates = np.concatenate(parts)
        interior = ((candidates[:, 0] > x.min()+.02*np.ptp(x)) &
                    (candidates[:, 0] < x.max()-.02*np.ptp(x)) &
                    (candidates[:, 1] > y.min()+.15*np.ptp(y)) &
                    (candidates[:, 1] < y.max()-.15*np.ptp(y)))
        candidates = candidates[interior] if interior.any() else candidates
        delta = (candidates[:, None, :] - black[None, :, :]) / np.array([np.ptp(x), np.ptp(y)])
        distance = np.sqrt(np.sum(delta*delta, axis=2)).min(axis=1)
        target = y.max()*.55 if level < 0 else y.min()*.55
        safe = distance > .09
        selection = np.flatnonzero(safe) if safe.any() else np.arange(len(candidates))
        score = np.abs(candidates[selection, 1]-target)/np.ptp(y) - .1*distance[selection]
        positions.append(tuple(candidates[selection[np.argmin(score)]]))
    ax.clabel(cp, manual=positions, fmt=lambda v: f"{v:g}", fontsize=8, inline=True)
    ax.plot(0, 0, "o", color="#be2e3c", ms=5, zorder=5)
    ax.set_xlabel(LABEL[lang]["x"])
    ax.set_ylabel(LABEL[lang]["y"])
    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(y.min(), y.max())
    if title:
        ax.set_title(LABEL[lang]["title"], pad=12)
    from matplotlib.lines import Line2D
    handles = [Line2D([0], [0], color="#171717", lw=2.1),
               Line2D([0], [0], color="#6a6a6a", ls="--"),
               Line2D([0], [0], marker="o", color="none", markerfacecolor="#be2e3c", markeredgecolor="#be2e3c")]
    fig.legend(handles, [LABEL[lang]["accept"], LABEL[lang]["payment"], LABEL[lang]["base"]],
               loc="lower center", bbox_to_anchor=(.5, .005), ncol=3, frameon=False, fontsize=8)
    fig.tight_layout(rect=(0, .065, 1, 1))
    fig.savefig(output, dpi=220)
    fig.savefig(output.with_suffix(".pdf"))
    plt.close(fig)
    with output.with_name(output.stem + "_contours.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(("kind", "level", "x", "y"))
        for kind, obj in (("payment", cp), ("acceptance", ca)):
            for level, parts in zip(obj.levels, obj.allsegs):
                for part in parts:
                    for xx, yy in part:
                        w.writerow((kind, level, xx, yy))
    with output.with_name(output.stem + "_checked.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(("fee_change_pct", "denial_change_pct", "acceptance_change", "payment_change_usd"))
        for j, yy in enumerate(y):
            for i, xx in enumerate(x):
                w.writerow((xx, yy, a[j, i], p[j, i]))


if __name__ == "__main__":
    q = argparse.ArgumentParser()
    q.add_argument("--input", type=Path, required=True)
    q.add_argument("--output", type=Path, required=True)
    q.add_argument("--lang", choices=("en", "zh"), required=True)
    q.add_argument("--title", action="store_true")
    arg = q.parse_args()
    draw(load(arg.input), arg.output, arg.lang, arg.title)
