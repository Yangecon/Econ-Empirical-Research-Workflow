---
name: research-empirics
description: "Execute the frozen empirical design through data construction, front-end visual diagnostics, estimation, robustness, output export, and run logging. Use for generic empirical execution across the project pipeline when the user asks to build the sample, diagnose data visually, run code, refresh output tables and figures, or record a new empirical run. Pair with `summary-visuals` for the figure specifications and `empirical-analysis-stata` when the task needs a Stata-first applied econ workflow. Triggers: run the empirics, build final sample, visual diagnostics, visualize the sample, descriptive figures, refresh output, run estimation, cleaned tables, cleaned figures, update run log."
---

# Research Empirics

## Purpose

Use this skill after the identification gate is frozen. The empirical front end is: build the exact analytic sample, inspect it through visual diagnostics, then estimate the pre-specified models.

## Trigger phrases

- run the empirics
- build final sample
- refresh output
- visual diagnostics
- visualize the sample
- descriptive figures
- cleaned tables
- cleaned figures
- update run log

## Folder rules

### Data

```text
data/raw/
data/build/
data/<final_sample>.dta
data/<final_sample>.csv
```

- `data/raw/` is read-only.
- `data/build/` stores constructed intermediate files.
- final samples live directly under `data/`.

### Code

```text
code/build/
code/00_setup.do
code/01_estimation.do
code/02_robustness.do
code/03_figures.do
code/04_tables.do
code/99_master.do
```

- `code/build/` stores sample-construction scripts.
- code root contains estimation, robustness, figures, tables, and master scripts.

### Output

```text
output/raw/
output/figures/
output/tables/
```

- `output/raw/` stores raw case-specific outputs.
- `output/figures/` stores cleaned paper-ready figures and figure files.
- `output/tables/` stores cleaned paper-ready tables and table files.

Do not prescribe the internal structure of `output/raw/`.

## Front-end visual diagnostics

Run visual diagnostics immediately after constructing the intended analytic sample and before the primary estimation. This is an empirical checkpoint, not a paper-figure polishing pass. Route the plotting work to `summary-visuals`; this skill specifies when the diagnostic runs and what must be recorded, without duplicating its figure recipes.

1. Record the analytic sample definition before plotting: input path and version/fingerprint, unit and time span, restrictions, constructed variables, transformations, and analytic weights.
2. Choose a small diagnostic set that fits the data and question rather than generating every chart. Start with coverage or trend and key-variable distributions. Add an **Agreement Scatter** when two paired measures of the same construct must be compared. Add a **Binned Conditional Scatter** when the conditional descriptive relationship between pre-specified x and y, after fixed effects or controls, needs to be inspected.
3. Use the same retained sample, weights, transformations, and--for conditional figures--the same residualization specification as the planned analysis. The figures are descriptive and cannot repair an inconsistent sample or substitute for the main model.
4. Put exploratory diagnostics under `work/<exploration_slug>/output/` with their code and run record. Once the analytic choices are settled, keep the reproducible diagnostic invocation in the project pipeline. Promote a diagnostic to `output/figures/` only when a human decides it belongs in the paper or formal deliverable.
5. If a diagnostic exposes a material sample, construction, support, or measurement problem, resolve and document it before estimating. If the resolution changes the frozen estimand, treatment, outcome, or identification assumptions, return to `research-identification` and re-freeze the design.

## Required tasks

1. Check that `notes/identification_status.json` is `freeze`.
2. Build or refresh the sample using `code/build/`.
3. Save final samples directly under `data/`.
4. Run and record front-end visual diagnostics through `summary-visuals` before the primary estimation.
5. Run estimation scripts from `code/`.
6. Save raw case-specific outputs under `output/raw/`.
7. Save cleaned paper-ready figures and tables under `output/figures/` and `output/tables/`.
8. Update `notes/run_log.md` with run date, entrypoint, data inputs, visual-diagnostic paths and decisions, and major outputs.

If the project uses the default Stata applied econ stack, prefer the 8-step pipeline in `empirical-analysis-stata` for the substantive analysis logic.

For descriptive and regression tables, apply `empirical-analysis-stata/references/08-tables-plots.md`: default to one XLSX workbook, with each sheet holding one complete table and its notes. Export other formats only when requested.

## Work folder rule

Exploratory analyses go under:

```text
work/<exploration_slug>/
```

Each exploration can have:

```text
work/<exploration_slug>/README.md
work/<exploration_slug>/code/
work/<exploration_slug>/output/
```

Do not merge work-folder outputs into the main `output/` unless a human explicitly promotes them.
