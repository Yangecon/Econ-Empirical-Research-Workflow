"""Mixed-unit binned outcomes with a continuous piecewise-linear kink fit."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont

# Edit IDs, window, labels, units, limits, and bin counts together in both scripts.
THRESHOLD = 850.0
XMIN, XMAX = 500.0, 1200.0
PANELS = (
    {"id":"replacement", "en":"(A) Replacement rate", "zh":"（A）替代率", "yen":"Daily benefits / daily wage", "yzh":"日津贴／日工资", "ymin":.55, "ymax":.82, "bins":12},
    {"id":"takeup", "en":"(B) Coverage take-up", "zh":"（B）保险购买比例", "yen":"Coverage purchase probability", "yzh":"保险购买概率", "ymin":.75, "ymax":.94, "bins":12},
    {"id":"risk_basic", "en":"(C) Risk under basic coverage", "zh":"（C）基本保险风险", "yen":"Predicted unemployment days", "yzh":"预测失业天数", "ymin":1.2, "ymax":4.1, "bins":12},
    {"id":"risk_comprehensive", "en":"(D) Risk under comprehensive coverage", "zh":"（D）综合保险风险", "yen":"Predicted unemployment days", "yzh":"预测失业天数", "ymin":7.7, "ymax":10.7, "bins":12},
)
TEXT={"en":{"x":"Running variable (illustrative units)","title":"Outcomes around a policy kink"},
      "zh":{"x":"运行变量（示例单位）","title":"政策折点两侧的结果"}}

def bin_index(x:np.ndarray,low:float,high:float,nb:int)->np.ndarray:
    """Equal-width bins with inclusive final endpoint and rightward internal ties."""
    return np.minimum(np.floor((x-low)/((high-low)/nb)).astype(int),nb-1)+1

def font(lang:str)->None:
    if lang=="zh":
        for family in ("Microsoft YaHei","SimHei","Noto Sans CJK SC","Source Han Sans SC"):
            try:
                findfont(FontProperties(family=family),fallback_to_default=False)
                plt.rcParams["font.family"]=family; break
            except ValueError: continue
        else: raise RuntimeError("Chinese font required")
    else: plt.rcParams["font.family"]="DejaVu Sans"
    plt.rcParams["axes.unicode_minus"]=False

def calculate(source:Path|pd.DataFrame)->tuple[pd.DataFrame,pd.DataFrame,pd.DataFrame]:
    df=source.copy() if isinstance(source,pd.DataFrame) else pd.read_csv(source,dtype={"panel":str,"id":str},encoding="utf-8-sig")
    need=["panel","id","running","outcome"]
    if not set(need).issubset(df) or df[need].isna().any().any() or df.panel.eq("").any() or df.id.eq("").any():
        raise ValueError("panel,id,running,outcome must be present and nonblank")
    if set(df.panel)!={p["id"] for p in PANELS} or df.duplicated(["panel","id"]).any():
        raise ValueError("configured panels and unique within-panel IDs required")
    for col in ("running","outcome"):
        df[col]=pd.to_numeric(df[col],errors="raise")
        if not np.isfinite(df[col]).all(): raise ValueError(f"{col} must be finite")
    if not XMIN<THRESHOLD<XMAX: raise ValueError("threshold must be inside x window")
    bins, fits, counts=[],[],[]
    for cfg in PANELS:
        original=df[df.panel==cfg["id"]]
        part=original[original.running.between(XMIN,XMAX)].copy()
        if len(part)<3*2*cfg["bins"]: raise ValueError("insufficient in-window rows")
        z=part.running.to_numpy()-THRESHOLD
        design=np.column_stack([np.ones(len(part)),z,np.maximum(z,0)])
        if np.linalg.matrix_rank(design)<3: raise ValueError("both sides need varying running values")
        b0,bl,delta=np.linalg.lstsq(design,part.outcome.to_numpy(),rcond=None)[0]
        endpoints=np.array([XMIN,THRESHOLD,XMAX])
        predicted=b0+bl*(endpoints-THRESHOLD)+delta*np.maximum(endpoints-THRESHOLD,0)
        fits.append({"panel":cfg["id"],"n":len(part),"level_at_threshold":b0,
                     "slope_left":bl,"slope_change":delta,"slope_right":bl+delta})
        counts.append({"panel":cfg["id"],"total_input_n":len(original),"window_n":len(part),
                       "excluded_outside_window_n":len(original)-len(part),
                       "exact_threshold_n":int((part.running==THRESHOLD).sum())})
        if (predicted<cfg["ymin"]).any() or (predicted>cfg["ymax"]).any():
            raise ValueError(f"{cfg['id']}: fit exceeds configured display range")
        part["side"]=np.where(part.running<THRESHOLD,"left","right")
        for side,low,high in (("left",XMIN,THRESHOLD),("right",THRESHOLD,XMAX)):
            sidepart=part[part.side==side].copy()
            nb=cfg["bins"]
            sidepart["bin"]=bin_index(sidepart.running.to_numpy(),low,high,nb)
            summary=sidepart.groupby("bin",sort=True).agg(x_mean=("running","mean"),y_mean=("outcome","mean"),n=("outcome","size")).reset_index()
            if len(summary)!=nb or (summary.n<2).any(): raise ValueError(f"{cfg['id']}/{side}: every bin needs >=2 rows")
            if not summary.y_mean.between(cfg["ymin"],cfg["ymax"]).all():
                raise ValueError(f"{cfg['id']}/{side}: bin mean exceeds display range")
            summary.insert(0,"side",side); summary.insert(0,"panel",cfg["id"])
            bins.append(summary)
    return pd.concat(bins,ignore_index=True),pd.DataFrame(fits),pd.DataFrame(counts)

def draw(bins:pd.DataFrame,fits:pd.DataFrame,output:Path,lang:str,title:bool)->None:
    font(lang)
    fig,axes=plt.subplots(2,2,figsize=(12.4,8.2),dpi=160)
    for ax,cfg in zip(axes.flat,PANELS):
        b=bins[bins.panel==cfg["id"]]
        f=fits[fits.panel==cfg["id"]].iloc[0]
        ax.scatter(b.x_mean,b.y_mean,s=17,facecolors="white",edgecolors="#17527d",linewidths=1.1,zorder=3)
        xx=np.array([XMIN,THRESHOLD,XMAX])
        yy=f.level_at_threshold+f.slope_left*(xx-THRESHOLD)+f.slope_change*np.maximum(xx-THRESHOLD,0)
        ax.plot(xx,yy,color="#d52a35",lw=1.6)
        ax.axvline(THRESHOLD,color="#d52a35",lw=1.1)
        ax.set_xlim(XMIN,XMAX);ax.set_ylim(cfg["ymin"],cfg["ymax"])
        ax.set_title(cfg[lang],fontsize=11,loc="left",pad=8)
        ax.set_xlabel(TEXT[lang]["x"],fontsize=9);ax.set_ylabel(cfg["yen" if lang=="en" else "yzh"],fontsize=9)
        ax.grid(axis="y",color="#d5d5d5",lw=.6)
        ax.spines[["top","right"]].set_visible(False)
        ax.tick_params(labelsize=8)
    if title: fig.suptitle(TEXT[lang]["title"],fontsize=13,y=.995)
    fig.tight_layout(rect=(0,0,1,.97 if title else 1),h_pad=1.7,w_pad=1.8)
    output.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(output,dpi=220);fig.savefig(output.with_suffix(".pdf"));plt.close(fig)

def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    ap.add_argument("--lang",choices=TEXT,default="en")
    ap.add_argument("--title",action="store_true")
    args=ap.parse_args()
    bins,fits,counts=calculate(args.input)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    stem=args.output.stem
    for kind,frame in (("bins",bins),("fits",fits),("sample",counts)):
        frame.to_csv(args.output.with_name(f"{stem}_{kind}.csv"),index=False,float_format="%.12g")
    draw(bins,fits,args.output,args.lang,args.title)
    print(f"PYTHON_COMPLETE input_rows={sum(counts.total_input_n)} window_rows={sum(counts.window_n)} bins={len(bins)} fits={len(fits)}")

if __name__=="__main__": main()
