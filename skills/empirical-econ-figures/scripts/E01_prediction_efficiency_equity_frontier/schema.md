# Input and policy-path semantics

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 long CSV with `algorithm`, `policy_rate`, `efficiency`, `disparity`, `ci_low`, `ci_high`, and `operating`. Edit the four algorithm IDs, labels and colors near the top of **both** plotting scripts when adapting. Exactly one additional `status_quo` row supplies the baseline x/y location. For that row, CI fields are blank and `operating=0`. For each algorithm, at least two unique nonnegative policy rates are required, with exactly one `operating=1` row. Efficiency must be nonnegative and **strictly increase with policy rate** for each algorithm, so the supplied y-confidence bands form valid x-ordered polygons. Disparity can be signed; every algorithm estimate must lie within complete finite supplied CI bounds. The reference row is not treated as part of any policy curve.

Each curve is connected in ascending **policy rate** order, never chosen by outcome or disparity. The x axis is supplied efficiency; the y axis is supplied disparity in percentage points. The CI band is for disparity at each supplied policy rate and is drawn as supplied. The scripts do not calculate confidence intervals, bootstrap draws, optimal policies, Pareto dominance, or a mathematical efficiency frontier. The family name describes a comparison of policy paths; it does not assert that all plotted points are efficient. Marked operating points and the baseline cross are display annotations, not inferential claims.

The demo's 69 rows and CI widths are synthetic. No source data or numerical estimates are reproduced. No annualization, weighting, audit selection, or disparity estimator is performed in these scripts.
