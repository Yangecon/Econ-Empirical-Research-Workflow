# C03 · Lorenz and concentration curves

[English](recipe.md) · [中文](recipe.zh-CN.md)

`lorenz_concentration_curves` · C03

Display cumulative population weights and resource shares, distinguishing concentration curves with a shared ranking variable from Lorenz curves ranked by each resource itself.

Classification: Cumulative resource shares under population ranking and an equality line; denominators and ranking variables differ from an ordinary CDF.

Tags: Lorenz curve, Concentration curve, Inequality

## Sources and scope

[Curbing Leakage in Public Programs: Evidence from India's Direct Benefit Transfer Policy (2024)](<https://doi.org/10.1257/aer.20161864>); Figure 1; PDF p.7

The original page image and PDF caption have been checked; Figure 1 in the upper part of the reference page corresponds to this template, while Figure 2 appears below it.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run in this template directory:

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/concentration.png --mode concentration --lang en
```

`--mode lorenz` ranks each resource curve by its own resource values; `--lang zh` switches to Chinese; `--title` explicitly enables a mode-specific title. Titles are hidden by default. Change resource column names, curve labels, and units together in the top-of-script configuration.

For each curve, x is cumulative observation weight divided by total weight and y is cumulative weight×resource divided by the weighted resource total. Exact ranking ties are aggregated before cumulation, avoiding arbitrary within-tie ordering. Values must be nonnegative and total weight and each weighted resource total positive; zero resources and zero individual weights are allowed.

The source ranks fuel purchases and total expenditure by the same household-consumption measure, making these concentration curves with a shared ranking. Lorenz mode is a general variant supplied by this template; changing the ranking changes the statistical object. Coordinates are also saved to points.csv. Gini indices, confidence intervals, and treatment effects are not generated automatically.

Shared drawing dependency: preserve this directory's relationship to sibling `_shared/line_geometry.py`; copy the shared module when transferring the template to a research project. Imports resolve relative to the script, allowing execution from other working directories. The shared module only draws supplied lines or right-continuous steps; each adapter still handles normalization, cumulative shares, fitted intervals, risk sets, and Greenwood intervals.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

900 synthetic household observations. English and Chinese concentration curves and an English Lorenz variant were executed and visually checked. Weighted endpoints, exact rank-tie aggregation, and differences between the two rankings passed tests. A titled Lorenz variant confirmed that title and mode agree. After adopting shared line/step geometry, reruns from a different working directory reproduced accepted default coordinates within 1e-10; statistical adapters were retained and C13 bars were unchanged.

Canonical figure name: `distribution_lorenz_concentration`
