# B01 · Scenario-specific cumulative distribution panels

[English](recipe.md) · [中文](recipe.zh-CN.md)

`scenario_cdf_panels` · B01

Facet CDFs by scenario and compare groups with different line styles, distinguishing the x outcome, CDF and model-scenario assumptions.

Classification: The two-stage attention/discrete plan-choice model V varies attention probabilities and switching costs to simulate the CDF of changes in overspending.

Tags: Counterfactual, CDF, Scenario comparison, Line plot

## Sources and scope

[Heiss et al., Inattention and Switching Costs as Sources of Inertia in Medicare Part D (2021)](<https://doi.org/10.1257/aer.20170471>); Figure 10; PDF p.40

The page image and PDF caption were checked. The original figure is the empirical CDF of counterfactual reductions in overspending under Model V, not attention probabilities.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run inside this template directory:

```shell
python plot.py --input demo.csv --lang en --output YOUR_PROJECT/figures/scenario_cdf.png
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/scenario_cdf.png" en 0
```

Python `--title` or the last Stata argument `1` enables an overall title; `zh` switches to Chinese. A matching PDF is automatically exported. Edit top-level panel/group IDs and bilingual labels for two scenarios with three curves each. Numeric values determine x order; a CDF cannot be treated as an unordered ordinary line.

Inputs are precomputed cumulative-distribution points. The code does not estimate a structural model or construct policy counterfactuals. The original paper compares reductions in overspending across low-, medium- and high-acuity groups under forced attention and removal of switching costs. These example curves demonstrate only the plotting method.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Four English/Chinese Python 3.12/Stata 19 PNGs were executed and inspected, with PDF exports. The common CSV has 966 rows: two panels × three groups × 161 x points. Each curve is checked for unique x, CDF range and monotonicity.

Canonical figure name: `counterfactual_cdf_panels`
