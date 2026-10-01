# Monthly phase input

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV with one row per cohort. Column order is arbitrary.

| Column | Meaning |
| --- | --- |
| `cohort` | Unique nonempty cohort ID. |
| `cohort_order` | Display order, consecutive integers from 1. |
| `cohort_label_en`, `cohort_label_zh` | Bilingual row labels. |
| `n` | Positive integer count displayed beside the cohort. Define its population in your accompanying source note. |
| `status` | `policy` or `nonpolicy`. At most one `nonpolicy` summary row. |
| `transition_start`, `transition_end` | Required interval for policy rows, dates as `YYYY-MM-01`. |
| `enforcement_start`, `enforcement_end` | Optional pair for policy rows, same date format. |
| `termination_month` | Optional common month-start marker. All nonblank values must agree. |

Intervals are **half-open**: a start month is included and an end month is excluded. Thus transition `[2020-04-01, 2020-08-01)` covers April–July, and enforcement can begin in August without overlap. Policy rows require a nonempty transition interval; enforcement endpoints must both be supplied or both blank, with enforcement starting at or after transition ends. No phase may extend beyond a supplied termination month. A nonpolicy row must have no phase intervals. The script rejects inverted or overlapping ranges and dates other than the first day of a month. The displayed calendar is calculated from these parsed monthly dates. The plot makes no causal claim or statement about compliance within a phase.
