# A01 · Event study, pre/post means and static DID

[English](README.md) · [中文](README.zh-CN.md)

The demonstration uses a balanced panel of 70 units observed for 14 periods: **980 rows**, with 35 treated units and 35 never-treated controls. Treatment starts at event time 0; the window is −6 through 7 and the reference is −1. Python and Stata independently estimate regressions from simulated observations. These are not predetermined coefficient inputs or reproductions of a paper's numerical results.

## The two mean lines

Keep the normalized reference β₋₁ = 0:

- Pre mean = (β₋₆ + β₋₅ + β₋₄ + β₋₃ + β₋₂ + 0) / 6.
- Post mean = (β₀ + … + β₇) / 8.
- DID contrast = Post mean − Pre mean.

The reference remains a hollow circle, without its own interval or significance test. It belongs to the pre-treatment sample and therefore contributes to the averaging denominator. The path is not recentered on its pre mean; the post line's height itself is not DID or ATT. A pre mean is not a joint parallel-trends test.

The equality holds for this balanced, common-timing design with the same sample and time window, no additional controls and no regression weights. Do not assume it for staggered timing, unbalanced panels or other estimators. With external inputs, the exported difference is first a specified coefficient contrast; its DID/ATT interpretation depends on the research design.

## Regressions and covariance

The static model is `y = unit FE + time FE + τ × treated × post + error`. The event-study model uses the same fixed effects and interacts treatment status with each period except −1.

Python uses two-way within OLS; Stata uses native `regress`. Both cluster by unit. Validation uses an uncorrected CR0 sandwich and normal 95% intervals. Stata's default clustered covariance has a finite-sample multiplier, which the program explicitly removes before comparing results. Default multipliers can differ between models with different parameter counts.

For mean weights w, variance is `w' V w`. For the difference, set `c = w_post − w_pre` and use `c' V c`. Retain the full covariance; do not add the two mean variances or use only individual coefficient standard errors.

Each horizontal shaded band is an interval for a **scalar mean**, not a simultaneous band for the dynamic path. Pointwise intervals determine filled versus hollow estimated markers. The normalized reference is always hollow.

## Inputs and outputs

`demo_panel.csv` has columns `unit,event_time,treated,post,y`. `estimate_demo_panel.py` records fixed-seed generation and Python estimation. The plotting `.py` reads the bundled panel and re-estimates by default; Stata's `MODE "demo"` independently estimates the same panel.

External estimates have fields `term,event_time,estimate,is_reference,weight`; weights are optional and default to 1. The reference coefficient and corresponding covariance row/column must be zero. Label covariance rows/columns by the same terms and include off-diagonal entries. Normalize weights within each window, including the reference in the pre window.

`demo_contrasts.csv` stores pre mean, post mean, post minus pre, static DID and a direct unit-change check. Plot outputs include `_summaries.csv` for the mean lines, `_contrast.csv` for the difference and its uncertainty, and `_periods.csv` for individual coefficients. See the adjacent [recipe](recipe.md) for commands and output settings.

Figures are English only by default, with no overall title or bottom notes. An explicit title is optional. The −1 marker is a hollow circle. `--post-is-att` / `POST_IS_ATT=1` is deprecated and rejected to prevent mislabeling the post line.

## Demonstration values

| Quantity | Estimate | CR0 standard error |
|---|---:|---:|
| Pre mean, including −1 | −0.050198027 | 0.067777896 |
| Post mean | 0.088908434 | 0.076495584 |
| Post − Pre / static DID | 0.139106461 | 0.033701696 |

The normal 95% DID interval is [0.073052351, 0.205160571]. The independent check computes each unit's post-minus-pre change and differences the group means, deriving CR0 variance from within-group variation in these changes. The recipe's validation section records execution status, errors and evidence.

## Source limits

The original local example's paper identity remains unverified. A supplemental analogue is Gandhi, Olenski, Ruffini and Shen, NBER Working Paper 32412, Figure 5 (PDF p.26). Its panels, sample, period windows and inference differ. This example borrows the presentation of dynamic estimates and pre/post lines only.

Canonical figure name: `event_study_pre_post_averages`
