# Input schema and interpretation

[English](schema.md) · [中文](schema.zh-CN.md)

The input CSV has one row per displayed country or category, in the exact desired **top-to-bottom order**. Required columns are `category`, `actual_pct`, and `perceived_pct`. `category_zh` is an optional complete Chinese label; without it, the Chinese figure uses `category` unchanged. Categories must be unique and nonblank.

All numeric inputs use **percentage units on a 0–100 scale**, not fractions: `12` means 12%, not 0.12. Actual and perceived values must be finite and within that range. Perceived may be lower than, equal to, or higher than actual. The output adds `gap_pct_points = perceived_pct - actual_pct`; a negative value means underestimation. The script draws the two supplied values and the segment connecting them. It never sorts by either value.

Optional confidence-interval columns are `perceived_ci_low_pct` and `perceived_ci_high_pct`. Supply **both columns with finite values for every row, or neither column**. These columns should contain externally computed 95% confidence limits; the code can check their bounds and whether they contain the mean, but cannot verify their coverage level. Partial intervals and an interval that does not contain its perceived mean are rejected. The shaded interval applies **only to the perceived mean**; no interval is drawn for actual. The script does not derive an SE or re-estimate an interval.

The supplied [`figures/demo_values.csv`](figures/demo_values.csv) contains six invented examples. Sweden has a negative gap and France has a zero gap to check line direction and coincident markers. None of its values are the source paper's estimates.
