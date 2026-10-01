"""F48: ternary topic composition, colored by supplied sentiment percentile."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import Normalize, LinearSegmentedColormap
import numpy as np
import pandas as pd

ROOT3 = np.sqrt(3) / 2


def configure_font():
    names = {f.name for f in font_manager.fontManager.ttflist}
    for font in ("Noto Sans CJK SC", "Microsoft YaHei", "SimHei", "Arial Unicode MS"):
        if font in names:
            plt.rcParams["font.sans-serif"] = [font, "DejaVu Sans"]
            break
    plt.rcParams["axes.unicode_minus"] = False


def prepare(data, centers, half_window):
    columns = ["book_id", "year", "religion", "political_economy", "science", "sentiment_percentile"]
    if not set(columns).issubset(data.columns):
        raise ValueError(f"Missing required columns: {sorted(set(columns) - set(data.columns))}")
    out = data[columns].copy()
    if out.isna().any().any() or out.book_id.astype(str).str.strip().eq("").any():
        raise ValueError("Required fields cannot be missing or blank")
    if out.book_id.duplicated().any():
        raise ValueError("book_id must be unique")
    for col in columns[1:]:
        out[col] = pd.to_numeric(out[col], errors="raise")
    if not np.isfinite(out[columns[1:]].to_numpy(dtype=float)).all():
        raise ValueError("All numeric fields must be finite")
    if not np.allclose(out.year, np.round(out.year), atol=1e-10, rtol=0):
        raise ValueError("year must be an integer")
    shares = out[["religion", "political_economy", "science"]].to_numpy(dtype=float)
    if (shares < -1e-10).any() or (shares > 1 + 1e-10).any() or not np.allclose(shares.sum(axis=1), 1, atol=1e-7, rtol=0):
        raise ValueError("Topic shares must be within [0,1] and sum to one")
    if not out.sentiment_percentile.between(0, 1).all():
        raise ValueError("Precomputed sentiment percentile must be in [0,1]")
    if not centers or len(set(centers)) != len(centers) or half_window < 0:
        raise ValueError("Provide unique facet center years and a nonnegative half-window")
    out["triangle_x"] = out.science + .5 * out.religion
    out["triangle_y"] = ROOT3 * out.religion
    counts = {str(c): int(out.year.between(c - half_window, c + half_window).sum()) for c in centers}
    if any(n == 0 for n in counts.values()):
        raise ValueError("Every requested center year needs at least one book")
    return out, counts


def triangle(ax, frame, center, half_window, cmap):
    path = np.array([[0, 0], [1, 0], [.5, ROOT3], [0, 0]])
    ax.plot(path[:, 0], path[:, 1], color="#3B4A5A", lw=1)
    sub = frame.loc[frame.year.between(center - half_window, center + half_window)]
    ax.scatter(sub.triangle_x, sub.triangle_y, c=sub.sentiment_percentile, cmap=cmap,
               vmin=0, vmax=1, s=8, alpha=.78, linewidth=0, rasterized=True)
    ax.text(.5, ROOT3 + .055, "Religion", ha="center", va="bottom", fontsize=8)
    ax.text(-.04, -.05, "Political economy", ha="left", va="top", fontsize=8)
    ax.text(1.04, -.05, "Science", ha="right", va="top", fontsize=8)
    ax.text(.5, -.15, f"{center}  (n={len(sub):,})", ha="center", va="top", fontsize=9, weight="bold")
    ax.set_xlim(-.12, 1.12)
    ax.set_ylim(-.18, ROOT3 + .12)
    ax.set_aspect("equal")
    ax.axis("off")


def render(frame, centers, half_window, output, title):
    configure_font()
    ncols = 2 if len(centers) <= 8 else 3
    nrows = int(np.ceil(len(centers) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(6.2 * ncols, 4.6 * nrows))
    axes = np.atleast_1d(axes).ravel()
    cmap = LinearSegmentedColormap.from_list("visible_gray", ["#171717", "#D0D0D0"])
    for ax, center in zip(axes, centers):
        triangle(ax, frame, center, half_window, cmap)
    for ax in axes[len(centers):]:
        ax.axis("off")
    sm = plt.cm.ScalarMappable(norm=Normalize(0, 1), cmap=cmap)
    fig.colorbar(sm, ax=axes.tolist(), fraction=.018, pad=.025, label="Precomputed progress sentiment percentile")
    if title:
        fig.suptitle(title, y=.995, fontsize=13)
    fig.subplots_adjust(left=.035, right=.87, top=.965 if not title else .94, bottom=.03,
                        hspace=.07, wspace=.03)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--centers", nargs="+", type=int, required=True)
    p.add_argument("--half-window", type=int, default=10)
    p.add_argument("--title", default="")
    a = p.parse_args()
    out, counts = prepare(pd.read_csv(a.input, dtype={"book_id": str}), a.centers, a.half_window)
    render(out, a.centers, a.half_window, a.output, a.title)
    out.to_csv(a.output.with_name(a.output.stem + "_checked.csv"), index=False)
    summary = {"status": "ok", "books_total": len(out), "center_years": a.centers,
               "half_window_years_inclusive": a.half_window, "facet_counts": counts,
               "sentiment_percentile_precomputed": True}
    a.output.with_name(a.output.stem + "_validation.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
