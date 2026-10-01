"""Signed stacks for an additive two-component decomposition."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

COLS=["bin_low","bin_high","relative_price","relative_productivity","relative_sales_per_worker"]
TEXT={"en":{"x":"Labor share","y":"Relative log components","price":"Relative prices","prod":"Relative physical labor productivity","title":"Components of relative sales per worker"},
      "zh":{"x":"劳动份额","y":"相对对数分量","price":"相对价格","prod":"相对实物劳动生产率","title":"相对人均销售额的分解"}}

def read(path:Path)->pd.DataFrame:
    d=pd.read_csv(path,dtype=str,keep_default_na=False)
    if not set(COLS).issubset(d): raise ValueError("Missing columns")
    if d[COLS].eq("").any().any(): raise ValueError("Blank value")
    for c in COLS:
        d[c]=pd.to_numeric(d[c],errors="raise")
        if not np.isfinite(d[c]).all(): raise ValueError("Nonfinite value")
    if len(d)<3: raise ValueError("At least three bins")
    d=d.sort_values("bin_low").reset_index(drop=True)
    width=d.bin_high-d.bin_low
    if (width<=0).any() or d.bin_low.min()<0 or d.bin_high.max()>1: raise ValueError("Bins must lie within [0,1]")
    if not np.allclose(width,width.iloc[0],rtol=0,atol=1e-9): raise ValueError("Equal-width bins required")
    if not np.allclose(d.bin_low.iloc[1:].to_numpy(),d.bin_high.iloc[:-1].to_numpy(),rtol=0,atol=1e-9): raise ValueError("Bins must be contiguous")
    if not np.allclose(d.relative_price+d.relative_productivity,d.relative_sales_per_worker,rtol=0,atol=2e-6):
        raise ValueError("Relative sales per worker must equal signed sum")
    p=d.relative_price.to_numpy();q=d.relative_productivity.to_numpy()
    d["mid"]=(d.bin_low+d.bin_high)/2
    d["price_low"]=np.minimum(0,p);d["price_high"]=np.maximum(0,p)
    d["prod_low"]=np.where(q<0,np.minimum(0,p)+q,np.maximum(0,p))
    d["prod_high"]=np.where(q<0,np.minimum(0,p),np.maximum(0,p)+q)
    return d

def draw(d:pd.DataFrame,output:Path,lang:str,title:bool):
    if lang=="zh":
        fonts=[f.name for f in font_manager.fontManager.ttflist]
        for name in ("Microsoft YaHei","Noto Sans CJK SC","SimHei"):
            if name in fonts: plt.rcParams["font.family"]=name;break
    plt.rcParams["axes.unicode_minus"]=False
    fig,ax=plt.subplots(figsize=(10.5,5.5),layout="constrained")
    width=float(d.bin_high.iloc[0]-d.bin_low.iloc[0])
    ax.bar(d.mid,d.price_high-d.price_low,bottom=d.price_low,width=width*.96,color="#73777b",edgecolor="white",linewidth=.5,label=TEXT[lang]["price"])
    ax.bar(d.mid,d.prod_high-d.prod_low,bottom=d.prod_low,width=width*.96,color="#c6c9cb",edgecolor="white",linewidth=.5,label=TEXT[lang]["prod"])
    ax.axhline(0,color="#3e4346",lw=.8)
    ax.set(xlim=(max(0,float(d.bin_low.min())-.01),min(1,float(d.bin_high.max())+.01)),xlabel=TEXT[lang]["x"],ylabel=TEXT[lang]["y"])
    ax.legend(frameon=False,ncol=2,loc="upper right")
    ax.spines[["top","right"]].set_visible(False)
    if title: fig.suptitle(TEXT[lang]["title"],fontsize=13)
    output.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(output,dpi=220)
    fig.savefig(output.with_suffix(".pdf"))
    plt.close(fig)

def main():
    p=argparse.ArgumentParser();p.add_argument("--input",type=Path,required=True);p.add_argument("--output",type=Path,required=True)
    p.add_argument("--lang",choices=["en","zh"],default="en");p.add_argument("--title",action="store_true");a=p.parse_args()
    d=read(a.input);a.output.parent.mkdir(parents=True,exist_ok=True)
    d.to_csv(a.output.with_name(a.output.stem+"_checked.csv"),index=False)
    draw(d,a.output,a.lang,a.title)
    print(f"SIGNED_DECOMP_COMPLETE bins={len(d)} output={a.output}")
if __name__=="__main__":main()
