"""Synthetic binned beliefs and declared benchmarks; no source-data recovery."""
import csv
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--lang", choices=("en", "zh"), default="en")
language = parser.parse_args().lang
p=Path(__file__).resolve().parent
freq={
    "r1": [(3,42,2),(9,66,1),(12,84,2),(18,81,60),(21,75,4),(24,69,2),
           (15,15,12),(21,21,3),(30,12,2),(39,54,1),(69,69,1),(90,66,1),(99,99,0)],
    "r200": [(0,0,5),(3,42,25),(6,48,20),(9,42,8),(12,42,5),(15,21,4),
             (18,84,16),(21,81,12),(24,69,3),(30,60,2),(39,54,1),(90,90,0)],
}
with (p/"demo.csv").open("w",encoding="utf-8",newline="") as f:
    w=csv.writer(f)
    w.writerow(("panel","kind","x","y","count","reference_label"))
    for panel in ("r1","r200"):
        for x,y,n in freq[panel]:
            w.writerow((panel,"bubble",x,y,n,""))
        w.writerow((panel,"benchmark",6,42,"","bayesian"))
        w.writerow((panel,"benchmark",20,80,"","perfect_brn"))
body=(p/"plot.do").read_text(encoding="utf-8").replace("args input output lang showtitle\n","")
for lang in (language,):
    for suffix,title in (("","0"),("_title","1")):
        prefix=(                f'local input "{(p/"demo.csv").as_posix()}"\n'
                f'local output "{(p/f"stata_{lang}{suffix}.png").as_posix()}"\n'
                f'local lang "{lang}"\nlocal showtitle "{title}"\n')
        (p/f"run_{lang}{suffix}.do").write_text(prefix+body,encoding="utf-8")
prefix=(        f'local input "{(p/"qa_missing_count.csv").as_posix()}"\n'
        f'local output "{(p/"qa_missing_count_stata.png").as_posix()}"\n'
        'local lang "en"\nlocal showtitle "0"\n')
(p/"run_qa_missing_count.do").write_text(prefix+body,encoding="utf-8")
