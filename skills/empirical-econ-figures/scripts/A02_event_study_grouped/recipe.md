# A02 · Grouped event study

[English](recipe.md) · [中文](recipe.zh-CN.md)

`grouped_event_study` · A02

Offset coefficients and confidence intervals for multiple groups, with filled/hollow significance markers and actual event-time spacing.

Classification: Offset coefficients and confidence intervals for multiple groups, with filled/hollow significance markers and actual event-time spacing.

Tags: Event study, DID-compatible display, Heterogeneity

## Sources and scope

Local reference; original paper unidentified; Figure A3

Supplemental analogue: [English Language Requirement and Educational Inequality: Evidence from 16 Million College Applicants in China](<https://doi.org/10.3386/w32162>); Figure 1; PDF p.24

The screenshot shows Figure A3; paper identity awaits verification against the primary materials.

NBER Figure 1 concerns English listening requirements and exam outcomes, with three panels and an interaction-weighted estimator. The screenshot concerns Broadband China and political trust by urban/rural hukou, with one panel and red/green offset estimates. They are separate studies; the NBER paper does not establish provenance of the screenshot.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

Read the explicit input checks at the top of the code.

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run inside this template directory and set the output to your project directory:

```shell
python grouped_event_study.py --input demo_estimates.csv --output-dir YOUR_PROJECT/figures
```

In Stata, load the program first, then call it:

```stata
do "PATH_TO_TEMPLATE/grouped_event_study.do"
grouped_event_study, input("PATH_TO_TEMPLATE/demo_estimates.csv") output("YOUR_PROJECT/figures/grouped_event_study") reference(-1) level(95) language(en)
```

Python `--title "..."` or Stata `title("...")` enables a title; none is drawn by default. Actual inputs may use se or paired ci_low/ci_high; ensure that level matches externally supplied intervals.

The normalized reference at event time −1 is displayed as a hollow circle with no confidence interval. It is not an estimated effect and is excluded from pre/post averages.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Python 3.12 and Stata 19 were executed and visually checked. The main example has 26 estimates, two groups and 14 intervals excluding zero. Tests also covered reordered columns, three groups, irregular event times and explicit intervals. Chinese Python figures were inspected; Chinese Stata figures were not separately inspected.

Canonical figure name: `event_study_grouped`
