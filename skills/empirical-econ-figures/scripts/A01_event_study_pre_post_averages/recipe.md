# A01 · Event study with pre/post averages

[English](recipe.md) · [中文](recipe.zh-CN.md)

`event_study_with_pre_post_averages` · A01

Actual estimates from a 980-row balanced common-timing panel: dynamic effects, a pre mean including the normalized reference zero, a post mean, and the post-minus-pre DID contrast, with full-covariance intervals.

Classification: Actual estimates from a 980-row balanced common-timing panel: dynamic effects, a pre mean including the normalized reference zero, a post mean, and the post-minus-pre DID contrast, with full-covariance intervals.

Tags: Event study, DID-compatible display, Pre/post averages

## Sources and scope

Local reference; original paper unidentified

Supplemental analogue: [Alleviating Worker Shortages Through Targeted Subsidies: Evidence from Incentive Payments in Healthcare](<https://doi.org/10.3386/w32412>); Figure 5; PDF p.26

User-provided local synthetic plotting example; not a verified paper figure.

The NBER reference has six outcome panels, calendar dates, gray confidence bands and red period averages that exclude quarters around the reform. This demonstration has one relative-time panel estimated from a 980-row synthetic balanced panel. Its six-period pre mean includes the normalized reference zero; its eight-period post mean minus the pre mean equals static DID under the documented common-timing specification. This is a methodological analogue, not a reproduction of the NBER estimates, sample, windows or inference.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

Read the explicit input checks at the top of the code.

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run from the template directory, writing output to your project:

```shell
python event_study_with_pre_post_averages.py --output YOUR_PROJECT/figures
```

The default reads the bundled 980-row panel and actually estimates both static DID and the event study. To draw external saved estimates, pass both `--estimates` and `--covariance`. To regenerate the fixed-seed panel and its numerical outputs, run `estimate_demo_panel.py --output-dir YOUR_PROJECT/example_inputs`.

In Stata, set `PANEL_CSV` to the bundled panel, `OUT` to your project output and keep `MODE "demo"`; the native do-file independently estimates the same models. Paths are relative to Stata's current directory unless explicitly set. `MODE "csv"` reads saved estimates and full covariance; `MODE "estimation"` reads existing e(b)/e(V), with TIMES/COEFS configured for the estimator.

The six-period pre mean includes the normalized −1 zero; the eight-period post mean minus pre mean equals static DID in this common-timing, balanced-panel example. The normalized reference is a hollow circle with no individual CI. The difference and its full-covariance interval are exported to `_contrast.csv`; it is not a third shaded band. Read [the methodology](README.md) for assumptions, covariance scaling and numeric checks.

Optional `--ci-style cap` / `CI_STYLE "cap"` uses error bars; `--connect` / `CONNECT 1` connects the points. `--title "..."` / `TITLE "..."` enables a title. Defaults have no title or bottom notes. `--post-is-att` / `POST_IS_ATT=1` is deprecated and rejected.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

A balanced common-timing panel with 980 rows and 70 units (35 treated / 35 controls) was actually estimated and plotted in Python and Stata 19. Six pre periods include the normalized −1 zero; there are eight post periods. Full covariance, unit-cluster CR0 and normal 95% intervals are used. Cross-language means, post-minus-pre and intervals agree within 1e-12; an independent unit-change check passed. Both PNGs were visually inspected.

Canonical figure name: `event_study_pre_post_averages`
