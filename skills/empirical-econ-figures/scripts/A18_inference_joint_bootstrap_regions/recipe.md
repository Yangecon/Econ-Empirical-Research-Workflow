# A18 · Joint bootstrap confidence regions

[English](recipe.md) · [中文](recipe.zh-CN.md)

`joint_bootstrap_region_display` · A18

Read an external two-dimensional grid and nested 90/95/99% joint regions, overlaying a point estimate and the x+y=0.5 reference line.

Classification: Equity-premium contribution estimates constructed from return and option data, with a block-bootstrap joint sampling distribution. The source compares them with asset-pricing theory models only in the next section.

Tags: Bootstrap, Joint uncertainty, Nested regions, Inference, Contour regions

## Sources and scope

[Dissecting the Equity Premium (2022)](<https://doi.org/10.1086/720396>); Figure 3; PDF p.11

The original page image and PDF caption were checked; synthetic data demonstrate only the drawing method.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run Python in the selected template directory, writing to the research project:

```shell
python plot.py --grid demo_joint_grid.csv --point demo_point.csv --output-prefix YOUR_PROJECT/figures/joint_bootstrap_region_display
```

Run Stata from this template directory with explicit arguments:

```stata
do plot.do "demo_joint_grid.csv" "demo_point.csv" "YOUR_PROJECT/figures/joint_region.png" 0
```

Python may add `--title "标题"`; change Stata’s last argument from 0 to 1 to enable the example title. Defaults omit the title and bottom notes. See schema.md for input fields and statistical boundaries.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Grid completeness, region nesting, rejection of invalid cells and cellwise Python/Stata agreement were checked. Example regions are supplied on a synthetic grid; the original block bootstrap is not implemented, and marginal rectangles or normal ellipses do not replace joint regions. Boundary contact requires truncation checks. Both languages were executed and the lead agent inspected figures; the example is not a numerical paper replication.

Canonical figure name: `inference_joint_bootstrap_regions`
