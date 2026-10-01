# Input schema

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV, one observation per row. Required header: `panel,group,rx,ry`.

| Column | Type | Meaning |
| --- | --- | --- |
| `panel` | string | ID matching one of the two configured panels; demo IDs `all_fields` and `computer_science` display as Sample A and Sample B |
| `group` | string | ID matching a configured group within that panel; inherited demo IDs `medicine`/`other` and `ai_late`/`ai_early`/`other` display as Group A/Other groups and Group A/Group B/Other groups |
| `rx` | finite number | Supplied residualized X, on the horizontal axis |
| `ry` | finite number | Supplied residualized Y, on the vertical axis |

Every listed panel/group combination must have at least one observation. Each panel must have at least three observations and varying `rx`. The dashed line is OLS of `ry` on a constant and `rx` using every observation drawn in that panel, including the gray background group. Group highlights do not change regression weights. The template does **not** residualize raw variables or infer a fixed-effects specification. If users prepare residuals upstream, they should residualize both variables on the same selected rows and controls, retain exactly that common sample in this CSV, and document the controls, missing-data rule, and weighting separately.
