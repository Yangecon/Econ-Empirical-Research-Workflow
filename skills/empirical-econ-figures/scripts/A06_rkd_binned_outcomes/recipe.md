# A06 · Regression kink panels with binned outcomes

[English](recipe.md) · [中文](recipe.zh-CN.md)

`threshold_binned_regression_panels` · A06

Bin means for multiple outcomes around one policy threshold, with continuous piecewise-linear fits displaying changes in slope.

Classification: The caption of Landais Figure 7 was verified: a regression kink at daily wages of SEK 850, including the replacement-rate rule, insurance selection and risk panels. The distinction between slope changes and level jumps is retained; plotting does not replace upstream residualization or identification.

Tags: RKD, Threshold, Binned scatter

## Sources and scope

[Risk-Based Selection in Unemployment Insurance: Evidence and Implications (2021)](<https://doi.org/10.1257/aer.20180820>); Figure 7; PDF p.30

The original page image and PDF caption were checked; synthetic data demonstrate only the drawing method.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run inside this template directory:

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/kink.png --lang en
```

In Stata:

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/kink_stata.png" "en" "0"
```

Python `--title` or the final Stata argument `1` enables an overall title; `zh` switches to Chinese. Update both scripts’ threshold, window, panel IDs, units, bin counts, display ranges and ticks together. Defaults are threshold 850, window [500,1200] and 12 bins per side. Four outcomes have independent y axes, so visual steepness cannot be compared directly.

The fit uses all in-window observations independently of binning: `y = a + b*(x-c) + d*max(x-c,0)`. The left slope is b, right slope b+d, and common threshold level a. This is a continuous kink display, not a discontinuity allowing a level jump. Bins only display means. Hollow points are a scatter style, not significance coding, because no intervals are shown.

The only source is Figure 7 in AER 2021. Its insurance outcomes are covariate-adjusted, with model estimates and standard errors under a 350 SEK bandwidth. This template does not perform the source residualization/inference or reproduce its numbers. Outcomes with explicitly documented upstream adjustments may be supplied, but units, display ranges and sample descriptions must also change. CSV outputs retain bins, fitted coefficients and sample counts. A visible slope change alone does not establish causal identification.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

The 17,600 synthetic rows produce 96 bins and four continuous-kink fits. English/Chinese Python/Stata executions and visual checks passed; maximum numerical CSV difference is within 4.60e-9. Both languages accept asymmetric panel samples with 24 left and 48 right observations and reject one fewer as expected. Additional checks cover endpoints, right-side threshold assignment, full rank and display bounds.

Canonical figure name: `rkd_binned_outcomes`
