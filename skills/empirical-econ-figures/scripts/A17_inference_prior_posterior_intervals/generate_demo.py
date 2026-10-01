"""Generate illustrative saved intervals, not estimates from the article."""
import csv
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--lang", choices=("en", "zh"), default="en")
language = parser.parse_args().lang
p = Path(__file__).resolve().parent
panels = ("export_2019", "variety_2019", "export_2020", "variety_2020")
sources = ("literature", "firm", "policymaker", "academic")
with (p / "demo.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(("panel", "source", "kind", "median", "low", "high"))
    for pi, panel in enumerate(panels):
        scale = 1 if panel.startswith("export") else 26
        shift = -.025 if pi >= 2 else 0
        itt = (-.015 if pi < 2 else -.055) * scale
        w.writerow((panel, "diffuse", "posterior", round(itt+.004*scale, 5), round(itt-.065*scale, 5), round(itt+.075*scale, 5)))
        for j, source in enumerate(sources):
            pm = (.075 + .014*j + shift) * scale
            pw = (.095 + .01*j) * scale
            post = itt + (.022 + .004*j)*scale
            postw = (.055 + .005*j)*scale
            w.writerow((panel, source, "posterior", round(post, 5), round(post-postw, 5), round(post+postw, 5)))
            w.writerow((panel, source, "prior", round(pm, 5), round(pm-pw, 5), round(pm+pw, 5)))
        w.writerow((panel, "itt", "itt", round(itt, 5), round(itt-.075*scale, 5), round(itt+.075*scale, 5)))

body = (p / "plot.do").read_text(encoding="utf-8").replace("args input output lang showtitle\n", "")
for lang in (language,):
    for suffix, title in (("", "0"), ("_title", "1")):
        prefix = (                  f'local input "{(p / "demo.csv").as_posix()}"\n'
                  f'local output "{(p / f"stata_{lang}{suffix}.png").as_posix()}"\n'
                  f'local lang "{lang}"\nlocal showtitle "{title}"\n')
        (p / f"run_{lang}{suffix}.do").write_text(prefix + body, encoding="utf-8")
for case in ("qa_bad_interval", "qa_missing_pair", "qa_reordered_columns"):
    prefix = (              f'local input "{(p / (case + ".csv")).as_posix()}"\n'
              f'local output "{(p / (case + "_stata.png")).as_posix()}"\n'
              'local lang "en"\nlocal showtitle "0"\n')
    (p / f"run_{case}.do").write_text(prefix + body, encoding="utf-8")
