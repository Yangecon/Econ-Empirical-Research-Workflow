"""Synthetic observations only; scheduled dates supplied by explicit anchors."""
from pathlib import Path
import pandas as pd

here = Path(__file__).resolve().parent
pd.DataFrame({"date": ["2024-01-01", "2024-01-07", "2024-02-29", "2024-07-04"],
              "schedule": ["6_day", "6_day", "3_day", "3_day"]}).to_csv(here / "demo_observed.csv", index=False)
print("SYNTHETIC_OBSERVATIONS_OK")
