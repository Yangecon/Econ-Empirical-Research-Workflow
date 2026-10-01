"""F34: within-industry labor-share distributions, averaged by industry VA."""
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


def calculate(frame: pd.DataFrame, edges: np.ndarray) -> tuple[pd.DataFrame, pd.DataFrame]:
    edges = np.asarray(edges, dtype=float)
    if edges.ndim != 1 or len(edges) < 2 or not np.isfinite(edges).all() or not np.all(np.diff(edges) > 0):
        raise ValueError("Bin edges must be a finite strictly increasing 1D sequence")
    need = {"year", "industry", "establishment_id", "labor_share", "value_added"}
    if missing := need - set(frame):
        raise ValueError(f"Missing columns: {sorted(missing)}")
    if frame.empty or frame[["year", "industry", "establishment_id"]].isna().any().any():
        raise ValueError("Identifiers cannot be blank")
    for c in ["year", "industry", "establishment_id"]:
        if frame[c].astype(str).str.strip().eq("").any():
            raise ValueError(f"{c} cannot be blank")
    if frame.duplicated(["year", "industry", "establishment_id"]).any():
        raise ValueError("Duplicate establishment within industry-year")
    data = frame.copy()
    for c in ["labor_share", "value_added"]:
        data[c] = pd.to_numeric(data[c], errors="coerce")
        if not np.isfinite(data[c].to_numpy()).all():
            raise ValueError(f"{c} must be finite and numeric")
    if (data.labor_share < 0).any() or (data.value_added < 0).any():
        raise ValueError("Negative labor shares or value added are unsupported")
    if not ((data.labor_share >= edges[0]) & (data.labor_share <= edges[-1])).all():
        raise ValueError("Labor share outside specified common bins")
    data["bin"] = pd.cut(data.labor_share, edges, right=False, labels=False,
                         include_lowest=True)
    data.loc[data.labor_share == edges[-1], "bin"] = len(edges)-2
    data["bin"] = data["bin"].astype(int)
    records, weights = [], []
    for year, yr in data.groupby("year", sort=True):
        totals = yr.groupby("industry").value_added.sum()
        if (totals <= 0).any():
            raise ValueError("Every included industry-year needs positive total value added")
        year_total = totals.sum()
        if year_total <= 0:
            raise ValueError("Year total value added must be positive")
        for industry, group in yr.groupby("industry", sort=True):
            industry_weight = totals[industry] / year_total
            counts = np.bincount(group.bin, minlength=len(edges)-1)
            va = np.bincount(group.bin, weights=group.value_added, minlength=len(edges)-1)
            n, industry_va = len(group), totals[industry]
            weights.append({"year": year, "industry": industry, "establishments": n,
                            "industry_va": industry_va, "industry_weight": industry_weight})
            for b in range(len(edges)-1):
                records.append({"year": year, "industry": industry, "bin": b,
                    "bin_left": edges[b], "bin_right": edges[b+1],
                    "firm_count_share": counts[b]/n,
                    "value_added_share": va[b]/industry_va,
                    "industry_weight": industry_weight})
    within = pd.DataFrame(records)
    within["weighted_firm_count_share"] = within.firm_count_share * within.industry_weight
    within["weighted_value_added_share"] = within.value_added_share * within.industry_weight
    result = within.groupby(["year", "bin", "bin_left", "bin_right"], as_index=False)[
        ["weighted_firm_count_share", "weighted_value_added_share"]].sum()
    for year, group in result.groupby("year"):
        if not np.allclose(group[["weighted_firm_count_share", "weighted_value_added_share"]].sum(), 1):
            raise AssertionError(f"Shares do not sum to one in {year}")
    return result, pd.DataFrame(weights)


def render(result: pd.DataFrame, prefix: Path, title: str | None) -> None:
    years = sorted(result.year.unique())
    fig, axes = plt.subplots(2, len(years), figsize=(max(7.8, 4.2*len(years)), 7.2),
                             squeeze=False, sharex=True, sharey=True)
    specs = [("weighted_firm_count_share", "Establishments", "#0173B2"),
             ("weighted_value_added_share", "Value added", "#D55E00")]
    ymax = result[[specs[0][0], specs[1][0]]].to_numpy().max() * 1.14
    for j, year in enumerate(years):
        group = result[result.year == year]
        width = group.bin_right.to_numpy() - group.bin_left.to_numpy()
        for i, (field, label, color) in enumerate(specs):
            ax = axes[i, j]
            ax.bar(group.bin_left, group[field], width=width, align="edge", color=color,
                   edgecolor="white", linewidth=.8, alpha=.78)
            ax.set_ylim(0, ymax)
            ax.set_xlim(group.bin_left.min(), group.bin_right.max())
            ax.grid(axis="y", linestyle="--", alpha=.4)
            ax.set_axisbelow(True)
            ax.spines[["top", "right"]].set_visible(False)
            ax.set_title(f"{year} · {label}", fontsize=11)
            if j == 0:
                ax.set_ylabel("Industry-VA-weighted bin share", fontsize=10)
            if i == 1:
                ax.set_xlabel("Establishment labor share", fontsize=10)
    if title:
        fig.suptitle(title, fontsize=13)
    fig.tight_layout()
    prefix.parent.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "pdf"):
        fig.savefig(prefix.with_suffix("."+ext), dpi=300,
                    bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--output-prefix", type=Path, required=True)
    ap.add_argument("--bin-min", type=float, default=0)
    ap.add_argument("--bin-max", type=float, default=1.4)
    ap.add_argument("--bin-width", type=float, default=.1)
    ap.add_argument("--title")
    a = ap.parse_args()
    if not (np.isfinite([a.bin_min, a.bin_max, a.bin_width]).all() and
            a.bin_width > 0 and a.bin_max > a.bin_min):
        raise ValueError("Invalid common bin range or width")
    n = (a.bin_max-a.bin_min)/a.bin_width
    if not np.isclose(n, round(n)):
        raise ValueError("Bin range must be an integer multiple of bin width")
    edges = np.linspace(a.bin_min, a.bin_max, round(n)+1)
    result, weights = calculate(pd.read_csv(a.input), edges)
    render(result, a.output_prefix, a.title)
    result.to_csv(a.output_prefix.with_name(a.output_prefix.name+"_checked.csv"), index=False)
    weights.to_csv(a.output_prefix.with_name(a.output_prefix.name+"_industry_weights.csv"), index=False)
    print(json.dumps({"status": "OK", "years": len(result.year.unique()),
                      "industry_years": len(weights), "output": str(a.output_prefix)}))


if __name__ == "__main__":
    main()
