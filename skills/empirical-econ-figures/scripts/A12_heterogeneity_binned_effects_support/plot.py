"""Independent Python effect-with-CI and aligned support-histogram panels."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont

# Edit IDs, panel units/ranges and bilingual labels together for another study.
CONFIG = [
    ("destination_share", (0, 1), (0, .08), "Destination support share", "目的地共同支持比例", "Migration rate", "迁移率"),
    ("destination_degree", (.5, 20.5), (-1, 2), "Destination network size", "目的地网络规模", "Estimated effect", "估计效应"),
    ("home_share", (0, 1), (0, .08), "Home support share", "原居地共同支持比例", "Migration rate", "迁移率"),
    ("home_degree", (.5, 20.5), (-1, 2), "Home network size", "原居地网络规模", "Estimated effect", "估计效应"),
]
TEXT = {"en": {"count": "Count", "title": "Effects and support"},
        "zh": {"count": "样本数", "title": "效应与样本分布"}}

def font(lang: str) -> None:
    if lang == "zh":
        for family in ("Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "Source Han Sans SC"):
            try:
                findfont(FontProperties(family=family), fallback_to_default=False)
                plt.rcParams["font.family"] = family
                break
            except ValueError:
                continue
        else:
            raise RuntimeError("A CJK font is required")
    else:
        plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False

def read(effect_path: Path, support_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    eff = pd.read_csv(effect_path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    sup = pd.read_csv(support_path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    if not {"panel", "panel_order", "x", "estimate", "ci_low", "ci_high"}.issubset(eff):
        raise ValueError("effect CSV missing columns")
    if not {"panel", "panel_order", "x_left", "x_right", "count"}.issubset(sup):
        raise ValueError("support CSV missing columns")
    for df in (eff, sup):
        if df.eq("").any().any():
            raise ValueError("blank input field")
        df["panel_order"] = pd.to_numeric(df.panel_order, errors="raise")
    for col in ("x", "estimate", "ci_low", "ci_high"):
        eff[col] = pd.to_numeric(eff[col], errors="raise")
    for col in ("x_left", "x_right", "count"):
        sup[col] = pd.to_numeric(sup[col], errors="raise")
    if not np.isfinite(eff[["panel_order", "x", "estimate", "ci_low", "ci_high"]]).all().all():
        raise ValueError("nonfinite effect value")
    if not np.isfinite(sup[["panel_order", "x_left", "x_right", "count"]]).all().all():
        raise ValueError("nonfinite support value")
    wanted = {(pid, i) for i, (pid, *_rest) in enumerate(CONFIG, 1)}
    for df in (eff, sup):
        if set(zip(df.panel, df.panel_order)) != wanted:
            raise ValueError("panel IDs/orders must match CONFIG")
    if eff.duplicated(["panel", "x"]).any() or not ((eff.ci_low <= eff.estimate) & (eff.estimate <= eff.ci_high)).all():
        raise ValueError("duplicate effect x or invalid CI")
    if not ((sup.x_left < sup.x_right) & (sup["count"] >= 0) & (sup["count"] % 1 == 0)).all():
        raise ValueError("invalid support bin or count")
    for i, (pid, xr, yr, *_rest) in enumerate(CONFIG, 1):
        e = eff[eff.panel == pid].sort_values("x")
        s = sup[sup.panel == pid].sort_values("x_left")
        if (e.x.min() < xr[0] or e.x.max() > xr[1] or e.ci_low.min() < yr[0] or e.ci_high.max() > yr[1]
                or s.x_left.min() < xr[0] or s.x_right.max() > xr[1]):
            raise ValueError(f"{pid}: config bounds exclude data")
        if (s.x_left.to_numpy()[1:] < s.x_right.to_numpy()[:-1]-1e-10).any():
            raise ValueError(f"{pid}: overlapping support bins")
        widths = (s.x_right-s.x_left).to_numpy()
        if not np.allclose(widths, widths[0], rtol=0, atol=1e-10):
            raise ValueError(f"{pid}: support bins must have common width for Stata parity")
    return eff, sup

def draw(eff: pd.DataFrame, sup: pd.DataFrame, lang: str, output: Path, title: bool) -> None:
    font(lang)
    n = len(CONFIG)
    ncol = 2 if n > 1 else 1
    nrow = int(np.ceil(n/ncol))
    fig = plt.figure(figsize=(5.2*ncol, 4.5*nrow), dpi=160)
    outer = fig.add_gridspec(nrow, ncol, hspace=.34, wspace=.30)
    for idx, (pid, xr, yr, x_en, x_zh, y_en, y_zh) in enumerate(CONFIG):
        inner = outer[idx//ncol, idx%ncol].subgridspec(2, 1, height_ratios=(3, 1), hspace=.04)
        top = fig.add_subplot(inner[0])
        bottom = fig.add_subplot(inner[1], sharex=top)
        e = eff[eff.panel == pid].sort_values("x")
        s = sup[sup.panel == pid].sort_values("x_left")
        top.errorbar(e.x, e.estimate, yerr=[e.estimate-e.ci_low, e.ci_high-e.estimate],
                     fmt="o", color="#252525", ecolor="#333333", markersize=3.2,
                     elinewidth=1.0, capsize=2.0, zorder=3)
        if yr[0] < 0 < yr[1]:
            top.axhline(0, color="#999999", linewidth=.8, linestyle="--", zorder=1)
        widths = s.x_right-s.x_left
        bottom.bar(s.x_left, s["count"], width=widths, align="edge", color="#969696",
                   edgecolor="#6c6c6c", linewidth=.35)
        top.set_xlim(*xr); top.set_ylim(*yr)
        bottom.set_ylim(bottom=0)
        top.set_ylabel(y_en if lang == "en" else y_zh, fontsize=9)
        bottom.set_ylabel(TEXT[lang]["count"], fontsize=9)
        bottom.set_xlabel(x_en if lang == "en" else x_zh, fontsize=9)
        if n > 1:
            top.set_title(f"({chr(97+idx)}) {x_en if lang == 'en' else x_zh}", fontsize=10, loc="left")
        top.tick_params(labelbottom=False)
        for ax in (top, bottom):
            ax.grid(axis="y", color="#e7e7e7", linewidth=.6)
            ax.spines[["top", "right"]].set_visible(False)
            ax.tick_params(labelsize=8)
    if title:
        fig.suptitle(TEXT[lang]["title"], fontsize=12)
    fig.savefig(output, dpi=240, bbox_inches="tight")
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--effect", type=Path, default=Path(__file__).with_name("effect_demo.csv"))
    p.add_argument("--support", type=Path, default=Path(__file__).with_name("support_demo.csv"))
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--lang", choices=TEXT, default="en")
    p.add_argument("--title", action="store_true")
    a = p.parse_args()
    eff, sup = read(a.effect, a.support)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    draw(eff, sup, a.lang, a.output, a.title)
    print(f"PYTHON_COMPLETE panels={len(CONFIG)} effects={len(eff)} support_bins={len(sup)} output={a.output}")

if __name__ == "__main__":
    main()
