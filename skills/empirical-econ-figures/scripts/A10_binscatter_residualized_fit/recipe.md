# A10 · Residualized binscatter with observation-level fit

[English](recipe.md) · [中文](recipe.zh-CN.md)

`residualized_binned_scatter` · A10

Equal-count bin means display residual relationships; the fit uses all original observations, with explicit sorting and tie rules.

Classification: Bin means and fitted relationships require explicit inputs and aggregation rules and are documented separately from observation-level scatterplots.

Tags: IV first stage, Residualization, Binscatter

## Sources and scope

[Thorsten Rogall, Mobilizing the Masses for Genocide (2021)](<https://doi.org/10.1257/aer.20160999>); Figure 1; PDF p.16

The original page image and PDF caption were checked; synthetic data demonstrate only the drawing method.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run inside this template directory, specifying the project output path:

```shell
python plot.py --input demo.csv --bins 50 --lang en --output YOUR_PROJECT/figures/binned_scatter.png
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/binned_scatter.png" en 50 0
```

Python `--title` or the last Stata argument `1` enables a title; `zh` switches to Chinese. Configure axis labels at the top of the code. Both languages independently generate bin-summary CSVs and PNG/PDF outputs. The Stata output parent directory should already exist; its logs and bin summary are written to the working directory.

This template accepts rx and ry already processed on the same analysis sample and controls. It does not residualize variables or call the fitted line an IV estimate. Binning sorts by rx and unique text id and assigns `floor((r-1)*B/N)+1`; ties may cross bins. This is an explicit, auditable demonstration rule, not a claim about the paper authors’ original tie algorithm.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

All four English/Chinese Python/Stata PNG figures were executed and visually inspected; PDFs were exported. The 503 observations form 50 bins of 10–11 rows. Bin counts agree across languages, means differ by less than 5e-11, and observation-level OLS intercepts/slopes agree to eight decimals. Many tied rx values verify the deterministic rule. A subsequent fix addressed first output to a nonexistent directory: English default and Chinese titled fresh-folder runs passed; all 50 exported bins match accepted values and the OLS coefficients for 503 observations agree. Stata and statistical calculations were unchanged.

Canonical figure name: `binscatter_residualized_fit`
