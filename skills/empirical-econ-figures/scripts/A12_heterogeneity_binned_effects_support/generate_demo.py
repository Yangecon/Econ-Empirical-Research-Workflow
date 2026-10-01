"""Synthetic four-panel effect and separate unconditional-support tables."""
from pathlib import Path
import csv
import numpy as np

ROOT = Path(__file__).parent
rng = np.random.default_rng(20260928)
panels = [
    ("destination_share", 1, "share"),
    ("destination_degree", 2, "degree"),
    ("home_share", 3, "share"),
    ("home_degree", 4, "degree"),
]
with (ROOT / "effect_demo.csv").open("w", newline="", encoding="utf-8") as handle:
    out = csv.writer(handle)
    out.writerow(["panel", "panel_order", "x", "estimate", "ci_low", "ci_high"])
    for panel, order, kind in panels:
        xs = np.arange(.025, 1., .05) if kind == "share" else np.arange(1, 21)
        for i, x in enumerate(xs):
            if kind == "share":
                estimate = (.025 + .025*x + .006*np.sin(11*x + order))
                half = .003 + .004*(abs(x-.55)/.55)**2
            else:
                estimate = .12 + .045*x + .12*np.sin(x*.5 + order)
                half = .25 + .024*x
            out.writerow([panel, order, f"{x:.8f}", f"{estimate:.8f}",
                          f"{estimate-half:.8f}", f"{estimate+half:.8f}"])
with (ROOT / "support_demo.csv").open("w", newline="", encoding="utf-8") as handle:
    out = csv.writer(handle)
    out.writerow(["panel", "panel_order", "x_left", "x_right", "count"])
    for panel, order, kind in panels:
        if kind == "share":
            lefts = np.arange(0, 1., .05)
            centers = lefts + .025
            base = np.exp(-.5*((centers-(.60 if order == 1 else .56))/.18)**2)
            counts = np.rint((8000 if order == 1 else 6000)*base + rng.integers(80, 260, len(base))).astype(int)
            width = .05
        else:
            lefts = np.arange(.5, 20.5, 1.)
            centers = lefts + .5
            base = np.exp(-centers/(3.3 if order == 2 else 8.0))
            counts = np.rint((14000 if order == 2 else 5000)*base + rng.integers(50, 180, len(base))).astype(int)
            width = 1.
        for left, count in zip(lefts, counts):
            out.writerow([panel, order, f"{left:.8f}", f"{left+width:.8f}", int(count)])
print("DEMO_COMPLETE effects=80 support_bins=80 synthetic")
