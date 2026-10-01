# A09 · Residualized scatter with fitted relationships

[English](recipe.md) · [中文](recipe.zh-CN.md)

`residualized_scatter_panels` · A09

Multi-panel residual scatterplots, gray comparison groups, highlighted groups and fitted lines calculated from the input data.

Classification: Multi-panel residual scatterplots, gray comparison groups, highlighted groups and fitted lines calculated from the input data.

Tags: Residualization, Scatter, Group highlighting

## Sources and scope

Local reference; original paper unidentified; Figure 1

Supplemental analogue: [Population Aging and Structural Transformation](<https://doi.org/10.3386/w26327>); Figure A6; PDF p.38

The screenshot shows Figure 1; paper identity awaits verification against the primary materials.

NBER Figure A6 has three sector rows, raw observations in the left column and residualized observations in the right; it does not highlight groups. The screenshot has two residualized panels, highlights medicine/AI subsets, and compares research grants with research output. No claim that its Figure 1 comes from this NBER paper.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run inside the template directory, specifying the project output location:

```shell
python plot.py --input demo.csv --lang en --output YOUR_PROJECT/figures/residual_scatter.png
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/residual_scatter.png" en 0
```

Python `--title` or the last Stata argument `1` enables an overall title; it is off by default. `zh` switches to Chinese. Both implementations automatically export a matching PDF.

To customize two panels and 2–3 groups per panel, edit Python PANEL_GROUPS/GROUP_STYLES/TEXT or Stata panel/group IDs and label locals at the top; the main plotting loop need not change. Fits use every displayed point in each panel, including the gray comparison group. The template reads already-residualized rx/ry and does not choose fixed effects or generate residuals for users.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Generic-label revision on 2026-09-29: all four English/Chinese Python 3.12/Stata 19 figures were executed and visually inspected, with complete PNG/PDF outputs. Samples remain 440/200 and the input CSV hash is unchanged. Both implementations retain the accepted intercepts and slopes and agree to six decimal places.

Canonical figure name: `scatter_residualized_fit`
