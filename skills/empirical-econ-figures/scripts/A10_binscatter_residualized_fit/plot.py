"""Binned residual scatter with OLS fitted to observations, not bin means."""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont
import numpy as np
import pandas as pd

# Edit labels for another pair of already-residualized variables.
TEXT = {
    "en": {"x": "Residualized distance × rainfall, 1994",
           "y": "Residualized log militia activity",
           "title": "Binned first-stage relationship"},
    "zh": {"x": "距离×1994年缓冲带降雨量的残差",
           "y": "民兵活动对数的残差",
           "title": "分箱后的第一阶段关系"},
}

def setup_font(lang: str) -> None:
    if lang == "zh":
        for family in ("Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "Source Han Sans SC"):
            try:
                findfont(FontProperties(family=family), fallback_to_default=False)
                plt.rcParams["font.family"] = family
                break
            except ValueError:
                continue
        else:
            raise RuntimeError("A CJK font is required for Chinese labels")
    else:
        plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False

def calculate(path: Path, bins: int) -> tuple[pd.DataFrame, dict]:
    df = pd.read_csv(path, dtype=str, encoding="utf-8-sig", keep_default_na=False)
    if not {"id", "rx", "ry"}.issubset(df):
        raise ValueError("CSV needs id,rx,ry headers")
    if df.id.eq("").any() or df.id.duplicated().any():
        raise ValueError("id must be nonempty and unique")
    for col in ("rx", "ry"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    if not np.isfinite(df[["rx", "ry"]].to_numpy(float)).all():
        raise ValueError("rx and ry must be finite numeric values")
    n = len(df)
    if bins < 2 or bins > n:
        raise ValueError("bins must be between 2 and the number of complete observations")
    if df.rx.nunique() < 2:
        raise ValueError("rx must vary")
    # The same complete observation sample supplies both the fit and bin means.
    x = df.rx.to_numpy(float); y = df.ry.to_numpy(float)
    slope, intercept = np.polyfit(x, y, 1)
    ordered = df.sort_values(["rx", "id"], kind="mergesort").reset_index(drop=True)
    ordered["bin"] = np.floor(np.arange(n)*bins/n).astype(int)+1
    means = (ordered.groupby("bin", sort=True)
             .agg(x_mean=("rx", "mean"), y_mean=("ry", "mean"), n=("id", "size"))
             .reset_index())
    assert len(means) == bins and means.n.max()-means.n.min() <= 1
    return means, {"n": n, "bins": bins, "intercept": float(intercept),
                   "slope": float(slope), "x_min": float(x.min()), "x_max": float(x.max())}

def draw(means: pd.DataFrame, fit: dict, lang: str, output: Path, title: bool) -> None:
    setup_font(lang)
    labels = TEXT[lang]
    fig, ax = plt.subplots(figsize=(8.2, 4.7))
    line_x = np.linspace(fit["x_min"], fit["x_max"], 150)
    ax.plot(line_x, fit["intercept"]+fit["slope"]*line_x,
            color="#272727", lw=1.6, zorder=1)
    ax.scatter(means.x_mean, means.y_mean, marker="D", s=26,
               color="#666666", edgecolor="#666666", zorder=2)
    ax.axhline(0, color="#c9c9c9", lw=.8, zorder=0)
    ax.set_xlabel(labels["x"], fontsize=10)
    ax.set_ylabel(labels["y"], fontsize=10)
    ax.grid(axis="y", color="#e5e5e5", lw=.6)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(labelsize=9)
    if title:
        ax.set_title(labels["title"], fontsize=12, pad=10)
    fig.subplots_adjust(left=.13, right=.98, top=.91, bottom=.17)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=220, facecolor="white")
    fig.savefig(output.with_suffix(".pdf"), facecolor="white")
    plt.close(fig)

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--bins", type=int, default=50)
    p.add_argument("--lang", choices=TEXT, default="en")
    p.add_argument("--title", action="store_true")
    args = p.parse_args()
    means, fit = calculate(args.input, args.bins)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    means.to_csv(args.output.with_name(f"bin_summary_python_{args.lang}.csv"), index=False, float_format="%.10f")
    draw(means, fit, args.lang, args.output, args.title)
    print(f"PYTHON_COMPLETE lang={args.lang} N={fit['n']} bins={fit['bins']} "
          f"intercept={fit['intercept']:.8f} slope={fit['slope']:.8f} "
          f"min_bin_n={means.n.min()} max_bin_n={means.n.max()} output={args.output.resolve()}")

if __name__ == "__main__":
    main()
