# Input contract

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV, five finite numeric columns in any column order: `horizon`, `admissible_low`, `admissible_high`, `pointwise_median`, `maxg_response`. At least three strictly increasing, unique, nonnegative numerical horizons are required. Bounds must satisfy `admissible_low <= admissible_high` at each horizon, and both supplied summary curves must lie within them. Any valid numerical horizon grid is allowed; the points are connected in input horizon order. The source uses quarters 1–15, with the shock in period 1. If another data set uses a different time origin, change the x-axis label accordingly. `demo.csv` is deterministic synthetic data and does not match article values.

`admissible_low`/`admissible_high` are extrema of the admissible response **set at each horizon**, not 95% confidence limits. `pointwise_median` is taken separately at each horizon; its connected line is a visual summary, not necessarily one jointly admissible candidate path. `maxg_response` is one given path associated with a selected admissible solution and is not found by maximizing anything here. Its consistency with event restrictions must be certified upstream. Values should be in the same outcome unit, e.g. GDP growth response in percentage points of year-on-year growth.
