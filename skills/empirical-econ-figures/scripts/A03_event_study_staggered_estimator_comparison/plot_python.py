"""Render the Stata-exported audited estimates; this does no estimation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D


METHODS = [
    ("TWFE OLS", "TWFE OLS", "#008837", "D"),
    ("Sun-Abraham", "Sun–Abraham", "#C51B2B", "o"),
    ("Callaway-Santanna", "Callaway–Sant’Anna", "#2B6CB0", "s"),
    ("dCDH dynamic", "de Chaisemartin–d’Haultfoeuille", "#8E44AD", "^"),
    ("BJS imputation", "Borusyak–Jaravel–Spiess", "#B36B00", "s"),
    ("Wooldridge jwdid", "Wooldridge (jwdid)", "#373737", "o"),
]
STATUSES = {"estimated", "pretrend_test", "placebo_test", "normalized_reference"}


def render(input_path: Path, output_stem: Path, title: str | None = None) -> dict:
    data = pd.read_csv(input_path)
    required = {"estimator", "event_time", "b", "se", "ci_low", "ci_high", "status"}
    if not required.issubset(data):
        raise ValueError(f"Missing columns: {sorted(required - set(data))}")
    if data.duplicated(["estimator", "event_time"]).any():
        raise ValueError("Duplicate estimator/event-time rows")
    if not np.isfinite(data["event_time"]).all() or not np.equal(data.event_time, np.floor(data.event_time)).all():
        raise ValueError("Event time must be finite integers")
    if set(data.estimator) != {m[0] for m in METHODS}:
        raise ValueError("Expected exactly the six verified estimator labels")
    if not set(data.status).issubset(STATUSES):
        raise ValueError("Unknown row status")
    ref = data.status.eq("normalized_reference")
    if not ((data.loc[ref, "event_time"] == -1) & (data.loc[ref, "b"] == 0)).all():
        raise ValueError("Invalid normalized reference")
    if data.loc[ref, ["se", "ci_low", "ci_high"]].notna().any().any():
        raise ValueError("A normalized reference cannot have uncertainty")
    if set(data.loc[ref, "estimator"]) != {"TWFE OLS", "Sun-Abraham"} or len(data.loc[ref]) != 2:
        raise ValueError("Unexpected normalized reference rows")
    est = data.loc[~ref]
    if est[["event_time", "b", "se", "ci_low", "ci_high"]].isna().any().any():
        raise ValueError("Missing estimate or interval")
    if not np.isfinite(est[["event_time", "b", "se", "ci_low", "ci_high"]]).all().all():
        raise ValueError("Nonfinite estimate or interval")
    if not ((est.ci_low <= est.b) & (est.b <= est.ci_high) & (est.se > 0)).all():
        raise ValueError("Invalid interval or standard error")
    z = 1.959963984540054
    if not np.allclose(est.ci_low, est.b - z * est.se, atol=1e-6):
        raise ValueError("Lower intervals differ from declared normal 95% rule")
    if not np.allclose(est.ci_high, est.b + z * est.se, atol=1e-6):
        raise ValueError("Upper intervals differ from declared normal 95% rule")

    fig, ax = plt.subplots(figsize=(9.4, 5.5))
    ax.set_axisbelow(True)
    ax.grid(axis="y", color="#E7E7E7", linewidth=0.8)
    ax.axhline(0, color="#888888", lw=0.9, zorder=1)
    ax.axvline(-0.5, color="#B2B2B2", lw=0.9, ls="--", zorder=1)
    legend = []
    for j, (key, label, color, marker) in enumerate(METHODS):
        block = data.loc[data.estimator.eq(key)].sort_values("event_time")
        x = block.event_time.to_numpy(dtype=float) + (j - 2.5) * 0.12
        sig = (block.ci_low.gt(0) | block.ci_high.lt(0)) & ~block.status.eq("normalized_reference")
        for idx, row in enumerate(block.itertuples(index=False)):
            if row.status != "normalized_reference":
                ax.vlines(x[idx], row.ci_low, row.ci_high, color=color, lw=1.0, zorder=2)
                ax.hlines([row.ci_low, row.ci_high], x[idx] - 0.025, x[idx] + 0.025,
                          color=color, lw=1.0, zorder=2)
            ax.scatter(x[idx], row.b,
                       marker="o" if row.status == "normalized_reference" else marker,
                       s=38, linewidths=1.15,
                       facecolors=color if sig.iloc[idx] else "white",
                       edgecolors=color, zorder=3)
        legend.append(Line2D([], [], color=color, marker=marker, linestyle="None",
                             markerfacecolor=color, markeredgecolor=color,
                             markersize=6, label=label))
    xmin, xmax = int(data.event_time.min()), int(data.event_time.max())
    ax.set_xticks(range(xmin, xmax + 1))
    ax.set_xlim(xmin - 0.7, xmax + 0.7)
    ax.set_xlabel("Periods relative to adoption", fontsize=11)
    ax.set_ylabel("Estimated effect (95% CI)", fontsize=11)
    if title:
        ax.set_title(title, fontsize=12)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(handles=legend, loc="upper center", bbox_to_anchor=(0.5, -0.14),
              ncol=3, frameon=False, fontsize=9)
    fig.tight_layout()
    output_stem.parent.mkdir(parents=True, exist_ok=True)
    for suffix in ("png", "pdf"):
        fig.savefig(output_stem.with_suffix(f".{suffix}"), dpi=300,
                    bbox_inches="tight", facecolor="white")
    plt.close(fig)
    summary = {
        "source": str(input_path.resolve()),
        "rows": int(len(data)),
        "estimated_or_test_rows": int((~ref).sum()),
        "normalized_reference_rows": int(ref.sum()),
        "rows_by_estimator": data.groupby("estimator").size().to_dict(),
        "rows_by_status": data.groupby("status").size().to_dict(),
        "confidence_level": 0.95,
        "interval_rule": "b +/- normal_0.975 * se",
        "python_role": "plot Stata-exported estimates; no independent Python estimation",
    }
    output_stem.with_name(output_stem.name + "_validation.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    root = Path(__file__).resolve().parent
    parser.add_argument("--input", type=Path, default=root / "audited_estimates.csv")
    parser.add_argument("--output-stem", type=Path, default=root / "staggered_comparison_python")
    parser.add_argument("--title", default=None)
    args = parser.parse_args()
    print(json.dumps(render(args.input, args.output_stem, args.title), ensure_ascii=False))
    print("STAGGERED_PYTHON_COMPLETE")
