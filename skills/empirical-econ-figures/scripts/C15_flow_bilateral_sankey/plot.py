#!/usr/bin/env python3
"""Conserved two-column bilateral flow diagram, amounts in USD billions."""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.path import Path as MplPath
from matplotlib.patches import PathPatch, Rectangle
import numpy as np
import pandas as pd

SOURCES = [
    ("British Virgin Islands", "英属维尔京群岛"),
    ("Cayman Islands", "开曼群岛"),
    ("Ireland", "爱尔兰"),
    ("Luxembourg", "卢森堡"),
    ("Netherlands", "荷兰"),
    ("Other tax havens", "其他避税地"),
]
DESTINATIONS = [
    ("Brazil", "巴西"), ("China", "中国"), ("India", "印度"),
    ("Russia", "俄罗斯"), ("South Africa", "南非"),
]
DEMO_MATRIX = [
    [1, 9, 0, 1, 0],
    [13, 17, 0, 0, 0],
    [0, 1, 0, 6, 0],
    [4, 1, 0, 5, 0],
    [17, 0, 1, 1, 4],
    [0, 5, 3, 0, 1],
]
COLORS = ["#E45756", "#4E91C2", "#72B76B", "#9A70AE", "#F3A24A"]


def make_demo() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Explicit synthetic edge and node-total tables, including zero edges."""
    edges = pd.DataFrame([
        (source, destination, DEMO_MATRIX[i][j])
        for i, (source, _) in enumerate(SOURCES)
        for j, (destination, _) in enumerate(DESTINATIONS)
    ], columns=["source", "destination", "amount_usd_billion"])
    source_totals = edges.groupby("source", sort=False).amount_usd_billion.sum()
    destination_totals = edges.groupby("destination", sort=False).amount_usd_billion.sum()
    nodes = pd.DataFrame(
        [("source", name, zh, source_totals[name]) for name, zh in SOURCES] +
        [("destination", name, zh, destination_totals[name]) for name, zh in DESTINATIONS],
        columns=["side", "node", "label_zh", "total_usd_billion"],
    )
    return edges, nodes


def validate(edges: pd.DataFrame, nodes: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    er = {"source", "destination", "amount_usd_billion"}
    nr = {"side", "node", "total_usd_billion"}
    if not er.issubset(edges) or not nr.issubset(nodes):
        raise ValueError(f"Missing edge columns {sorted(er-set(edges))} or node columns {sorted(nr-set(nodes))}")
    e, n = edges.copy(), nodes.copy()
    if e.empty or n.empty or e[["source", "destination"]].isna().any().any():
        raise ValueError("Nonempty edges and nonblank endpoint names required")
    if n[["side", "node"]].isna().any().any() or n.duplicated(["side", "node"]).any():
        raise ValueError("Node names must be present and unique within each side")
    if e.duplicated(["source", "destination"]).any():
        raise ValueError("One row per source-destination pair is required")
    if not n.side.isin(["source", "destination"]).all():
        raise ValueError("side must be source or destination")
    if "label_zh" in n and n.label_zh.isna().any():
        raise ValueError("label_zh must be complete when supplied")
    for frame, col in ((e, "amount_usd_billion"), (n, "total_usd_billion")):
        frame[col] = pd.to_numeric(frame[col], errors="raise")
        if frame[col].isna().any() or not np.isfinite(frame[col].to_numpy(dtype=float)).all():
            raise ValueError(f"{col} must be finite")
        if (frame[col] < 0).any():
            raise ValueError(f"{col} must be nonnegative")
    sources = n.loc[n.side.eq("source"), "node"].tolist()
    destinations = n.loc[n.side.eq("destination"), "node"].tolist()
    if not sources or not destinations:
        raise ValueError("Both node sides are required")
    if not set(e.source).issubset(sources) or not set(e.destination).issubset(destinations):
        raise ValueError("Every edge endpoint needs a declared node")
    if e.amount_usd_billion.sum() <= 0:
        raise ValueError("At least one flow must be positive")
    rows = []
    for row in n.itertuples(index=False):
        selected = e.source.eq(row.node) if row.side == "source" else e.destination.eq(row.node)
        actual = float(e.loc[selected, "amount_usd_billion"].sum())
        expected = float(row.total_usd_billion)
        difference = actual - expected
        if not np.isclose(actual, expected, rtol=1e-10, atol=1e-9):
            raise ValueError(f"Unmatched balance at {row.side}:{row.node}: declared {expected}, edges {actual}")
        rows.append((row.side, row.node, expected, actual, difference))
    check = pd.DataFrame(rows, columns=["side", "node", "declared_total_usd_billion",
                                        "edge_total_usd_billion", "difference_usd_billion"])
    left = n.loc[n.side.eq("source"), "total_usd_billion"].sum()
    right = n.loc[n.side.eq("destination"), "total_usd_billion"].sum()
    if not np.isclose(left, right, rtol=1e-10, atol=1e-9):
        raise ValueError("Source and destination totals must agree")
    e["source"] = pd.Categorical(e.source, categories=sources, ordered=True)
    e["destination"] = pd.Categorical(e.destination, categories=destinations, ordered=True)
    e = e.sort_values(["source", "destination"], kind="stable").reset_index(drop=True)
    return e, n, check


def chinese_font() -> str:
    names = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in ("Microsoft YaHei", "SimHei", "Noto Sans CJK SC",
                      "Source Han Sans SC", "Arial Unicode MS"):
        if candidate in names:
            return candidate
    raise RuntimeError("No installed Chinese font found")


def node_bands(n: pd.DataFrame, side: str, gap: float) -> dict[str, tuple[float, float]]:
    """Top-down node intervals in the same quantitative y unit as each edge."""
    pos = 0.0
    bands = {}
    part = n.loc[n.side.eq(side)]
    for row in part.itertuples(index=False):
        bands[row.node] = (pos, pos + float(row.total_usd_billion))
        pos += float(row.total_usd_billion) + gap
    return bands


def ribbon(x0: float, x1: float, left: tuple[float, float],
           right: tuple[float, float], color: str) -> PathPatch:
    a, b = left
    c, d = right
    dx = (x1 - x0) * 0.5
    vertices = [(x0, a), (x0 + dx, a), (x1 - dx, c), (x1, c),
                (x1, d), (x1 - dx, d), (x0 + dx, b), (x0, b), (x0, a)]
    codes = [MplPath.MOVETO, MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4,
             MplPath.LINETO, MplPath.CURVE4, MplPath.CURVE4, MplPath.CURVE4,
             MplPath.CLOSEPOLY]
    return PathPatch(MplPath(vertices, codes), facecolor=color, edgecolor="none", alpha=0.66)


def render(e: pd.DataFrame, n: pd.DataFrame, out: Path,
           language: str, title: str | None) -> None:
    if language == "zh":
        plt.rcParams["font.family"] = chinese_font()
        plt.rcParams["axes.unicode_minus"] = False
        left_heading, right_heading = "避税地注册地", "最终归属国家"
    else:
        plt.rcParams["font.family"] = "DejaVu Sans"
        left_heading, right_heading = "Tax-haven affiliate", "Ultimate country"
    total = float(e.amount_usd_billion.sum())
    gap = max(total * 0.023, 1.5)
    source = node_bands(n, "source", gap)
    destination = node_bands(n, "destination", gap)
    max_source = max(high for _, high in source.values())
    max_destination = max(high for _, high in destination.values())
    height = max(max_source, max_destination) + gap * 1.4
    fig, ax = plt.subplots(figsize=(10.2, 7.1))
    color_map = {name: COLORS[i % len(COLORS)] for i, name in
                 enumerate(n.loc[n.side.eq("destination"), "node"])}
    source_cursor = {name: low for name, (low, _) in source.items()}
    destination_cursor = {name: low for name, (low, _) in destination.items()}
    # Edges sorted by declared node order, so stacking is reproducible. All
    # vertical spans equal the input amount; zero edges have no ribbon.
    for row in e.itertuples(index=False):
        amount = float(row.amount_usd_billion)
        if amount == 0:
            continue
        s, d = str(row.source), str(row.destination)
        sl = (source_cursor[s], source_cursor[s] + amount)
        dl = (destination_cursor[d], destination_cursor[d] + amount)
        ax.add_patch(ribbon(0.27, 0.73, sl, dl, color_map[d]))
        source_cursor[s] += amount
        destination_cursor[d] += amount
    for side, bands, x0, x1, text_x, align in (
        ("source", source, 0.22, 0.27, 0.205, "right"),
        ("destination", destination, 0.73, 0.78, 0.795, "left"),
    ):
        part = n.loc[n.side.eq(side)]
        for row in part.itertuples(index=False):
            low, high = bands[row.node]
            if high > low:
                ax.add_patch(Rectangle((x0, low), x1-x0, high-low,
                                       facecolor="#F1F1F1", edgecolor="#B6B6B6",
                                       linewidth=0.7, zorder=5))
            label = row.label_zh if language == "zh" and "label_zh" in n else row.node
            value = f"{row.total_usd_billion:g}"
            amount_label = f"${value}B" if language == "en" else f"{value}十亿美元"
            ax.text(text_x, (low + high) / 2, f"{label}\n{amount_label}",
                    ha=align, va="center", fontsize=9.2, color="#303030")
    ax.text(0.245, -gap * 0.35, left_heading, ha="center", va="bottom", fontsize=10)
    ax.text(0.755, -gap * 0.35, right_heading, ha="center", va="bottom", fontsize=10)
    ax.set_xlim(0, 1)
    ax.set_ylim(height, -gap * 0.7)
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=12, pad=10)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.91 if title else 0.97, bottom=0.03)
    for extension in ("png", "pdf"):
        fig.savefig(out / f"bilateral_flow_sankey_{language}.{extension}",
                    dpi=300, facecolor="white")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--flows", type=Path, help="Positive/zero bilateral flows CSV")
    parser.add_argument("--nodes", type=Path, help="Declared source/destination totals CSV")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "figures")
    parser.add_argument("--title-en", help="Optional English title")
    parser.add_argument("--title-zh", help="Optional Chinese title")
    parser.add_argument("--lang", choices=("en", "zh"), default="en")
    args = parser.parse_args()
    if (args.flows is None) != (args.nodes is None):
        parser.error("Supply both --flows and --nodes, or neither for the synthetic demo")
    args.output.mkdir(parents=True, exist_ok=True)
    if args.flows:
        edges, nodes = pd.read_csv(args.flows), pd.read_csv(args.nodes)
        status = "user-supplied bilateral amounts"
    else:
        edges, nodes = make_demo()
        edges.to_csv(args.output / "demo_flows.csv", index=False)
        nodes.to_csv(args.output / "demo_nodes.csv", index=False)
        status = "synthetic bilateral amounts"
    edges, nodes, check = validate(edges, nodes)
    check.to_csv(args.output / "flow_balance_checks.csv", index=False)
    render(edges, nodes, args.output, args.lang, args.title_en if args.lang == "en" else args.title_zh)
    print(f"Input status: {status}; total USD billions: {edges.amount_usd_billion.sum():g}")
    print(f"Edges: {len(edges)} ({int((edges.amount_usd_billion == 0).sum())} zero); node checks: {len(check)}")
    print("BILATERAL_FLOW_SANKEY_COMPLETE")


if __name__ == "__main__":
    main()
