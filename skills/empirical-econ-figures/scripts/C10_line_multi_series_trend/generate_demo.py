"""Invented upstream rate series, with explicit missing years."""
from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(372)
years = np.arange(1980, 2016)
patents = 3.0*(1+.005*(years-1980)+.12*np.sin((years-1980)/2.5)+rng.normal(0,.025,len(years)))
publications = 1.7*(1-.012*(years-1980)+.08*np.sin((years-1980)/2.4)+rng.normal(0,.025,len(years)))
rows = []
for year, pat, pub in zip(years, patents, publications):
    if year not in (1988, 1989):
        rows.append((f"{year}-01-01", "patents", max(pat,.01)))
    if year not in (1996, 1997):
        rows.append((f"{year}-01-01", "publications", max(pub,.01)))
pd.DataFrame(rows, columns=["date", "series", "value"]).to_csv(
    Path(__file__).with_name("demo.csv"), index=False, float_format="%.12g")
print(f"DEMO_COMPLETE rows={len(rows)}")
