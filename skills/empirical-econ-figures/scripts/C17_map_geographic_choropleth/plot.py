"""F45: real Cameroon ADM1 GeoJSON boundaries with externally supplied region values."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import BoundaryNorm
from matplotlib.patches import PathPatch, Patch
from matplotlib.path import Path as MplPath
import numpy as np
import pandas as pd


def configure_font():
    names = {f.name for f in font_manager.fontManager.ttflist}
    for name in ("Noto Sans CJK SC", "Microsoft YaHei", "SimHei", "Arial Unicode MS"):
        if name in names:
            plt.rcParams["font.sans-serif"] = [name, "DejaVu Sans"]
            break
    plt.rcParams["axes.unicode_minus"] = False


def load_geometry(path):
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    if obj.get("type") != "FeatureCollection":
        raise ValueError("Geometry must be a GeoJSON FeatureCollection")
    crs = obj.get("crs", {}).get("properties", {}).get("name", "")
    if crs != "urn:ogc:def:crs:OGC:1.3:CRS84":
        raise ValueError("Expected CRS84 longitude-latitude boundary coordinates")
    features = obj.get("features", [])
    ids = [f.get("properties", {}).get("shapeID") for f in features]
    if not features or any(not x for x in ids) or len(set(ids)) != len(ids):
        raise ValueError("Boundary shapeID values must be present and unique")
    for f in features:
        if f.get("geometry", {}).get("type") not in ("Polygon", "MultiPolygon"):
            raise ValueError("Only Polygon and MultiPolygon geometries are supported")
        geom = f["geometry"]
        polygons = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
        coords = np.asarray([pt[:2] for polygon in polygons for ring in polygon for pt in ring], dtype=float)
        if coords.ndim != 2 or coords.shape[1] != 2 or not np.isfinite(coords).all():
            raise ValueError("Geometry coordinates must be finite longitude-latitude pairs")
        if (np.abs(coords[:, 0]) > 180).any() or (np.abs(coords[:, 1]) > 90).any():
            raise ValueError("CRS84 longitude/latitude outside [-180,180] / [-90,90]")
        if (np.abs(coords[:, 1]) > 75).any() or np.ptp(coords[:, 0]) > 180:
            raise ValueError("Local display projection excludes polar and antimeridian-spanning geometries")
    return features


def prepare(features, values, edges):
    edges = np.asarray(edges, dtype=float)
    if edges.ndim != 1 or len(edges) < 3 or not np.isfinite(edges).all() or not np.all(np.diff(edges) > 0):
        raise ValueError("Bins must be finite, 1D, and strictly increasing")
    if not {"shapeID", "value"}.issubset(values.columns):
        raise ValueError("Values CSV needs shapeID and value")
    frame = values[["shapeID", "value"]].copy()
    if frame.shapeID.isna().any() or frame.shapeID.astype(str).str.strip().eq("").any() or frame.shapeID.duplicated().any():
        raise ValueError("Values shapeID must be nonblank and unique")
    frame["value"] = pd.to_numeric(frame.value, errors="raise")
    if not np.isfinite(frame.value.dropna()).all():
        raise ValueError("Nonmissing values must be finite")
    geom_ids = {f["properties"]["shapeID"] for f in features}
    unknown = set(frame.shapeID) - geom_ids
    if unknown:
        raise ValueError(f"Values contain unknown shapeID: {sorted(unknown)}")
    valid = frame.value.dropna()
    if ((valid < edges[0]) | (valid > edges[-1])).any():
        raise ValueError("Supplied values fall outside the common bin range")
    output = pd.DataFrame({"shapeID": [f["properties"]["shapeID"] for f in features],
                           "shapeName": [f["properties"].get("shapeName", "") for f in features]})
    output = output.merge(frame, on="shapeID", how="left", validate="one_to_one")
    output["bin_index"] = pd.cut(output.value, bins=edges, labels=False, include_lowest=True, right=True)
    return output, edges


def _signed_area(points):
    xy = np.asarray(points, dtype=float)
    return float(np.sum(xy[:-1, 0] * xy[1:, 1] - xy[1:, 0] * xy[:-1, 1]) / 2)


def polygon_path(geometry, cos_lat):
    polygons = [geometry["coordinates"]] if geometry["type"] == "Polygon" else geometry["coordinates"]
    vertices, codes = [], []
    for polygon in polygons:
        for ring_index, ring in enumerate(polygon):
            xy = np.asarray(ring, dtype=float)
            if xy.ndim != 2 or xy.shape[1] < 2 or len(xy) < 4 or not np.isfinite(xy[:, :2]).all():
                raise ValueError("Invalid polygon ring")
            xy = xy[:, :2].copy()
            if not np.allclose(xy[0], xy[-1]):
                raise ValueError("Polygon rings must close")
            xy[:, 0] *= cos_lat
            # Opposite windings make holes empty under Matplotlib's nonzero fill rule.
            area = _signed_area(xy)
            if abs(area) < 1e-12:
                raise ValueError("Degenerate polygon ring")
            if (ring_index == 0 and area < 0) or (ring_index > 0 and area > 0):
                xy = xy[::-1]
            vertices.extend(xy)
            codes.extend([MplPath.MOVETO] + [MplPath.LINETO] * (len(xy) - 2) + [MplPath.CLOSEPOLY])
    return MplPath(np.asarray(vertices), np.asarray(codes))


def render(features, checked, edges, output, legend_title, title):
    configure_font()
    lats = []
    for f in features:
        polys = [f["geometry"]["coordinates"]] if f["geometry"]["type"] == "Polygon" else f["geometry"]["coordinates"]
        lats.extend(float(pt[1]) for poly in polys for ring in poly for pt in ring)
    ref_lat = (min(lats) + max(lats)) / 2
    cos_lat = float(np.cos(np.deg2rad(ref_lat)))
    cmap = plt.get_cmap("YlOrBr", len(edges) - 1)
    fig, ax = plt.subplots(figsize=(8.1, 7.6))
    lookup = checked.set_index("shapeID")
    for f in features:
        ident = f["properties"]["shapeID"]
        row = lookup.loc[ident]
        missing = pd.isna(row.value)
        face = "#E8EBEE" if missing else cmap(int(row.bin_index))
        patch = PathPatch(polygon_path(f["geometry"], cos_lat), facecolor=face,
                          edgecolor="#39434D", lw=.8, hatch="///" if missing else None)
        ax.add_patch(patch)
    ax.autoscale_view()
    ax.set_aspect("equal", adjustable="datalim")
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=13)
    handles = []
    for i in range(len(edges) - 1):
        label = f"[{edges[i]:g}, {edges[i+1]:g}]" if i == 0 else f"({edges[i]:g}, {edges[i+1]:g}]"
        handles.append(Patch(facecolor=cmap(i), edgecolor="#39434D", label=label))
    if checked.value.isna().any():
        handles.append(Patch(facecolor="#E8EBEE", edgecolor="#39434D", hatch="///", label="No data"))
    ax.legend(handles=handles, title=legend_title, frameon=False, loc="lower left",
              bbox_to_anchor=(.01, .02), fontsize=9, title_fontsize=10)
    fig.tight_layout()
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return ref_lat


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("values", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--geometry", type=Path, default=Path(__file__).with_name("cameroon_adm1.geojson"))
    p.add_argument("--bins", nargs="+", type=float, required=True)
    p.add_argument("--legend-title", default="Value")
    p.add_argument("--title", default="")
    a = p.parse_args()
    features = load_geometry(a.geometry)
    checked, edges = prepare(features, pd.read_csv(a.values, dtype={"shapeID": str}), a.bins)
    ref_lat = render(features, checked, edges, a.output, a.legend_title, a.title)
    checked.to_csv(a.output.with_name(a.output.stem + "_checked.csv"), index=False)
    summary = {"status": "ok", "geometry_features": len(features), "joined_values": int(checked.value.notna().sum()),
               "missing_values": int(checked.value.isna().sum()), "bins": edges.tolist(), "crs": "OGC:CRS84",
               "display": f"local equirectangular x=longitude*cos({ref_lat:.4f} degrees), y=latitude"}
    a.output.with_name(a.output.stem + "_validation.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
