# B03 · Impulse-response matrix with nested posterior bands

[English](recipe.md) · [中文](recipe.zh-CN.md)

`impulse_response_matrix_nested_bands` · B03

Arrange dynamic medians and 68%/90% posterior intervals by response and shock, sharing a y scale within each response row.

Classification: Orthogonal structural shocks in an SVAR with t-distributed errors and 68%/90% posterior response intervals; these are not arbitrary dynamic regression coefficients.

Tags: IRF, Structural model, Posterior bands, SVAR, Line plot

## Sources and scope

[Feedbacks, Financial Markets, and Economic Activity (2021)](<https://doi.org/10.1257/aer.20180733>); Figure 1; PDF p.14

The original page image and PDF caption were checked; synthetic data demonstrate only the drawing method.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run inside this template directory:

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/irf.png --lang en
```

In Stata:

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/irf_stata.png" "en" "0"
```

Python `--title` or the last Stata argument `1` enables an overall title; `zh` switches to Chinese. Shock-column names, response-row names and units are necessary panel identifiers and remain by default. Adapt the 5×5 panel IDs, units and y ranges at the top of both scripts for other systems. Rows may have different units, but shocks within a row share a scale.

Light/dark bands are the supplied 90%/68% posterior intervals and the black line is the median. Markers at selected horizons are an additional template feature: filled means the outer 90% posterior interval excludes zero; hollow means it includes zero. This is not a frequentist significance test, and the original figure does not use this marker layer. Configure marked horizons in the scripts.

Inputs must contain every response×shock cell on the same horizon grid starting at 0. These IRFs do not use the event-study -1 omitted period. Posterior intervals and shock scales come from the upstream model. Scripts cannot establish model identification, estimate posteriors or generate p-values from this figure.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

The 525 synthetic posterior summaries form 25 panels. English/Chinese Python/Stata versions were executed and inspected; maximum numerical difference is zero and both count 331 rows whose outer interval excludes zero. A 425-row variant ending at 48 months also agrees; Stata 0/24/48 ticks were inspected. Extra unknown cells return r(9). Checks also cover matrix completeness, common horizon grid, interval nesting and row-specific display bounds; no VAR/posterior is re-estimated.

Canonical figure name: `irf_nested_confidence_bands`
