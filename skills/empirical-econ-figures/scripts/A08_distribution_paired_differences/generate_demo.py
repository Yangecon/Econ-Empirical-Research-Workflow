"""Synthetic twin-profile pairs for drawing; never paper data."""
from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(5)
black = rng.poisson(23, 130)
white = np.maximum(0, black + rng.normal(3.2, 6.5, 130).round().astype(int))
pd.DataFrame({"pair_id": [f"twin_{i:03d}" for i in range(130)],
              "black_contacts": black, "white_contacts": white}).to_csv(
                  Path(__file__).with_name("demo_pairs.csv"), index=False)
print("SYNTHETIC_PAIRS_OK")
