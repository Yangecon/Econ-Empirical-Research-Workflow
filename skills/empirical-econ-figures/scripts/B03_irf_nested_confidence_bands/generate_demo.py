"""Invented 5x5 posterior-summary matrix; no article estimates."""
from pathlib import Path
import numpy as np
import pandas as pd

responses = ["activity", "prices", "rate", "household_credit", "business_credit"]
shocks = ["monetary", "household", "firm", "stress_a", "stress_b"]
amplitudes = np.array([
    [-.006, -.001, -.0015, -.004, -.002],
    [-.004, .004, .002, -.002, -.0025],
    [.004, .0006, .0012, -.0015, -.001],
    [-.018, .012, .009, -.004, -.009],
    [-.014, .001, .014, -.014, -.006],
])
widths = [.002, .002, .0011, .0038, .004]
rows = []
for i, response in enumerate(responses):
    for j, shock in enumerate(shocks):
        for h in range(0, 61, 3):
            scale = (1-np.exp(-h/11))*np.exp(-h/180)
            median = amplitudes[i, j]*scale + amplitudes[i,j]*.08*np.sin(h/11)*scale
            w90 = widths[i]*(.2+.8*(1-np.exp(-h/18)))
            w68 = w90*.55
            rows.append((response, shock, h, median, median-w68, median+w68,
                         median-w90, median+w90))
pd.DataFrame(rows, columns=["response", "shock", "horizon", "median", "lo68", "hi68", "lo90", "hi90"]).to_csv(
    Path(__file__).with_name("demo.csv"), index=False, float_format="%.12g")
print(f"DEMO_COMPLETE rows={len(rows)}")
