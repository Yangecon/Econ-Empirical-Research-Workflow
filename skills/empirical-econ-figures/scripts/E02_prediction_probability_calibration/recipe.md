# E02 · Predicted-versus-realized probability calibration

[English](recipe.md) · [中文](recipe.zh-CN.md)

`probability_belief_calibration` · E02

Compare predicted and true probabilities by bins, displaying the interquartile range of individual predictions, a full-sample linear fit, and a 45-degree benchmark.

Classification: Resample application lists and priority types, draw lottery numbers, and simulate the matching mechanism 500 times. Predictions use current applications and historical extrapolation; the ex post benchmark uses actual applications. Figure I A evaluates platform prediction quality, not respondent beliefs or structural calibration of preference/cost parameters.

Tags: Probability calibration, Binscatter, Prediction, Calibration, Matching simulation, Model validation

## Sources and scope

[Smart Matching Platforms and Heterogeneous Beliefs in Centralized School Choice (2022)](<https://doi.org/10.1093/qje/qjac013>); Figure I Panel A: Predicted vs. True Placement Probabilities; PDF p.25

The original page image and PDF caption have been checked; synthetic data demonstrate the drawing only.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run in the template directory:

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/calibration.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/calibration_stata.png" "en" "0"
```

Create the Stata output parent directory beforehand. Python `--title` or final Stata argument `1` enables the overall title; `zh` produces Chinese. Overall titles and bottom notes are absent by default.

x is true/reference probability and y is predicted probability, on a 0–1 scale. Observations from 0 through .99 inclusive are stably sorted by x and unique ID into ten approximately equal-count bins; >.99 is separate bin 11. At least 40 regular and four tail observations are required. Equal x values may be split across bins by ID; this is an explicit template convention, not attributed to the source. Bin x and y coordinates are observation means. Quartiles use linear interpolation at position 1+(n-1)p.

The pale band is the conditional 25th–75th percentile range of individual predictions, not a confidence interval for their mean. OLS uses all raw observations, including the >.99 tail, not the 11 bin points. This sample convention is declared by the template and is not claimed to match the source estimation implementation. Hollow circles style bin means without encoding significance. Only the drawing approach of Figure I Panel A is reproduced; Panel B's histogram is not implemented. The source prediction model and standard errors are not recalculated. All demonstration values are synthetic.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

160 synthetic observations: ten regular bins of 12 people each plus a >.99 tail group of 40. Maximum cross-language difference in means, linearly interpolated quartiles, and OLS fits was 2.5e-8. Exact .99 belongs to the regular group and >.99 to the tail. Both languages rejected probability 1.01. English/Chinese default/titled figures were executed; default figures passed visual checks.

Canonical figure name: `prediction_probability_calibration`
