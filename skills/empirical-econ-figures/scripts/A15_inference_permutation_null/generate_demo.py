"""Synthetic supplied-null-draw example; this is not a randomization procedure."""
from pathlib import Path
import csv
import numpy as np

rng = np.random.default_rng(20260928)
panels = [
    ("setting_a", 1, "Setting A", "情景甲", .38, .050, .54),
    ("setting_b", 2, "Setting B", "情景乙", .40, .048, .55),
]
path = Path(__file__).with_name("demo.csv")
with path.open("w", newline="", encoding="utf-8") as handle:
    out = csv.writer(handle)
    out.writerow(["panel", "panel_order", "panel_label_en", "panel_label_zh", "draw_id", "null_stat", "observed_stat"])
    for panel, order, en, zh, mean, sd, observed in panels:
        draws = np.clip(rng.normal(mean, sd, 2500), 0, 1)
        for i, draw in enumerate(draws, 1):
            out.writerow([panel, order, en, zh, i, f"{draw:.8f}", f"{observed:.8f}"])
print(f"DEMO_COMPLETE rows=5000 path={path}")
