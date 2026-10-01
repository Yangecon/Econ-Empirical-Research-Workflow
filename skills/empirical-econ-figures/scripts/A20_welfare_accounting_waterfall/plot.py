"""Paired money waterfalls with a separate dimensionless ratio."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

GROUPS=[("group_a","Group A","组 A"),("group_b","Group B","组 B")]
LEDGERS=["revenue","wtp"]
ITEMS={
 "audit_cost":("Audit cost","审计成本"),"upfront_revenue":("Upfront revenue","当期收入"),
 "interim_revenue":("Interim revenue","阶段收入"),
 "deterrence_revenue":("Deterrence revenue","威慑收入"),"net_revenue":("Net revenue","净收入"),
 "upfront_taxes":("Upfront taxes","当期税款"),"deterrence_taxes":("Deterrence taxes","威慑税款"),
 "response_burden":("Response burden","应对负担"),"net_wtp":("Net WTP","净支付意愿")}
TEXT={"en":{"axis":"Amount per additional $1 of audit spending","ratio":"MVPF = WTP / net revenue","title":"Accounting for marginal audits"},
      "zh":{"axis":"每增加 1 美元审计支出的金额（美元）","ratio":"MVPF = 支付意愿 / 政府净收入","title":"边际审计的福利核算"}}

def read(path:Path)->tuple[pd.DataFrame,pd.DataFrame]:
    df=pd.read_csv(path,dtype=str,keep_default_na=False)
    req={"group","ledger","seq","item","kind","value"}
    if not req.issubset(df): raise ValueError(f"Missing columns: {req-set(df)}")
    if len(df)==0 or df[list(req)].eq("").any().any(): raise ValueError("Blank or empty input")
    if set(df.group)!=set(g[0] for g in GROUPS) or set(df.ledger)!=set(LEDGERS): raise ValueError("Unknown/missing group or ledger")
    if set(df.kind)-{"component","subtotal","total"}: raise ValueError("Unknown kind")
    if set(df.item)-set(ITEMS): raise ValueError("Unknown item")
    for c in ("seq","value"):
        df[c]=pd.to_numeric(df[c],errors="raise")
        if not np.isfinite(df[c]).all(): raise ValueError("Nonfinite number")
    if not (df.seq>=1).all() or not np.equal(df.seq,df.seq.astype(int)).all(): raise ValueError("seq must be a positive integer")
    df["seq"]=df.seq.astype(int)
    allowed={"revenue":{"audit_cost","upfront_revenue","interim_revenue","deterrence_revenue","net_revenue"},
             "wtp":{"upfront_taxes","deterrence_taxes","response_burden","net_wtp"}}
    if any(r.item not in allowed[r.ledger] for r in df.itertuples()): raise ValueError("Item assigned to wrong ledger")
    records=[];ratios=[];blueprints={}
    for group,_,_ in GROUPS:
        totals={}
        for ledger in LEDGERS:
            d=df[(df.group==group)&(df.ledger==ledger)].sort_values("seq")
            if len(d)<3 or d.seq.tolist()!=list(range(1,len(d)+1)) or d.kind.iloc[-1]!="total" or (d.kind=="total").sum()!=1:
                raise ValueError("Each group-ledger requires contiguous steps and one final total")
            if d.item.duplicated().any(): raise ValueError("Duplicate item")
            if d.item.iloc[-1] != ("net_revenue" if ledger=="revenue" else "net_wtp"):
                raise ValueError("Final total item does not match ledger")
            blueprint=list(zip(d.seq,d.item,d.kind))
            if ledger in blueprints and blueprints[ledger]!=blueprint: raise ValueError("Group steps must align")
            blueprints[ledger]=blueprint
            running=0.0
            for r in d.itertuples():
                if r.kind=="component":
                    bottom=min(running,running+r.value);top=max(running,running+r.value);running+=r.value
                else:
                    if abs(r.value-running)>1e-8: raise ValueError("Subtotal/total does not balance")
                    bottom=min(0,r.value);top=max(0,r.value)
                records.append({**r._asdict(),"bottom":bottom,"top":top,"running":running})
            totals[ledger]=running
        if totals["revenue"]<=0: raise ValueError("Net revenue denominator must be positive")
        ratios.append({"group":group,"net_revenue":totals["revenue"],"net_wtp":totals["wtp"],"mvpf":totals["wtp"]/totals["revenue"]})
    return pd.DataFrame(records).drop(columns=["Index"]),pd.DataFrame(ratios)

def draw(df:pd.DataFrame,ratios:pd.DataFrame,output:Path,lang:str,title:bool):
    if lang=="zh":
        fonts=[f.name for f in font_manager.fontManager.ttflist]
        for name in ("Microsoft YaHei","Noto Sans CJK SC","SimHei"):
            if name in fonts: plt.rcParams["font.family"]=name;break
    plt.rcParams["axes.unicode_minus"]=False
    fig,axes=plt.subplots(2,1,figsize=(11.5,8.6),layout="constrained")
    colors={"component":"#c4c7c9","subtotal":"#7a9db8","total":"#406d91"}
    revmax=int(df.loc[df.ledger=="revenue","seq"].max());wtpmax=int(df.loc[df.ledger=="wtp","seq"].max())
    offset=revmax+1
    for ax,(group,en,zh) in zip(axes,GROUPS):
        d=df[df.group==group]
        ymin=min(-1.8,float(d.bottom.min())-.8)
        ymax=float(d.top.max())+max(1.1,.15*float(d.top.max()))
        for ledger,shift in (("revenue",0),("wtp",offset)):
            part=d[d.ledger==ledger]
            for r in part.itertuples():
                x=shift+r.seq
                ax.bar(x,r.top-r.bottom,bottom=r.bottom,width=.65,color=colors[r.kind],edgecolor="white",linewidth=.7)
                y=r.top+.12 if r.value>=0 else r.bottom-.17
                ax.text(x,y,f"{r.value:+.2f}" if r.kind=="component" else f"{r.value:.2f}",ha="center",va="bottom" if r.value>=0 else "top",fontsize=8,color="#333333")
        ax.axhline(0,color="#777777",lw=.8)
        ax.set_ylim(ymin,ymax);ax.set_xlim(.25,offset+wtpmax+.75)
        ax.set_xticks([*range(1,revmax+1),*[offset+i for i in range(1,wtpmax+1)]])
        ax.set_xticklabels([ITEMS[r.item][0 if lang=="en" else 1].replace(" ","\n") for r in d.sort_values(["ledger","seq"]).itertuples()],fontsize=8)
        ax.set_ylabel(TEXT[lang]["axis"])
        ax.text(.01,.96,en if lang=="en" else zh,transform=ax.transAxes,ha="left",va="top",weight="bold",fontsize=11)
        ratio=float(ratios.loc[ratios.group==group,"mvpf"].iloc[0])
        ax.text(offset,-.85,f"{TEXT[lang]['ratio']}: {ratio:.2f}",ha="center",va="center",fontsize=9)
        ax.spines[["top","right"]].set_visible(False)
    if title: fig.suptitle(TEXT[lang]["title"],fontsize=13)
    output.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(output,dpi=220)
    fig.savefig(output.with_suffix(".pdf"))
    plt.close(fig)

def main():
    p=argparse.ArgumentParser();p.add_argument("--input",required=True,type=Path);p.add_argument("--output",required=True,type=Path)
    p.add_argument("--lang",choices=["en","zh"],default="en");p.add_argument("--title",action="store_true");a=p.parse_args()
    d,r=read(a.input);a.output.parent.mkdir(parents=True,exist_ok=True)
    d.to_csv(a.output.with_name(a.output.stem+"_checked.csv"),index=False)
    r.to_csv(a.output.with_name(a.output.stem+"_ratios.csv"),index=False)
    draw(d,r,a.output,a.lang,a.title)
    print(f"WATERFALL_COMPLETE rows={len(d)} groups={len(r)} output={a.output}")
if __name__=="__main__":main()
