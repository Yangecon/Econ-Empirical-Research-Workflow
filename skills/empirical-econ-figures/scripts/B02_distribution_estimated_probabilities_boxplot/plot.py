"""Independent Python box summaries and plot from raw observations."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont
from matplotlib.patches import Rectangle

LABELS = {
    "en": {"x": "Acuity decile", "y": "Attention probability", "title": "Probability by acuity decile"},
    "zh": {"x": "敏锐度十分位", "y": "注意概率", "title": "各十分位的注意概率"},
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

def read(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    required = {"id", "group", "group_order", "group_label_en", "group_label_zh", "value"}
    if not required.issubset(df):
        raise ValueError(f"missing columns: {sorted(required-set(df))}")
    if df[list(required)].eq("").any().any() or df.id.duplicated().any():
        raise ValueError("blank required field or duplicate id")
    df["group_order"] = pd.to_numeric(df.group_order, errors="raise")
    df["value"] = pd.to_numeric(df.value, errors="raise")
    if not (np.isfinite(df.value).all() and np.isfinite(df.group_order).all()):
        raise ValueError("nonfinite numeric input")
    if not ((df.group_order % 1 == 0) & (df.group_order >= 1)).all():
        raise ValueError("group_order must be a positive integer")
    meta = df[["group", "group_order", "group_label_en", "group_label_zh"]].drop_duplicates()
    if meta.group.duplicated().any() or meta.group_order.duplicated().any():
        raise ValueError("group metadata inconsistent")
    if sorted(meta.group_order.astype(int)) != list(range(1, len(meta)+1)):
        raise ValueError("group order must be consecutive from 1")
    return df.sort_values(["group_order", "value", "id"])

def summaries(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows, outliers = [], []
    for order, part in df.groupby("group_order", sort=True):
        values = np.sort(part.value.to_numpy(float))
        q1, median, q3 = np.quantile(values, [.25, .5, .75], method="linear")
        lo, hi = q1 - 1.5*(q3-q1), q3 + 1.5*(q3-q1)
        inside = values[(values >= lo) & (values <= hi)]
        if not len(inside):
            raise ValueError("no values within fences")
        flagged = part[(part.value < lo) | (part.value > hi)]
        outliers.extend({"id": r.id, "group_order": int(order), "value": r.value} for r in flagged.itertuples())
        rows.append({"group": part.group.iloc[0], "group_order": int(order), "n": len(values),
                     "q1": q1, "median": median, "q3": q3, "whisker_low": inside.min(),
                     "whisker_high": inside.max(), "outlier_n": len(flagged)})
    return pd.DataFrame(rows), pd.DataFrame(outliers, columns=["id", "group_order", "value"])

def draw(df: pd.DataFrame, summary: pd.DataFrame, outliers: pd.DataFrame, lang: str, output: Path,
         title: bool, ymin: float, ymax: float) -> None:
    setup_font(lang)
    if not ymin < ymax or (df.value.min() < ymin or df.value.max() > ymax):
        raise ValueError("axis range must contain every observation")
    fig, ax = plt.subplots(figsize=(9.2, 5.4), dpi=160)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.grid(axis="y", color="#e4e4e4", linewidth=.65, zorder=0)
    for r in summary.itertuples():
        x = r.group_order
        ax.add_patch(Rectangle((x-.29, r.q1), .58, r.q3-r.q1, facecolor="white",
                               edgecolor="#656565", linewidth=1.2, zorder=3))
        ax.plot([x-.29, x+.29], [r.median, r.median], color="#3b3b3b", linewidth=1.8, zorder=4)
        ax.plot([x, x], [r.whisker_low, r.q1], color="#6b6b6b", linewidth=1.1, zorder=2)
        ax.plot([x, x], [r.q3, r.whisker_high], color="#6b6b6b", linewidth=1.1, zorder=2)
        ax.plot([x-.14, x+.14], [r.whisker_low]*2, color="#6b6b6b", linewidth=1.1, zorder=2)
        ax.plot([x-.14, x+.14], [r.whisker_high]*2, color="#6b6b6b", linewidth=1.1, zorder=2)
    if len(outliers):
        ax.scatter(outliers.group_order, outliers.value, s=9, c="#676767", alpha=.65, zorder=5)
    label_col = f"group_label_{lang}"
    names = df.groupby("group_order", sort=True)[label_col].first().tolist()
    ax.set_xticks(summary.group_order, names)
    ax.set_xlim(.4, len(summary)+.6)
    pad = .018 * (ymax-ymin)
    ax.set_ylim(ymin-pad, ymax+pad)
    ax.set_yticks(np.linspace(ymin, ymax, 6))
    ax.set_xlabel(LABELS[lang]["x"], fontsize=11)
    ax.set_ylabel(LABELS[lang]["y"], fontsize=11)
    if title:
        ax.set_title(LABELS[lang]["title"], fontsize=12)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=240)
    fig.savefig(output.with_suffix(".pdf"))
    plt.close(fig)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, default=Path(__file__).with_name("demo.csv"))
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--lang", choices=LABELS, default="en")
    p.add_argument("--title", action="store_true")
    p.add_argument("--ymin", type=float, default=0.0)
    p.add_argument("--ymax", type=float, default=1.0)
    a = p.parse_args()
    df = read(a.input)
    summary, outliers = summaries(df)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(a.output.with_name(f"summary_python_{a.lang}.csv"), index=False, float_format="%.12g")
    draw(df, summary, outliers, a.lang, a.output, a.title, a.ymin, a.ymax)
    print(f"PYTHON_COMPLETE rows={len(df)} groups={len(summary)} outliers={len(outliers)} output={a.output}")

if __name__ == "__main__":
    main()
