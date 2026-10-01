"""Create synthetic bounded observations with ties and deliberate outliers."""
from pathlib import Path
import csv
import numpy as np

rng = np.random.default_rng(20260928)
path = Path(__file__).with_name("demo.csv")
with path.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle)
    writer.writerow(["id", "group", "group_order", "group_label_en", "group_label_zh", "value"])
    for g in range(1, 11):
        vals = np.round(rng.beta(2.0 + g * .4, 11 - g * .55, 68), 2)
        vals = np.r_[vals, [0., 1.]]
        for i, val in enumerate(vals, 1):
            writer.writerow([f"g{g:02d}_{i:03d}", f"decile_{g}", g, str(g), str(g), f"{val:.2f}"])
print(f"DEMO_COMPLETE rows=700 path={path}")
