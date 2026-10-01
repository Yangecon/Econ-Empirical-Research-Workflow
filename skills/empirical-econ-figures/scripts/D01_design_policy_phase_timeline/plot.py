"""Policy rollout phases with real monthly dates and optional termination."""
from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont
from matplotlib.patches import Rectangle
import pandas as pd

TEXT = {
    "en": {"transition": "Transition", "enforcement": "Enforcement",
           "termination": "Termination", "n": "n={n}",
           "title": "Staggered policy rollout and termination"},
    "zh": {"transition": "过渡期", "enforcement": "强制执行期",
           "termination": "政策终止", "n": "样本数={n}",
           "title": "分批政策实施与终止时间线"},
}
TRANSITION = "#c8d7eb"
ENFORCEMENT = "#155c8a"

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

def month(value: str, field: str) -> pd.Timestamp | None:
    if value == "":
        return None
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d")
    except ValueError as e:
        raise ValueError(f"{field}: use ISO YYYY-MM-01") from e
    if parsed.day != 1:
        raise ValueError(f"{field}: use the first day of a month")
    return pd.Timestamp(parsed)

def read(path: Path) -> tuple[pd.DataFrame, pd.Timestamp | None]:
    df = pd.read_csv(path, dtype=str, encoding="utf-8-sig", keep_default_na=False)
    fields = {"cohort", "cohort_order", "cohort_label_en", "cohort_label_zh", "n",
              "status", "transition_start", "transition_end", "enforcement_start",
              "enforcement_end", "termination_month"}
    if not fields.issubset(df):
        raise ValueError(f"CSV missing columns: {sorted(fields-set(df))}")
    if df.empty or df.cohort.eq("").any() or df.cohort.duplicated().any():
        raise ValueError("need unique, nonempty cohort IDs")
    if df[["cohort_label_en", "cohort_label_zh"]].eq("").any().any():
        raise ValueError("each cohort needs bilingual labels")
    if not df.status.isin(["policy", "nonpolicy"]).all():
        raise ValueError("status must be policy or nonpolicy")
    for col in ("cohort_order", "n"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    if df[["cohort_order", "n"]].isna().any().any() or (df.n <= 0).any():
        raise ValueError("cohort_order and n must be positive integers")
    if sorted(df.cohort_order.tolist()) != list(range(1, len(df)+1)) or (df.cohort_order%1 != 0).any() or (df.n%1 != 0).any():
        raise ValueError("cohort_order must be unique and consecutive from 1; n must be integer")
    date_cols = ["transition_start", "transition_end", "enforcement_start", "enforcement_end", "termination_month"]
    for col in date_cols:
        df[col] = pd.Series([month(value, col) for value in df[col]], index=df.index, dtype=object)
    present = lambda value: value is not None and not pd.isna(value)
    terms = {t for t in df.termination_month if present(t)}
    if len(terms) > 1:
        raise ValueError("termination_month must be the same in every nonblank row")
    termination = next(iter(terms)) if terms else None
    if len(df[df.status == "nonpolicy"]) > 1:
        raise ValueError("at most one nonpolicy row is supported")
    for row in df.itertuples():
        trans = (row.transition_start, row.transition_end)
        enf = (row.enforcement_start, row.enforcement_end)
        if row.status == "nonpolicy":
            if any(present(v) for v in (*trans, *enf)):
                raise ValueError("nonpolicy row cannot have phase intervals")
            continue
        if any(not present(v) for v in trans) or not trans[0] < trans[1]:
            raise ValueError(f"{row.cohort}: transition range must be nonempty and increasing")
        if present(enf[0]) != present(enf[1]):
            raise ValueError(f"{row.cohort}: enforcement needs both endpoints or neither")
        if present(enf[0]) and (not enf[0] < enf[1] or enf[0] < trans[1]):
            raise ValueError(f"{row.cohort}: enforcement must follow transition without overlap")
        if termination is not None and (trans[1] > termination or (present(enf[1]) and enf[1] > termination)):
            raise ValueError(f"{row.cohort}: phase extends after termination")
    if not (df.status == "policy").any():
        raise ValueError("need at least one policy cohort")
    return df.sort_values("cohort_order"), termination

def render(df: pd.DataFrame, termination: pd.Timestamp | None, lang: str, output: Path, title: bool) -> None:
    setup_font(lang)
    labels = TEXT[lang]
    starts = [t for t in df.transition_start if not pd.isna(t)]
    ends = [t for t in df.transition_end if not pd.isna(t)] + [t for t in df.enforcement_end if not pd.isna(t)]
    first = min(starts) - pd.DateOffset(months=1)
    last = max(ends + ([termination] if termination is not None else [])) + pd.DateOffset(months=2)
    months = pd.date_range(first, last, freq="MS")
    index = {m: i for i, m in enumerate(months)}
    mcount = len(months)
    policy_rows = df[df.status == "policy"]
    nrows = len(df)
    fig, ax = plt.subplots(figsize=(11.2, max(4.3, 1.0*nrows+1.8)))
    header_y = nrows+.15
    for i, m in enumerate(months):
        ax.add_patch(Rectangle((i, header_y), 1, .58, facecolor="#5d5d5d", edgecolor="white", lw=.5))
        ax.text(i+.5, header_y+.29, m.strftime("%b") if lang=="en" else f"{m.month}月",
                color="white", ha="center", va="center", fontsize=8.5)
    for year in sorted({m.year for m in months}):
        positions = [i for i,m in enumerate(months) if m.year==year]
        ax.text((min(positions)+max(positions)+1)/2, header_y+.87, str(year),
                ha="center", va="center", fontsize=10.5, fontweight="bold")
    for _, row in df.iterrows():
        y = nrows-row.cohort_order
        ax.text(-.25, y+.25, f"{row[f'cohort_label_{lang}']}\n({labels['n'].format(n=int(row.n))})",
                ha="right", va="center", fontsize=9)
        if row.status == "nonpolicy":
            continue
        a,b = index[row.transition_start], index[row.transition_end]
        ax.add_patch(Rectangle((a,y), b-a, .52, facecolor=TRANSITION, edgecolor="none"))
        ax.text((a+b)/2, y+.26, labels["transition"], ha="center", va="center", fontsize=9, color="#202020")
        if not pd.isna(row.enforcement_start):
            a,b = index[row.enforcement_start], index[row.enforcement_end]
            ax.add_patch(Rectangle((a,y), b-a, .52, facecolor=ENFORCEMENT, edgecolor="none"))
            ax.text((a+b)/2, y+.26, labels["enforcement"], ha="center", va="center", fontsize=8.5, color="white")
    if termination is not None:
        x = index[termination]
        ax.vlines(x, -.25, header_y, color="#bb3038", linestyle=(0,(4,3)), linewidth=1.5)
        ax.text(x+.12, -.3, labels["termination"], color="#a32b33", fontsize=8.5, va="top")
    ax.set_xlim(-.4, mcount+.05)
    ax.set_ylim(-.75, header_y+1.05)
    ax.set_axis_off()
    if title:
        fig.suptitle(labels["title"], fontsize=12, y=.99)
    fig.subplots_adjust(left=.25, right=.985, top=.90 if title else .94, bottom=.07)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=220, facecolor="white")
    fig.savefig(output.with_suffix(".pdf"), facecolor="white")
    plt.close(fig)

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--lang", choices=TEXT, default="en")
    p.add_argument("--title", action="store_true")
    args = p.parse_args()
    df, termination = read(args.input)
    render(df, termination, args.lang, args.output, args.title)
    print(f"PYTHON_COMPLETE lang={args.lang} cohorts={len(df)} policy={sum(df.status=='policy')} "
          f"termination={termination.date() if termination is not None else 'none'} output={args.output.resolve()}")

if __name__ == "__main__":
    main()
