---
name: empirical-econ-figures
description: Draw empirical economics figures from explicit data or saved estimates using a curated library of paper-inspired Python and Stata templates. Use for event-study, coefficient, regression-result and descriptive figure requests; inspect the catalog for supported patterns and input schemas.
---

[English](SKILL.md) · [中文](SKILL.zh-CN.md)

This library contains 50 accepted source/method variants organized into 40 drawing targets, curated from the supplied 2021–2026 corpus of Top 5 journal papers (AER, QJE, JPE, Econometrica and REStud) plus selected NBER working papers. This covers six calendar-year labels and is not an exhaustive collection of all papers published in those outlets. Consult [the catalog](references/catalog.md) for implementations and validation limits. The final scope includes accepted implementations only; all candidate suggestions were declined, with none pending.

Start with the [40 grouped drawing targets](references/targets.md), choose a variant by analytical purpose and available input, then read its linked recipe. Result figures normally have Python and Stata versions; HonestDiD is an explicitly approved Stata-only exception. Descriptive figures may offer Python only. Use a supplied implementation rather than approximating its inference logic from its appearance.

Classify by the numbers being plotted: Reduced-form estimates, Structural-form estimates, Summary, Research design, or Prediction & algorithm evaluation. Heterogeneity, robustness, welfare, calibration, counterfactuals and drawing geometry are tags. A counterfactual need not be structural; a calibrated probability need not be an estimated structural parameter. Follow each catalog item's numeric-origin explanation. Old folder names are storage compatibility paths, not the current classification.

The catalog records merged drawing targets alongside accepted source-specific implementations. Reuse a line or scatter renderer when geometry is shared, while preserving distinct statistical inputs (risk sets, weights, reference periods, covariance and interval meaning). A merged target label does not imply that a universal executable interface already exists. Only accepted implementations belong in the executable catalog.

When choosing among similar plots or transferring to a different research topic, consult [the selection guide](references/selection_guide.md). Direct generated files to the working project, keeping the installed skill free of PNG outputs.

For installation, shared dependencies and the boundary with estimation and draft-sync stages, read [environment and workflow integration](references/setup.md).

## Shared conventions

- Default: no title, subtitle, caption, or bottom notes in the rendered figure. Enable a title only when requested. Preserve axis labels, units, legends and useful panel labels. Put attribution and statistical notes in the accompanying Markdown or draft.
- Stable snake_case filenames; white background, restrained colors, readable legends. Save PNG for inspection and vector PDF for the paper when supported.
- Event studies default to reference period -1. For event studies and other estimated dynamic effects, use filled markers when the displayed interval excludes zero and hollow markers otherwise. Document the interval level and whether it is frequentist or posterior. Reference normalization is not an estimated effect or a significance test.
- Apply that marker rule to confidence or posterior intervals, not to set-identified bounds or scenario envelopes. A set-bound template uses markers to distinguish supplied paths; zero exclusion by its bounds is not statistical significance.
- Plot the supplied estimator's results. Record confidence level, pointwise/simultaneous status, reference period, weighting, sample and clustering outside the image. A visual pattern never establishes causal identification.
- Pre/post averages require the full covariance matrix: each mean has variance w'Vw, and the post-minus-pre contrast has variance (w_post-w_pre)'V(w_post-w_pre). In A01's balanced, common-timing panel with the same sample/window, no additional controls and no regression weights, include the normalized reference zero in the pre-period denominator; post minus pre then equals static DID. Do not label the post height itself DID or ATT under this normalization, or assume the identity for staggered timing, unbalanced panels or different specifications.
- Synthetic examples demonstrate drawing methods; never describe them as replicated paper results. Preserve source-paper/figure attribution and numerical-data status in the recipe.
- Validate the input schema and inspect the exported image. Report whether each language was actually executed; static review alone is not a successful Stata run.

## Command-driven inference figures

For staggered DID, run the simulated-data estimation pipeline before drawing: six actual Stata estimators including `jwdid` export a common table for Stata/Python. Preserve each estimator's support and preperiod interpretation; never synthesize missing coefficients to align curves.

For HonestDiD, use the `honestdid_sensitivity` recipe. Run an event-study estimator on data and pass the ordered coefficients and full covariance to `honestdid`; draw separate relative-magnitude and smoothness sensitivity intervals with the package. Specify the target post-period contrast, omitted baseline and M grid outside the graph. A robust interval's midpoint is not a new effect estimate. Smoothness M=0 permits a linear differential trend and is not the conventional parallel-trends interval. Do not treat package success as validation of identifying assumptions.

## Portable resources

The catalog links each available recipe and corresponding code. No PNG files belong inside this skill; visual previews and source crops live in the separate gallery. The project-level requirements and validation report describe the tested environment.

For workflow routing, [catalog.json](references/catalog.json) provides accepted template IDs, categories, languages, entrypoints, schemas and example inputs. Paths are relative to the skill root. Read the selected recipe before invocation: the templates have purpose-specific input contracts and do not assume one universal command interface.


Generate English figures only by default; do not generate a second Chinese copy. The English and Chinese documentation pages are independent of the figure language. Older validation records may describe historical Chinese test renders.

## Host workflow handoff

In this repository, use [the integration guide](references/workflow_integration.md) for estimation-to-figure-to-draft routing and catalog discovery. Project-wide empirical gates remain the host workflow's responsibility. For a standalone plotting request, use the supplied observations or saved estimates and the selected recipe without scaffolding a new research project. Never use gallery example values as project results.
