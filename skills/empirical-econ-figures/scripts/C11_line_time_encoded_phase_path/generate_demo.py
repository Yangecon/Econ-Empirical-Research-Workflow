"""Synthetic coordinates: visual grammar only, no digitized history."""
import csv
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--lang", choices=("en", "zh"), default="en")
language = parser.parse_args().lang
p = Path(__file__).resolve().parent
rows = [
    (1250,20.70,-5.08,"early"),(1300,20.54,-5.36,"early"),
    (1350,20.30,-5.24,"early"),(1400,20.18,-4.84,"early"),
    (1450,20.39,-4.69,"early"),(1500,20.23,-4.74,"early"),
    (1550,20.47,-5.00,"middle"),(1600,20.76,-5.12,"middle"),
    (1650,20.83,-5.27,"middle"),(1700,21.05,-5.10,"middle"),
    (1730,21.00,-4.95,"middle"),(1760,21.19,-5.04,"middle"),
    (1780,21.10,-5.14,"middle"),(1800,21.52,-5.06,"middle"),
    (1810,21.68,-4.96,"late"),(1820,21.84,-4.86,"late"),
    (1830,21.98,-4.75,"late"),(1840,22.08,-4.68,"late"),
    (1850,22.19,-4.61,"late"),(1860,22.30,-4.51,"late"),
]
labels = {1250,1450,1600,1730,1800,1860}
with (p / "demo.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(("year","x","y","phase","year_label"))
    for year,x,y,phase in rows:
        w.writerow((year,x,y,phase,str(year) if year in labels else ""))

body = (p / "plot.do").read_text(encoding="utf-8").replace("args input output lang showtitle\n", "")
for lang in (language,):
    for suffix,title in (("","0"),("_title","1")):
        prefix = (                  f'local input "{(p / "demo.csv").as_posix()}"\n'
                  f'local output "{(p / f"stata_{lang}{suffix}.png").as_posix()}"\n'
                  f'local lang "{lang}"\nlocal showtitle "{title}"\n')
        (p / f"run_{lang}{suffix}.do").write_text(prefix + body, encoding="utf-8")
for case in ("qa_unsorted", "qa_repeated_phase"):
    prefix = (              f'local input "{(p / (case + ".csv")).as_posix()}"\n'
              f'local output "{(p / (case + "_stata.png")).as_posix()}"\n'
              'local lang "en"\nlocal showtitle "0"\n')
    (p / f"run_{case}.do").write_text(prefix + body, encoding="utf-8")
