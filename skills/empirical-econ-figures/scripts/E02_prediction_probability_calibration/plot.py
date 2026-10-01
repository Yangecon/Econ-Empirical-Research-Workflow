"""Raw-observation calibration plot: decile means, conditional IQR, and OLS line."""
import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

TEXT={"en":{"x":"True placement probability","y":"Predicted placement probability",
            "mean":"Bin mean","fit":"Linear fit","line":"45°","iqr":"Conditional IQR",
            "title":"Predicted versus true placement probabilities"},
      "zh":{"x":"真实录取概率","y":"预测录取概率","mean":"分箱均值",
            "fit":"线性拟合","line":"45度线","iqr":"条件四分位距",
            "title":"预测概率与真实概率的校准"}}


def load(path):
    fields=("id","true_prob","predicted_prob")
    with path.open(encoding="utf-8-sig",newline="") as f:
        rd=csv.DictReader(f)
        if not set(fields).issubset(rd.fieldnames or []):
            raise ValueError(f"Required columns: {fields}")
        rows=list(rd)
    if len(set(r["id"] for r in rows))!=len(rows) or any(not r["id"] for r in rows):
        raise ValueError("Nonempty unique IDs required")
    for r in rows:
        try:
            x,y=float(r["true_prob"]),float(r["predicted_prob"])
        except (TypeError,ValueError):
            raise ValueError("Probabilities must be numeric") from None
        if not np.isfinite([x,y]).all() or not (0<=x<=1 and 0<=y<=1):
            raise ValueError("Probabilities must be finite and in [0,1]")
    regular=[r for r in rows if float(r["true_prob"])<=.99]
    tail=[r for r in rows if float(r["true_prob"])>.99]
    if len(regular)<40 or len(tail)<4:
        raise ValueError("Need at least 40 regular and four >.99-tail observations")
    regular.sort(key=lambda r:(float(r["true_prob"]),r["id"]))
    for i,r in enumerate(regular):
        r["bin"]=1+(10*i//len(regular))
    for r in tail:
        r["bin"]=11
    return rows


def summarize(rows):
    out=[]
    for b in range(1,12):
        group=[r for r in rows if r["bin"]==b]
        x=np.array([float(r["true_prob"]) for r in group])
        y=np.array([float(r["predicted_prob"]) for r in group])
        # NumPy linear quantiles use position 1+(n-1)p, shared with plot.do.
        out.append({"bin":b,"n":len(group),"mean_true":float(x.mean()),
                    "mean_predicted":float(y.mean()),"q25":float(np.quantile(y,.25,method="linear")),
                    "q75":float(np.quantile(y,.75,method="linear"))})
    x=np.array([float(r["true_prob"]) for r in rows])
    y=np.array([float(r["predicted_prob"]) for r in rows])
    slope,intercept=np.polyfit(x,y,1)
    return out,intercept,slope


def draw(rows,output,lang,title):
    output.parent.mkdir(parents=True,exist_ok=True)
    summaries,intercept,slope=summarize(rows)
    plt.rcParams.update({"font.family":"Microsoft YaHei" if lang=="zh" else "DejaVu Sans",
                         "axes.unicode_minus":False,"pdf.fonttype":42})
    t=TEXT[lang]
    x=np.array([r["mean_true"] for r in summaries])
    mean=np.array([r["mean_predicted"] for r in summaries])
    low=np.array([r["q25"] for r in summaries])
    high=np.array([r["q75"] for r in summaries])
    fig,ax=plt.subplots(figsize=(7.7,5.5))
    ax.fill_between(x,low,high,color="#dbeaf4",alpha=.8,label=t["iqr"])
    ax.plot([0,1],[0,1],color="#242424",ls=":",lw=1.5,label=t["line"])
    ax.plot([0,1],[intercept,intercept+slope],color="#2879b9",ls=(0,(9,5)),lw=1.4,label=t["fit"])
    ax.scatter(x,mean,s=70,facecolors="white",edgecolors="#2879b9",lw=1.2,zorder=4,label=t["mean"])
    ax.set(xlim=(-.02,1.02),ylim=(-.02,1.02),xlabel=t["x"],ylabel=t["y"])
    ax.set_xticks(np.arange(0,1.01,.2))
    ax.set_yticks(np.arange(0,1.01,.2))
    if title:
        ax.set_title(t["title"],pad=10)
    ax.grid(axis="y",color="#e6e6e6",lw=.7)
    ax.spines[["top","right"]].set_visible(False)
    ax.legend(loc="lower right",frameon=True,fontsize=8.5)
    fig.tight_layout()
    fig.savefig(output,dpi=220)
    fig.savefig(output.with_suffix(".pdf"))
    plt.close(fig)
    with output.with_name(output.stem+"_bins.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=("bin","n","mean_true","mean_predicted","q25","q75"))
        w.writeheader();w.writerows(summaries)
    with output.with_name(output.stem+"_fit.csv").open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f);w.writerow(("intercept","slope"));w.writerow((intercept,slope))


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",required=True,type=Path)
    ap.add_argument("--output",required=True,type=Path)
    ap.add_argument("--lang",required=True,choices=("en","zh"))
    ap.add_argument("--title",action="store_true")
    a=ap.parse_args();draw(load(a.input),a.output,a.lang,a.title)
