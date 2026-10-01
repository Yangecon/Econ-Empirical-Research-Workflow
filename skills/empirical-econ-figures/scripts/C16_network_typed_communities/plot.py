"""F44: typed, explicitly listed ties over an exam-group node layout."""
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
from matplotlib.lines import Line2D
from matplotlib.patches import Circle

STYLES = {"blood": "-.", "provincial_exam": ":", "national_exam": "-"}
_fonts = {font.name for font in font_manager.fontManager.ttflist}
plt.rcParams["font.family"] = next((name for name in
    ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "DejaVu Sans"] if name in _fonts), "DejaVu Sans")
plt.rcParams["axes.unicode_minus"] = False


def prepare(nodes: pd.DataFrame, edges: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    req_nodes = {"id", "label", "region", "exam_group", "label_show"}
    req_edges = {"source", "target", "type", "directed"}
    if m := req_nodes - set(nodes):
        raise ValueError(f"Missing node columns: {sorted(m)}")
    if m := req_edges - set(edges):
        raise ValueError(f"Missing edge columns: {sorted(m)}")
    if nodes.empty or edges.empty:
        raise ValueError("Need at least one node and one listed edge")
    n, e = nodes.copy(), edges.copy()
    for field in ["id", "label", "region", "exam_group"]:
        if n[field].isna().any() or n[field].astype(str).str.strip().eq("").any():
            raise ValueError(f"Blank node {field}")
        n[field] = n[field].astype(str).str.strip()
    for field in ["source", "target", "type"]:
        if e[field].isna().any() or e[field].astype(str).str.strip().eq("").any():
            raise ValueError(f"Blank edge {field}")
        e[field] = e[field].astype(str).str.strip()
    if n.id.duplicated().any():
        raise ValueError("Node IDs must be unique")
    regions = sorted(n.region.unique())
    if len(regions) > 2:
        raise ValueError("This black/white renderer supports at most two region values")
    n.label_show = pd.to_numeric(n.label_show, errors="coerce")
    e.directed = pd.to_numeric(e.directed, errors="coerce")
    if not n.label_show.isin([0, 1]).all() or not e.directed.isin([0, 1]).all():
        raise ValueError("label_show and directed must be 0/1")
    if not e.source.isin(n.id).all() or not e.target.isin(n.id).all():
        raise ValueError("Every edge endpoint needs a listed node")
    if not e.type.isin(STYLES).all() or (e.source == e.target).any():
        raise ValueError("Unknown edge type or self-loop")
    keys = []
    for row in e.itertuples(index=False):
        pair = (row.source, row.target) if row.directed else tuple(sorted([row.source, row.target]))
        keys.append((pair, row.type, int(row.directed)))
    if len(set(keys)) != len(keys):
        raise ValueError("Duplicate typed edge (including reversed undirected tie)")
    coords = {"x", "y"}.issubset(n)
    if ("x" in n) != ("y" in n):
        raise ValueError("Provide both x and y, or neither")
    if coords:
        for field in ["x", "y"]:
            n[field] = pd.to_numeric(n[field], errors="coerce")
            if not np.isfinite(n[field].to_numpy()).all():
                raise ValueError("Coordinates must be finite")
    else:
        # Stable schematic exam-group placement; never interpreted as geography.
        groups = sorted(n.exam_group.unique())
        center_angles = np.linspace(0, 2*np.pi, len(groups), endpoint=False)
        centers = {group: (3*np.cos(angle), 2.2*np.sin(angle))
                   for group, angle in zip(groups, center_angles)}
        n["x"], n["y"] = 0.0, 0.0
        for group, subset in n.groupby("exam_group"):
            ids = sorted(subset.id)
            angles = np.linspace(0, 2*np.pi, len(ids), endpoint=False)
            cx, cy = centers[group]
            for node_id, angle in zip(ids, angles):
                at = n.id == node_id
                n.loc[at, "x"] = cx + .42*np.cos(angle)
                n.loc[at, "y"] = cy + .42*np.sin(angle)
    return n, e


def render(nodes: pd.DataFrame, edges: pd.DataFrame, prefix: Path,
           title: str | None) -> None:
    fig, ax = plt.subplots(figsize=(9, 6.8))
    positions = nodes.set_index("id")[["x", "y"]]
    # Group rings encode membership only; no unlisted within-group ties are drawn.
    for group, subset in nodes.groupby("exam_group", sort=True):
        cx, cy = subset[["x", "y"]].mean()
        radius = max(0.48, np.sqrt(((subset.x-cx)**2 + (subset.y-cy)**2).max()) + .22)
        ax.add_patch(Circle((cx, cy), radius, facecolor="#F4F4F4",
                            edgecolor="#BBBBBB", linewidth=1, zorder=0))
        ax.text(cx, cy+radius+.08, str(group), ha="center", va="bottom",
                fontsize=9, color="#555555")
    for row in edges.itertuples(index=False):
        x1, y1 = positions.loc[row.source]
        x2, y2 = positions.loc[row.target]
        if row.directed:
            ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops={"arrowstyle": "->", "color": "#555555", "lw": 1.1,
                            "linestyle": STYLES[row.type], "shrinkA": 6, "shrinkB": 6}, zorder=1)
        else:
            ax.plot([x1, x2], [y1, y2], linestyle=STYLES[row.type],
                    color="#555555", linewidth=1.1, zorder=1)
    regions = sorted(nodes.region.unique())
    for i, region in enumerate(regions):
        subset = nodes[nodes.region == region]
        ax.scatter(subset.x, subset.y, s=55, facecolor="black" if i == 0 else "white",
                   edgecolor="black", linewidth=.8, zorder=2, label=region)
    for row in nodes[nodes.label_show == 1].itertuples(index=False):
        ax.annotate(row.label, (row.x, row.y), xytext=(5, 5),
                    textcoords="offset points", fontsize=9, zorder=3)
    edge_handles = [Line2D([], [], linestyle=style, color="#555555", label=kind.replace("_", " "))
                    for kind, style in STYLES.items() if kind in set(edges.type)]
    region_handles = [Line2D([], [], linestyle="", marker="o", markerfacecolor="black" if i == 0 else "white",
                    markeredgecolor="black", label=region) for i, region in enumerate(regions)]
    ax.legend(handles=edge_handles+region_handles, loc="upper left", bbox_to_anchor=(1.01, 1),
              frameon=False, fontsize=9)
    ax.set_aspect("equal", adjustable="datalim")
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=13)
    fig.tight_layout()
    prefix.parent.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "pdf"):
        fig.savefig(prefix.with_suffix("."+ext), dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--nodes", type=Path, required=True)
    ap.add_argument("--edges", type=Path, required=True)
    ap.add_argument("--output-prefix", type=Path, required=True)
    ap.add_argument("--title")
    a = ap.parse_args()
    nodes, edges = prepare(pd.read_csv(a.nodes, dtype={"id": str}),
                           pd.read_csv(a.edges, dtype={"source": str, "target": str}))
    render(nodes, edges, a.output_prefix, a.title)
    nodes.to_csv(a.output_prefix.with_name(a.output_prefix.name+"_nodes_checked.csv"), index=False)
    edges.to_csv(a.output_prefix.with_name(a.output_prefix.name+"_edges_checked.csv"), index=False)
    print(json.dumps({"status": "OK", "nodes": len(nodes), "listed_edges": len(edges),
                      "output": str(a.output_prefix)}))


if __name__ == "__main__":
    main()
