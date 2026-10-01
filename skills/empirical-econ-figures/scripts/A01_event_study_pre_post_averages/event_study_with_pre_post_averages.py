#!/usr/bin/env python3
"""Event study with pre- and post-treatment coefficient averages.

Standalone demo:
    python event_study_with_pre_post_averages.py

Real estimates:
    python event_study_with_pre_post_averages.py --estimates estimates.csv \
        --covariance covariance.csv

Required estimates.csv columns:
    term, event_time, estimate, is_reference
Optional column: weight (nonnegative fixed aggregation weights; default 1).
The covariance CSV has a first column named term and matching term columns.
Include exactly one normalized reference at -1 with estimate=0 and a zero
covariance row/column. Each non-reference diagonal variance must be positive.
A complete covariance matrix, NOT merely individual SEs, is required.

The demo estimates a bundled balanced synthetic panel, not the supplied paper.
The horizontal ribbons are CIs for two scalar summaries, NOT uniform bands.
The post summary is not automatically an ATT. The pre summary is a placebo
mean, not a treatment effect or a joint pre-trend test.
No title, subtitle, caption, or notes are drawn; add these in your manuscript.
CI style, bar width, and figure size affect appearance only, NOT CI endpoints.
Dependencies: numpy, pandas, matplotlib, scipy. Python 3.10+.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
from scipy.stats import norm, t
from estimate_demo_panel import estimate


# ===================== EDIT FIGURE LABELS HERE =====================
PRE_TEXT = "Pre-treatment"
POST_TEXT = "Post-treatment"
LABEL_Y_FRACTION = 0.065   # Fraction of axes height measured from the bottom.
FIRST_TREATED_PERIOD = 0
REFERENCE_PERIOD = -1
CI_WIDTH_FRACTION = 0.22 # Bar width / minimum event-time gap.
PERIOD_SPACING = 0.43     # Smaller values make the figure horizontally denser.
FIG_WIDTH_MIN = 6.2       # Inches; keep labels legible with few periods.
FIG_WIDTH_MAX = 11.0      # Inches; more periods use automatic tick thinning.
FIG_WIDTH_OVERHEAD = 1.25
FIG_HEIGHT = 4.15         # Inches; no space reserved for title or notes.
# The divider is calculated halfway between the last pre and first post tick.
# With annual integer periods it is -0.5, NOT the baseline period -1.
# ==================================================================


def critical_value(level: float, df: float | None = None) -> float:
    """Two-sided pointwise normal / Student-t critical value."""
    if not 0 < level < 1:
        raise ValueError("level must be a fraction between 0 and 1, e.g. 0.95.")
    if df is not None and (not np.isfinite(df) or df <= 0):
        raise ValueError("df must be positive and finite, or None.")
    quantile = (1 + level) / 2
    return float(norm.ppf(quantile) if df is None else t.ppf(quantile, df))


def demo_inputs() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Estimate the bundled fixed-seed panel used by both languages."""
    here = Path(__file__).resolve().parent
    estimates, covariance, _ = estimate(pd.read_csv(here / "demo_panel.csv"))
    return estimates, covariance


