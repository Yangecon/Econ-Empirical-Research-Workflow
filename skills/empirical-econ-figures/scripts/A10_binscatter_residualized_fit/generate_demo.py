"""Deterministic synthetic already-residualized observations."""
from pathlib import Path
import csv
import numpy as np

out = Path(__file__).with_name("demo.csv")
rng = np.random.default_rng(20260928)
n = 503
rx = np.round(np.clip(rng.normal(0, .32, n), -.92, .92), 2)  # ties are intentional
ry = -.32*rx + rng.normal(0, .36, n)
with out.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "rx", "ry"])
    for i, (x, y) in enumerate(zip(rx, ry), 1):
        writer.writerow([f"obs{i:06d}", f"{x:.6f}", f"{y:.8f}"])
print(f"DEMO_COMPLETE rows={n} tied_rx={n-len(set(rx))} output={out}")
