"""Calendar-spaced multi-series trends with optional explicit common-base indexing."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.font_manager import FontProperties, findfont
from matplotlib.colors import is_color_like

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_shared"))
from line_geometry import draw_trace

SERIES = (
    ("patents", "Patents", "专利", "#292929", "-"),
    ("publications", "Publications", "论文", "#292929", (0, (4, 3))),
)
TEXT = {
    "en": {"x_annual": "Year", "x_monthly": "Month", "y_raw_annual": "Annual count per sales unit",
           "y_raw_monthly": "Count per sales unit", "y_index": "Index (base = 100)",
           "title": "Annual trends"},
    "zh": {"x_annual": "年份", "x_monthly": "月份", "y_raw_annual": "每单位销售额的年度数量",
           "y_raw_monthly": "每单位销售额的月度数量", "y_index": "指数（基期 = 100）",
           "title": "年度趋势"},
}

def load_config(path: Path) -> dict:
    spec = json.loads(path.read_text(encoding="utf-8"))
    entries = spec.get("series")
    if not isinstance(entries, list) or not entries:
        raise ValueError("config.series must be a nonempty list")
    ids = []
    for row in entries:
        if not isinstance(row, dict) or any(not str(row.get(k, "")).strip() for k in ("id", "label_en", "label_zh")):
            raise ValueError("Each series needs nonblank id, label_en and label_zh")
        if not is_color_like(row.get("color")) or row.get("linestyle") not in ("-", "--", ":", "-."):
            raise ValueError("Series color or linestyle is invalid")
        ids.append(row["id"])
    if len(set(ids)) != len(ids):
        raise ValueError("Series IDs must be unique")
    keys = ("x_annual", "x_monthly", "y_raw_annual", "y_raw_monthly", "y_index", "title")
    axes = spec.get("axes", {})
    for lang in ("en", "zh"):
        if not isinstance(axes.get(lang), dict) or any(not str(axes[lang].get(k, "")).strip() for k in keys):
            raise ValueError(f"config.axes.{lang} needs all nonblank axis labels and title")
    return spec


def configured_series(config=None):
    if config is None:
        return SERIES
    return tuple((r["id"], r["label_en"], r["label_zh"], r["color"], r["linestyle"])
                 for r in config["series"])

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

def read(path: Path, frequency: str, config=None) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    cols = ["date", "series", "value"]
    if not set(cols).issubset(df) or df[cols].eq("").any().any():
        raise ValueError("required nonblank date, series, value")
    if set(df.series) != {s[0] for s in configured_series(config)}:
        raise ValueError("series IDs must match configured series")
    if not df.date.str.fullmatch(r"\d{4}-\d{2}-\d{2}").all():
        raise ValueError("dates must be ISO YYYY-MM-DD")
    df["date"] = pd.to_datetime(df.date, format="%Y-%m-%d", errors="raise")
    if frequency == "annual" and not ((df.date.dt.month == 1)&(df.date.dt.day == 1)).all():
        raise ValueError("annual dates must be January 1")
    if frequency == "monthly" and not (df.date.dt.day == 1).all():
        raise ValueError("monthly dates must be the first day of month")
    if df.duplicated(["series", "date"]).any():
        raise ValueError("duplicate series-date")
    df["value"] = pd.to_numeric(df.value, errors="raise")
    if not np.isfinite(df.value).all() or (df.value < 0).any():
        raise ValueError("value must be finite and nonnegative")
    return df

def calculate(df: pd.DataFrame, frequency: str, base_date: str | None, config=None) -> pd.DataFrame:
    if frequency not in ("annual", "monthly"):
        raise ValueError("frequency must be annual or monthly")
    if base_date:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", base_date):
            raise ValueError("base date must be ISO YYYY-MM-DD")
        base = pd.Timestamp(base_date)
        for sid, *_ in configured_series(config):
            row = df[(df.series == sid)&(df.date == base)]
            if len(row) != 1 or row.value.iloc[0] <= 0:
                raise ValueError(f"{sid}: base date must have a positive observed value")
    rows = []
    freq = "YS" if frequency == "annual" else "MS"
    for sid, *_ in configured_series(config):
        part = df[df.series == sid].set_index("date").sort_index()
        if len(part) < 2:
            raise ValueError(f"{sid}: at least two observations required")
        # Complete calendar only within observed span; absent periods remain NaN,
        # which makes matplotlib break rather than interpolate the line.
        span = pd.date_range(part.index.min(), part.index.max(), freq=freq)
        part = part.reindex(span)
        divisor = float(df[(df.series == sid)&(df.date == base)].value.iloc[0]) if base_date else 1.0
        part["plot_value"] = part.value/divisor*100 if base_date else part.value
        part["series"] = sid
        part.index.name = "date"
        rows.append(part.reset_index()[["date", "series", "value", "plot_value"]])
    return pd.concat(rows, ignore_index=True)

def draw(points: pd.DataFrame, lang: str, output: Path, frequency: str, base_date: str | None, title: bool, config=None) -> None:
    set_font(lang)
    series = configured_series(config)
    text = TEXT if config is None else config["axes"]
    fig, ax = plt.subplots(figsize=(9.4, 5.5), dpi=160)
    for sid, en, zh, color, style in series:
        p = points[points.series == sid]
        draw_trace(ax, p.date, p.plot_value, color=color, linewidth=2.0, linestyle=style)
        last = p.dropna(subset=["plot_value"]).iloc[-1]
        ax.annotate(en if lang == "en" else zh, xy=(last.date, last.plot_value),
                    xytext=(8, 0), textcoords="offset points", ha="left", va="center",
                    fontsize=10, color=color)
    span_days = (points.date.max()-points.date.min()).days
    # Reserve a small fraction of the observed calendar span for direct labels.
    # A fixed multi-year extension would crush a short monthly series.
    right_pad_days = max(30, span_days*.08)
    left_pad_days = 3 if frequency == "monthly" and span_days <= 210 else 0
    ax.set_xlim(points.date.min()-pd.Timedelta(days=left_pad_days),
                points.date.max()+pd.Timedelta(days=right_pad_days))
    ax.set_xlabel(text[lang]["x_"+frequency])
    ax.set_ylabel(text[lang]["y_index" if base_date else "y_raw_"+frequency])
    if frequency == "monthly" and span_days <= 210:
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    else:
        locator = mdates.AutoDateLocator(minticks=4, maxticks=9)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
    ax.grid(axis="y", color="#cecece", lw=.7)
    ax.spines[["top", "right"]].set_visible(False)
    if title:
        ax.set_title(text[lang]["title"])
    fig.tight_layout()
    fig.savefig(output, dpi=240)
    fig.savefig(output.with_suffix(".pdf"))
    plt.close(fig)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--lang", choices=TEXT, default="en")
    p.add_argument("--frequency", choices=("annual", "monthly"), default="annual")
    p.add_argument("--normalize-base", metavar="YYYY-MM-DD")
    p.add_argument("--title", action="store_true")
    p.add_argument("--config", type=Path, help="Optional series and axis-label JSON")
    a = p.parse_args()
    config = load_config(a.config) if a.config else None
    df = read(a.input, a.frequency, config)
    points = calculate(df, a.frequency, a.normalize_base, config)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    points.to_csv(a.output.with_name(a.output.stem+"_plotted.csv"), index=False, date_format="%Y-%m-%d", float_format="%.12g")
    draw(points, a.lang, a.output, a.frequency, a.normalize_base, a.title, config)
    print(f"PYTHON_COMPLETE rows={len(df)} calendar_rows={len(points)} base={a.normalize_base or 'none'} output={a.output}")

if __name__ == "__main__":
    main()
