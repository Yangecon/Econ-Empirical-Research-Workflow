# C02 · Distribution overlays with thresholds

[English](recipe.md) · [中文](recipe.zh-CN.md)

`distribution_overlay_with_thresholds` · C02

Compare distributions across groups, shade complete bins below explicit thresholds, and label shares calculated using the full-sample weight denominator.

Classification: Compare income distributions by year and mark common or year-specific thresholds and the mass below them, retaining density-normalization and weight definitions.

Tags: Weighted distribution, Threshold shares, Histogram

## Sources and scope

[Evaluating the Success of the War on Poverty since 1963 Using an Absolute Full-Income Poverty Measure (2024)](<https://doi.org/10.1086/725705>); Figure 10; PDF p.37

The original page image and PDF caption have been checked; synthetic data demonstrate the drawing only.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run in this template directory:

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/distributions.png --lang en --xmax 120000 --binwidth 1000
```

`--lang zh` switches to Chinese; `--title` explicitly enables a title. Configure groups, thresholds, labels, colors, and each group's shading threshold at the top of the script. Shares for all thresholds in each group are also saved to shares.csv. Change axis units in the same configuration.

Inputs must be nonnegative and the left bound is fixed at 0. Thresholds must align with bin edges. Shading extends over complete bins to the threshold; exact shares use value<threshold, leaving ties on the upper side. All visible bins are left-closed and right-open. Observations at or above xmax are not drawn but remain in the weight denominator.

The vertical axis is the weighted percentage in each equal-width bin, not a kernel density. Changing bin width changes curve height. The script does not automatically adjust for inflation, equivalize household size, derive poverty lines, or perform survey-sampling inference; upstream analysis must handle those steps. The source also includes median reference lines; this general example retains the core distribution, threshold, and share presentation.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

English and Chinese Python PNG/PDF outputs were executed and visually checked. For 14,000 synthetic observations, each group-threshold weighted share matched the mass of the complete bins. Tests covered observations exactly at thresholds and the horizontal upper bound, rejection of a nonzero lower bound, and creation of nested output directories. The 597 later-period observations truncated on the right remained in the denominator; visible mass was approximately 91.4856%, without renormalization to 100%.

Canonical figure name: `distribution_threshold_overlay`
