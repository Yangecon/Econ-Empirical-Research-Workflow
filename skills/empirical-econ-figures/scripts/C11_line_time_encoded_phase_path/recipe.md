# C11 · Time-encoded phase trajectory

[English](recipe.md) · [中文](recipe.zh-CN.md)

`time_encoded_phase_path` · C11

Connect two supplied coordinate variables in year order, using phase grayscale and year labels to encode a historical path.

Classification: Historical population on x and real wages on y, connected by year. Although later analysis estimates a labor-demand model, Figure II itself displays the data relationship.

Tags: Time path, Phase trajectory, Trend, Phase path, Measurement, Line plot

## Sources and scope

[When Did Growth Begin? New Estimates of Productivity Growth in England from 1250 to 1870 (2025)](<https://doi.org/10.1093/qje/qjae046>); Figure II: Real Wages and Population; PDF p.5

The original page image and PDF caption have been checked; synthetic data demonstrate the drawing only.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run in the template directory:

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/phase_path.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/phase_path_stata.png" "en" "0"
```

Create the Stata output directory first. Python `--title` or final Stata argument `1` enables a title; `zh` uses Chinese. Titles and bottom notes are absent by default.

Connect strictly by increasing year, never by sorting x; a segment crossing a phase boundary belongs to the new phase. Input x/y already use their display scale: log population and log real wages in the source example. The script does not log them again. Source population comes from model estimation; the plot uses upstream supplied coordinates without re-estimating historical population or fitting the relationship. Default phases are early/middle/late, each requiring at least two consecutive points. All demonstration values are synthetic.

Shared drawing dependency: preserve this directory's relationship to sibling `_shared/line_geometry.py`; copy the shared module into the research project as well. Imports resolve relative to the script and permit execution from other working directories. The shared module only draws supplied lines or right-continuous steps; normalization, cumulative shares, fitted intervals, risk sets, and Greenwood intervals remain the responsibility of each adapter.

Use the supplied JSON to customize series/phases and axis units; omitting `--config` preserves the original example:

```shell
python plot.py --input custom_demo.csv --config custom_config.json --output YOUR_PROJECT/figures/custom.png --lang en
```

`--lang zh` uses Chinese labels and `--title` displays the configured title. This configuration extension is Python-only; any retained Stata entry point follows the original schema. C10 retains finite nonnegative values, date rules, and an explicit base period. C11 connects points in year order and must not reorder them by x.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

20 synthetic years, numerically identical English/Chinese outputs across both implementations, preserving backward movement in x. Both implementations reject unsorted years and noncontiguous repeated phases. Default and titled versions were executed and default figures visually checked. Main acceptance added integer checks for annotated years and support for extra CSV columns. After adopting shared line/step geometry, reruns from a different working directory reproduced accepted default coordinates within 1e-10; statistical adapters were retained and C13 bars were unchanged. External series/phase IDs, Chinese labels, and optional-title examples were executed; invalid values or phase/year order are rejected.

Canonical figure name: `line_time_encoded_phase_path`
