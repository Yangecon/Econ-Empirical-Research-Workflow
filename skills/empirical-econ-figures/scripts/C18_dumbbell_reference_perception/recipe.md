# C18 · Reference–perception dumbbell plot

[English](recipe.md) · [中文](recipe.zh-CN.md)

`reference_perception_dumbbell` · C18

Connect actual shares and perceived means within each group, showing supplied intervals only for perceived means and retaining input order.

Classification: Descriptive comparison of actual immigration shares and respondent-perceived means/intervals across six countries; not structural estimation.

Tags: Beliefs, Actual–perceived gap, Dumbbell, Distribution, Measurement

## Sources and scope

[Immigration and Redistribution (2023)](<https://doi.org/10.1093/restud/rdac011>); Figure 2, left panel only; PDF p.12

The original page image and PDF caption have been checked; synthetic data demonstrate the drawing only.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run in the template directory:

```shell
python plot.py --input figures/demo_values.csv --output YOUR_PROJECT/figures/perception
```

Generates English PNG/PDF outputs and a numerical summary. `--title-en "Title"` enables titles; no title or bottom notes appear by default.

Diamonds indicate actual values, squares perceived means, and pale bands only the supplied 95% confidence intervals for perceived means. Inputs are percentages on a 0–100 scale; differences are percentage points. Provide both interval bounds for every category, or omit intervals entirely. This script does not estimate means or intervals. The example includes underestimation and equal values; markers coincide when values are equal. Change horizontal units and legends for other measures.

Only the left panel of original Figure 2 is implemented. The right panel displays mean misperceptions for different demographic groups and is not implemented; it is not another presentation of these same country gaps. All example values are synthetic.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Six categories retain input order, with synthetic negative and zero gaps. Percentage-range (0–100) and complete-interval checks passed. Supports either intervals for every category or none, rejecting partial/invalid intervals. English/Chinese PNG/PDF outputs were executed and visually checked; source image and caption were verified. Main acceptance corrected optional-title clipping, reran both titled language versions, and visually checked a representative figure.

Canonical figure name: `dumbbell_reference_perception`
