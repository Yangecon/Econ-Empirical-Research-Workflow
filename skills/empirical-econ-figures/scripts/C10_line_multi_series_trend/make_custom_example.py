"""Invent three externally named series from the accepted synthetic demo."""
from pathlib import Path
import pandas as pd

p = Path(__file__).parent
source = pd.read_csv(p / "demo.csv")
a = source.loc[source.series == "patents"].assign(series="coastal")
b = source.loc[source.series == "publications"].assign(series="inland")
c = source.loc[source.series == "patents"].assign(series="services", value=lambda d: d.value * .7 + .6)
pd.concat([a, b, c], ignore_index=True).sort_values(["date", "series"]).to_csv(p / "custom_demo.csv", index=False)
