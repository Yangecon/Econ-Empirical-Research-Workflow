# Input CSV contract

[English](schema.md) · [中文](schema.zh-CN.md)

One row per `variant`–`panel`–`term`–`group` estimate. Column order does not matter. Both implementations import by header name.

| Column | Required | Meaning |
| --- | --- | --- |
| `variant` | yes | Selects one configured figure, such as `robustness` or `subgroup`. |
| `panel` | yes | Panel ID configured in the plotting script. |
| `panel_order` | yes | Consecutive 1–4 display order, consistent within panel. |
| `term` | yes | Category ID for a specification or outcome. |
| `term_order` | yes | Consecutive order starting at 1; never inferred alphabetically. |
| `term_label_en`, `term_label_zh` | yes | Axis category labels in each language. |
| `group` | yes | Group ID configured in the plotting script. |
| `group_order` | yes | Group order matching the configuration. |
| `estimate` | yes | Point estimate. |
| `ci_low`, `ci_high` | normally | Interval endpoints, in the same unit as the estimate. Must bracket the estimate. |
| `se` | fallback | When **both** interval endpoints are blank, compute `estimate ± 1.96 × se` in both implementations. The multiplier is configurable (`--ci-multiplier` in Python; edit the marked calculation in Stata). It is a normal critical-value approximation for the supplied SE, not a substitute for the paper's own interval rule. |

Each configured group must have one row for every ordered term in each panel. For a horizontal multi-panel figure, panels must share the same ordered terms so rows align. Panel axis limits are derived independently from that panel's intervals and zero. Panel titles and effect-axis unit labels are set separately in each script's configuration block. The visualization accepts estimates and intervals; it does not calculate the estimator, clustered standard errors, or sample sizes.
