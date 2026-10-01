"""F23: cost-ordered steps whose widths are actual dispatched MWh."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

_fonts = {font.name for font in font_manager.fontManager.ttflist}
plt.rcParams["font.family"] = next((name for name in
    ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "DejaVu Sans"] if name in _fonts), "DejaVu Sans")
plt.rcParams["axes.unicode_minus"] = False

COLORS = ["#222222", "#888888", "#0173B2", "#D55E00"]


def prepare(frame: pd.DataFrame, tolerance: float = 1e-8) -> tuple[pd.DataFrame, pd.DataFrame]:
    fields = ["scenario", "unit_id", "marginal_cost", "dispatched_mwh"]
    if missing := set(fields) - set(frame):
        raise ValueError(f"Missing columns: {sorted(missing)}")
    data = frame.copy()
    if data.empty or data[["scenario", "unit_id"]].isna().any().any():
        raise ValueError("Scenario and unit IDs must be present")
    for field in ["scenario", "unit_id"]:
        if data[field].astype(str).str.strip().eq("").any():
            raise ValueError(f"Blank {field}")
    if data.duplicated(["scenario", "unit_id"]).any():
        raise ValueError("Duplicate unit within scenario")
    for field in ["marginal_cost", "dispatched_mwh"]:
        data[field] = pd.to_numeric(data[field], errors="coerce")
        if not np.isfinite(data[field].to_numpy()).all() or (data[field] < 0).any():
            raise ValueError(f"{field} must be finite and nonnegative")
    if (data.dispatched_mwh <= 0).any():
        raise ValueError("Only positive dispatched MWh appear in cost steps")
    totals = data.groupby("scenario").dispatched_mwh.sum()
    if len(totals) != 2:
        raise ValueError("Need exactly two comparable dispatch scenarios")
    if not np.allclose(totals, totals.iloc[0], rtol=tolerance, atol=tolerance):
        raise ValueError("Scenario total dispatched MWh must match common demand")
    data = data.sort_values(["scenario", "marginal_cost", "unit_id"]).reset_index(drop=True)
    data["x_end"] = data.groupby("scenario").dispatched_mwh.cumsum()
    data["x_start"] = data.x_end - data.dispatched_mwh
    coords = []
    for row in data.itertuples(index=False):
        coords.extend([{"scenario": row.scenario, "unit_id": row.unit_id,
                        "endpoint": k, "x_mwh": x, "marginal_cost": row.marginal_cost}
                       for k, x in [(0, row.x_start), (1, row.x_end)]])
    return data, pd.DataFrame(coords)


def render(steps: pd.DataFrame, coords: pd.DataFrame, prefix: Path,
           title: str | None = None) -> None:
    fig, ax = plt.subplots(figsize=(8.5, 5.0))
    for i, (scenario, part) in enumerate(coords.groupby("scenario", sort=False)):
        ax.plot(part.x_mwh, part.marginal_cost, drawstyle="default", linewidth=2.1,
                color=COLORS[i % len(COLORS)], label=scenario)
    ax.set(xlabel="Cumulative dispatched energy (MWh)", ylabel="Marginal cost (currency/MWh)",
           xlim=(0, float(steps.x_end.max())))
    ax.set_ylim(bottom=0)
    ax.grid(axis="y", linestyle="--", alpha=.45)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=9)
    if title:
        ax.set_title(title, fontsize=13)
    fig.tight_layout()
    prefix.parent.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "pdf"):
        fig.savefig(prefix.with_suffix("."+ext), dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output-prefix", type=Path, required=True)
    p.add_argument("--title")
    args = p.parse_args()
    steps, coords = prepare(pd.read_csv(args.input))
    render(steps, coords, args.output_prefix, args.title)
    steps.to_csv(args.output_prefix.with_name(args.output_prefix.name+"_steps.csv"), index=False)
    coords.to_csv(args.output_prefix.with_name(args.output_prefix.name+"_coordinates.csv"), index=False)
    print(json.dumps({"status": "PYTHON_OK", "units": len(steps),
                      "scenarios": steps.scenario.nunique(), "demand_mwh": float(steps.x_end.max())}))


if __name__ == "__main__":
    main()
