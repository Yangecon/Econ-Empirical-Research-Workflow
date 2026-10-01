"""Generate deterministic illustrative response summaries, not source estimates."""
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
    w.writerow(("horizon", "admissible_low", "admissible_high", "pointwise_median", "maxg_response"))
    for h in range(1, 16):
        median = -1.65 if h <= 3 else -.065 - 1.585*math.exp(-(h-3)/1.25)
        low = median - (.36*math.exp(-h/12)+.07)
        high = median + (.43*math.exp(-h/11)+.08)
        maxg = median - (.14*math.exp(-h/7)+.015)
        w.writerow((h, *(round(v, 6) for v in (low, high, median, maxg))))

body = (p / "plot.do").read_text(encoding="utf-8").replace("args input output lang showtitle\n", "")
for lang in (language,):
    for suffix, title in (("", "0"), ("_title", "1")):
        prefix = (                  f'local input "{(p / "demo.csv").as_posix()}"\n'
                  f'local output "{(p / f"stata_{lang}{suffix}.png").as_posix()}"\n'
                  f'local lang "{lang}"\nlocal showtitle "{title}"\n')
        (p / f"run_{lang}{suffix}.do").write_text(prefix + body, encoding="utf-8")
for case in ("qa_outside_bounds", "qa_unsorted"):
    prefix = (              f'local input "{(p / (case + ".csv")).as_posix()}"\n'
              f'local output "{(p / (case + "_stata.png")).as_posix()}"\n'
              'local lang "en"\nlocal showtitle "0"\n')
    (p / f"run_{case}.do").write_text(prefix + body, encoding="utf-8")
