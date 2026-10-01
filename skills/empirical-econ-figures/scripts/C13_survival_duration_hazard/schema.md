# C13 CSV schema

[English](schema.md) · [中文](schema.zh-CN.md)

Long CSV columns: `panel`, `series`, `duration`, `events`, `risk_set`. One row per panel-series-positive integer duration. `events` and `risk_set` are integer counts with `0 <= events <= risk_set` and `risk_set > 0`. The adapter sorts durations, rejects duplicate keys, and calculates `hazard = events / risk_set`. A missing duration stays an empty bar position; it is never assigned zero or interpolated. The renderer scales this fraction by 100 for the percentage axis.

Counts should refer to the same risk definition, event window, and population within each row. The adapter cannot verify upstream cohort entry, censoring, competing events, or whether successive risk sets follow a valid longitudinal sample. Document those choices with real data.
