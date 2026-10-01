# C01 · Signed component decomposition

[English](recipe.md) · [中文](recipe.zh-CN.md)

`signed_component_decomposition` · C01

Display positive and negative components along a binned horizontal axis, stacking each sign separately and checking that the components sum to the total.

Classification: Product prices and sales shares construct relative prices; the labor-productivity component is relative sales per worker minus the price component. This figure displays cross-sectional accounting relationships in the data and is not generated from structurally estimated parameters.

Tags: Decomposition, Signed components, Accounting identity, Accounting, Stacked bars

## Sources and scope

[The Micro-Level Anatomy of the Labor Share Decline (2021)](<https://doi.org/10.1093/qje/qjab002>); Figure VIII; PDF p.37

The original page image and PDF caption have been checked; synthetic data demonstrate the drawing only.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run in the template directory:

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/decomposition.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/decomposition_stata.png" "en" "0"
```

Create the Stata output parent directory in advance. Python `--title` or final Stata argument `1` enables the overall title; `zh` switches to Chinese. No overall title or bottom notes appear by default.

Each row is a labor-share bin; bins must be equal-width, contiguous, and within [0,1]. Relative prices, relative physical labor productivity, and relative sales per worker use the same relative log units, with prices plus productivity equaling sales. The example uses synthetic values and only reads and checks these three precomputed variables; it does not reproduce their upstream estimation.

Positive and negative components stack upward and downward separately from zero. The algebraic total can lie between the two stack endpoints. This is not a 100% composition chart, and the topmost bar height cannot substitute for the total. The exported `_checked.csv` retains component lower/upper endpoints and the original total.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

20 contiguous equal-width bins. English, Chinese, and titled Python and Stata versions were executed and visually checked; maximum numerical difference was 1.11e-16. Reversed mixed signs (negative prices and positive productivity) were also checked. Stata rejected inputs violating the adding-up identity; Python rejected gaps, unequal widths, and bins outside [0,1].

Canonical figure name: `decomposition_signed_components`
