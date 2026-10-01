# C09 · Weighted distribution comparison

[English](recipe.md) · [中文](recipe.zh-CN.md)

`weighted_distribution_comparison` · C09

Calculate establishment-count and value-added shares within industries, then weight them by industry value added, using common bins and a shared vertical scale.

Classification: PDF Figure I's caption has been checked: first compute establishment-count and value-added shares within each three-digit industry, then average using that year's industry value-added weights. This differs from directly weighting all establishments. Two explicit denominators share the same x variable; common-scale panels/overlays avoid arbitrary dual-axis scaling.

Tags: Weighted shares, Industry aggregation, Distribution

## Sources and scope

[The Micro-Level Anatomy of the Labor Share Decline (2021)](<https://doi.org/10.1093/qje/qjab002>); Figure I; PDF p.3

The original page image and PDF caption have been checked; synthetic data demonstrate the drawing only.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run in this template directory:

```shell
python plot.py --input demo.csv --output-prefix YOUR_PROJECT/figures/weighted_distribution_comparison
```

`--title "标题"` explicitly adds a title; no title or bottom notes appear by default. See schema.md for input fields, exclusions, and display interpretation. Outputs include PNG, PDF, and accounting CSV.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Verified both within-industry denominators, annual industry weights, shares summing to one, common bin endpoints, and invalid-bin checks. Python was executed and visually checked. All demonstration values and relationships are synthetic, not reproductions of the paper.

Canonical figure name: `distribution_weighted_comparison`
