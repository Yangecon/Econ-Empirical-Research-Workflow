# B02 · Quantile-group boxplots of estimated probabilities

[English](recipe.md) · [中文](recipe.zh-CN.md)

`quantile_group_boxplot` · B02

Compare distributions of individual estimates across predefined quantile groups, with explicit quartile interpolation, whisker and outlier rules.

Classification: Individual attention probabilities estimated by the same behavioral model V are displayed by latent-acuity decile; this is not an ordinary boxplot of raw observed probabilities.

Tags: Estimated probabilities, Quantile groups, Boxplot, Heterogeneity

## Sources and scope

[Heiss et al., Inattention and Switching Costs as Sources of Inertia in Medicare Part D (2021)](<https://doi.org/10.1257/aer.20170471>); Figure 1; PDF p.29

The original page image and PDF caption were checked; synthetic data demonstrate only the drawing method.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run inside this template directory:

```shell
python plot.py --input demo.csv --lang en --output YOUR_PROJECT/figures/grouped_boxplot.png
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/grouped_boxplot.png" en 0 0 1
```

The last three Stata arguments are the title switch, input lower bound and input upper bound. Python `--title` enables a title; `--ymin` / `--ymax` adjust input bounds. Use `zh` for Chinese in both languages. Each implementation also outputs a grouped-statistics CSV.

Explicit Hyndman–Fan type 7 quartiles and 1.5×IQR whiskers are used for cross-language consistency; these are not claimed as the paper’s original software defaults. Whiskers are not confidence intervals, and points beyond whiskers are not necessarily erroneous. Boundary probabilities of 1 must not be deleted merely because they look extreme.

The template reads predefined group and value fields; it does not construct acuity deciles or estimate attention probabilities. When switching variables, also change bounds, units and axis labels.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

English/Chinese Python/Stata PNG/PDF outputs were executed and inspected. There are 700 synthetic rows with ties, ten groups and 21 observations beyond whiskers. Group counts, whiskers and outlier counts agree; maximum quartile difference is about 1.11e-16. Python also passed nested-new-directory tests; boundary observations at 0/1 are fully visible.

Canonical figure name: `distribution_estimated_probabilities_boxplot`
