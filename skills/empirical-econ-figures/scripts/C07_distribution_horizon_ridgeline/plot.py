#!/usr/bin/env python3
"""Two-panel horizon ridgelines; descriptive drawing method with synthetic demo."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import pandas as pd

HORIZONS = (1, 10, 100, 1000, 10000)
METRICS = ("price_impact", "profits")
COLORS = ("#f5a5a5", "#d3cf75", "#71cdb6", "#78cdef", "#dfa2e9")
LIMITS = {"price_impact": (-20.0, 20.0), "profits": (-10.0, 10.0)}


def demo_data(seed: int = 20260928, n_races: int = 600) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for h in HORIZONS:
        for metric in METRICS:
            for race in range(n_races):
                if metric == "price_impact":
                    value = rng.gamma(1.5 + 0.12*np.log10(h), 1.25)
                    value += rng.normal(0, 0.18 + 0.1*np.log10(h))
                else:
                    side = rng.choice((-1, 1), p=(0.42, 0.58))
                    value = side * rng.gamma(1.8, 1.05) + rng.normal(0, 0.33)
                if rng.random() < 0.18:
                    value = 0.0
                rows.append((race, h, metric, value))
    return pd.DataFrame(rows, columns=["race_id", "horizon_ms", "metric", "value_bps"])


def validate_input(df: pd.DataFrame) -> pd.DataFrame:
    required = {"race_id", "horizon_ms", "metric", "value_bps"}
    if not required <= set(df):
        raise ValueError(f"Required columns: {sorted(required)}")
    out = df.copy()
    if out["race_id"].isna().any() or out["race_id"].astype(str).str.strip().eq("").any():
        raise ValueError("race_id must be nonempty")
    out["horizon_ms"] = pd.to_numeric(out["horizon_ms"], errors="raise")
    if set(out.horizon_ms) != set(HORIZONS):
        raise ValueError(f"Exactly the five horizons {HORIZONS} are required")
    if set(out.metric) != set(METRICS):
        raise ValueError(f"Exactly the two metrics {METRICS} are required")
    if out.duplicated(["race_id", "horizon_ms", "metric"]).any():
        raise ValueError("Duplicate race_id × horizon_ms × metric")
    out["value_bps"] = pd.to_numeric(out["value_bps"], errors="raise")
    if np.isinf(out.value_bps).any():
        raise ValueError("Infinite value_bps")
    return out


def compute(df: pd.DataFrame, bandwidth: float = 0.55, zero_policy: str = "exclude", n_grid: int = 401):
    if not np.isfinite(bandwidth) or bandwidth <= 0 or n_grid < 101:
        raise ValueError("bandwidth must be positive and grid must have at least 101 points")
    if zero_policy not in ("exclude", "include"):
        raise ValueError("zero_policy must be exclude or include")
    df = validate_input(df)
    densities, counts = [], []
    for metric in METRICS:
        # One fixed x grid and Gaussian bandwidth for all five horizons within a panel.
        grid = np.linspace(*LIMITS[metric], n_grid)
        for h in HORIZONS:
            raw = df[(df.metric == metric) & (df.horizon_ms == h)].value_bps.to_numpy(float)
            finite = raw[np.isfinite(raw)]
            zeros = int(np.sum(finite == 0))
            used = finite[finite != 0] if zero_policy == "exclude" else finite
            if len(used) == 0:
                raise ValueError(f"No density observations for {metric}, {h} ms")
            z = (grid[:, None] - used[None, :]) / bandwidth
            density = np.exp(-0.5*z*z).mean(axis=1) / (bandwidth*np.sqrt(2*np.pi))
            counts.append({"metric": metric, "horizon_ms": h, "n_rows": len(raw),
                           "n_missing": len(raw)-len(finite), "n_finite": len(finite),
                           "n_zero": zeros, "zero_share_of_finite": zeros/len(finite) if len(finite) else None,
                           "n_density": len(used), "density_denominator": "n_density",
                           "zero_policy": zero_policy})
            densities.extend((metric, h, float(x), float(y)) for x, y in zip(grid, density))
    return (pd.DataFrame(densities, columns=["metric", "horizon_ms", "value_bps", "density"]),
            pd.DataFrame(counts))


def chinese_font():
    names = {f.name for f in font_manager.fontManager.ttflist}
    for candidate in ("Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "Source Han Sans SC", "Arial Unicode MS"):
        if candidate in names:
            return candidate
    return "DejaVu Sans"


def draw(density: pd.DataFrame, output: Path, lang: str = "en", title: bool = False):
    if lang not in ("en", "zh"):
        raise ValueError("lang must be en or zh")
    plt.rcParams.update({"font.family": chinese_font() if lang == "zh" else "DejaVu Sans",
                         "axes.unicode_minus": False, "pdf.fonttype": 42})
    fig, axs = plt.subplots(1, 2, figsize=(12.8, 6.0), sharey=True)
    max_density = float(density.density.max())
    height_scale = 0.78/max_density  # shared across both panels; peaks retain their quantitative differences
    labels = ("Price impact", "Profits") if lang == "en" else ("价格影响", "利润")
    for ax, metric, panel, panel_label in zip(axs, METRICS, "AB", labels):
        for i, h in enumerate(HORIZONS):
            sub = density[(density.metric == metric) & (density.horizon_ms == h)]
            x, y = sub.value_bps.to_numpy(), sub.density.to_numpy()
            ax.fill_between(x, i, i+height_scale*y, color=COLORS[i], alpha=0.75, linewidth=0)
            ax.plot(x, i+height_scale*y, color="#202020", lw=1.1)
            ax.hlines(i, *LIMITS[metric], color="#555555", lw=0.65)
        ax.axvline(0, color="#9a9a9a", lw=0.7, zorder=0)
        ax.set_xlim(*LIMITS[metric]); ax.set_ylim(-0.34, 4.94)
        ax.set_yticks(range(5), ("1 ms", "10 ms", "100 ms", "1 s", "10 s"))
        ax.tick_params(axis="y", length=0, pad=8)
        ax.grid(axis="x", color="#e9e9e9", lw=0.7)
        ax.set_axisbelow(True)
        ax.set_xlabel((f"Per-share {panel_label.lower()} (basis points)" if lang == "en"
                       else f"每股{panel_label}（基点）"), fontsize=10)
        ax.set_title(f"({panel}) {panel_label}", loc="left", fontsize=14, pad=10)
        for spine in ax.spines.values(): spine.set_visible(False)
    axs[0].set_ylabel("Kernel density by horizon" if lang == "en" else "核密度", labelpad=10)
    if title:
        fig.suptitle("Race price impact and profits by horizon" if lang == "en" else "不同时间窗口的竞速价格影响与利润", y=0.99, fontsize=15)
    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.16, top=0.83 if title else 0.88, wspace=0.40)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=230, facecolor="white")
    plt.close(fig)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path)
    p.add_argument("--outdir", type=Path, default=Path(__file__).parent / "outputs")
    p.add_argument("--lang", choices=("en", "zh"), default="en")
    p.add_argument("--title", action="store_true")
    p.add_argument("--bandwidth", type=float, default=0.55)
    p.add_argument("--zero-policy", choices=("exclude", "include"), default="exclude")
    a = p.parse_args()
    a.outdir.mkdir(parents=True, exist_ok=True)
    if a.input is None:
        data = demo_data()
        data.to_csv(a.outdir / "synthetic_input.csv", index=False)
        status = "synthetic demonstration; not paper observations"
    else:
        data = pd.read_csv(a.input)
        status = "user-supplied observations; no source-paper replication claim"
    den, counts = compute(data, a.bandwidth, a.zero_policy)
    den.to_csv(a.outdir / "density_grid.csv", index=False)
    counts.to_csv(a.outdir / "sample_counts.csv", index=False)
    suffix = "_title" if a.title else ""
    for ext in ("png", "pdf"):
        draw(den, a.outdir / f"horizon_density_{a.lang}{suffix}.{ext}", a.lang, a.title)
    (a.outdir / "run_metadata.json").write_text(json.dumps({"data_status": status, "bandwidth_bps": a.bandwidth,
       "bandwidth_rule": "fixed user-supplied Gaussian bandwidth, common across both panels and all horizons",
       "grid_points_per_panel": 401, "grid_limits_bps": LIMITS, "zero_policy": a.zero_policy,
       "height_scale": "single absolute density-to-ridge scale shared by both panels"}, indent=2), encoding="utf-8")
    print("HORIZON_DENSITY_COMPLETE")


if __name__ == "__main__": main()
