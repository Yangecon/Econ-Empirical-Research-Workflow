# A05 · Regression discontinuity with binned outcomes

[English](recipe.md) · [中文](recipe.zh-CN.md)

`regression_discontinuity_binned_outcomes` · A05

Equal-width bin means on each side of a cutoff and separate lines fitted to raw observations inside the window display a level discontinuity.

Classification: Binning and fits on both sides of a cutoff emphasize a level jump. Identification and inputs are distinguished from the queued policy-kink slope-change figure; visual appearance does not establish design validity.

Tags: RD, Binned scatter, Local linear fit

## Sources and scope

[Political Foundations of Racial Violence in the Post-Reconstruction South (2026)](<https://doi.org/10.1093/qje/qjaf045>); Figure V; PDF p.26

The original page image and PDF caption were checked; synthetic data demonstrate only the drawing method.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run inside this template directory:

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/rd.png --lang en
```

In Stata:

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/rd_stata.png" "en" "0"
```

Python `--title` or the final Stata argument `1` enables an overall title; `zh` switches to Chinese. Configure panels, variable labels, windows, bins per side and display ranges consistently at the top of both scripts. The default two outcome panels have ten bins per side and share a probability y scale. After replacing data, adjust y limits and ticks together; the code rejects out-of-range points or fitted endpoints.

The running variable is already centered at the cutoff. Zero belongs to the right; both window endpoints are retained. Each side is binned separately into equal-width bins, none crossing zero, with at least two observations per bin. Lines use equally weighted OLS on all in-window observations, never regressions on bin means. Bin, side-coefficient and sample-count CSVs accompany the figure.

The paper includes election-period and state fixed effects and quadratic longitude/latitude terms, with windows from Table II optimal bandwidths. This template demonstrates only drawing, using synthetic binary outcomes, manually set windows and uncontrolled side-specific OLS. It does not recover the source adjustment, choose optimal bandwidths or calculate RD standard errors, p-values or identification validity. Outcomes must be in [0,1]; residuals that may exceed this range cannot be inserted directly.

### Stata package command variant

The native version is `plot_twoway.do` (byte-identical to the original `plot.do` entry point). The added `rdplot` version is `command_variants/rdplot/plot_rdplot.do`, reading the same explicit input CSV. First read [rdplot methods and differences](command_variants/rdplot/README.md), then run:

```stata
do "PATH_TO_TEMPLATE/command_variants/rdplot/run_demo.do" "PATH_TO_TEMPLATE/command_variants/rdplot" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/rdplot"
```

`PATH_TO_TEMPLATE` is this template’s absolute directory; outputs should belong to the research project. This runner generates default and optional-title examples. When calling `plot_rdplot.do` directly, set its last title switch to `0` (argument order is in its README).

Install the official rdrobust suite in a project-local ado directory; the runner accepts that directory as its fourth argument. Default results do not display RD confidence intervals. The package uses bin midpoints for x, while the native version uses the sample mean x in each bin.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

The 5,900 synthetic input rows produce 40 bins and four side-specific OLS lines. English/Chinese Python/Stata executions and visual checks passed, with maximum numerical difference within 4.57e-11. Checks cover window endpoints, cutoff assignment, excluded observations, duplicate/unknown IDs and probability bounds. Valid high-probability inputs beyond display bounds were rejected by both languages (Stata r(9)), preventing silent clipping. Four Stata runs of rdplot 11.1.0 passed for English/Chinese defaults and optional titles; counts and means of 40 bins match the native version (difference <2.14e-14), and four fitted lines differ by <3.11e-15. The bin-midpoint versus sample-mean x distinction is retained.

Canonical figure name: `rd_binned_outcomes`
