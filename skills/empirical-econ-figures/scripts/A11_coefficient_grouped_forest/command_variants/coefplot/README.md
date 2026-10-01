# A11 · `coefplot` package variant

[English](README.md) · [中文](README.zh-CN.md)

This is Ben Jann's `coefplot` alternative to the accepted manual grouped-coefficient forest. Both read the same synthetic CSV of supplied estimates and confidence endpoints; neither estimates a model. The package's documented matrix syntax `coefplot matrix(B), ci((2 3))` reads the estimate, lower endpoint, and upper endpoint from three matrix rows. The code follows the [author's repository and help](https://github.com/benjann/coefplot), using version 1.8.8 (22 August 2025). The unmodified ado, help, and license are bundled in project-local `packages/c`; package_manifest.json (`package_manifest.json`) records SHA-256 hashes and sources. No global package installation was made.

plot_coefplot.do (`plot_coefplot.do`) accepts `input.csv output.png en|zh robustness|subgroup horizontal|vertical 0|1 [package-dir]`. The input and output are required. run_demo.do (`run_demo.do`) accepts a template root, an **explicit input CSV path**, and an output directory. The runner writes English robustness and subgroup PNG/PDF figures, plus a titled English subgroup example. Default figures have no overall title or bottom notes; multi-panel robustness retains panel headings, while single-panel subgroup has no redundant subtitle. Effect units, category labels, zero lines, and the subgroup legend remain. The preferred robustness estimate and its interval are red, as in the manual figure, by splitting the preferred term into a second `coefplot` matrix series at the same position.

All five native Stata runs completed with `COEFPLOT_COMPLETE`; final figures were visually checked. Validation (`validation.json`) checks the 38 input rows (32 robustness and six subgroup), exact interval fallback for the one row with a supplied SE, complete panel/group coverage, output files, and terminal logs. The package receives the same numerical estimates and intervals as the manual plot. Its plotted coordinates were visually checked rather than exported for an independent numerical coordinate comparison. The demo remains synthetic and does not reproduce the source papers' estimates. See schema.md (`schema.md`) for the input contract and matrix mapping.


Example images and execution evidence are archived in the gallery; the installed skill contains code and inputs only. Supply the parent template demo.csv explicitly to run_demo.do.

Canonical figure name: `coefficient_grouped_forest`
