# B05 · Policy counterfactual contours

[English](recipe.md) · [中文](recipe.zh-CN.md)

`policy_counterfactual_contours` · B05

Overlay a constant-acceptance line and contours of payment changes per visit on a policy grid of fees and denial probabilities.

Classification: A Bellman model of optimal claim resubmission and estimated costs, combined with estimated Medicaid-acceptance effects: policy simulation using mixed structural and reduced-form inputs.

Tags: Counterfactual, Policy grid, Contours, Mixed structural/reduced-form inputs, Contour plot

## Sources and scope

[A Denial a Day Keeps the Doctor Away (2024)](<https://doi.org/10.1093/qje/qjad035>); Figure VIII; PDF p.39

The original page image and PDF caption were checked; synthetic data demonstrate only the drawing method.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run inside the template directory:

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/policy_contours.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/policy_contours_stata.png" "en" "0"
```

Create the Stata output parent directory first. Python `--title` or the last Stata argument `1` enables an overall title; `zh` switches to Chinese. Defaults omit overall titles and bottom notes.

Input a complete two-dimensional policy grid and two precomputed outcome surfaces. X is percentage change in fees; y is relative percentage change in denial probability. +10 means d becomes 1.1d, not an increase of ten percentage points. The origin is the observed baseline and both outcome changes must be zero there. The black solid line is acceptance change=0; dashed values are payment changes per visit in dollars. They do not share outcome units.

Input rows may be unordered; scripts sort actual numeric coordinates and reject incomplete grids. When changing payment levels, update Python PAYMENT_LEVELS, the Stata level loop and range checks together. The code does not estimate a structural model or determine feasible policy-parameter ranges.

Python uses Matplotlib’s contour algorithm. Stata independently interpolates linearly along grid edges, with deterministic adjacent-edge pairing in saddle cells; curves can differ on coarse grids or highly nonlinear surfaces. Stata leaves small gaps in each segment to form dashes; full unbroken contours are separately retained in CSV as plot_style=4. Numerical validation includes analytic curve positions; pixel identity is not a pass condition.

The example contains 651 synthetic cells. Original model outputs and figure values are not recovered. The output _checked.csv is the grid and _contours.csv is contour evidence. Inspect label/line crossings again with new data and adjust label positions as needed.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Complete 651-cell grid with identical input numbers across languages. Independently extracted contours have maximum endpoint residual 4.08e-5 against analytic curves. Checks cover all nine payment levels in correct order and the zero-acceptance line through the origin. A horizontal-contour Stata fixture retains all levels. Both languages reject incomplete grids and an unnormalized origin. English/Chinese defaults and title variants were executed and inspected; missing dashed segments and Python label collisions were repaired.

Canonical figure name: `counterfactual_policy_contours`
