# A11 · Grouped coefficient forest plot

[English](recipe.md) · [中文](recipe.zh-CN.md)

`grouped_coefficient_forest` · A11

Horizontal multi-outcome specification comparisons and vertical grouped-coefficient variants, retaining outcome-specific units, confidence intervals and explicit display order.

Classification: One configurable figure family supports horizontal specification comparisons and vertical grouped outcome coefficients while preserving each outcome unit and interval meaning.

Tags: Heterogeneity, Coefficient plot, Specification comparison, Robustness, Forest plot

## Sources and scope

[Andrew Goodman-Bacon, The Long-Run Effects of Childhood Insurance Coverage: Medicaid Implementation, Adult Health, and Labor Market Outcomes (2021)](<https://doi.org/10.1257/aer.20171671>); Figure 8; PDF p.31

Additional reference: [Desmond Ang, The Effects of Police Violence on Inner-City Students](<https://doi.org/10.1093/qje/qjaa027>); Figure VIII; PDF p.44

Original page images and PDF captions were checked. The first source compares IV specifications and the other reports DD subgroup results; their estimands are not merged.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run inside this template directory, specifying project output paths:

```shell
python plot.py --input demo.csv --variant robustness --orientation horizontal --lang en --output YOUR_PROJECT/figures/forest.png
python plot.py --input demo.csv --variant subgroup --orientation vertical --lang en --output YOUR_PROJECT/figures/grouped_coefficients.png
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/forest.png" en robustness horizontal 0
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/grouped_coefficients.png" en subgroup vertical 0
```

Python `--title` / the final Stata argument `1` enables a title; `zh` switches to Chinese. A matching PDF is automatically exported. The top CONFIG or corresponding Stata locals configure 1–4 panels, 1–3 groups, panel units and the reference specification. CSV inputs explicitly supply term/panel/group order. Horizontal panels share specification rows without forcing effect axes with different units to share scales.

Explicit CIs take precedence; only when both endpoints are missing is estimate ± 1.96×se used. This fallback is a normal approximation; real analyses should supply estimator-specific intervals. Filled/hollow symbols here distinguish specifications or groups, unlike the significance coding in the event-study template.

### Stata package command variant

The native version is `plot_twoway.do` (byte-identical to the original `plot.do`). The added `coefplot` version is `command_variants/coefplot/plot_coefplot.do`, reading the same explicit input CSV. First read [coefplot methods and differences](command_variants/coefplot/README.md), then run:

```stata
do "PATH_TO_TEMPLATE/command_variants/coefplot/run_demo.do" "PATH_TO_TEMPLATE/command_variants/coefplot" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/coefplot"
```

`PATH_TO_TEMPLATE` is this template’s absolute directory; outputs should belong to the research project. The runner generates default and optional-title examples. When directly calling `plot_coefplot.do`, set the final title switch to `0` (argument order is in the corresponding README).

Unmodified coefplot 1.8.8 ado/help/license files are bundled with the template; the runner adds only that project-local package directory. The figure displays supplied estimates and intervals without running regressions.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Both orientations in English and Chinese were executed in Python 3.12 and Stata 19, and all eight PNGs visually checked. The four-panel horizontal example has 32 rows; the single-panel vertical example has six, including one SE fallback. Four Stata logs contain completion markers. Single panels omit the top name by default; multiple panels retain outcome labels. Additional Stata checks reject a one-sided missing CI (expected rc=9) and inconsistent horizontal term order (expected rc=459); all four valid runs were repeated after repair. Five coefplot 1.8.8 Stata runs passed; 38 input rows and interval fallback were checked, and preferred estimates/intervals highlighted red. Figures were inspected; package plotting coordinates were not separately exported for independent numerical comparison. Single panels have no default title; multiple panels keep necessary names.

Canonical figure name: `coefficient_grouped_forest`
