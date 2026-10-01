# Data schema

[English](schema.md) · [中文](schema.zh-CN.md)

`synthetic_panel.dta`: 2,880 observations, one for each `id` (1–320) × `t` (1–9). `treated` denotes the 160 treated units, `k=t-5` is event time, `tau` is the generated treatment component, and `y` is the simulated outcome. `lead4`, `lead3`, `lead2`, and `lag0`–`lag4` are treated-by-event indicators. Event time -1 has no indicator and is the reference.

`event_study_coefficients.csv`: one row per included event time. `event_time` is integer relative to treatment start and `estimate` is the coefficient from the fixed-effects event study. The order is -4, -3, -2, 0, 1, 2, 3, 4. Omitted -1 is absent, not stored as an estimated zero.

`event_study_covariance.csv`: eight rows and eight numeric columns, in `lead4`, `lead3`, `lead2`, `lag0`, `lag1`, `lag2`, `lag3`, `lag4` order. `row_name` identifies the covariance row. Values are the full symmetric clustered covariance submatrix, not only standard errors.

`rm_intervals.csv` and `sd_intervals.csv`: ten rows each. `restriction` identifies `DeltaRM` or `DeltaSD`; `bound_M` is blank for the conventional `Original` row and numeric for nine restriction strengths; `ci_low` and `ci_high` are the lower and upper endpoints of the package's 95% interval. These are stored directly from `HonestEventStudy.CI` after each actual `honestdid` run. Blank means inapplicable, not zero.
