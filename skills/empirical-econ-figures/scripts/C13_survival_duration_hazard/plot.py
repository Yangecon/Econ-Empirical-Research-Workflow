"""F37/F38/F39: shared line, bar and step renderer with statistical adapters."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_shared"))
from line_geometry import draw_trace

PALETTE = ["#0173B2", "#D55E00", "#009E73", "#CC79A7", "#666666"]
_fonts = {entry.name for entry in font_manager.fontManager.ttflist}
plt.rcParams["font.family"] = next((name for name in
    ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "DejaVu Sans"] if name in _fonts),
    "DejaVu Sans")
plt.rcParams["axes.unicode_minus"] = False


def required(frame: pd.DataFrame, fields: list[str]) -> None:
    missing = sorted(set(fields) - set(frame.columns))
    if missing:
        raise ValueError(f"Missing columns: {', '.join(missing)}")
    if frame.empty:
        raise ValueError("Input has no rows")


def number(frame: pd.DataFrame, field: str, *, nonnegative=True) -> pd.Series:
    val = pd.to_numeric(frame[field], errors="coerce")
    if not np.isfinite(val.to_numpy(dtype=float)).all():
        raise ValueError(f"{field} must be finite and numeric")
    if nonnegative and (val < 0).any():
        raise ValueError(f"{field} must be nonnegative")
    return val


def unique(frame: pd.DataFrame, fields: list[str]) -> None:
    if frame.duplicated(fields).any():
        raise ValueError(f"Duplicate {fields} keys")


def labels(frame: pd.DataFrame, fields: list[str]) -> None:
    for field in fields:
        if frame[field].isna().any() or frame[field].astype(str).str.strip().eq("").any():
            raise ValueError(f"{field} must have a nonblank label")


def calendar_dates(values: pd.Series) -> pd.Series:
    # Numeric dates must be unambiguous four-digit years, never Unix nanoseconds.
    if pd.api.types.is_numeric_dtype(values):
        years = pd.to_numeric(values, errors="coerce")
        if years.isna().any() or not years.between(1000, 9999).all() or not np.equal(years, np.floor(years)).all():
            raise ValueError("Numeric dates must be four-digit years")
        return pd.to_datetime(years.astype(int).astype(str) + "-01-01", errors="raise")
    out = pd.to_datetime(values, errors="coerce")
    if out.isna().any():
        raise ValueError("date must be a valid calendar date")
    return out


def trend_adapter(frame: pd.DataFrame, events: pd.DataFrame | None = None):
    required(frame, ["date", "series", "value"])
    data = frame.copy()
    data["date"] = calendar_dates(data["date"])
    labels(data, ["series"])
    # Missing values are explicit breaks, never interpolated.
    bad = data["value"].notna() & pd.to_numeric(data["value"], errors="coerce").isna()
    if bad.any():
        raise ValueError("value has malformed nonmissing numbers")
    data["value"] = pd.to_numeric(data["value"], errors="coerce")
    if np.isinf(data["value"]).any():
        raise ValueError("value cannot be infinite")
    unique(data, ["date", "series"])
    data = data.sort_values(["series", "date"])
    annotations = []
    if events is not None:
        required(events, ["date", "label"])
        for row in events.itertuples(index=False):
            date = calendar_dates(pd.Series([getattr(row, "date")])).iloc[0]
            label = str(getattr(row, "label")).strip()
            if pd.isna(date) or not label:
                raise ValueError("Policy event needs a valid date and label")
            if not data.date.min() <= date <= data.date.max():
                raise ValueError("Policy event date outside plotted span")
            annotations.append({"x": date, "label": label})
    panels = [{"name": "", "series": [
        {"name": str(name), "x": part.date.to_numpy(), "y": part.value.to_numpy(dtype=float), "kind": "line"}
        for name, part in data.groupby("series", sort=False)
    ], "events": annotations}]
    return panels, data


def hazard_adapter(frame: pd.DataFrame):
    required(frame, ["panel", "series", "duration", "events", "risk_set"])
    data = frame.copy()
    labels(data, ["panel", "series"])
    for field in ["duration", "events", "risk_set"]:
        data[field] = number(data, field)
    if not np.equal(data.duration, np.floor(data.duration)).all() or (data.duration < 1).any():
        raise ValueError("duration must be positive integer periods")
    if not np.equal(data.events, np.floor(data.events)).all() or not np.equal(data.risk_set, np.floor(data.risk_set)).all():
        raise ValueError("events and risk_set must be integer counts")
    if (data.risk_set <= 0).any() or (data.events > data.risk_set).any():
        raise ValueError("Require positive risk_set and events <= risk_set")
    unique(data, ["panel", "series", "duration"])
    data["hazard"] = data.events / data.risk_set
    data = data.sort_values(["panel", "series", "duration"])
    panels = []
    for panel, part in data.groupby("panel", sort=False):
        panels.append({"name": str(panel), "series": [
            {"name": str(name), "x": subset.duration.to_numpy(dtype=float), "y": subset.hazard.to_numpy(dtype=float), "kind": "bar"}
            for name, subset in part.groupby("series", sort=False)
        ]})
    return panels, data


def km_adapter(frame: pd.DataFrame, ci: bool = False):
    required(frame, ["panel", "series", "duration", "event"])
    data = frame.copy()
    labels(data, ["panel", "series"])
    if "id" in data.columns:
        if data["id"].isna().any() or data["id"].astype(str).str.strip().eq("").any():
            raise ValueError("id must be nonblank when supplied")
        unique(data, ["panel", "series", "id"])
    data["duration"] = number(data, "duration")
    data["event"] = number(data, "event")
    if not data.event.isin([0, 1]).all() or (data.duration < 0).any():
        raise ValueError("duration >= 0 and event in {0,1} required")
    panels = []
    summary = []
    for panel, part in data.groupby("panel", sort=False):
        traces = []
        for name, group in part.groupby("series", sort=False):
            n = len(group)
            table = group.groupby("duration").event.agg(events="sum", total="size").sort_index()
            at_risk = n
            survival = 1.0
            greenwood = 0.0
            ci_lower = ci_upper = 1.0
            xs, ys, lows, highs = [0.0], [1.0], [1.0], [1.0]
            for time, row in table.iterrows():
                d = int(row.events)
                c = int(row.total - d)
                if d > at_risk:
                    raise ValueError("Events exceed risk set")
                # Events precede censoring at tied durations.
                if d:
                    survival *= 1 - d / at_risk
                    if at_risk > d:
                        greenwood += d / (at_risk * (at_risk - d))
                    xs.append(float(time))
                    ys.append(survival)
                    se = survival * np.sqrt(greenwood) if survival else 0.0
                    ci_lower = max(0.0, survival - 1.96 * se)
                    ci_upper = min(1.0, survival + 1.96 * se)
                    lows.append(ci_lower)
                    highs.append(ci_upper)
                summary.append({"panel": panel, "series": name, "duration": time,
                                "risk_set": at_risk, "events": d, "censored": c,
                                "survival": survival, "ci_lower": ci_lower if ci else np.nan,
                                "ci_upper": ci_upper if ci else np.nan})
                at_risk -= d + c
            if at_risk != 0:
                raise AssertionError("Risk-set accounting failed")
            # Carry the last survival value to the final observed censor/event time.
            endpoint = float(table.index.max())
            if endpoint > xs[-1]:
                xs.append(endpoint)
                ys.append(survival)
                lows.append(lows[-1])
                highs.append(highs[-1])
            traces.append({"name": str(name), "x": np.asarray(xs), "y": np.asarray(ys),
                           "lower": np.asarray(lows) if ci else None,
                           "upper": np.asarray(highs) if ci else None, "kind": "step"})
        panels.append({"name": str(panel), "series": traces})
    return panels, pd.DataFrame(summary)


def render(panels: list[dict], prefix: Path, *, xlabel: str, ylabel: str,
           title: str | None = None, events: bool = False, percent: bool = False) -> None:
    n = len(panels)
    fig, axes = plt.subplots(n, 1, figsize=(8.4, max(4.8, 3.7*n)), squeeze=False)
    for ax, panel in zip(axes[:, 0], panels):
        series = panel["series"]
        for j, trace in enumerate(series):
            x, y, kind = trace["x"], trace["y"], trace["kind"]
            color = PALETTE[j % len(PALETTE)]
            if kind == "line":
                draw_trace(ax, x, y, marker="o", markersize=3.5, linewidth=2.1,
                           color=color, label=trace["name"])
            elif kind == "bar":
                # Discrete hazard is a period probability, so source-like bars.
                width = 0.72 / len(series)
                offset = (j - (len(series)-1)/2) * width
                ax.bar(x + offset, y * (100 if percent else 1), width=width * .92,
                       color=color, alpha=.8, label=trace["name"])
            elif kind == "step":
                draw_trace(ax, x, y, kind="step", linewidth=2.1, color=color,
                           linestyle="--" if j % 2 else "-", label=trace["name"],
                           lower=trace.get("lower"), upper=trace.get("upper"))
            else:
                raise ValueError(f"Unknown rendering kind: {kind}")
        if events:
            for k, event in enumerate(panel.get("events", [])):
                ax.axvline(event["x"], color="#777777", linestyle=":", linewidth=1)
                ax.annotate(event["label"], (event["x"], 1),
                            xycoords=("data", "axes fraction"), xytext=(3, -7 - 19*(k % 2)),
                            textcoords="offset points", rotation=90, va="top", fontsize=9,
                            bbox={"facecolor": "white", "edgecolor": "none", "alpha": .8})
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
        ax.set(xlabel=xlabel, ylabel=ylabel)
        if panel["name"]:
            ax.text(0, 1.03, panel["name"], transform=ax.transAxes,
                    fontsize=11, fontweight="semibold")
        if series[0]["kind"] == "step":
            ax.set_ylim(0, 1.02)
        elif series[0]["kind"] == "bar":
            ax.set_ylim(bottom=0)
        ax.grid(axis="y", linestyle="--", color="#D0D0D0", alpha=.65)
        ax.set_axisbelow(True)
        ax.spines[["top", "right"]].set_visible(False)
        if len(series) > 1:
            if events:
                ax.legend(frameon=False, fontsize=9, ncol=min(len(series), 3),
                          loc="lower left", bbox_to_anchor=(0, 1.02), borderaxespad=0)
            else:
                ax.legend(frameon=False, fontsize=9, ncol=min(len(series), 3))
    if title:
        fig.suptitle(title, fontsize=13)
    fig.tight_layout()
    prefix.parent.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "pdf"):
        fig.savefig(prefix.with_suffix("." + ext), dpi=300,
                    bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("variant", choices=["historical_policy_timeline", "discrete_duration_hazard_panels", "kaplan_meier_survival_panels"])
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output-prefix", type=Path, required=True)
    p.add_argument("--events", type=Path, help="F37 dated event CSV")
    p.add_argument("--ci", action="store_true", help="F39 pointwise Greenwood normal 95 percent CI")
    p.add_argument("--title", help="Optional figure title; omitted by default")
    p.add_argument("--xlabel")
    p.add_argument("--ylabel")
    args = p.parse_args()
    frame = pd.read_csv(args.input)
    if args.variant == "historical_policy_timeline":
        panels, checked = trend_adapter(frame, pd.read_csv(args.events) if args.events else None)
        xlabel, ylabel, events, percent = "Year", "Value", True, False
    elif args.variant == "discrete_duration_hazard_panels":
        panels, checked = hazard_adapter(frame)
        xlabel, ylabel, events, percent = "Duration (periods)", "Conditional event probability (%)", False, True
    else:
        panels, checked = km_adapter(frame, ci=args.ci)
        xlabel, ylabel, events, percent = "Duration", "Survival probability", False, False
    render(panels, args.output_prefix, xlabel=args.xlabel or xlabel,
           ylabel=args.ylabel or ylabel, title=args.title,
           events=events, percent=percent)
    checked.to_csv(args.output_prefix.with_name(args.output_prefix.name + "_checked.csv"), index=False)
    print(json.dumps({"status": "OK", "variant": args.variant, "rows": len(frame),
                      "panels": len(panels), "output_prefix": str(args.output_prefix)}))


if __name__ == "__main__":
    main()
