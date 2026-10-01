"""Generate reproducible synthetic individual probabilities."""
import csv
import random
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--lang", choices=("en", "zh"), default="en")
language = parser.parse_args().lang
p=Path(__file__).resolve().parent
rng=random.Random(20260928)
rows=[]
for i in range(120):
    x=0.0 if i<5 else .99 if i>=115 else .99*(i/119)**2
    y=min(1.0,max(0.0,.12+.8*x+rng.uniform(-.10,.10)))
    rows.append((f"obs_{i+1:04d}",round(x,8),round(y,8)))
for i in range(40):
    x=1.0
    y=min(1.0,max(0.0,.90+rng.uniform(-.07,.07)))
    rows.append((f"obs_{121+i:04d}",x,round(y,8)))
with (p/"demo.csv").open("w",encoding="utf-8",newline="") as f:
    w=csv.writer(f);w.writerow(("id","true_prob","predicted_prob"));w.writerows(rows)
body=(p/"plot.do").read_text(encoding="utf-8").replace("args input output lang showtitle\n","")
for lang in (language,):
    for suffix,title in (("","0"),("_title","1")):
        prefix=(f'local input "{(p/"demo.csv").as_posix()}"\n'
                f'local output "{(p/f"stata_{lang}{suffix}.png").as_posix()}"\n'
                f'local lang "{lang}"\nlocal showtitle "{title}"\n')
        (p/f"run_{lang}{suffix}.do").write_text(prefix+body,encoding="utf-8")
prefix=(f'local input "{(p/"qa_bad_probability.csv").as_posix()}"\n'
        f'local output "{(p/"qa_bad_probability_stata.png").as_posix()}"\n'
        'local lang "en"\nlocal showtitle "0"\n')
(p/"run_qa_bad_probability.do").write_text(prefix+body,encoding="utf-8")
