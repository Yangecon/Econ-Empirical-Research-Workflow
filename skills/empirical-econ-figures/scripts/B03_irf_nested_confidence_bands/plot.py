"""Matrix of supplied impulse-response medians and nested posterior regions."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont

# Edit row/column IDs, units, and row-specific y limits together.
RESPONSES = (
    ("activity", "Activity (log points)", "经济活动（对数点）", -.011, .008),
    ("prices", "Prices (log points)", "价格（对数点）", -.009, .008),
    ("rate", "Rate (percentage points)", "利率（百分点）", -.004, .006),
    ("household_credit", "Household credit (log points)", "家庭信贷（对数点）", -.03, .015),
    ("business_credit", "Business credit (log points)", "企业信贷（对数点）", -.03, .018),
)
SHOCKS = (
    ("monetary", "Monetary", "货币政策"),
    ("household", "Household credit", "家庭信贷"),
    ("firm", "Firm credit", "企业信贷"),
    ("stress_a", "Stress A", "压力冲击 A"),
    ("stress_b", "Stress B", "压力冲击 B"),
)
MARKER_HORIZONS = (0, 12, 24, 36, 48, 60)
TEXT = {"en": {"x": "Months after shock", "title": "Impulse responses"},
        "zh": {"x": "冲击后的月数", "title": "脉冲响应"}}

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
    cols = ["response", "shock", "horizon", "median", "lo68", "hi68", "lo90", "hi90"]
    if not set(cols).issubset(df) or df[cols].eq("").any().any():
        raise ValueError(f"required nonblank columns: {cols}")
    ids = {(r[0], s[0]) for r in RESPONSES for s in SHOCKS}
    if set(zip(df.response, df.shock)) != ids:
        raise ValueError("every configured response-shock cell is required")
    for c in cols[2:]:
        df[c] = pd.to_numeric(df[c], errors="raise")
        if not np.isfinite(df[c]).all():
            raise ValueError(f"{c} must be finite")
    if (df.horizon < 0).any() or not (df.horizon == np.floor(df.horizon)).all():
        raise ValueError("horizons must be nonnegative integer months")
    if df.duplicated(["response", "shock", "horizon"]).any():
        raise ValueError("duplicate response-shock-horizon")
    if not ((df.lo90 <= df.lo68)&(df.lo68 <= df["median"]) &
            (df["median"] <= df.hi68)&(df.hi68 <= df.hi90)).all():
        raise ValueError("90% and 68% posterior bounds must be nested around median")
    common = None
    for (response, shock), part in df.groupby(["response", "shock"]):
        h = tuple(sorted(part.horizon.astype(int)))
        if len(h) < 3 or h[0] != 0 or (common is not None and h != common):
            raise ValueError("every cell needs same >=3-horizon grid starting at zero")
        common = h
        row = next(r for r in RESPONSES if r[0] == response)
        if part.lo90.min() < row[3] or part.hi90.max() > row[4]:
            raise ValueError(f"{response}: posterior bounds exceed configured y limits")
    df["outer_excludes_zero"] = ((df.lo90 > 0) | (df.hi90 < 0)).astype(int)
    return df

def draw(df: pd.DataFrame, lang: str, output: Path, title: bool) -> None:
    set_font(lang)
    nr, nc = len(RESPONSES), len(SHOCKS)
    fig, axes = plt.subplots(nr, nc, figsize=(14.5, 11.5), dpi=160,
                             sharex=True, squeeze=False)
    xmax = int(df.horizon.max())
    for i, (rid, ren, rzh, ymin, ymax) in enumerate(RESPONSES):
        for j, (sid, sen, szh) in enumerate(SHOCKS):
            ax = axes[i, j]
            p = df[(df.response == rid)&(df.shock == sid)].sort_values("horizon")
            x = p.horizon.to_numpy()
            ax.fill_between(x, p.lo90.to_numpy(), p.hi90.to_numpy(), color="#a7cde4", linewidth=0)
            ax.fill_between(x, p.lo68.to_numpy(), p.hi68.to_numpy(), color="#287db2", linewidth=0)
            ax.plot(x, p["median"], color="#202020", lw=1.0)
            marks = p[p.horizon.isin(MARKER_HORIZONS)]
            filled = marks[marks.outer_excludes_zero == 1]
            hollow = marks[marks.outer_excludes_zero == 0]
            ax.scatter(filled.horizon, filled["median"], s=11, color="#202020", zorder=4)
            ax.scatter(hollow.horizon, hollow["median"], s=11, facecolors="white",
                       edgecolors="#202020", linewidths=.7, zorder=4)
            ax.axhline(0, color="#303030", lw=.9)
            ax.set_xlim(0, xmax); ax.set_ylim(ymin, ymax)
            ax.set_xticks([0, xmax//2, xmax])
            ax.grid(axis="y", color="#d8d8d8", lw=.5)
            ax.spines[["top", "right"]].set_visible(False)
            ax.tick_params(labelsize=8)
            if j == 0:
                ax.set_ylabel(ren if lang == "en" else rzh, fontsize=9)
            else:
                ax.tick_params(labelleft=False)
            if i == 0:
                ax.set_title(sen if lang == "en" else szh, fontsize=10)
            if i == nr-1:
                ax.set_xlabel(TEXT[lang]["x"], fontsize=9)
    if title:
        fig.suptitle(TEXT[lang]["title"], y=.995, fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, .98 if title else 1), h_pad=1.0, w_pad=.7)
    fig.savefig(output, dpi=220); fig.savefig(output.with_suffix(".pdf")); plt.close(fig)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--lang", choices=TEXT, default="en")
    p.add_argument("--title", action="store_true")
    a = p.parse_args()
    df = read(a.input)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(a.output.with_name(a.output.stem+"_checked.csv"), index=False, float_format="%.12g")
    draw(df, a.lang, a.output, a.title)
    print(f"PYTHON_COMPLETE rows={len(df)} responses={len(RESPONSES)} shocks={len(SHOCKS)} output={a.output}")

if __name__ == "__main__":
    main()
