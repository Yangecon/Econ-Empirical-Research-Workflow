"""Synthetic weighted value distributions; no source microdata."""
from pathlib import Path
import csv
import numpy as np

rng = np.random.default_rng(20260928)
path = Path(__file__).with_name("demo.csv")
with path.open("w", newline="", encoding="utf-8") as handle:
    out = csv.writer(handle)
    out.writerow(["id", "series", "value", "weight"])
    for series, median, sigma in (("earlier", 18000, .55), ("later", 47000, .68)):
        values = rng.lognormal(np.log(median), sigma, 7000)
        weights = rng.uniform(.5, 1.5, len(values))
        for i, (value, weight) in enumerate(zip(values, weights), 1):
            out.writerow([f"{series}_{i:05d}", series, f"{value:.5f}", f"{weight:.8f}"])
print(f"DEMO_COMPLETE rows=14000 path={path}")
