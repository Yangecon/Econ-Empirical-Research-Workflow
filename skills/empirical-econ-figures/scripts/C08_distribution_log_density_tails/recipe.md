# C08 · Log-density tail comparison

[English](recipe.md) · [中文](recipe.zh-CN.md)

`log_density_tail_comparison` · C08

Display a normal benchmark and left/right tail slopes over explicit intervals from supplied densities or log densities.

Classification: The source image and PDF p11 have been checked: natural log density, a normal benchmark, and log-density straight lines over explicit left/right intervals. Read positive density or explicitly supplied log density; do not add epsilon to zero densities. Plotted slopes +1.40/−2.18 differ from the text's tail exponents 0.40/1.18. The template reports fitted slopes only and cannot automatically call them Pareto exponents.

Tags: Log density, Tail slopes, Normal benchmark

## Sources and scope

[What Do Data on Millions of U.S. Workers Reveal About Lifecycle Earnings Dynamics? (2021)](<https://doi.org/10.3982/ECTA14603>); Figure 6; PDF p.11

The original page image and PDF caption have been checked; synthetic data demonstrate the drawing only.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run in the template directory; the output directory below should belong to the research project:

```shell
python plot.py demo_density.csv YOUR_PROJECT/figures/log_density.png --density-column density --left -4 -1.1 --right 1.1 3.5 --normal-sd 0.51
```

`--title "标题"` explicitly enables a title; titles and bottom notes are absent by default. See schema.md for fields, statistical objects, and display restrictions.

Shared drawing dependency: preserve this directory's relationship to sibling `_shared/line_geometry.py`; copy the shared module into the research project as well. Imports resolve relative to the script and permit execution from other working directories. The shared module only draws supplied lines or right-continuous steps; normalization, cumulative shares, fitted intervals, risk sets, and Greenwood intervals remain the responsibility of each adapter.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Verified a finite-grid demonstration density integral of 1, exact left/right slopes +1.40/−2.18, and rejection of zero density/duplicate x. Log-density slopes do not automatically equal Pareto exponents. User inputs are not automatically normalized, and the normal benchmark is displayed only within mean±4 SD. Python was executed and the main agent visually checked it; the drawing example is not a numerical reproduction of the paper. After adopting shared line/step geometry, reruns from a different working directory reproduced accepted default coordinates within 1e-10; statistical adapters were retained and C13 bars were unchanged.

Canonical figure name: `distribution_log_density_tails`
