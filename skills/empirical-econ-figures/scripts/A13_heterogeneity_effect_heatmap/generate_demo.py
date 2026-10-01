from pathlib import Path
import csv

p=Path(__file__).resolve().parent
rows=[]
for panel in ("te","jobs"):
    for sd in range(1,6):
        for sr in range(1,6):
            if panel=="te": value=round(.065+.014*sr+.008*sd+.003*((sr*sd)%3),4)
            else: value=round(.08+.11*sr+.055*sd+.025*((sr+sd)%4),4)
            rows.append([panel,sr,sd,value])
with (p/"demo.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.writer(f);w.writerow(["panel","sr","sd","value"]);w.writerows(rows)
