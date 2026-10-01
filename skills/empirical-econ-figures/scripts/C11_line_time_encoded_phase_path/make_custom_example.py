"""Invent a two-phase variant of the accepted synthetic path."""
from pathlib import Path
import pandas as pd

p = Path(__file__).parent
data = pd.read_csv(p / "demo.csv", dtype={"year_label": str}, keep_default_na=False)
data["phase"] = ["pre"] * 10 + ["post"] * (len(data) - 10)
data.to_csv(p / "custom_demo.csv", index=False)
