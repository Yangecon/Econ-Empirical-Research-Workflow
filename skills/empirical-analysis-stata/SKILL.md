---
name: empirical-analysis-stata
description: Classical end-to-end empirical analysis workflow in the traditional Stata ecosystem for Default applied econ papers only. Use when Codex needs a reproducible `.do`-file pipeline for AER, QJE, or AEJ-style work, or when the user names a Stata step such as `reghdfe`, `ivreg2`, `csdid`, `rdrobust`, `synth`, `teffects`, `esttab`, `coefplot`, `boottest`, `ritest`, `bacondecomp`, `honestdid`, `rwolf`, `winsor2`, `balancetable`, or `binscatter`. Triggers: Stata empirical analysis, full Stata pipeline, reproducible do-file, reghdfe two-way FE, ivreg2 weak IV, csdid event study, rdrobust, synth, teffects matching, esttab LaTeX table, coefplot, robustness battery, applied micro Stata.
---

# Empirical Analysis Stata

This skill is the default Stata playbook for applied economics papers.

It is intentionally narrower than the reference skill it was adapted from:

```text
Default applied econ only
No epidemiology branch
No ML-causal branch
```

Use it when the user wants the full Stata pipeline, or when they ask for one named Stata step inside that pipeline.

## Trigger phrases

- Stata empirical analysis
- full Stata pipeline
- reproducible do-file
- applied micro Stata
- reghdfe two-way FE
- ivreg2 weak IV
- csdid event study
- rdrobust
- synth
- teffects matching
- esttab LaTeX table
- coefplot
- boottest
- ritest
- bacondecomp
- honestdid
- rwolf

## Philosophy

1. Use Stata idioms, not Python-translated analogies.
2. Prefer reproducible `.do` files over interactive one-off commands.
3. Treat cleaning, Table 1, diagnostics, robustness, and publication output as first-class steps.
4. Produce paper-ready artifacts, not just coefficients in the Results window.
5. Keep the main workflow in this file and deeper command catalogs in `references/`.

## Project files to inspect first

Read:

```text
README.md
project.yaml
notes/identification.md
notes/identification_status.json
notes/estimand_registry.csv
notes/robustness_plan.csv
notes/run_log.md
code/
output/
```

If identification is not frozen, stop and route back to `research-identification`.

## Canonical 8-step pipeline

Run the default applied econ pipeline in this order:

1. import and cleaning
2. variable construction
3. Table 1
4. diagnostic tests
5. baseline modeling
6. robustness gauntlet
7. mechanism and heterogeneity
8. publication-ready tables and figures

Do not jump straight to Step 5 unless the user explicitly asks for a local fix to an existing model script.

## Reference files

Use the matching reference file when a step needs more depth:

```text
references/01-data-cleaning.md
references/02-data-transformation.md
references/03-descriptive-stats.md
references/04-statistical-tests.md
references/05-modeling.md
references/06-robustness.md
references/07-further-analysis.md
references/08-tables-plots.md
```

## Default output contract

Unless the user explicitly asks for a single isolated estimate, aim to produce the full applied econ output set:

- `table1_balance` or equivalent descriptives
- `table2_main_results` as the centerpiece
- `table3_mechanism`
- `table4_heterogeneity`
- `table5_robustness`
- event-study, coefficient, RD, SCM, or binscatter figures when the design calls for them

Store:

- raw logs and scratch outputs under `output/raw/`
- cleaned paper-ready figures under `output/figures/`
- cleaned paper-ready tables under `output/tables/`

## The centerpiece table

The default centerpiece is a progressive main-results table. Do not collapse it to one column unless the user explicitly wants a one-off summary.

Canonical column logic:

```text
M1 raw relationship
M2 + basic controls
M3 + richer controls
M4 + unit FE
M5 + unit and time FE
M6 preferred specification
```

If the project's frozen design is IV, DID, RD, SCM, or matching, preserve the same logic:

- early columns establish comparability
- later columns move toward the preferred design

## Step 5 estimator menu

Choose the estimator family that matches the frozen design:

- HDFE baseline: `reghdfe`
- IV: `ivreg2` or `ivreghdfe`
- DID: `csdid`, `eventstudyinteract`, `did_imputation`, or `sdid`
- RD: `rdrobust`
- SCM: `synth` or `synth_runner`
- matching and reweighting: `teffects`, `psmatch2`, or `ebalance`

Use one main design as the centerpiece. Alternative designs usually belong in the robustness or appendix-style output set.

## Step 6 robustness gauntlet

Match the robustness battery to the identifying threat. The default toolkit includes:

- `bacondecomp` for TWFE decomposition
- `honestdid` for relaxed parallel-trends sensitivity
- `boottest` for wild-cluster bootstrap inference
- `ritest` for randomization inference
- `rwolf` for Romano-Wolf multiple-testing adjustment
- `psacalc` for Oster-style omitted-variable sensitivity

Do not force all six into every paper. Use the subset that matches the design.

## Step 7 further analysis

Default further-analysis outputs include:

- mechanism outcomes
- subgroup heterogeneity
- interactions
- event-study dynamics
- binscatter or margins-based interpretation plots

Keep Step 7 downstream of a stable baseline result. Do not lead with heterogeneity before the main estimate is credible.

## Step 8 publication-ready bundle

For tables, prefer:

- `esttab`
- `outreg2`
- `estout`

For figures, prefer:

- `coefplot`
- `binscatter`
- `marginsplot`
- `rdplot`
- clean `twoway` graphs

Figures should be:

- readable in grayscale
- exportable to PDF or PNG
- saved with stable names
- ready for `draft/` ingestion without manual renaming

## Stata package checklist

Before relying on a command, check that it exists in the environment. The default package set for this workflow is:

- `reghdfe`
- `ftools`
- `ivreg2`
- `ivreghdfe`
- `csdid`
- `did_imputation`
- `eventstudyinteract`
- `sdid`
- `bacondecomp`
- `honestdid`
- `rdrobust`
- `rddensity`
- `synth`
- `synth_runner`
- `psmatch2`
- `teffects`
- `ebalance`
- `boottest`
- `ritest`
- `rwolf`
- `estout`
- `outreg2`
- `coefplot`
- `winsor2`
- `balancetable`
- `binscatter`

If a needed package is missing, say so clearly and either install it if the user wants that action or fall back to the closest built-in workflow.

## Coding rules

- prefer one `99_master.do` entrypoint
- keep sample construction in `code/build/`
- keep root-level empirical scripts readable and sequential
- use globals from `00_setup.do` for paths
- write output files deterministically with stable names
- save intermediate datasets only when they are reused
- comment only where the identification logic or file contract would otherwise be unclear

## Deliverable

When finishing a task under this skill, report:

- which pipeline step changed
- which `.do` files or reference files were added or revised
- which tables or figures are now expected in `output/`
- which package assumptions still need human confirmation
