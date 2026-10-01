"""Generate illustrative binary outcomes; no observations come from the source paper."""
from pathlib import Path
import numpy as np
import pandas as pd

here = Path(__file__).resolve().parent
rng = np.random.default_rng(20260928)
parts = []
for panel, bandwidth, n in (("outcome_a", 16.0, 2400), ("outcome_b", 25.0, 3500)):
    x = rng.uniform(-bandwidth, bandwidth, n)
    x[:12] = 0.0  # exercise the right-of-cutoff convention
    x[12:14] = [-bandwidth, bandwidth]  # exercise both closed window endpoints
    if panel == "outcome_a":
        p = np.where(x < 0, .09 - .005*x, .175 - .009*x)
    else:
        p = np.where(x < 0, .022 + .0002*x, .016 + .00045*x)
    y = rng.binomial(1, p)
    parts.append(pd.DataFrame({"panel": panel, "id": [f"{panel}_{i:05d}" for i in range(n)],
                               "running": x, "outcome": y}))
demo = pd.concat(parts, ignore_index=True)
demo.to_csv(here / "demo.csv", index=False, float_format="%.12g")
print(f"DEMO_COMPLETE rows={len(demo)} zero_running={(demo.running == 0).sum()}")
