"""Generate invented smooth heavy-tail density grid for drawing demonstration."""
from pathlib import Path
import numpy as np
import pandas as pd

x = np.linspace(-4, 4, 161)
# Piecewise tails with exact log-linear slopes; center is deliberately sharp.
log_density = np.where(x < -1, -1.4 + 1.4 * (x + 1),
               np.where(x > 1, -1.4 - 2.18 * (x - 1), 1.1 - 2.5 * np.abs(x)))
density = np.exp(log_density)
density /= np.trapz(density, x)  # Normalize this finite-grid demonstration only.
pd.DataFrame({"x": x, "density": density}).to_csv(Path(__file__).with_name("demo_density.csv"), index=False)
