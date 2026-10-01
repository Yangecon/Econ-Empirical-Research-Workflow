"""Ordered specification result curve with a spec-ID-locked binary choice matrix."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties,findfont

# Edit IDs, row order, bilingual labels, and result meaning together in both scripts.
OPTIONS=(
 ("baseline","Baseline","基准设定"),
 ("regional","Regional policies included","纳入区域政策"),
 ("first_round","First round only","仅首轮试点"),
 ("exclude_municipalities","Municipalities excluded","排除直辖市"),
 ("pool_one_site","One-site policies pooled","合并单点政策"),
 ("logarithm","Logarithm","对数形式"),
 ("gdp","GDP","GDP"),
 ("gdp_per_capita","GDP per capita","人均GDP"),
 ("population","Population","人口"),
 ("fiscal_income","Fiscal income","财政收入"),
 ("fiscal_expenditure","Fiscal expenditure","财政支出"),
)
RESULT_LABEL={"en":"Mean t-statistic across experiments","zh":"各实验t统计量的均值"}
TEXT={"en":{"x":"Specifications sorted by result","title":"Specification curve"},
      "zh":{"x":"按结果排序的模型设定","title":"模型设定曲线"}}
RESULT_MIN,RESULT_MAX=-1.0,6.0

def font(lang:str)->None:
    if lang=="zh":
        for family in ("Microsoft YaHei","SimHei","Noto Sans CJK SC","Source Han Sans SC"):
            try: findfont(FontProperties(family=family),fallback_to_default=False);plt.rcParams["font.family"]=family;break
            except ValueError: continue
        else: raise RuntimeError("Chinese font required")
    else: plt.rcParams["font.family"]="DejaVu Sans"
    plt.rcParams["axes.unicode_minus"]=False

def read(source:Path|pd.DataFrame)->pd.DataFrame:
    df=source.copy() if isinstance(source,pd.DataFrame) else pd.read_csv(source,dtype=str,keep_default_na=False,encoding="utf-8-sig")
    options=["opt_"+o[0] for o in OPTIONS]
    required=["spec_id","result",*options]
    extra_options=[c for c in df.columns if c.startswith("opt_") and c not in options]
    if extra_options:
        raise ValueError(f"unconfigured option columns: {extra_options}")
    if not set(required).issubset(df) or df[required].isna().any().any() or df[required].astype(str).eq("").any().any():
        raise ValueError(f"required nonblank columns: {required}")
    if df.spec_id.duplicated().any() or len(df)<5:
        raise ValueError("at least five unique spec_id values required")
    has_low="ci_low" in df;has_high="ci_high" in df
    if has_low!=has_high: raise ValueError("CI columns must be supplied together")
    if not has_low:
        df["ci_low"]="";df["ci_high"]=""
    for col in options:
        if not df[col].astype(str).isin(["0","1"]).all():
            raise ValueError(f"{col} must contain explicit 0 or 1, never blank")
        df[col]=pd.to_numeric(df[col]).astype(int)
    for col in ("result","ci_low","ci_high"):
        df[col]=pd.to_numeric(df[col].replace("",np.nan),errors="raise")
    if not np.isfinite(df.result).all(): raise ValueError("result must be finite")
    if not df.ci_low.isna().equals(df.ci_high.isna()):
        raise ValueError("CI bounds must both be present or both blank for each spec")
    with_ci=df.ci_low.notna()
    if not ((df.loc[with_ci,"ci_low"]<=df.loc[with_ci,"result"]) &
            (df.loc[with_ci,"result"]<=df.loc[with_ci,"ci_high"])).all():
        raise ValueError("supplied CI must contain result")
    if not np.isfinite(df.loc[with_ci,["ci_low","ci_high"]]).all().all():
        raise ValueError("CI values must be finite")
    values=pd.concat([df.result,df.ci_low.dropna(),df.ci_high.dropna()])
    if not values.between(RESULT_MIN,RESULT_MAX).all():
        raise ValueError("results/CI exceed configured display range; edit limits")
    df=df.sort_values(["result","spec_id"],kind="mergesort").reset_index(drop=True)
    df.insert(0,"rank",np.arange(1,len(df)+1))
    return df

def draw(df:pd.DataFrame,lang:str,output:Path,title:bool)->None:
    font(lang)
    n=len(df)
    fig=plt.figure(figsize=(12.6,7.6),dpi=160)
    gs=fig.add_gridspec(2,1,height_ratios=[2.5,3.4],hspace=.09,left=.25,right=.985,top=.94 if title else .97,bottom=.09)
    top=fig.add_subplot(gs[0]);bottom=fig.add_subplot(gs[1],sharex=top)
    with_ci=df.ci_low.notna()
    if with_ci.any():
        top.vlines(df.loc[with_ci,"rank"],df.loc[with_ci,"ci_low"],df.loc[with_ci,"ci_high"],color="#7d2730",lw=.85,alpha=.8)
    top.scatter(df["rank"],df["result"],s=20,color="#7e171b",zorder=3)
    top.axhline(0,color="#999999",lw=.9,ls=(0,(5,3)))
    top.set_ylim(RESULT_MIN,RESULT_MAX)
    top.set_ylabel(RESULT_LABEL[lang],fontsize=10)
    top.grid(axis="y",color="#e1e1e1",lw=.5)
    top.tick_params(axis="x",labelbottom=False,bottom=False)
    top.spines[["top","right"]].set_visible(False)
    for j,(_,en,zh) in enumerate(OPTIONS):
        row=len(OPTIONS)-j
        col="opt_"+OPTIONS[j][0]
        on=df[col]==1
        bottom.scatter(df.loc[~on,"rank"],np.full((~on).sum(),row),s=16,color="#c2c5c8",linewidths=0)
        bottom.scatter(df.loc[on,"rank"],np.full(on.sum(),row),s=18,color="#252525",linewidths=0)
    bottom.set_yticks(range(1,len(OPTIONS)+1),[o[1] if lang=="en" else o[2] for o in reversed(OPTIONS)],fontsize=9)
    bottom.set_ylim(.4,len(OPTIONS)+.6)
    bottom.set_xlabel(TEXT[lang]["x"],fontsize=10)
    bottom.set_xticks(np.unique(np.r_[1,np.arange(10,n+1,10),n]))
    bottom.set_xlim(.3,n+.7)
    bottom.tick_params(axis="y",length=0)
    bottom.spines[["top","right","left"]].set_visible(False)
    if title: fig.suptitle(TEXT[lang]["title"],fontsize=13,y=.995)
    output.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(output,dpi=220);fig.savefig(output.with_suffix(".pdf"));plt.close(fig)

def main()->None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    ap.add_argument("--lang",choices=TEXT,default="en")
    ap.add_argument("--title",action="store_true")
    args=ap.parse_args()
    df=read(args.input)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(args.output.with_name(args.output.stem+"_ordered.csv"),index=False,float_format="%.12g")
    draw(df,args.lang,args.output,args.title)
    print(f"PYTHON_COMPLETE specs={len(df)} choices={len(OPTIONS)} ci_specs={df.ci_low.notna().sum()} output={args.output}")

if __name__=="__main__":main()
