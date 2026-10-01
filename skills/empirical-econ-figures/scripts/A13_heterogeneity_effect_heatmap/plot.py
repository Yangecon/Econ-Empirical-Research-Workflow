"""Two separate-unit bivariate effect heatmaps from supplied estimates."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch

COLORS=["#ffffcc","#ffeda0","#fed976","#feb24c","#fd8d3c",
        "#fc4e2a","#e31a1c","#bd0026","#990026","#800026"]

PANELS={"te":{"en":"Firm employment growth effect","zh":"企业就业增长处理效应","unit_en":"Log-change in firm employment","unit_zh":"企业就业对数变化","limits":(.05,.20)},
        "jobs":{"en":"Cost effectiveness","zh":"每 €100,000 补贴新增岗位","unit_en":"New jobs per €100,000 subsidy","unit_zh":"每 €100,000 补贴新增岗位数","limits":(0,1.25)}}
TEXT={"en":{"x":"Objective rules quintile (SR)","y":"Political discretion quintile (SD)","title":"Effects by rules and discretion"},
      "zh":{"x":"客观规则五分位（SR）","y":"政治裁量五分位（SD）","title":"规则与裁量分组效应"}}

def read(path:Path)->pd.DataFrame:
    d=pd.read_csv(path,dtype=str,keep_default_na=False)
    if not {"panel","sr","sd","value"}.issubset(d): raise ValueError("Missing required columns")
    if len(d)==0 or set(d.panel)!=set(PANELS): raise ValueError("Both configured panels required")
    if d[["panel","sr","sd"]].eq("").any().any(): raise ValueError("Blank key")
    for c in ("sr","sd"):
        d[c]=pd.to_numeric(d[c],errors="raise")
        if not d[c].isin(range(1,6)).all(): raise ValueError("SR/SD must be quintile IDs 1..5")
        d[c]=d[c].astype(int)
    if d.duplicated(["panel","sr","sd"]).any(): raise ValueError("Duplicate cell")
    if not (d.groupby("panel").size()==25).all(): raise ValueError("Supply all 25 coordinates per panel; blank value means missing")
    d["missing_value"]=d.value.eq("")
    d["value"]=pd.to_numeric(d.value.replace("",np.nan),errors="raise")
    for panel,cfg in PANELS.items():
        v=d.loc[d.panel==panel,"value"].dropna()
        if v.empty: raise ValueError("Panel has no observed estimates")
        if not np.isfinite(v).all() or (v<cfg["limits"][0]).any() or (v>cfg["limits"][1]).any():
            raise ValueError("Value outside configured panel scale")
        edges=np.round(np.linspace(*cfg["limits"],11),12)
        mask=d.panel==panel
        d.loc[mask,"shade"]=np.where(d.loc[mask,"missing_value"],np.nan,
            1+np.searchsorted(edges[1:-1],d.loc[mask,"value"].to_numpy(),side="right"))
    return d.sort_values(["panel","sd","sr"]).reset_index(drop=True)

def draw(d:pd.DataFrame,output:Path,lang:str,title:bool):
    if lang=="zh":
        fonts=[f.name for f in font_manager.fontManager.ttflist]
        for name in ("Microsoft YaHei","Noto Sans CJK SC","SimHei"):
            if name in fonts: plt.rcParams["font.family"]=name;break
    plt.rcParams["axes.unicode_minus"]=False
    fig,axes=plt.subplots(1,2,figsize=(11.4,5.3),layout="constrained")
    cmap=ListedColormap(COLORS);cmap.set_bad("#e5e5e5")
    for ax,(panel,cfg) in zip(axes,PANELS.items()):
        arr=np.full((5,5),np.nan)
        for r in d[d.panel==panel].itertuples(): arr[r.sd-1,r.sr-1]=r.value
        edges=np.round(np.linspace(*cfg["limits"],11),12)
        norm=BoundaryNorm(edges,len(COLORS),clip=True)
        actual=norm(arr[np.isfinite(arr)])+1
        exported=d.loc[(d.panel==panel)&d.value.notna(),"shade"].to_numpy(dtype=int)
        assert np.array_equal(actual,exported),"Rendered and exported shades differ"
        im=ax.imshow(arr,origin="lower",cmap=cmap,norm=norm,extent=(.5,5.5,.5,5.5),interpolation="none",aspect="equal")
        ax.set(xticks=range(1,6),yticks=range(1,6),xlabel=TEXT[lang]["x"],ylabel=TEXT[lang]["y"])
        ax.set_title(cfg[lang],loc="left",fontsize=11)
        cb=fig.colorbar(im,ax=ax,shrink=.77,pad=.03,boundaries=edges,ticks=edges[::2],spacing="uniform")
        cb.set_label(cfg["unit_en" if lang=="en" else "unit_zh"],fontsize=9)
        if np.isnan(arr).any():
            ax.legend(handles=[Patch(facecolor="#e5e5e5",edgecolor="#999999",label="No estimate" if lang=="en" else "无估计")],
                      loc="upper left",bbox_to_anchor=(1.01,.09),fontsize=8,frameon=False)
        ax.set_xticks(np.arange(.5,5.6,1),minor=True);ax.set_yticks(np.arange(.5,5.6,1),minor=True)
        ax.grid(which="minor",color="white",linewidth=.6);ax.tick_params(which="minor",bottom=False,left=False)
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
    print(f"HEATMAP_COMPLETE rows={len(d)} observed={d.value.notna().sum()} output={a.output}")
if __name__=="__main__":main()
