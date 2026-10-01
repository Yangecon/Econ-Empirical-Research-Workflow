# A16 · Specification curve with a choice matrix

[English](recipe.md) · [中文](recipe.zh-CN.md)

`specification_curve_with_choice_matrix` · A16

Sort precomputed results and align each model’s explicit choices precisely with the same column.

Classification: Figure 3 Panel B orders the specification curve by results and aligns a binary specification-choice matrix below it. The original y axis is the mean t-statistic across experiments, not a coefficient or one t-test; do not mechanically add ±1.96 thresholds to that mean. After sorting, spec_id must preserve a one-to-one match of choices to results; blank choices cannot become zero. Panel A is a separate statistic-distribution layer; priority is the Panel B curve plus choice matrix.

Tags: Specification curve, Model choices, Robustness

## Sources and scope

[Policy Experimentation in China: The Political Economy of Policy Learning (2025)](<https://doi.org/10.1086/734873>); Figure 3, Panel B: Average t statistics among all experiments; PDF p.21

The original page image and PDF caption were checked; synthetic data demonstrate only the drawing method.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run inside the template directory:

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/specification.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/specification_stata.png" "en" "0"
```

Python `--title` or the last Stata argument `1` enables an overall title; `zh` selects Chinese. The example follows Figure 3 Panel B: y is the mean t-statistic across experiments, not a regression coefficient or a single test’s t-statistic, so no ±1.96 critical lines are drawn. Data are entirely synthetic; the program receives results rather than running the original experimental estimation.

Results and spec_id determine sorting; the upper figure and every choice use the same rank. Gray dots explicitly mean 0 and black dots 1; missing values cannot become 0. To replace model choices, update option IDs, row order, labels and result range in both scripts.

`qa_with_ci.csv` illustrates caller-supplied intervals: each row must have both endpoints blank or both present and containing the result. Original Panel B has no such intervals; the template does not infer interval type, coverage or significance. A multi-outcome matrix variant with clustered and Conley 95% intervals has not yet been implemented.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Forty-eight models and 11 choices; ordered results and choice matrices agree exactly across languages, and shuffled input leaves outputs unchanged. English/Chinese, optional-interval and title variants were executed and inspected. Changing the Stata result range to [-5,10] retains separation from the matrix. One-sided intervals, nonnumeric intervals and unknown choice columns are rejected as expected.

Canonical figure name: `robustness_specification_curve`
