"""Two invented, already-dispatched equal-demand scenarios."""
from pathlib import Path
import numpy as np
import pandas as pd

rows = []
for scenario in ["Spatial constraints and curtailment", "Unconstrained"]:
    constrained = scenario.startswith("Spatial")
    for i in range(30):
        mwh = 3000.0
        if i < (10 if constrained else 11):
            cost = 0.0
        elif i < 15:
            cost = 18.0
        else:
            cost = 19 + (i-15) * (2.4 if constrained else 1.25)
        rows.append({"scenario": scenario, "unit_id": f"unit_{i:02d}",
                     "marginal_cost": round(cost, 3), "dispatched_mwh": mwh})
pd.DataFrame(rows).to_csv(Path(__file__).with_name("demo_dispatch.csv"), index=False)
print("SYNTHETIC_DISPATCH_OK common_demand_mwh=90000")
