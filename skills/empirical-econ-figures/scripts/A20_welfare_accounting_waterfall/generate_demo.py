from pathlib import Path
import csv

here=Path(__file__).resolve().parent
rows=[]
for group,upfront,deterrence,burden in [
    ("group_a",2.4,1.8,0.3), ("group_b",4.7,5.3,0.7)
]:
    ledgers={
        "revenue":[("audit_cost",-1.0),("upfront_revenue",upfront),("deterrence_revenue",deterrence)],
        "wtp":[("upfront_taxes",upfront),("deterrence_taxes",deterrence),("response_burden",burden)]
    }
    for ledger,items in ledgers.items():
        running=0
        for seq,(item,value) in enumerate(items,1):
            running+=value
            rows.append([group,ledger,seq,item,"component",value])
            if ledger=="revenue" and seq==2:
                rows.append([group,ledger,3,"interim_revenue","subtotal",running])
        if ledger=="revenue":
            for row in rows:
                if row[0]==group and row[1]==ledger and row[2]==3 and row[4]=="component": row[2]=4
        rows.append([group,ledger,5 if ledger=="revenue" else 4,"net_revenue" if ledger=="revenue" else "net_wtp","total",running])
with (here/"demo.csv").open("w",newline="",encoding="utf-8") as f:
    w=csv.writer(f);w.writerow(["group","ledger","seq","item","kind","value"]);w.writerows(rows)
