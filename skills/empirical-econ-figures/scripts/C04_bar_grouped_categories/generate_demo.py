"""Invented subgroup counts, never article attendance rates."""
from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(527)
cats = ["small", "lower_middle", "middle", "upper_middle", "large", "very_large"]
rows = []
for i, cid in enumerate(cats):
    for gid, offset in (("before", .04), ("after", 0)):
        n = int(rng.integers(250, 420))
        p = .24 + .045*i + offset + .015*np.sin(i+int(gid=="before"))
        successes = int(rng.binomial(n, p))
        rows.append((cid, gid, successes, n))
pd.DataFrame(rows, columns=["category", "group", "numerator", "denominator"]).to_csv(
    Path(__file__).with_name("demo.csv"), index=False)
print(f"DEMO_COMPLETE rows={len(rows)}")
