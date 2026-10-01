"""Deterministic synthetic counts; these numbers are not extracted from the article."""
import csv
import math
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--lang", choices=("en", "zh"), default="en")
language = parser.parse_args().lang
p = Path(__file__).resolve().parent
with (p / "demo.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(("bin_center", "observed_count", "counterfactual_count"))
    for x in range(505, 1500, 10):
        cf = 1650 * math.exp(-(x - 500) / 270) + 185
        if x < 1000:
            bump = 630 * math.exp(-((x - 985) / 43) ** 2)
            obs = cf + bump + 16 * math.sin(x / 21)
        else:
            obs = cf * (0.39 + 0.58 * (1 - math.exp(-(x - 1000) / 190))) + 14 * math.sin(x / 23)
        w.writerow((x, round(max(0, obs), 5), round(cf, 5)))

body = (p / "plot.do").read_text(encoding="utf-8").replace("args input output lang showtitle\n", "")
for lang in (language,):
    for suffix, title in (("", "0"), ("_title", "1")):
        prefix = (                  f'local input "{(p / "demo.csv").as_posix()}"\n'
                  f'local output "{(p / f"stata_{lang}{suffix}.png").as_posix()}"\n'
                  f'local lang "{lang}"\nlocal showtitle "{title}"\n')
        (p / f"run_{lang}{suffix}.do").write_text(prefix + body, encoding="utf-8")
for case in ("qa_negative_count", "qa_unequal_bins"):
    prefix = (              f'local input "{(p / (case + ".csv")).as_posix()}"\n'
              f'local output "{(p / (case + "_stata.png")).as_posix()}"\n'
              'local lang "en"\nlocal showtitle "0"\n')
    (p / f"run_{case}.do").write_text(prefix + body, encoding="utf-8")
