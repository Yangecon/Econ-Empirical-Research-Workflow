"""Deterministic invented households for drawing-method checks only."""
from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(412)
n = 900
rank = rng.lognormal(mean=3.2, sigma=.65, size=n)
weight = rng.uniform(.6, 1.6, size=n)
expenditure = rank * rng.lognormal(0, .12, n)
fuel = np.maximum(rank - np.quantile(rank, .53), 0)**1.7 * rng.uniform(.5, 1.4, n)
out = pd.DataFrame({"id": [f"H{i+1:04d}" for i in range(n)], "rank_value": rank,
                    "weight": weight, "expenditure": expenditure, "fuel": fuel})
out.to_csv(Path(__file__).with_name("demo.csv"), index=False, float_format="%.12g")
print(f"DEMO_COMPLETE rows={n}")
