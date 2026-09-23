Stata-first applied econ templates with project-root detection, relative paths, and a default 8-step pipeline structure.

Included files:

- `00_build_sample.do`: raw-to-analysis-sample construction
- `_write_version_log.do`: per-script package and environment log writer
- `00_setup.do`: path globals and log setup
- `01_estimation.do`: baseline modeling plus core diagnostics
- `02_robustness.do`: robustness gauntlet skeleton
- `03_figures.do`: publication-ready figure exports
- `04_tables.do`: stage Table 1 and main regression table as raw CSVs
- `99_master.do`: one-command entrypoint

Each `.do` file should append its own package/version footprint to:

- `output/raw/stata_version_log.csv`

The `.do` templates are project scaffolds. Their CSVs under `output/raw/` are inputs for the default single `output/tables/results_tables.xlsx` workbook. Put one complete table and its note on each sheet. Do not mark output ready until that workbook is built and checked against the stored Stata estimates. See `skills/empirical-analysis-stata/references/08-tables-plots.md` for the format contract and `09-table-examples.md` for illustrative sheets. Export Word or TeX only when requested.
