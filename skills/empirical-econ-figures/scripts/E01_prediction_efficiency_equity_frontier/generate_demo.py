"""Synthetic model-output paths and supplied confidence bounds (not bootstrap results)."""
from pathlib import Path
import numpy as np
import pandas as pd

rates = np.unique(np.concatenate([np.linspace(0, 3, 16), [1.45]]))
specs = [
    ("credit_prediction", 4900, 3.25, .18),
    ("credit_oracle", 7800, 2.05, .22),
    ("total_prediction", 7100, -1.05, .16),
    ("total_oracle", 13200, -.45, .20),
]
rows = []
for aid, xmax, yend, width in specs:
    for r in rates:
        x = xmax*(r/3)**.9
        y = yend*(r/3)**.8 + (.1*np.sin(r*3) if r else 0)
        half = width*(r/3)**.65
        rows.append((aid, r, x, y, y-half, y+half, int(abs(r-1.45)<1e-8)))
rows.append(("status_quo", 1.45, 2100, 1.9, "", "", 0))
pd.DataFrame(rows, columns=["algorithm", "policy_rate", "efficiency", "disparity",
                            "ci_low", "ci_high", "operating"]).to_csv(
    Path(__file__).with_name("demo.csv"), index=False, float_format="%.12g")
print(f"DEMO_COMPLETE rows={len(rows)}")
