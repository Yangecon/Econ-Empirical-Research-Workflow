# C07 · Horizon-specific density ridgelines

[English](recipe.md) · [中文](recipe.zh-CN.md)

`horizon_density_ridgeline` · C07

Compare two measures' distributions using density curves by horizon, with a common bandwidth and height scale and separate accounting for zero and missing-value denominators.

Classification: Ridgelines show KDEs of price impact and profits over millisecond/second horizons. The source excludes exact-zero mass. Templates must explicitly include/exclude zero and report the exclusion share, sharing bandwidth rules, grids, and density-height scales rather than independently normalizing peaks. Vertical positions are categorical, not a real-time axis.

Tags: Density, Horizons, Ridgeline

## Sources and scope

[Quantifying the High-Frequency Trading ‘Arms Race’ (2022)](<https://doi.org/10.1093/qje/qjab032>); Figure V, panels A and B; PDF p.39

The original page image and PDF caption have been checked; synthetic data demonstrate the drawing only.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run in the template directory:

```shell
python plot.py --input outputs/synthetic_input.csv --outdir YOUR_PROJECT/figures/ridgeline --lang en
```

Use `--lang zh` for Chinese, requiring an available Chinese font; `--title` enables the overall title. Overall titles and bottom notes are absent by default; metric-panel names remain. `--bandwidth` specifies a common Gaussian bandwidth in basis points, default 0.55.

Default `--zero-policy exclude` removes exact zeros and computes conditional density using the nonzero valid sample count. `sample_counts.csv` retains raw, missing, zero, and final denominator counts for every metric and horizon. The figure cannot identify zero incidence; missing combinations are not automatically filled with zeros. `include` smooths zero observations as KDE inputs rather than separately showing discrete zero mass.

The five horizons in each panel share a horizontal grid, and both panels use one absolute density-to-height ratio. Peaks are not stretched to equal heights. Vertical positions are horizon categories, not linearly elapsed time. Densities normalize over the real line; tails outside the display are not redistributed. Source profits and price impact use different benchmark prices, to be constructed upstream. This template does not identify trading races or recalculate profits. The bandwidth and synthetic distributions are demonstration settings, not reproductions of paper values.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

6,000 synthetic rows produce ten curves (two metrics×five horizons), with a shared Gaussian bandwidth of 0.55 bps, a common 401-point grid in each panel, and one figure-wide height scale. Checks covered zero exclusion/inclusion, missing-value denominators, and rejection of all-zero groups. English and Chinese default/titled PNG/PDF outputs were executed and visually checked.

Canonical figure name: `distribution_horizon_ridgeline`
