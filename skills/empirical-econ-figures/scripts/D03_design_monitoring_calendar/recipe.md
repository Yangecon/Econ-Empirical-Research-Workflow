# D03 · Monitoring calendar

[English](recipe.md) · [中文](recipe.zh-CN.md)

`monitoring_calendar` · D03

Display monitoring schedules using complete dates and explicit cycle anchors, independently marking observed implementation and preserving cross-month continuity.

Classification: Daily institutional calendar: actual dates and weekday positions, with explicit monitoring dates or cycle anchors. Every three days is not every Wednesday. Distinguish planned schedules from implementation; this has lower implementation priority than main-results figures.

Tags: Monitoring schedule, Calendar, Institutional design

## Sources and scope

[Unwatched Pollution: The Effect of Intermittent Monitoring on Air Quality (2021)](<https://doi.org/10.1257/aer.20181346>); Figure 1; PDF p.6

The original page image and PDF caption have been checked; synthetic data demonstrate the drawing only.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run in this template directory:

```shell
python plot.py --year 2024 --anchor-3 2024-01-01 --anchor-6 2024-01-01 --observed demo_observed.csv --output-prefix YOUR_PROJECT/figures/monitoring_calendar
```

`--title "标题"` explicitly adds a title; titles and bottom notes are absent by default. See schema.md for input fields, exclusions, and interpretation. Outputs include PNG, PDF, and accounting CSV.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Verified leap year 2024, date positions, three-/six-day cycles across months, and separation of scheduled/observed monitoring. Python was executed and visually checked. Six-day borders and three-day fills encode schedules independently. All demonstration values and relationships are synthetic, not reproductions of the paper.

Canonical figure name: `design_monitoring_calendar`
