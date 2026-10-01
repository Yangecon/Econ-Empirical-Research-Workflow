"""Create an illustrative gridded policy response, not a structural-model estimate."""
import csv
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--lang", choices=("en", "zh"), default="en")
language = parser.parse_args().lang
p = Path(__file__).resolve().parent
with (p / "demo.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(("fee_change_pct", "denial_change_pct", "acceptance_change", "payment_change_usd"))
    for y in range(-30, 31, 2):
        for x in range(-20, 21, 2):
            a = y - 1.9*x + .003*x*y
            pay = 1.1*x - .055*y + .0008*x*y
            w.writerow((x, y, round(a, 6), round(pay, 6)))

with (p / "qa_horizontal.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(("fee_change_pct", "denial_change_pct", "acceptance_change", "payment_change_usd"))
    for y in range(-30, 31, 2):
        for x in range(-20, 21, 2):
            w.writerow((x, y, round(y - 1.9*x + .003*x*y, 6), y))

body = (p / "plot.do").read_text(encoding="utf-8").replace("args input output lang showtitle\n", "")
for lang in (language,):
    for suffix, title in (("", "0"), ("_title", "1")):
        prefix = (                  f'local input "{(p / "demo.csv").as_posix()}"\n'
                  f'local output "{(p / f"stata_{lang}{suffix}.png").as_posix()}"\n'
                  f'local lang "{lang}"\nlocal showtitle "{title}"\n')
        (p / f"run_{lang}{suffix}.do").write_text(prefix + body, encoding="utf-8")
prefix = (          f'local input "{(p / "qa_horizontal.csv").as_posix()}"\n'
          f'local output "{(p / "qa_horizontal_stata.png").as_posix()}"\n'
          'local lang "en"\nlocal showtitle "0"\n')
(p / "run_qa_horizontal.do").write_text(prefix + body, encoding="utf-8")
for case in ("qa_missing_cell", "qa_bad_baseline"):
    prefix = (              f'local input "{(p / (case + ".csv")).as_posix()}"\n'
              f'local output "{(p / (case + "_stata.png")).as_posix()}"\n'
              'local lang "en"\nlocal showtitle "0"\n')
    (p / f"run_{case}.do").write_text(prefix + body, encoding="utf-8")
