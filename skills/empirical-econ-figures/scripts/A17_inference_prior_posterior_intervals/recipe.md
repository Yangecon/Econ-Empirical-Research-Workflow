# A17 · Prior–posterior interval comparison

[English](recipe.md) · [中文](recipe.zh-CN.md)

`prior_posterior_interval_comparison` · A17

Pair prior/posterior medians and intervals by source, displaying ITT point estimates and confidence intervals separately.

Classification: RCT ITT and posteriors updated with experimental data. Bayesian analysis is an inference method; the source figure does not estimate structural economic-behavior parameters.

Tags: Bayesian inference, Prior/posterior, Interval comparison, RCT, Inference, Point-interval plot

## Sources and scope

[Bayesian Impact Evaluation with Informative Priors: An Application to a Colombian Management and Export Improvement Program (2025)](<https://doi.org/10.3982/ECTA21567>); Figure 2; PDF p.15

The original page image and PDF caption were checked; synthetic data demonstrate only the drawing method.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run inside the template directory:

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/prior_posterior.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/prior_posterior_stata.png" "en" "0"
```

Create the Stata output parent directory first. Python `--title` or the final Stata argument `1` enables an overall title; `zh` switches to Chinese. Outcome/year panel labels remain, while overall titles and bottom notes are omitted by default.

Inputs are uniquely identified by panel, source and interval type. Academic, policymaker, firm and literature sources each have prior and posterior rows, alongside the diffuse-prior posterior and frequentist ITT. The current four panels contain 40 rows. When changing panels/sources, update configurations and row-count checks in both scripts.

`median` means the median for Bayesian rows and the point estimate for ITT; its name does not make ITT a median estimator. `low/high` hold 95% prior intervals, 95% posterior intervals or 95% frequentist CIs. Scripts only read saved values; they do not update Bayesian distributions, require posterior intervals to nest within priors, or interpret posterior exclusion of zero as frequentist significance.

In the source, left-column export participation is a probability difference; right-column product-country varieties are count differences. These cannot share one outcome unit. Each panel independently sets its x range. Example values were generated separately to demonstrate layout/type distinctions and do not reproduce the source updating results. Python uses a shared legend; Stata distinguishes rows through labels and line styles. Interval meanings are also retained in this documentation.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Forty rows across four panels agree exactly across languages by panel/source/kind. Both reject invalid intervals and missing pairs, and reordered CSV columns preserve values. English/Chinese defaults and title variants were executed and inspected; Stata row labels were rechecked after readability adjustment.

Canonical figure name: `inference_prior_posterior_intervals`
