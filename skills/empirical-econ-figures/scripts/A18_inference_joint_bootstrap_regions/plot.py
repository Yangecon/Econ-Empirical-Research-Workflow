"""F16: draw supplied nested joint-bootstrap grid memberships only."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
from matplotlib import font_manager
import warnings

_fonts = {font.name for font in font_manager.fontManager.ttflist}
plt.rcParams["font.family"] = next((name for name in
    ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "DejaVu Sans"] if name in _fonts), "DejaVu Sans")
plt.rcParams["axes.unicode_minus"] = False

SHADES = {99: "#EAEAEA", 95: "#C8C8C8", 90: "#999999"}


def prepare(grid: pd.DataFrame, point: pd.DataFrame) -> tuple[pd.DataFrame, tuple[float, float]]:
    fields = ["x_center", "y_center", "x_lo", "x_hi", "y_lo", "y_hi", "in90", "in95", "in99"]
    if missing := set(fields)-set(grid):
        raise ValueError(f"Missing grid columns: {sorted(missing)}")
    if not {"x", "y"}.issubset(point) or len(point) != 1 or grid.empty:
        raise ValueError("Need nonempty grid and one x,y point estimate")
    data = grid.copy()
    for field in fields:
        data[field] = pd.to_numeric(data[field], errors="coerce")
        if not np.isfinite(data[field].to_numpy()).all():
            raise ValueError(f"{field} must be finite")
    for field in ["in90", "in95", "in99"]:
        if not data[field].isin([0, 1]).all():
            raise ValueError("Membership flags must be 0/1")
    if not ((data.in90 <= data.in95) & (data.in95 <= data.in99)).all():
        raise ValueError("Joint regions must be nested: 90 inside 95 inside 99")
    if not ((data.x_lo < data.x_center) & (data.x_center < data.x_hi) &
            (data.y_lo < data.y_center) & (data.y_center < data.y_hi)).all():
        raise ValueError("Each center must lie inside a positive-area cell")
    if data.duplicated(["x_center", "y_center"]).any():
        raise ValueError("Duplicate grid-cell center")
    xs, ys = np.sort(data.x_center.unique()), np.sort(data.y_center.unique())
    if len(xs) < 2 or len(ys) < 2 or len(data) != len(xs)*len(ys):
        raise ValueError("Require complete two-dimensional rectangular grid")
    widths = data.x_hi-data.x_lo
    heights = data.y_hi-data.y_lo
    if not np.allclose(widths, widths.iloc[0]) or not np.allclose(heights, heights.iloc[0]):
        raise ValueError("Grid cells must have common width and height")
    if not np.allclose(data.x_center, (data.x_lo+data.x_hi)/2) or not np.allclose(data.y_center, (data.y_lo+data.y_hi)/2):
        raise ValueError("Grid cells must be centered on their bounds")
    if not np.allclose(np.diff(xs), widths.iloc[0]) or not np.allclose(np.diff(ys), heights.iloc[0]):
        raise ValueError("Grid cells must be contiguous with no gaps or overlaps")
    for x, subset in data.groupby("x_center"):
        if len(subset) != len(ys):
            raise ValueError("Incomplete y cells at x")
    xy = point[["x", "y"]].apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float).ravel()
    if not np.isfinite(xy).all():
        raise ValueError("Point estimate must be finite")
    data["region"] = np.select([data.in90.eq(1), data.in95.eq(1), data.in99.eq(1)], [90, 95, 99], default=0)
    hit = bool(((data.x_center.isin([xs[0], xs[-1]]) | data.y_center.isin([ys[0], ys[-1]])) & data.in99.eq(1)).any())
    if hit:
        warnings.warn("99% region reaches grid boundary; display may truncate the supplied region", stacklevel=2)
    data = data.sort_values(["x_center", "y_center"])
    data.attrs["region_hits_boundary"] = hit
    return data, (float(xy[0]), float(xy[1]))


def render(data: pd.DataFrame, estimate: tuple[float, float], prefix: Path,
           title: str | None = None) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 5.7))
    for row in data.itertuples(index=False):
        if row.region:
            ax.add_patch(Rectangle((row.x_lo, row.y_lo), row.x_hi-row.x_lo,
                                   row.y_hi-row.y_lo, facecolor=SHADES[row.region],
                                   edgecolor="none", zorder=1))
    xmin, xmax = float(data.x_lo.min()), float(data.x_hi.max())
    ymin, ymax = float(data.y_lo.min()), float(data.y_hi.max())
    xline = np.array([max(xmin, .5-ymax), min(xmax, .5-ymin)])
    if xline[0] < xline[1]:
        ax.plot(xline, .5-xline, color="#333333", linewidth=1.5, zorder=3,
                label="x + y = 0.5")
    ax.scatter(*estimate, color="black", s=42, zorder=4, label="Point estimate")
    ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax),
           xlabel="EP(-10%) - EP(-30%)", ylabel="EP(-30%)")
    ax.grid(color="#BBBBBB", alpha=.5, zorder=0)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    handles = [Patch(color=SHADES[k], label=f"{k}% joint region") for k in [99, 95, 90]]
    from matplotlib.lines import Line2D
    handles += [Line2D([], [], color="#333333", label="x + y = 0.5"),
                Line2D([], [], color="black", marker="o", linestyle="", label="Point estimate")]
    ax.legend(handles=handles, frameon=False, fontsize=9, loc="lower right")
    if title:
        ax.set_title(title, fontsize=13)
    fig.tight_layout()
    prefix.parent.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "pdf"):
        fig.savefig(prefix.with_suffix("."+ext), dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--grid", type=Path, required=True)
    p.add_argument("--point", type=Path, required=True)
    p.add_argument("--output-prefix", type=Path, required=True)
    p.add_argument("--title")
    a = p.parse_args()
    checked, point = prepare(pd.read_csv(a.grid), pd.read_csv(a.point))
    render(checked, point, a.output_prefix, a.title)
    checked.to_csv(a.output_prefix.with_name(a.output_prefix.name+"_checked.csv"), index=False)
    print(json.dumps({"status": "PYTHON_OK", "cells": len(checked),
                      "region_cells": checked.region.value_counts().to_dict(), "point": point,
                      "region_hits_boundary": checked.attrs["region_hits_boundary"]}))


if __name__ == "__main__":
    main()
