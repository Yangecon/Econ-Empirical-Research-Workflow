"""F05: genuine ID-matched outcomes, marginal densities, means and pair gaps."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from matplotlib import font_manager

_fonts = {font.name for font in font_manager.fontManager.ttflist}
plt.rcParams["font.family"] = next((name for name in
    ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "DejaVu Sans"] if name in _fonts), "DejaVu Sans")
plt.rcParams["axes.unicode_minus"] = False


def prepare(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    fields = {"pair_id", "black_contacts", "white_contacts"}
    if missing := fields-set(frame):
        raise ValueError(f"Missing columns: {sorted(missing)}")
    data = frame.copy()
    if len(data) < 3 or data.pair_id.isna().any() or data.pair_id.astype(str).str.strip().eq("").any():
        raise ValueError("Need at least three complete pair IDs")
    data["pair_id"] = data.pair_id.astype(str).str.strip()
    if data.pair_id.duplicated().any():
        raise ValueError("Each true pair ID must occur once")
    for field in ["black_contacts", "white_contacts"]:
        data[field] = pd.to_numeric(data[field], errors="coerce")
        if not np.isfinite(data[field].to_numpy()).all() or (data[field] < 0).any() or not np.equal(data[field], np.floor(data[field])).all():
            raise ValueError(f"{field} must be nonnegative integer counts")
    data["difference_white_minus_black"] = data.white_contacts-data.black_contacts
    data = data.sort_values("pair_id").reset_index(drop=True)
    n = len(data)
    data["x_black"] = [1 + (((i*37) % 101)/100-.5)*.13 for i in range(1, n+1)]
    data["x_white"] = data.x_black+1
    summary = []
    for label, values in [("Black", data.black_contacts), ("White", data.white_contacts),
                          ("White minus Black, paired", data.difference_white_minus_black)]:
        mean = float(values.mean())
        se = float(values.std(ddof=1)/np.sqrt(n))
        summary.append({"measure": label, "pairs": n, "mean": mean,
                        "se": se, "ci_low": mean-1.96*se, "ci_high": mean+1.96*se})
    return data, pd.DataFrame(summary)


def kde(values: np.ndarray, grid: np.ndarray) -> np.ndarray:
    std = float(np.std(values, ddof=1))
    bandwidth = max(.75, 1.06*std*len(values)**(-.2))
    z = (grid[:, None]-values[None, :])/bandwidth
    return np.exp(-.5*z*z).mean(axis=1)/(bandwidth*np.sqrt(2*np.pi))


def render(data: pd.DataFrame, summary: pd.DataFrame, prefix: Path,
           title: str | None = None) -> None:
    fig, ax = plt.subplots(figsize=(8.6, 5.6))
    norm = TwoSlopeNorm(vcenter=0, vmin=-max(1, abs(data.difference_white_minus_black).max()),
                        vmax=max(1, abs(data.difference_white_minus_black).max()))
    cmap = plt.get_cmap("coolwarm")
    for row in data.itertuples(index=False):
        ax.plot([row.x_black, row.x_white], [row.black_contacts, row.white_contacts],
                color=cmap(norm(row.difference_white_minus_black)), alpha=.36, linewidth=.85, zorder=1)
    ax.scatter(data.x_black, data.black_contacts, s=14, color="#0173B2", alpha=.8, zorder=2)
    ax.scatter(data.x_white, data.white_contacts, s=14, color="#D55E00", alpha=.8, zorder=2)
    ymin = max(0, min(data.black_contacts.min(), data.white_contacts.min())-3)
    ymax = max(data.black_contacts.max(), data.white_contacts.max())+4
    grid = np.linspace(ymin, ymax, 250)
    d_black = kde(data.black_contacts.to_numpy(dtype=float), grid)
    d_white = kde(data.white_contacts.to_numpy(dtype=float), grid)
    scale = .34/max(d_black.max(), d_white.max())
    ax.fill_betweenx(grid, .58-d_black*scale, .58, color="#0173B2", alpha=.17)
    ax.fill_betweenx(grid, .58, .58+d_white*scale, color="#D55E00", alpha=.17)
    ax.plot(.58-d_black*scale, grid, color="#0173B2", linewidth=1.2)
    ax.plot(.58+d_white*scale, grid, color="#D55E00", linewidth=1.2)
    for measure, x, color in [("Black", .78, "#0173B2"), ("White", 2.22, "#D55E00")]:
        row = summary.loc[summary.measure == measure].iloc[0]
        ax.errorbar(x, row["mean"], yerr=[[row["mean"]-row.ci_low], [row.ci_high-row["mean"]]],
                    fmt="o", markersize=7, capsize=4, linewidth=1.3, color=color, zorder=4)
    ax.set(xlim=(.13, 2.48), ylim=(ymin, ymax), ylabel="Number of contacts")
    ax.set_xticks([.58, 1, 2], ["Marginal distributions", "Black profile", "White profile"])
    ax.grid(axis="y", linestyle="--", alpha=.35)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
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
    a = p.parse_args()
    data, summary = prepare(pd.read_csv(a.input, dtype={"pair_id": str}))
    render(data, summary, a.output_prefix, a.title)
    data.to_csv(a.output_prefix.with_name(a.output_prefix.name+"_pairs_checked.csv"), index=False)
    summary.to_csv(a.output_prefix.with_name(a.output_prefix.name+"_summary.csv"), index=False)
    print(json.dumps({"status": "PYTHON_OK", "pairs": len(data),
                      "mean_paired_gap": float(summary.iloc[2]["mean"])}))


if __name__ == "__main__":
    main()
