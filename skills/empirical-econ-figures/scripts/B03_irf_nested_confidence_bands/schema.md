# Supplied posterior-summary input

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV with one row per `response × shock × horizon`. Required columns: `response`, `shock`, nonnegative integer `horizon` in **months**, `median`, `lo68`, `hi68`, `lo90`, `hi90`. All cells must be present exactly once on the same horizon grid, with at least three horizons starting at zero. The currently configured demonstration has five response rows and five shock columns; edit their IDs, bilingual labels, units, and **response-specific y limits** in both plotting scripts for another study. Each row shares a y scale across its shocks, but different response rows can use different physical units and ranges.

Each input row must satisfy `lo90 <= lo68 <= median <= hi68 <= hi90`; all numbers are finite and the 90% bounds must fit the configured response-row limits. The plotting scripts draw the **supplied 90% posterior uncertainty region** in light blue, the **supplied 68% posterior region** in darker blue, and the median path in black. They do not estimate a VAR, calculate a posterior, or compute intervals from raw draws.

Optional small horizon markers make zero exclusion visible: a filled marker means the **outer supplied 90% posterior region excludes zero** (`lo90>0` or `hi90<0`); otherwise it is hollow. This is a display classification, not a frequentist test, p-value, or proof of an economic effect. Marker horizons are configurable; input estimates and bands remain continuous across all supplied horizons. Output `_checked.csv` records the derived `outer_excludes_zero` flag for every row.
