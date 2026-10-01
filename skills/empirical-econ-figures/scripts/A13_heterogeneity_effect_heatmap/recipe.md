# A13 · Bivariate effect heatmap

[English](recipe.md) · [中文](recipe.zh-CN.md)

`bivariate_effect_heatmap` · A13

Estimated results on a grid of two grouping dimensions, with outcome-specific units, color bands and missing cells.

Classification: Groups are defined by rules and discretion scores. Estimated treatment effects and mean covariates yield heterogeneity; firm size and subsidy totals then produce cost effectiveness. Classified as empirical effects and derived accounting.

Tags: Heterogeneity, Interaction, Heatmap, Cost effectiveness

## Sources and scope

[Making Subsidies Work: Rules versus Discretion (2025)](<https://doi.org/10.3982/ecta21319>); Figure 8; PDF p.25

The original page image and PDF caption were checked; synthetic data demonstrate only the drawing method.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run inside the template directory:

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/heatmap.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/heatmap_stata.png" "en" "0"
```

Create the Stata output parent directory first. Python `--title` or the final Stata argument `1` enables an overall title; `zh` switches to Chinese. Coordinates are quintile categories: SR on x and SD on y, with all 25 cells per panel. If an estimate is unavailable, retain the row and leave value blank; do not substitute zero or omit the row.

Both languages share ten RGB color bands, with boundaries generated from each panel’s independent range and rounded to 12 decimals. Bands include the lower endpoint and exclude the upper; the last includes the maximum. Python uses a stepped colorbar and Stata a band-by-band legend. Statistical inputs and color assignments match; layouts are not pixel-identical.

The source objects are treatment effects on six-year firm employment log changes and additional jobs per €100,000 subsidy. The same color need not mean the same number in different panels. Estimation, firm-size-weighted jobs and total subsidies are upstream constructions; scripts only read saved results. No CIs or significance stars are drawn. The source’s 90% clustered-bootstrap intervals are in a separate table and cannot be inferred from color. The example is entirely synthetic.

`qa_boundaries_missing.csv` illustrates color boundaries, gray missing cells and true zeros. When replacing outcomes, update units, panel IDs and color ranges in both scripts, not just displayed wording.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Fifty cells across two panels. English/Chinese, title and missing-value Python/Stata variants were executed and inspected. Estimates, missing flags and color bands match cell by cell. All 11 color boundaries per panel were tested: employment effect 0.125 falls in band 6 and the maximum in band 10. Both languages reject omitted coordinate rows; gray missing values are distinct from numeric zero.

Canonical figure name: `heterogeneity_effect_heatmap`
