# A07 · Bandwidth sensitivity profile

[English](recipe.md) · [中文](recipe.zh-CN.md)

`bandwidth_sensitivity_profile` · A07

Compare coefficients as regression sample bandwidth changes, distinguishing two inference methods at the same coverage with a gray band and dotted lines.

Classification: Spatial-bandwidth robustness profiles for six outcomes: x is the maximum distance from the border allowed in each regression, not an individual running variable; 61 regressions per outcome. Gray bands are census-block-clustered robust 95% CIs; dotted lines are Conley 95% CIs. These are two inference methods, not 68/95 confidence levels. Inputs explicitly name methods and supply intervals; no clustering/Conley estimation is performed. An optional benchmark needs a user-specified meaning; the original blue dashed line is not guessed.

Tags: Bandwidth sensitivity, Spatial inference, Robustness, Line plot

## Sources and scope

[Multinationals, Monopsony, and Local Development: Evidence From the United Fruit Company (2022)](<https://doi.org/10.3982/ECTA19514>); Figure 3; PDF p.13

The original page image and PDF caption were checked; synthetic data demonstrate only the drawing method.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run inside the template directory:

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/bandwidth.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/bandwidth_stata.png" "en" "0"
```

Create the Stata output parent directory first. Python `--title` or the final Stata argument `1` enables an overall title; `zh` switches to Chinese. Configure outcome names, units and order consistently in both scripts. Each outcome uses its own y range. The source’s total unmet-needs outcome is a count difference; the other five are probability differences.

The x axis is the maximum distance from the border included in each regression. The source ranges from 5 to 20 km in 0.25 km increments, giving 61 sample bandwidths. This is neither an individual running variable nor the Conley spatial-correlation cutoff (separately set to 2 km in the source). The example retains the grid but uses synthetic coefficients and intervals.

The gray band and dotted lines respectively show clustered-robust 95% and Conley 95% intervals for the same estimate. Do not relabel these as 68%/95% nested intervals or require nesting across methods. `qa_crossing.csv` supplies a valid crossing example. Scripts read precomputed results without estimating standard errors or inferring causal identification.

The original blue dashed line’s precise meaning was not verified from the caption, so it is omitted. A benchmark requires a specified value and meaning first. Python uses a shared legend; Stata repeats the same two methods below each panel. Layout differences are allowed.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Six outcomes at 61 bandwidths each, 366 rows. English/Chinese, title and crossing-interval Python/Stata variants were executed and inspected; maximum numerical output difference is zero. Both languages accept the valid fixture where the two 95% intervals cross while each contains the estimate. Python also checks the common grid, duplicate keys, negative bandwidths and invalid intervals.

Canonical figure name: `robustness_spatial_bandwidth`
