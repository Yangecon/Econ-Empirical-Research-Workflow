Stata-first applied econ templates with project-root detection, relative paths, and a default 8-step pipeline structure.

Included files:

- `00_build_sample.do`: raw-to-analysis-sample construction
- `_write_version_log.do`: per-script package and environment log writer
- `00_setup.do`: path globals and log setup
- `01_estimation.do`: baseline modeling plus core diagnostics
- `02_robustness.do`: robustness gauntlet skeleton
- `03_figures.do`: publication-ready figure exports
- `04_tables.do`: Table 1 and main-table bundle
- `99_master.do`: one-command entrypoint

Each `.do` file should append its own package/version footprint to:

- `output/raw/stata_version_log.csv`
