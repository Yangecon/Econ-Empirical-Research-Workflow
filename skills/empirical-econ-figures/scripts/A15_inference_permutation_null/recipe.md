# A15 · Permutation null distribution

[English](recipe.md) · [中文](recipe.zh-CN.md)

`permutation_null_distribution` · A15

Side-by-side supplied randomization null distributions and observed values, with explicitly defined one-/two-sided extremes and Monte Carlo p-values.

Classification: The permutation null distribution and observed statistic are inference diagnostics, retained in both languages. Tail rules and permutation p-values must be explicit.

Tags: Randomization inference, Permutation, Null distribution, Inference, Histogram

## Sources and scope

[An Experimental Evaluation of Deferred Acceptance: Evidence from Over 100 Army Officer Labor Markets (2026)](<https://doi.org/10.3982/ecta22160>); Figure 1; PDF p.19

The original page image and PDF caption were checked; synthetic data demonstrate only the drawing method.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run inside this template directory:

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/permutation.png --lang en --tail right --xmin 0 --xmax 1 --binwidth .01
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/permutation.png" en right "" 0 1 .01 0
```

Stata arguments are input, output, language, tail rule, null center, x minimum, x maximum, bin width and title switch. Python `--title` or the last Stata argument `1` enables a title. `zh` switches to Chinese.

The B supplied draws exclude the observed assignment; p=(E+1)/(B+1). Right tails count null>=observed, left tails null<=observed; two-sided tests require an explicit center c and use |null-c|>=|observed-c|. Equality counts as extreme. This add-one rule is for Monte Carlo draws, not full-enumeration counts already containing the observed assignment.

Each bar height is the bin draw count/B, not probability density. P-values and counts are saved separately in results.csv; no test notes are printed inside the figure. The template does not construct a valid assignment mechanism. Real applications must first generate null distributions based on experimental or quasi-experimental designs; ordinary bootstrap draws cannot simply be called a randomization test.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

English/Chinese Python/Stata PNG/PDF outputs were executed and inspected. Single panels omit top names by default; multiple panels retain labels, and Stata y tick labels are horizontal. Two panels have 2,500 synthetic draws each. Right-tail, left-tail and explicitly centered two-sided extreme counts agree; maximum p-value difference is below 5.2e-14.

Canonical figure name: `inference_permutation_null`
