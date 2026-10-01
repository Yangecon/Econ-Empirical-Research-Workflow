# Count input and proportion definition

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV with one unique row for each configured `category × group` pair. Required fields: `category`, `group`, `numerator`, and `denominator`. Category and group IDs, order, bilingual labels, and bar treatment are configured near the top of `plot.py`; this paired-bar layout requires **exactly two groups**, and the complete Cartesian set must appear exactly once. Counts are finite integers, with `denominator > 0` and `0 <= numerator <= denominator` in each row. `proportion = numerator / denominator` is calculated independently for each category-group cell; the denominator is **that cell's eligible observation count**, not a pooled count across groups. The `_rates.csv` sidecar preserves numerator, denominator, and computed proportion.

The horizontal scale starts at zero. Bars are descriptive cell proportions; the script does not calculate standard errors, tests, treatment effects, adjusted attendance rates, or a causal contrast. Category ordering is the configured order, never alphabetical or sorted by bar height. The black and outline styles distinguish the two groups in grayscale.
