from pathlib import Path
import csv,math

p=Path(__file__).resolve().parent
rows=[]
for k in range(20):
    low=k/20;high=(k+1)/20;x=(low+high)/2
    price=.47*math.exp(-5.7*x)-.022+ .006*math.sin(16*x)
    prod=.19*(1-x)-.31*x+.012*math.cos(12*x)
    rows.append([round(low,4),round(high,4),round(price,6),round(prod,6),round(price+prod,6)])
with (p/"demo.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.writer(f);w.writerow(["bin_low","bin_high","relative_price","relative_productivity","relative_sales_per_worker"]);w.writerows(rows)
