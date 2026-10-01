"""Invented irregular nested cell memberships; no bootstrap algorithm implied."""
from pathlib import Path
import numpy as np
import pandas as pd

here = Path(__file__).resolve().parent
dx, dy = .04, .01
rows = []
for x in np.round(np.arange(0, 1.801, dx), 6):
    for y in np.round(np.arange(0, .461, dy), 6):
        centerline = .045 + .225*x - .052*x*x + .007*np.sin(9*x)
        score = abs(x-.75)/.32 + abs(y-centerline)/.08 + .08*np.sin(12*y+5*x)
        flags = [int(score <= cutoff) for cutoff in [.9, 1.35, 1.9]]
        rows.append({"x_center": x, "y_center": y,
                     "x_lo": round(x-dx/2, 6), "x_hi": round(x+dx/2, 6),
                     "y_lo": round(y-dy/2, 6), "y_hi": round(y+dy/2, 6),
                     "in90": flags[0], "in95": flags[1], "in99": flags[2]})
pd.DataFrame(rows).to_csv(here / "demo_joint_grid.csv", index=False)
pd.DataFrame({"x": [.68], "y": [.135]}).to_csv(here / "demo_point.csv", index=False)
print(f"SYNTHETIC_NESTED_GRID_OK cells={len(rows)}")
