"""Synthetic mixed-unit four-outcome kink demonstration."""
from pathlib import Path
import numpy as np
import pandas as pd

here = Path(__file__).resolve().parent
rng = np.random.default_rng(20260928)
rows = []
for panel in ("replacement", "takeup", "risk_basic", "risk_comprehensive"):
    x = rng.uniform(500, 1200, 4400)
    x[:3] = [500, 850, 1200]
    z = x-850
    if panel == "replacement":
        y = .79-.000025*z-.00058*np.maximum(z, 0)+rng.normal(0, .006, len(z))
    elif panel == "takeup":
        p = np.clip(.85+.00016*z-.00013*np.maximum(z, 0), .01, .99)
        y = rng.binomial(1, p)
    elif panel == "risk_basic":
        y = 1.9+.00055*z+.0021*np.maximum(z, 0)+rng.normal(0, .50, len(z))
    else:
        y = 8.8+.00028*z+.0028*np.maximum(z, 0)+rng.normal(0, .55, len(z))
    rows.append(pd.DataFrame({"panel": panel, "id": [f"{panel}_{i:05d}" for i in range(len(z))],
                              "running": x, "outcome": y}))
pd.concat(rows, ignore_index=True).to_csv(here / "demo.csv", index=False, float_format="%.12g")
print("DEMO_COMPLETE rows=17600 panels=4 threshold=850")