def prepare_estimates(
    estimates: pd.DataFrame, covariance: pd.DataFrame, *, level: float = 0.95,
    df: float | None = None, post_is_att: bool = False,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Align the covariance by names and compute fixed-weight summaries w'b, w'Vw.

    Weights are normalized SEPARATELY within pre and post. The normalized
    reference is INCLUDED in the pre denominator. Estimated weights need their own uncertainty treatment;
    use estimator-specific aggregation/influence functions in that case.
    """
    critical = critical_value(level, df)
    if post_is_att:
        raise ValueError("Post height under the -1 reference is not the static DID; use the post-minus-pre contrast.")
    required = {"term", "event_time", "estimate", "is_reference"}
    if not required.issubset(estimates.columns):
        raise ValueError(f"Missing columns: {sorted(required - set(estimates.columns))}")
    data = estimates.copy().sort_values("event_time").reset_index(drop=True)
    if len(data) < 3:
        raise ValueError("Supply pre and post estimates plus any reference period.")
    if not data["is_reference"].isin([0, 1, False, True]).all():
        raise ValueError("is_reference must contain only 0 or 1.")
    if "weight" not in data:
        data["weight"] = 1.0
    data["term"] = data["term"].astype(str)
    if data["term"].duplicated().any() or data["event_time"].duplicated().any():
        raise ValueError("term and event_time must each be unique.")
    numeric = data[["event_time", "estimate", "weight"]].to_numpy(dtype=float)
    if not np.isfinite(numeric).all() or (data["weight"] < 0).any():
        raise ValueError("Inputs must be finite; weights must be nonnegative.")
    names = data["term"].tolist()
    if covariance.index.has_duplicates or covariance.columns.has_duplicates:
        raise ValueError("Covariance row/column names must be unique.")
    if set(covariance.index) != set(names) or set(covariance.columns) != set(names):
        raise ValueError("Covariance labels must match the term column exactly.")
    v = covariance.loc[names, names].to_numpy(dtype=float)
    if not np.isfinite(v).all() or not np.allclose(v, v.T, rtol=1e-8, atol=1e-12):
        raise ValueError("Covariance must be finite and symmetric.")
    tolerance = 1e-10 * max(float(np.abs(v).max()), np.finfo(float).eps)
    if np.linalg.eigvalsh(v).min() < -tolerance:
        raise ValueError("Covariance must be positive semidefinite.")
    reference = data["is_reference"].astype(bool).to_numpy()
    beta = data["estimate"].to_numpy(dtype=float)
    if reference.sum() != 1 or data.loc[reference, "event_time"].iloc[0] != REFERENCE_PERIOD:
        raise ValueError("Exactly one normalized reference at event_time=-1 is required.")
    if not np.allclose(beta[reference], 0) or not np.allclose(v[reference], 0, atol=1e-14):
        raise ValueError("A normalized reference must have zero estimate and covariance.")
    if np.any(np.diag(v)[~reference] <= 0):
        raise ValueError("Every non-reference coefficient needs positive variance.")
    data["se"] = np.sqrt(np.maximum(np.diag(v), 0))
    data["ci_low"] = beta - critical * data["se"]
    data["ci_high"] = beta + critical * data["se"]
    data["significant"] = (~reference) & ((data["ci_low"] > 0) | (data["ci_high"] < 0))
    data["group"] = np.where(data["event_time"] < FIRST_TREATED_PERIOD, "pre", "post")
    # The reference has a real pre-period observation even though its coefficient
    # is fixed at zero. It therefore contributes one period to the pre mean.
    rows = []
    for group in ("pre", "post"):
        selected = data["group"].eq(group).to_numpy()
        raw = data["weight"].to_numpy(dtype=float)
        if not selected.any() or raw[selected].sum() <= 0:
            raise ValueError(f"{group} requires at least one positive-weight estimate.")
        weights = np.zeros(len(data))
        weights[selected] = raw[selected] / raw[selected].sum()
        estimate = float(weights @ beta)
        variance = float(weights @ v @ weights)
        if variance < -tolerance:
            raise ValueError("The variance of a summary is negative.")
        se = float(np.sqrt(max(variance, 0)))
        label = "Pre mean" if group == "pre" else "Post mean"
        rows.append({
            "group": group, "label": label, "estimate": estimate, "se": se,
            "ci_low": estimate - critical * se, "ci_high": estimate + critical * se,
            "first_period": float(data.loc[selected, "event_time"].min()),
            "last_period": float(data.loc[selected, "event_time"].max()),
            "n_terms": int(selected.sum()), "level": level,
        })
        data[f"weight_{group}"] = weights
    return data, pd.DataFrame(rows)


def add_pre_post_labels(ax: Axes, divider: float) -> None:
    """All labels are generated by code; no image editor is used.

    x uses event-time units; y uses a fraction of the axes height. Consequently,
    changes in the outcome's scale do not require hand-editing the text height.
    """
    left, right = ax.get_xlim()
    pre_center = (left + divider) / 2
    post_center = (divider + right) / 2
    ax.text(pre_center, LABEL_Y_FRACTION, PRE_TEXT,
            transform=ax.get_xaxis_transform(), ha="center", va="center", fontsize=11)
    ax.text(post_center, LABEL_Y_FRACTION, POST_TEXT,
            transform=ax.get_xaxis_transform(), ha="center", va="center", fontsize=11)


def figure_dimensions(
    n_periods: int, *, width: float | None = None,
    height: float = FIG_HEIGHT, period_spacing: float = PERIOD_SPACING,
) -> tuple[float, float]:
    """Compact auto-width; event-time coordinates are never relabeled or compressed."""
    if n_periods < 3:
        raise ValueError("Supply at least three event periods.")
    if not np.isfinite(height) or height < 3:
        raise ValueError("Figure height must be finite and at least 3 inches.")
    if not np.isfinite(period_spacing) or period_spacing <= 0:
        raise ValueError("period_spacing must be finite and positive.")
    if width is None:
        width = float(np.clip(FIG_WIDTH_OVERHEAD + period_spacing * n_periods,
                              FIG_WIDTH_MIN, FIG_WIDTH_MAX))
    if not np.isfinite(width) or width < 5:
        raise ValueError("Figure width must be finite and at least 5 inches.")
    return float(width), float(height)


def event_ticks(data: pd.DataFrame, figure_width: float) -> np.ndarray:
    """Thin labels, not observations, and retain the endpoints, reference, and onset."""
    periods = data["event_time"].to_numpy(dtype=float)
    capacity = max(8, int(np.floor(figure_width * 2.2)))
    stride = max(1, int(np.ceil(len(periods) / capacity)))
    selected = np.zeros(len(periods), dtype=bool)
    selected[::stride] = True
    selected[0] = selected[-1] = True
    selected |= data["is_reference"].eq(1).to_numpy()
    selected[np.flatnonzero(periods >= FIRST_TREATED_PERIOD)[0]] = True
    return periods[selected]


def draw_figure(
    data: pd.DataFrame, summaries: pd.DataFrame, *, post_is_att: bool,
    level: float, synthetic: bool = False, ci_width: float = CI_WIDTH_FRACTION,
    figure_width: float | None = None, figure_height: float = FIG_HEIGHT,
    period_spacing: float = PERIOD_SPACING,
    title: str | None = None,
    ci_style: str = "bar", connect: bool = False,
) -> Figure:
    """One axes, without title/subtitle/notes; use the manuscript for those elements.

    post_is_att, level, and synthetic remain in the interface for compatibility.
    All estimates and CI endpoints have already been computed by prepare_estimates.
    ci_width changes vertical bar thickness only. It never changes a standard
    error, confidence level, or CI endpoint. True event-time spacing is retained.
    """
    if not np.isfinite(ci_width) or not 0 < ci_width <= 1:
        raise ValueError("ci_width must be in (0, 1].")
    if ci_style not in ("bar", "cap"):
        raise ValueError("ci_style must be bar or cap.")
    data = data.sort_values("event_time").reset_index(drop=True)
    periods = data["event_time"].to_numpy(dtype=float)
    width, height = figure_dimensions(len(periods), width=figure_width,
                                      height=figure_height, period_spacing=period_spacing)
    fig = plt.figure(figsize=(width, height), dpi=160)
    # Physical margins remain small when the auto-width grows.
    left = 0.78 / width
    right_margin = 0.16 / width
    bottom = 0.80 / height
    top_margin = 0.14 / height
    ax = fig.add_axes([left, bottom, 1 - left - right_margin,
                       1 - bottom - top_margin])
    ink = plt.rcParams["text.color"]
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_linewidth(0.65)
        ax.spines[side].set_alpha(0.6)
    ax.tick_params(labelsize=9, length=3, width=0.65)
    step = float(np.diff(periods).min())
    if step <= 0:
        raise ValueError("event_time values must be unique.")
    last_pre = float(periods[periods < FIRST_TREATED_PERIOD].max())
    first_post = float(periods[periods >= FIRST_TREATED_PERIOD].min())
    divider = (last_pre + first_post) / 2
    ax.set_xlim(periods.min() - 0.6 * step, periods.max() + 0.6 * step)
    lower = float(min(data["ci_low"].min(), summaries["ci_low"].min(), 0))
    upper = float(max(data["ci_high"].max(), summaries["ci_high"].max(), 0))
    span = max(upper - lower, 0.01)
    # This small internal strip is for the Pre-treatment / Post-treatment labels.
    ax.set_ylim(lower - 0.23 * span, upper + 0.13 * span)
    ax.axhline(0, linestyle=(0, (2, 3)), linewidth=0.85, color=ink, alpha=0.35, zorder=0)
    ax.axvline(divider, linestyle=(0, (3, 3)), linewidth=0.85, color=ink, alpha=0.4, zorder=0)
    estimated = data.loc[data["is_reference"].eq(0)]
    # Narrow gray bars retain the source's visual grammar; only marker fill
    # encodes whether the displayed CI excludes zero.
    if ci_style == "bar":
        ax.bar(estimated["event_time"], estimated["ci_high"] - estimated["ci_low"],
               bottom=estimated["ci_low"], width=ci_width * step,
               color="#808080", alpha=0.22, linewidth=0, zorder=1)
    else:
        ax.errorbar(estimated["event_time"], estimated["estimate"],
                    yerr=[estimated["estimate"] - estimated["ci_low"],
                          estimated["ci_high"] - estimated["estimate"]],
                    fmt="none", ecolor="#888888", elinewidth=1.05,
                    capsize=2.2, zorder=2)
    if connect:
        for group in ("pre", "post"):
            section = estimated.loc[estimated["group"].eq(group)]
            gaps = np.flatnonzero(np.diff(section["event_time"]) > 1.5 * step) + 1
            for positions in np.split(np.arange(len(section)), gaps):
                block = section.iloc[positions]
                ax.plot(block["event_time"], block["estimate"],
                        linestyle=(0, (2, 2)), linewidth=0.8,
                        color="#555555", zorder=3)
    for sig, color in ((False, "#777777"), (True, "#111111")):
        section = estimated.loc[estimated["significant"].eq(sig)]
        ax.scatter(section["event_time"], section["estimate"], s=23,
                   facecolors=color if sig else "white", edgecolors=color,
                   linewidths=1.1, zorder=5 if sig else 4)
    handles, legend_labels = [], []
    for row, summary_color in zip(summaries.itertuples(index=False),
                                  ("#1f77b4", "#ff7f0e")):
        ends = [row.first_period - 0.42 * step, row.last_period + 0.42 * step]
        line, = ax.plot(ends, [row.estimate] * 2, linewidth=2.4, zorder=5,
                        color=summary_color, solid_capstyle="butt")
        ax.fill_between(ends, [row.ci_low] * 2, [row.ci_high] * 2,
                        color=line.get_color(), alpha=0.17, linewidth=0, zorder=2)
        handles.append(line)
        legend_labels.append(f"{row.label} = {row.estimate:.3f}")
    reference = data.loc[data["is_reference"].eq(1)]
    ax.plot(reference["event_time"], reference["estimate"], linestyle="none",
            marker="o", markersize=5.0, markerfacecolor="white",
            markeredgecolor="#777777", zorder=6)
    add_pre_post_labels(ax, divider)
    ticks = event_ticks(data, width)
    ax.set_xticks(ticks, [f"{period:g}" for period in ticks])
    ax.set_xlabel("Event time relative to treatment", fontsize=10, labelpad=8)
    ax.set_ylabel("Estimated effect", fontsize=10, labelpad=8)
    if title:
        ax.set_title(title, fontsize=12, pad=8)
    legend_center = left + (1 - left - right_margin) / 2
    fig.legend(handles, legend_labels, loc="upper center",
               bbox_to_anchor=(legend_center, 0.255 / height),
               ncol=2, frameon=False, fontsize=9.5, handlelength=2.5, columnspacing=2.4,
               borderaxespad=0)
    return fig


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--estimates", type=Path)
    parser.add_argument("--covariance", type=Path)
    parser.add_argument("--output", type=Path, default=Path.cwd() / "figures")
    parser.add_argument("--level", type=float, default=0.95)
    parser.add_argument("--df", type=float, default=None)
    parser.add_argument("--post-is-att", action="store_true", help="Deprecated; rejected because post height is not the DID contrast.")
    parser.add_argument("--title", default=None, help="Optional figure title; omitted by default.")
    parser.add_argument("--ci-width", type=float, default=CI_WIDTH_FRACTION,
                        help="Vertical CI bar width / minimum event-time gap (default 0.22).")
    parser.add_argument("--ci-style", choices=("bar", "cap"), default="bar")
    parser.add_argument("--connect", action="store_true",
                        help="Draw a faint dashed line through estimates within each window.")
    parser.add_argument("--width", type=float, default=None,
                        help="Figure width in inches; omitted = adapt to the number of periods.")
    parser.add_argument("--height", type=float, default=FIG_HEIGHT)
    parser.add_argument("--period-spacing", type=float, default=PERIOD_SPACING,
                        help="Smaller values give a denser auto-width figure.")
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args(argv)
    if (args.estimates is None) != (args.covariance is None):
        parser.error("Pass both --estimates and --covariance, or neither for the demo.")
    synthetic = args.estimates is None
    if synthetic:
        estimates, covariance = demo_inputs()
    else:
        estimates = pd.read_csv(args.estimates)
        covariance = pd.read_csv(args.covariance, index_col=0)
    post_is_att = args.post_is_att
    data, summaries = prepare_estimates(estimates, covariance, level=args.level,
                                        df=args.df, post_is_att=post_is_att)
    pre_w = data.weight_pre.to_numpy(dtype=float)
    post_w = data.weight_post.to_numpy(dtype=float)
    contrast_w = post_w - pre_w
    beta = data.estimate.to_numpy(dtype=float)
    v = covariance.loc[data.term, data.term].to_numpy(dtype=float)
    contrast_b = float(contrast_w @ beta)
    contrast_se = float(np.sqrt(contrast_w @ v @ contrast_w))
    critical = critical_value(args.level, args.df)
    contrast = pd.DataFrame([{"estimand": "post_minus_pre", "estimate": contrast_b,
                              "se": contrast_se, "ci_low": contrast_b - critical*contrast_se,
                              "ci_high": contrast_b + critical*contrast_se}])
    figure = draw_figure(data, summaries, post_is_att=post_is_att,
                         level=args.level, synthetic=synthetic,
                         ci_width=args.ci_width, figure_width=args.width,
                         figure_height=args.height, period_spacing=args.period_spacing,
                         title=args.title, ci_style=args.ci_style,
                         connect=args.connect)
    args.output.mkdir(parents=True, exist_ok=True)
    stem = args.output / "event_study_with_pre_post_averages_python"
    for extension in ("png", "pdf", "svg"):
        figure.savefig(stem.with_suffix(f".{extension}"), dpi=300)
    summaries.to_csv(stem.with_name(stem.name + "_summaries.csv"), index=False)
    contrast.to_csv(stem.with_name(stem.name + "_contrast.csv"), index=False)
    data.to_csv(stem.with_name(stem.name + "_periods.csv"), index=False)
    if synthetic:
        estimates.to_csv(args.output / "demo_estimates.csv", index=False)
        covariance.to_csv(args.output / "demo_covariance.csv")
    print(summaries[["label", "estimate", "se", "ci_low", "ci_high"]].to_string(index=False))
    print(f"Figure size: {figure.get_figwidth():.2f} x {figure.get_figheight():.2f} inches")
    print(f"CI style: {args.ci_style}; bar width fraction: {args.ci_width:g}; CI endpoints unchanged.")
    if synthetic:
        print("Synthetic demonstration inputs only; NOT original paper estimates.")
    print(f"Saved: {stem}.png / .pdf / .svg")
    print("PYTHON_EVENT_AVERAGES_COMPLETE")
    if args.show:
        plt.show()
    plt.close(figure)


if __name__ == "__main__":
    main()
