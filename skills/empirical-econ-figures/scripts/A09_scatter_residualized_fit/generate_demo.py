"""Create deterministic synthetic already-residualized example observations."""
from pathlib import Path
import csv
import numpy as np

OUT = Path(__file__).with_name("demo.csv")
rng = np.random.default_rng(20260928)
rows = []

def add(panel, group, n, x_sd, slope, noise_sd, x_shift=0.0, y_shift=0.0):
    x = rng.normal(x_shift, x_sd, n)
    y = slope * x + rng.normal(y_shift, noise_sd, n)
    rows.extend((panel, group, round(float(a), 6), round(float(b), 6))
                for a, b in zip(x, y))

# The values demonstrate the visual grammar. They are not digitized paper data.
add("all_fields", "other", 255, 1.20, .22, .55)
add("all_fields", "medicine", 185, .37, .22, .37)
add("computer_science", "other", 160, .22, .70, .23)
add("computer_science", "ai_early", 31, .15, .70, .12)
add("computer_science", "ai_late", 9, .20, .70, .15, .28, .09)

with OUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["panel", "group", "rx", "ry"])
    writer.writerows(rows)
print(f"DEMO_COMPLETE rows={len(rows)} path={OUT}")
