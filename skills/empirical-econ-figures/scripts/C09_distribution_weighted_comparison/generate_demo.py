"""Synthetic establishments for F34 drawing only; no paper values."""
from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(34)
rows = []
for year, shift in [(1967, 0), (2012, -.13)]:
    for industry, mean, n in [("A", .35, 150), ("B", .63, 170), ("C", .85, 130)]:
        shares = np.clip(rng.normal(mean+shift, .19, n), .01, 1.39)
        va = rng.lognormal(mean=1.0 + .35*float(industry == "B"), sigma=.7, size=n)
        rows += [{"year": year, "industry": industry,
                  "establishment_id": f"{year}-{industry}-{i:03d}",
                  "labor_share": round(float(s), 5), "value_added": round(float(v), 5)}
                 for i, (s, v) in enumerate(zip(shares, va))]
path = Path(__file__).with_name("demo.csv")
pd.DataFrame(rows).to_csv(path, index=False)
print(f"SYNTHETIC_DEMO_OK rows={len(rows)}")
