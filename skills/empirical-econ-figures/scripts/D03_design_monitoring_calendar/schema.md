# Input schema and checks

[English](schema.md) · [中文](schema.zh-CN.md)

Required CLI: `--year` and `--output-prefix`. Choose exactly one schedule source: `--schedule` with CSV columns `date,schedule`, or `--anchor-3` and/or `--anchor-6`. Schedule values must be `3_day` or `6_day`; dates and anchors are exact ISO `YYYY-MM-DD`. Anchors set a calendar-day sequence by `(date - anchor).days mod 3/6 == 0` across the requested year. No weekday periodicity is inferred. The source's 1-in-6 schedule can be a subset of 1-in-3 when anchors align; this is not assumed for arbitrary supplied dates.

Optional `--observed` CSV has the same `date,schedule` columns. Observed dates may be off schedule and remain separately marked. Duplicate date-schedule rows, dates outside the requested year, unknown schedule types, invalid dates, absent schedule sources, and conflicting file/anchor sources are rejected. Calendar days derive from the standard Gregorian calendar, including leap day.
