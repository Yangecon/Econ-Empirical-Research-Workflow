# Input contract

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV in any column order with `panel,kind,x,y,count,reference_label`. This edition requires `panel` IDs `r1` and `r200`; at least one positive-frequency bubble in each. `kind=bubble` rows require a nonnegative integer `count` (including zero), a blank reference label, and unique `(panel,x,y)`. `kind=benchmark` rows require blank count and a configured `reference_label` ID (`bayesian` or `perfect_brn`); both scripts map these IDs to English or Chinese display text. Coordinates are finite and within 0–100 in the source-style percentage setting. Configure both scripts' axis labels and bounds for other scales. Missing combinations need no row; explicit zero counts are allowed and retained, but not plotted.

One bubble represents the **joint number of people** at the displayed `x,y` pair. The source rounds individual beliefs to multiples of three before counting; that preparation is upstream. `x` is the belief conditional on a negative signal and `y` the belief conditional on a positive signal, both percentages. The two panels represent round 1 and round 200. Benchmark rows are interpretive reference coordinates; synthetic demo values are not taken as article estimates.

For count `n`, the bubble diameter is `27 sqrt(n/max_count)` printer points, so area divided by the maximum bubble area is `n/max_count`. The same `max_count` is computed across panels. Stata prints diameters to eight decimal places, creating only negligible rounding error. The checked CSV includes `bubble_area_ratio` for audit; benchmark rows leave it blank.
