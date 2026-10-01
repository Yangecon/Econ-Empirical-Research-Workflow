# Input CSV contract

[English](schema.md) · [中文](schema.zh-CN.md)

One row per observed or supplied point on a scenario/group CDF. UTF-8 CSV with these header names in any column order:

| Column | Meaning |
| --- | --- |
| `panel` | Configured scenario ID; demo: `forced_attention`, `no_switching_costs`. |
| `panel_order` | Explicit display order, 1 or 2. |
| `group` | Configured curve ID; demo: `low`, `medium`, `high` acuity. |
| `group_order` | Explicit legend order, 1–3. |
| `x_reduction` | Monetary reduction in overspending; can be negative. Edit the axis label when using another quantity or unit. |
| `cdf` | Cumulative share at `x_reduction`, from 0 to 1. |

Each of the six configured panel/group curves needs at least two points. Values must be finite; `x_reduction` must be unique within a curve; sorting by `x_reduction` must give a nondecreasing `cdf` within `[0,1]`. Curves need not reach exactly 0 or 1 at the supplied x endpoints because the displayed range may truncate the distribution's tails. Both implementations use these supplied CDF points directly and do not calculate a CDF from observations, estimate the counterfactual model, or interpret `cdf` as the probability of paying attention.
