# C14 · Kaplan–Meier survival panels

[English](recipe.md) · [中文](recipe.zh-CN.md)

`kaplan_meier_survival_panels` · C14

Calculate Kaplan–Meier step survival curves from durations and right-censoring indicators, optionally displaying pointwise Greenwood normal intervals.

Classification: Grouped survival curves from raw employment spells, including referral groups and randomized treatment-group comparisons; the caption defines survival by days since hiring. Do not automatically treat nearby covariate-adjusted hazard regressions as this figure's input. An RCT context tag is possible; a separately plotted regression-adjusted treatment effect belongs in Reduced-form.

Tags: Survival, Kaplan–Meier, Censoring

## Sources and scope

[What Do Employee Referral Programs Do? Measuring the Direct and Overall Effects of a Management Practice (2023)](<https://doi.org/10.1086/721735>); 3; PDF p.20

The original page image and PDF caption have been checked; synthetic data demonstrate the drawing only.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Three source variants share one Python CLI, differing only in statistical adapters and inputs. Run in this template directory:

```shell
python plot.py kaplan_meier_survival_panels --input f39_spells.csv --ci --output-prefix YOUR_PROJECT/figures/f39
```

`--title "标题"` enables an optional title; `--xlabel` / `--ylabel` customize axis names. No title or bottom notes appear by default. `_checked.csv` is also exported for checking. The original paper's statistical tests are not added automatically. Only Python is accepted for the current Summary variants. The three portable directories' plot.py files are synchronized copies of one implementation, not three independent line algorithms.

Shared drawing dependency: preserve this directory's relationship to sibling `_shared/line_geometry.py`; copy the shared module into the research project as well. Imports resolve relative to the script and permit execution from other working directories. The shared module only draws supplied lines or right-continuous steps; normalization, cumulative shares, fitted intervals, risk sets, and Greenwood intervals remain the responsibility of each adapter.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Python was executed and visually checked by the main agent. Shared-adapter tests passed for hand-calculated risk sets, tied failures/censoring, Greenwood calculations, all-failure cases, missing months, and invalid inputs. An independent portable-directory rerun returned rc=0; no reproduction of the original paper's values is claimed. After adopting shared line/step geometry, reruns from a different working directory reproduced accepted default coordinates within 1e-10; statistical adapters were retained and C13 bars were unchanged. An argparse help-text percent-sign issue that caused --help to fail was also fixed; only text changed, and the help command passed execution.

Canonical figure name: `survival_kaplan_meier`
