"""Supplied policy paths in policy-parameter order, with supplied y confidence bands."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont

# Change algorithm IDs/labels/colors and axis units together for another application.
ALGORITHMS = (
    ("credit_prediction", "Credit prediction", "抵免额预测", "#8177aa"),
    ("credit_oracle", "Credit oracle", "抵免额实际值", "#438b9e"),
    ("total_prediction", "Total prediction", "总额预测", "#695b9b"),
    ("total_oracle", "Total oracle", "总额实际值", "#176177"),
)
TEXT = {
    "en": {"x": "Detected underreporting (synthetic units)",
           "y": "Disparity (percentage points)", "status": "Status quo",
           "op": "Operating rate", "title": "Efficiency and disparity paths"},
    "zh": {"x": "查获少报金额（合成单位）", "y": "差距（百分点）",
           "status": "现状", "op": "执行比例", "title": "效率与差距路径"},
}

def set_font(lang: str) -> None:
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

def read(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    cols = ["algorithm", "policy_rate", "efficiency", "disparity", "ci_low", "ci_high", "operating"]
    if not set(cols).issubset(df):
        raise ValueError(f"required columns: {cols}")
    if df[["algorithm", "policy_rate", "efficiency", "disparity", "operating"]].eq("").any().any():
        raise ValueError("blank required field")
    expected = {a[0] for a in ALGORITHMS} | {"status_quo"}
    if set(df.algorithm) != expected:
        raise ValueError("algorithm IDs must match configuration plus status_quo")
    for c in cols[1:]:
        df[c] = pd.to_numeric(df[c].replace("", np.nan), errors="raise")
    if not np.isfinite(df[["policy_rate", "efficiency", "disparity", "operating"]]).all().all():
        raise ValueError("nonfinite required numeric field")
    if (df.policy_rate < 0).any() or (df.efficiency < 0).any() or not df.operating.isin([0, 1]).all():
        raise ValueError("invalid rate, efficiency or operating flag")
    baseline = df[df.algorithm == "status_quo"]
    if len(baseline) != 1 or baseline.operating.iloc[0] != 0:
        raise ValueError("exactly one non-operating status_quo row required")
    if baseline[["ci_low", "ci_high"]].notna().any().any():
        raise ValueError("status_quo CI fields must be blank")
    for aid, *_ in ALGORITHMS:
        part = df[df.algorithm == aid].sort_values("policy_rate")
        if len(part) < 2 or part.policy_rate.duplicated().any():
            raise ValueError(f"{aid}: >=2 distinct policy rates required")
        if not np.all(np.diff(part.efficiency) > 0):
            raise ValueError(f"{aid}: efficiency must increase with policy rate")
        if not np.isfinite(part[["ci_low", "ci_high"]]).all().all():
            raise ValueError(f"{aid}: complete finite CI bounds required")
        if not ((part.ci_low <= part.disparity)&(part.disparity <= part.ci_high)).all():
            raise ValueError(f"{aid}: CI must contain estimate")
        if part.operating.sum() != 1:
            raise ValueError(f"{aid}: exactly one operating point required")
    return df

def draw(df: pd.DataFrame, lang: str, output: Path, title: bool) -> None:
    set_font(lang)
    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=160)
    ax.axhline(0, color="#858585", lw=.8, zorder=0)
    baseline = df[df.algorithm == "status_quo"].iloc[0]
    ax.axvline(baseline.efficiency, color="#bd6666", lw=1, ls=":", zorder=0)
    ax.axhline(baseline.disparity, color="#bd6666", lw=1, ls=":", zorder=0)
    for aid, en, zh, color in ALGORITHMS:
        part = df[df.algorithm == aid].sort_values("policy_rate")
        x = part.efficiency.to_numpy(); y = part.disparity.to_numpy()
        ax.fill_between(x, part.ci_low.to_numpy(), part.ci_high.to_numpy(),
                        color=color, alpha=.16, linewidth=0, zorder=1)
        ax.plot(x, y, color=color, lw=2.0, label=en if lang == "en" else zh, zorder=2)
        op = part[part.operating == 1].iloc[0]
        ax.scatter([op.efficiency], [op.disparity], color="black", s=31, zorder=4)
    ax.scatter([], [], color="black", s=31, label=TEXT[lang]["op"])
    ax.scatter([baseline.efficiency], [baseline.disparity], marker="x", s=72,
               color="#aa4949", lw=2, label=TEXT[lang]["status"], zorder=5)
    ax.set_xlabel(TEXT[lang]["x"]); ax.set_ylabel(TEXT[lang]["y"])
    if title:
        ax.set_title(TEXT[lang]["title"])
    ax.grid(color="#e9e9e9", lw=.55)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, loc="upper left", ncol=2, fontsize=9)
    fig.tight_layout()
    fig.savefig(output, dpi=240); fig.savefig(output.with_suffix(".pdf")); plt.close(fig)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--lang", choices=TEXT, default="en")
    p.add_argument("--title", action="store_true")
    a = p.parse_args()
    df = read(a.input)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    draw(df, a.lang, a.output, a.title)
    print(f"PYTHON_COMPLETE rows={len(df)} curves={len(ALGORITHMS)} output={a.output}")

if __name__ == "__main__":
    main()
