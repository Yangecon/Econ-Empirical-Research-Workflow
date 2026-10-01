# Observation CSV contract

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV with column headers `id,rx,ry` in any order:

| Column | Meaning |
| --- | --- |
| `id` | Nonempty, unique text identifier. It breaks ties in `rx` lexically. |
| `rx` | Finite, already-residualized horizontal variable. |
| `ry` | Finite, already-residualized vertical variable. |

Both implementations use **every complete row** in the supplied CSV for both steps:

1. Fit unweighted OLS `ry = intercept + slope × rx + error` with an intercept on observations.
2. Sort observations by numeric `rx`, then text `id`. With sorted one-based rank `r`, sample size `N`, and chosen bin count `B`, assign `bin = floor((r−1) × B / N) + 1`. Compute the arithmetic mean of `rx` and `ry` in each bin and plot those means.

This rule yields exactly `B` nonempty bins when `2 ≤ B ≤ N`, with sizes differing by at most one. Tied `rx` values may cross a bin boundary according to the explicit `id` rule. The line is fitted to the **underlying observations**, never to the plotted bin means. `rx` must vary. This implementation does not residualize raw variables or derive an IV estimate. To reproduce a first-stage specification, prepare both residuals using the same common analysis sample and controls upstream, then document that process separately.
