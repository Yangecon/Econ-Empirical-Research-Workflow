# Input schema

[English](schema.md) · [中文](schema.zh-CN.md)

Values CSV: `shapeID` (unique nonblank string matching an ID in the GeoJSON), `value` (finite numeric or empty for no data). Missing region rows are permitted and rendered as no data; unknown IDs and duplicate IDs are errors. All observed values must lie inside the explicitly supplied finite, 1D, strictly increasing `--bins` edges, of which at least three are required.

Geometry: GeoJSON FeatureCollection with `crs.properties.name = urn:ogc:def:crs:OGC:1.3:CRS84`. Every feature must have a unique nonblank `properties.shapeID` and a Polygon or MultiPolygon geometry. Coordinates must be finite longitude/latitude within ±180°/±90°. The local display approximation rejects coordinates beyond ±75° latitude and any feature with longitude span above 180°; antimeridian crossing is unsupported. Closed exterior and hole rings are supported. The provided geometry has 10 modern Cameroon ADM1 regions (2016), which have a different unit and historical period from the AER Figure 2 source.
