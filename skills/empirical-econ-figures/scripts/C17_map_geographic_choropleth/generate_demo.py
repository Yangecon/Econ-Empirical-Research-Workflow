"""Invent regional values for a drawing demonstration; source geometry is real."""
import json
from pathlib import Path
import numpy as np
import pandas as pd

p = Path(__file__).parent
features = json.loads((p / "cameroon_adm1.geojson").read_text(encoding="utf-8"))["features"]
rng = np.random.default_rng(45)
rows = []
for f in features:
    prop = f["properties"]
    rows.append({"shapeID": prop["shapeID"], "value": round(float(rng.uniform(0, 10)), 1)})
rows[-1]["value"] = np.nan  # Explicit missing-data hatch demonstration.
pd.DataFrame(rows).to_csv(p / "demo_region_values.csv", index=False)
