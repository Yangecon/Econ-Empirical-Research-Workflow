"""Six-outcome sensitivity profile from supplied estimates and two 95% CI methods."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

OUTCOMES=[("poverty","Poverty probability","贫困概率","Probability difference","概率差"),
          ("unmet_needs","Unmet basic needs","未满足基本需求","Count difference","数量差"),
          ("housing","Housing dimension","住房维度","Probability difference","概率差"),
          ("health","Health dimension","健康维度","Probability difference","概率差"),
          ("education","Education dimension","教育维度","Probability difference","概率差"),
          ("consumption","Consumption dimension","消费维度","Probability difference","概率差")]
TEXT={"en":{"x":"Maximum allowed distance from border (km)","title":"Sensitivity to border distance","cluster":"Census-block clustered 95% CI","conley":"Conley 95% CI"},
      "zh":{"x":"回归允许的距边界最大距离（公里）","title":"边界距离敏感性","cluster":"人口普查区块聚类 95% 区间","conley":"Conley 95% 区间"}}
NUM=["bandwidth_km","estimate","cluster_low","cluster_high","conley_low","conley_high"]

def read(path:Path)->pd.DataFrame:
    d=pd.read_csv(path,dtype=str,keep_default_na=False)
    if not {"outcome",*NUM}.issubset(d): raise ValueError("Missing required columns")
    if d[["outcome",*NUM]].eq("").any().any(): raise ValueError("Blank values")
    if set(d.outcome)!={o[0] for o in OUTCOMES}: raise ValueError("Unknown/missing outcomes")
    for c in NUM:
        d[c]=pd.to_numeric(d[c],errors="raise")
        if not np.isfinite(d[c]).all(): raise ValueError("Nonfinite values")
    if (d.bandwidth_km<=0).any() or d.duplicated(["outcome","bandwidth_km"]).any(): raise ValueError("Invalid bandwidth key")
    d=d.sort_values(["outcome","bandwidth_km"]).reset_index(drop=True)
    grid=None
    for outcome,*_ in OUTCOMES:
        sub=d[d.outcome==outcome]
        if len(sub)<3: raise ValueError("At least three distances per outcome")
        x=sub.bandwidth_km.to_numpy()
        if grid is None: grid=x
        elif not np.array_equal(x,grid): raise ValueError("Common bandwidth grid required")
    for lo,hi in (("cluster_low","cluster_high"),("conley_low","conley_high")):
        if ((d[lo]>d.estimate)|(d.estimate>d[hi])).any(): raise ValueError("CI must contain estimate")
    return d

def draw(d:pd.DataFrame,output:Path,lang:str,title:bool):
    if lang=="zh":
        fonts=[f.name for f in font_manager.fontManager.ttflist]
        for name in ("Microsoft YaHei","Noto Sans CJK SC","SimHei"):
            if name in fonts: plt.rcParams["font.family"]=name;break
    plt.rcParams["axes.unicode_minus"]=False
    fig,axes=plt.subplots(3,2,figsize=(11.5,10.6))
    fig.subplots_adjust(left=.09,right=.97,top=.94,bottom=.11,hspace=.63,wspace=.28)
    for ax,(outcome,en,zh,unit_en,unit_zh) in zip(axes.flat,OUTCOMES):
        s=d[d.outcome==outcome];x=s.bandwidth_km.to_numpy();y=s.estimate.to_numpy()
        ax.fill_between(x,s.cluster_low.to_numpy(),s.cluster_high.to_numpy(),color="#bcbfc2",alpha=.85,label=TEXT[lang]["cluster"])
        ax.plot(x,s.conley_low.to_numpy(),color="#62676a",lw=1,ls=":",label=TEXT[lang]["conley"])
        ax.plot(x,s.conley_high.to_numpy(),color="#62676a",lw=1,ls=":")
        ax.plot(x,y,color="#1e2529",lw=1.8)
        ax.set_title(en if lang=="en" else zh,loc="left",fontsize=10)
        ax.set_xlabel(TEXT[lang]["x"],fontsize=8)
        ax.set_ylabel(unit_en if lang=="en" else unit_zh,fontsize=8)
        ax.set_xlim(float(x.min()),float(x.max()))
        ax.spines[["top","right"]].set_visible(False)
        ax.tick_params(labelsize=8)
    handles,labels=axes.flat[0].get_legend_handles_labels()
    fig.legend(handles,labels,loc="lower center",bbox_to_anchor=(.5,.025),ncol=2,frameon=False,fontsize=9)
    if title: fig.suptitle(TEXT[lang]["title"],y=.985,fontsize=13)
    output.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(output,dpi=220,bbox_inches="tight",pad_inches=.08)
    fig.savefig(output.with_suffix(".pdf"),bbox_inches="tight",pad_inches=.08)
    plt.close(fig)

def main():
    p=argparse.ArgumentParser();p.add_argument("--input",type=Path,required=True);p.add_argument("--output",type=Path,required=True)
    p.add_argument("--lang",choices=["en","zh"],default="en");p.add_argument("--title",action="store_true");a=p.parse_args()
    d=read(a.input);a.output.parent.mkdir(parents=True,exist_ok=True)
    d.to_csv(a.output.with_name(a.output.stem+"_checked.csv"),index=False)
    draw(d,a.output,a.lang,a.title)
    print(f"BANDWIDTH_COMPLETE rows={len(d)} distances={d.bandwidth_km.nunique()} output={a.output}")
if __name__=="__main__":main()
