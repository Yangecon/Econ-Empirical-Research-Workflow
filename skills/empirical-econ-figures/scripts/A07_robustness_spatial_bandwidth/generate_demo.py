from pathlib import Path
import csv,math

p=Path(__file__).resolve().parent
outcomes=[("poverty",-.040,.008),("unmet_needs",-.098,.011),("housing",-.052,.006),
          ("health",-.021,.004),("education",-.013,.004),("consumption",-.020,.004)]
rows=[]
for j,(name,base,spread) in enumerate(outcomes):
    for k in range(61):
        bw=5+.25*k
        est=base+spread*((bw-11.5)/15)**2+.0012*math.sin(k/4+j)
        cl=est-(.007+.002*abs(bw-11)/10)*(1+j*.12)
        ch=est+(.0075+.002*abs(bw-11)/10)*(1+j*.12)
        cy=est+(.020+.002*abs(bw-12)/10)*(1+j*.08)
        cx=est-(.021+.002*abs(bw-12)/10)*(1+j*.08)
        rows.append([name,round(bw,4),round(est,6),round(cl,6),round(ch,6),round(cx,6),round(cy,6)])
with (p/"demo.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.writer(f);w.writerow(["outcome","bandwidth_km","estimate","cluster_low","cluster_high","conley_low","conley_high"]);w.writerows(rows)
