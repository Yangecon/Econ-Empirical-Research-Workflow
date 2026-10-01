# A14 · Quantile coefficient profile

[English](recipe.md) · [中文](recipe.zh-CN.md)

`quantile_coefficient_profile` · A14

Connect pre-estimated coefficients at numerical quantile locations, with supplied confidence intervals at each quantile.

Classification: Regression coefficients and precomputed intervals at outcome-distribution quantiles. The source uses unconditional quantile regression of standardized PSAT scores on BNI, with 99% ZIP-clustered CIs. Numerical quantile positions and interval levels are retained. This is neither mean outcomes grouped by x quantiles nor automatically a quantile treatment effect. The template does not treat qreg as an unconditional quantile estimator.

Tags: Quantile coefficients, UQR, Confidence intervals, Heterogeneity, Coefficient plot

## Sources and scope

[Distinctively Black Names and Educational Outcomes (2023)](<https://doi.org/10.1086/722093>); Figure 4; PDF p.15

The original page image and PDF caption were checked; synthetic data demonstrate only the drawing method.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run inside the template directory:

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/quantile.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/quantile_stata.png" "en" "0"
```

Create the Stata output parent directory first. Python `--title` or the last Stata argument `1` enables an overall title; `zh` switches to Chinese. Defaults omit overall titles and bottom notes.

The x axis is the numerical percentile of the outcome distribution, between 0 and 100; inputs must be strictly increasing by quantile. Connections are reading aids only. Coefficients and intervals are read directly, without estimating regressions or standard errors. Edit script labels for actual units and document interval coverage and inference methods in the text.

The source uses unconditional quantile regression of standardized PSAT scores on BNI, with 99% ZIP-clustered confidence intervals. The nine-quantile example uses synthetic coefficients and illustrative intervals. Ordinary Stata `qreg` is not automatically an unconditional quantile estimator, and the coefficient cannot unconditionally be relabeled a quantile treatment effect. This differs from averaging outcomes within bins of an explanatory variable.

Both languages place points on a numeric x axis; automatic ticks and margins differ. CSV outputs permit elementwise checks.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Python/Stata exported values at nine quantiles agree exactly. Both languages reject intervals that omit the estimate and unsorted quantiles; reordered CSV columns preserve values. English/Chinese defaults and title variants ran successfully; defaults were visually inspected by the lead agent.

Canonical figure name: `coefficient_quantile_profile`
