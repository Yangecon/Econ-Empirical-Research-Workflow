# C12 CSV schema

[English](schema.md) · [中文](schema.zh-CN.md)

Trend CSV: `date` (parseable calendar date, or numeric four-digit year interpreted as January 1), `series` (nonblank legend text), `value` (finite numeric, blank permitted to make an explicit line break; malformed nonblank values rejected). One row per series-date. Dates are sorted by the adapter; spacing follows elapsed calendar time. Include explicit blank rows at unobserved periods when a visible gap is required. No normalization or real-wage deflation is performed.

Event CSV: `date`, `label`, with each dated event inside the trend span. Events are shown as thin vertical reference rules and labels; supply only source-verified event timing. `--events` is optional.
