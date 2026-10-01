# Externally constructed joint-region inputs

[English](schema.md) · [中文](schema.zh-CN.md)

Grid CSV columns: `x_center,y_center,x_lo,x_hi,y_lo,y_hi,in90,in95,in99`. One cell per Cartesian grid position. Bounds must make a complete, regular rectangular grid with equal, positive cell widths and heights and unique centers. Membership flags are 0/1 and must satisfy `in90 <= in95 <= in99` in every cell. A zero in all flags means outside the displayed joint regions. The flags are supplied by upstream joint inference and are **not** computed from marginal intervals or a parametric shape here.

Point CSV: exactly one row, columns `x,y`, finite numbers. Axis variables follow the source: x = EP(-10%) - EP(-30%); y = EP(-30%). A black reference line is the set `x+y=0.5` within the plotted domain. The checked output includes `region` equal to 90, 95, 99, or 0 for exclusive display shading. If any 99% cell lies on an outer grid edge, the Python command warns and logs `region_hits_boundary=true`; extend the supplied grid or disclose the truncation. The example grid has no boundary hit.
