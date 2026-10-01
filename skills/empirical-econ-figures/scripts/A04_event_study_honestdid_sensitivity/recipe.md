# A04 · HonestDiD sensitivity intervals: relative magnitudes and smoothness

[English](recipe.md) · [中文](recipe.zh-CN.md)

`honestdid_sensitivity` · A04

Actually estimate an event study and its full covariance matrix on a synthetic panel. honestdid computes 95% robust intervals under relative-magnitude and second-difference smoothness restrictions, then plots through native coefplot options.

Classification: Use synthetic unit×time data to actually estimate event-study b and full V, then use honestdid to compute robust intervals for the target post-treatment effect under two restriction classes. Stata draws natively; coefficients are not entered by hand, and interval midpoints are not treated as new effect estimates.

Tags: DID, Event study, Robustness, Sensitivity, Parallel trends, Confidence interval, honestdid, Relative magnitudes, Smoothness

## Sources and scope

[Rambachan and Roth, A More Credible Approach to Parallel Trends (2023)](<https://doi.org/10.1093/restud/rdad018>); Method reference

Additional reference: [Rambachan and Roth (2023), A More Credible Approach to Parallel Trends](<https://doi.org/10.1093/restud/rdad018>); Figure 5; PDF p.31

Additional reference: [Rambachan and Roth (2023), A More Credible Approach to Parallel Trends](<https://doi.org/10.1093/restud/rdad018>); Figure 7; PDF p.33

The method sources are the Rambachan–Roth paper and HonestDiD author command documentation. This does not correspond to a specified paper figure, and no invented original image is attached.

Published examples use different data and target effects; existing template remains a simulated-data demonstration.

Published examples use different data and target effects; existing template remains a simulated-data demonstration.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Copy the template into a work subdirectory of the research project and run in Stata:

```stata
do "YOUR_PROJECT/honestdid_sensitivity/build.do" "YOUR_PROJECT/honestdid_sensitivity"
```

Stata actually runs the entire process from synthetic-data generation and fixed-effects event-study estimation to both sensitivity-interval classes and plots. Optional title and separate filenames:

```stata
do "YOUR_PROJECT/honestdid_sensitivity/build.do" "YOUR_PROJECT/honestdid_sensitivity" "Sensitivity analysis" "_titled"
```

Read schema.md and README.md. The figures are honestdid_relative_magnitude and honestdid_smoothness. Overall titles and bottom notes are absent by default. Do not run inside the installed skill directory, to avoid writing outputs back into the skill.

At the user's explicit request, this item is Stata-only. CSV files retain actual intervals for future Python redrawing. M and M-bar are not interchangeable; SD at M=0 and the Original interval do not impose the same assumption. The example targets the first post-treatment effect. To target an average effect, change l_vec and retain the full covariance matrix.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Stata 19 executed xtreg and honestdid on a synthetic panel of 320 units×nine periods. Reference period is −1, the full covariance is an 8×8 unit-clustered matrix, and the target is k=0. RM and SD each contain nine restriction values and one conventional Original interval. Log completion markers, numerical ranges, covariance, intervals, and optional-title checks passed, as did main-agent visual inspection. Uses tested HonestDiD 1.3.0 and Windows plugins; other platforms or the latest version are not claimed to be validated.

Canonical figure name: `event_study_honestdid_sensitivity`
