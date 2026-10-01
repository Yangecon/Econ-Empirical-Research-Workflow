"""Synthetic scenario-by-acuity CDF curves; no paper values are reproduced."""
from pathlib import Path
import csv
import numpy as np

OUT = Path(__file__).with_name("demo.csv")
x_values = np.arange(-120, 521, 4, dtype=float)
# Values control only synthetic curve shapes. They are not read from Figure 10.
CURVES = {
    "forced_attention": {
        "low": (.78, 24, 20),
        "medium": (.52, 29, 92),
        "high": (.31, 34, 165),
    },
    "no_switching_costs": {
        "low": (.58, 26, 31),
        "medium": (.43, 29, 45),
        "high": (.27, 32, 58),
    },
}
with OUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["panel", "panel_order", "group", "group_order", "x_reduction", "cdf"])
    n = 0
    for panel_order, (panel, groups) in enumerate(CURVES.items(), 1):
        for group_order, (group, (mass_at_zero, left_scale, right_scale)) in enumerate(groups.items(), 1):
            curve = np.where(x_values < 0,
                             mass_at_zero * np.exp(x_values / left_scale),
                             1 - (1 - mass_at_zero) * np.exp(-x_values / right_scale))
            for x, cdf in zip(x_values, curve):
                writer.writerow([panel, panel_order, group, group_order,
                                 f"{x:.0f}", f"{cdf:.8f}"])
                n += 1
print(f"DEMO_COMPLETE rows={n} output={OUT}")
