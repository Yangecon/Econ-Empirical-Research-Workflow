---
name: research-empirics
description: Execute the frozen empirical design through data construction, estimation, robustness, output export, and run logging. Use for generic empirical execution across the project pipeline when the user asks to build the sample, run code, refresh output tables and figures, or record a new empirical run. Pair with `empirical-analysis-stata` when the task needs a Stata-first applied econ workflow. Triggers: run the empirics, build final sample, refresh output, run estimation, cleaned tables, cleaned figures, update run log.
---

# Research Empirics

## Purpose

Use this skill after the identification gate is frozen.

## Trigger phrases

- run the empirics
- build final sample
- refresh output
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

## Required tasks

1. Check that `notes/identification_status.json` is `freeze`.
2. Build or refresh the sample using `code/build/`.
3. Save final samples directly under `data/`.
4. Run estimation scripts from `code/`.
5. Save raw case-specific outputs under `output/raw/`.
6. Save cleaned paper-ready figures and tables under `output/figures/` and `output/tables/`.
7. Update `notes/run_log.md` with run date, entrypoint, data inputs, and major outputs.

If the project uses the default Stata applied econ stack, prefer the 8-step pipeline in `empirical-analysis-stata` for the substantive analysis logic.

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
