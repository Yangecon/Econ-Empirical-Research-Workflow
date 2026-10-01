# B04 · Set-identified impulse-response bounds

[English](recipe.md) · [中文](recipe.zh-CN.md)

`set_identified_impulse_response_bounds` · B04

Display horizon-specific admissible response bounds, pointwise medians and a supplied representative maxG path separately.

Classification: An event-restricted panel VAR selects structural-shock response matrices from the reduced-form covariance and plots admissible-set bounds; these are not confidence bands.

Tags: IRF, Partial identification, Identified bounds, SVAR, Line plot

## Sources and scope

[Using Disasters to Estimate the Impact of Uncertainty (2024)](<https://doi.org/10.1093/restud/rdad036>); Figure 3; PDF p.20

The original page image and PDF caption were checked; synthetic data demonstrate only the drawing method.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run inside the template directory:

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/set_bounds.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/set_bounds_stata.png" "en" "0"
```

Create the Stata output parent directory first. Python `--title` or the last Stata argument `1` enables an overall title; `zh` switches to Chinese. Defaults omit overall titles and bottom notes.

Blue lines are horizon-specific minima/maxima of admissible response sets; green crosses are pointwise medians and red hollow circles are the supplied maxG path. There are no confidence or posterior intervals here. Marker shapes distinguish paths, not significance.

Input horizons must be unique and strictly increasing; both representative series lie within the bounds at each horizon. The connected pointwise median need not represent one jointly feasible structural solution. maxG feasibility and restrictions must be verified upstream; plotting does not re-solve the VAR, event restrictions or maximization problem.

Period 1 is the contemporaneous shock in the source. The example includes periods 1–15 and explicitly marks shock timing on the axis. If changing to a zero-based horizon or other units, update both scripts’ labels. GDP year-on-year growth responses are in percentage points. All example values are synthetic. Bounds excluding zero cannot be interpreted as sampling confidence intervals excluding zero.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Fifteen horizons have exactly matching English/Chinese Python/Stata outputs. Both reject medians outside admissible bounds and unordered horizons. English/Chinese defaults and title variants ran successfully; defaults were inspected. The x axis was corrected to identify period 1 as the contemporaneous shock.

Canonical figure name: `irf_set_identified_bounds`
