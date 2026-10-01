# C04 · Grouped category-share bars

[English](recipe.md) · [中文](recipe.zh-CN.md)

`grouped_category_bars` · C04

Compare two groups' proportions in a configured category order, using cell-specific numerators and denominators, a zero baseline, and black-and-white fills.

Classification: A basic grouped-bar example: specify category order, groups, proportion denominators, and a zero baseline; use horizontal paired bars for long labels. The source describes attendance rates by lottery prize size and timing; bar-height differences do not directly establish causality.

Tags: Group comparison, Categorical shares, Bars

## Sources and scope

[Parental Resources and College Attendance: Evidence from Lottery Wins (2021)](<https://doi.org/10.1257/aer.20171272>); Figure 1; PDF p.13

The original page image and PDF caption have been checked; synthetic data demonstrate the drawing only.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run in this template directory:

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/grouped_bars.png --lang en
```

`--lang zh` switches to Chinese; `--title` enables the otherwise absent title. The current template explicitly supports two groups. Configure group IDs, labels, categories, and order at the top of the script. The proportion axis starts at zero. Outline/solid bars distinguish groups, not statistical significance.

Each category×group must have exactly one row. Integer counts must satisfy `0 <= numerator <= denominator` with a positive denominator. The denominator is the number of eligible observations in that cell, not the full sample. `_rates.csv` saves both raw counts and calculated proportions. Categories follow configuration order, not bar height or alphabetical order.

The source describes attendance within one year by prize amount and timing, without displaying cell counts or intervals. Template numerators, denominators, and category labels are synthetic examples, not recovered paper values. The script does not calculate adjusted effects, confidence intervals, or causal tests.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

12 synthetic cells, six categories, and two groups. English, Chinese, and titled modes were executed and visually checked; title-legend overlap was corrected. Proportions equaled each cell's numerator/denominator exactly. Numerators above denominators, zero denominators, duplicate cells, noninteger counts, and a third configured group were rejected as expected.

Canonical figure name: `bar_grouped_categories`
