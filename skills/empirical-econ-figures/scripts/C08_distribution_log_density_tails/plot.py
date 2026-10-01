"""F33: supplied density curve with explicit log-density tail fits."""
import argparse
import json
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_shared"))
from line_geometry import draw_trace


def configure_font():
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in ("Noto Sans CJK SC", "Microsoft YaHei", "SimHei", "Arial Unicode MS"):
        if name in available:
            plt.rcParams["font.sans-serif"] = [name, "DejaVu Sans"]
            break
    plt.rcParams["axes.unicode_minus"] = False


def prepare(frame, density_column, log_density_column, left, right, mean, sd):
    if (density_column is None) == (log_density_column is None):
        raise ValueError("Choose exactly one density or log-density column")
    col = density_column or log_density_column
    if not {"x", col}.issubset(frame.columns):
        raise ValueError(f"Input needs x and {col}")
    out = frame[["x", col]].copy()
    for key in ("x", col):
        out[key] = pd.to_numeric(out[key], errors="raise")
    if out.isna().any().any() or not np.isfinite(out.to_numpy(dtype=float)).all():
        raise ValueError("x and density values must be finite and nonmissing")
    if density_column and (out[col] <= 0).any():
        raise ValueError("Density values must be strictly positive; no epsilon is inserted")
    out = out.rename(columns={col: "source_value"}).sort_values("x").reset_index(drop=True)
    if out.x.duplicated().any() or len(out) < 7:
        raise ValueError("Need at least seven unique x values")
    out["log_density"] = np.log(out.source_value) if density_column else out.source_value
    if not np.isfinite([mean, sd]).all() or sd <= 0:
        raise ValueError("Normal benchmark requires finite mean and positive SD")
    out["normal_log_density"] = -.5 * ((out.x - mean) / sd) ** 2 - np.log(sd * np.sqrt(2 * np.pi))
    fits = {}
    for label, bounds in (("left", left), ("right", right)):
        lo, hi = bounds
        if not np.isfinite(bounds).all() or lo >= hi:
            raise ValueError(f"Invalid {label} tail interval")
        subset = out.loc[out.x.between(lo, hi)]
        if len(subset) < 3:
            raise ValueError(f"{label} tail interval has fewer than three grid points")
        slope, intercept = np.polyfit(subset.x, subset.log_density, 1)
        fits[label] = {"x_min": lo, "x_max": hi, "n_grid_points": len(subset),
                       "slope": float(slope), "intercept": float(intercept)}
        out[f"{label}_fit"] = np.where(out.x.between(lo, hi), slope * out.x + intercept, np.nan)
    if left[1] >= right[0]:
        raise ValueError("Left and right fitting intervals must be separate")
    return out, fits


def render(out, fits, output, title, normal_mean, normal_sd):
    configure_font()
    fig, ax = plt.subplots(figsize=(8.7, 5.3))
    draw_trace(ax, out.x, out.log_density, color="#1764A0", linewidth=2.4, label="Supplied distribution")
    # Show the central normal benchmark where it remains readable against the tails.
    benchmark = out.loc[out.x.between(normal_mean - 4 * normal_sd, normal_mean + 4 * normal_sd)]
    draw_trace(ax, benchmark.x, benchmark.normal_log_density, color="#D55E00", linewidth=2, linestyle="--", label="Normal benchmark")
    for label in ("left", "right"):
        f = fits[label]
        sub = out.loc[out.x.between(f["x_min"], f["x_max"])]
        draw_trace(ax, sub.x, sub[f"{label}_fit"], color="#242424", linewidth=1.9, linestyle="-.",
                   label=f"{label.title()} fitted slope = {f['slope']:+.2f}")
    ax.set(xlabel="Outcome change", ylabel="Natural log of density")
    if title:
        ax.set_title(title)
    ax.grid(color="#D9DFE5", lw=.7, alpha=.7)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, loc="upper right", fontsize=9)
    fig.tight_layout()
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input", type=Path)
    p.add_argument("output", type=Path)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--density-column")
    g.add_argument("--log-density-column")
    p.add_argument("--left", nargs=2, type=float, required=True, metavar=("MIN", "MAX"))
    p.add_argument("--right", nargs=2, type=float, required=True, metavar=("MIN", "MAX"))
    p.add_argument("--normal-mean", type=float, default=0)
    p.add_argument("--normal-sd", type=float, required=True)
    p.add_argument("--title", default="")
    a = p.parse_args()
    out, fits = prepare(pd.read_csv(a.input), a.density_column, a.log_density_column,
                        a.left, a.right, a.normal_mean, a.normal_sd)
    render(out, fits, a.output, a.title, a.normal_mean, a.normal_sd)
    out.to_csv(a.output.with_name(a.output.stem + "_checked.csv"), index=False)
    summary = {"status": "ok", "n_grid_points": len(out), "normal_mean": a.normal_mean,
               "normal_sd": a.normal_sd, "fitted_log_density_slopes_not_pareto_indices": fits}
    a.output.with_name(a.output.stem + "_validation.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
