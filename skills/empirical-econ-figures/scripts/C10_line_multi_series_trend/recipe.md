# C10 · Multi-series time trends and base-year indices

[English](recipe.md) · [中文](recipe.zh-CN.md)

`multi_series_time_trend` · C10

Display multiple trends with actual annual or monthly spacing, break lines at missing periods, and optionally normalize each series to 100 at an explicit common date.

Classification: A synthetic demonstration exists, with short monthly-series date ticks and whitespace being corrected. Basic annual/monthly lines retain actual date spacing, missing periods, and explicit base-period normalization.

Tags: Time series, Trends, Base-year index

## Sources and scope

[Knowledge Spillovers and Corporate Investment in Scientific Research (2021)](<https://doi.org/10.1257/aer.20171742>); Figure 2; PDF p.5

The original page image and PDF caption have been checked; synthetic data demonstrate the drawing only.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run in this template directory:

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/trend.png --normalize-base 1980-01-01 --lang en
python plot.py --input qa_monthly.csv --output YOUR_PROJECT/figures/monthly_trend.png --frequency monthly --lang en
```

Omit `--normalize-base` to plot original input units. When enabled, each series is divided by its own positive observation at that date and multiplied by 100; another date cannot silently replace a missing base observation. `--lang zh` uses Chinese labels; only `--title` displays a title. Configure series IDs, text, and units at the top of the script.

Annual dates must be January 1 and monthly dates the first day of the month. Series/date keys cannot repeat. Observed inputs must be finite and nonnegative, with at least two periods per series. Internal missing periods are inserted as blank values to break lines, without interpolation. Observations are not extended before or after each series' observed span.

The paper first divides annual patents or papers by total sample sales and then normalizes those ratios. Sales denominators, paper sample conditions, and annual aggregation belong to upstream data construction; this template only optionally rebases and plots. Historical-event annotations are not yet implemented; not all richly annotated trend plots are claimed to be reproduced.

Shared drawing dependency: preserve this directory's relationship to sibling `_shared/line_geometry.py`; copy the shared module into the research project as well. Imports resolve relative to the script and permit execution from other working directories. The shared module only draws supplied lines or right-continuous steps; normalization, cumulative shares, fitted intervals, risk sets, and Greenwood intervals remain the responsibility of each adapter.

Use the supplied JSON to customize series/phases and axis units; omitting `--config` preserves the original example:

```shell
python plot.py --input custom_demo.csv --config custom_config.json --output YOUR_PROJECT/figures/custom.png --lang en
```

`--lang zh` uses Chinese labels and `--title` displays the configured title. This configuration extension is Python-only; any retained Stata entry point follows the original schema. C10 retains finite nonnegative values, date rules, and an explicit base period. C11 connects points in year order and must not reorder them by x.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

68 synthetic annual observations become 72 rows after inserting internal missing periods; both series equal 100 in base year 1980. Annual English/Chinese, original-unit mode, and short three-/six-month series were executed. Visual checks passed after correcting date ticks and right whitespace. Monthly-gap and missing-base-date rejection checks passed. After adopting shared line/step geometry, reruns from a different working directory reproduced accepted default coordinates within 1e-10; statistical adapters were retained and C13 bars were unchanged. External series/phase IDs, Chinese labels, and optional-title examples were executed; invalid values or phase/year ordering are rejected.

Canonical figure name: `line_multi_series_trend`
