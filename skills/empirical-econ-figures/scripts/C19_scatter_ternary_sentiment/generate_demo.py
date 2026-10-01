"""Generate synthetic books; neither topics nor sentiment are source-paper estimates."""
from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(4848)
centers = [1550, 1600, 1650, 1700, 1750, 1800, 1850]
rows = []
for j, center in enumerate(centers):
    n = [80, 120, 180, 290, 410, 560, 700][j]
    topics = rng.dirichlet([3.5 - .35 * j, 3.4, .6 + .48 * j], size=n)
    years = rng.integers(center - 9, center + 10, size=n)
    sentiment = np.clip(.15 + .55 * topics[:, 2] + .08 * j / 6 + rng.normal(0, .16, n), 0, 1)
    for i in range(n):
        rows.append((f"demo_{center}_{i:04d}", years[i], *topics[i], sentiment[i]))
rows.extend([("demo_political_vertex", 1550, 0, 1, 0, .1),
             ("demo_religion_vertex", 1600, 1, 0, 0, .5),
             ("demo_science_vertex", 1850, 0, 0, 1, .9)])
pd.DataFrame(rows, columns=["book_id", "year", "religion", "political_economy", "science",
                            "sentiment_percentile"]).to_csv(Path(__file__).with_name("demo_books.csv"), index=False)
