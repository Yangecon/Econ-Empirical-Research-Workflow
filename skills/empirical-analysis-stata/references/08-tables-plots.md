# Step 8 - Descriptive Tables, Regression Tables, and Plots

Export complete descriptive and regression tables from reproducible results. Apply this contract to Table 1, main, mechanism, heterogeneity, and robustness tables. A coefficient-only summary, screenshot, or copied Results-window text does not satisfy a regression-table deliverable. See [table examples](09-table-examples.md) for concrete layouts based on the structure of inspected project workbooks; example numbers there are illustrative.

## Default workbook

For a full empirical run, write one consolidated `output/tables/results_tables.xlsx` (or a project-specific stable name). Put each distinct summary-statistics or regression table on its own named sheet, with one reader-facing table and its notes on that sheet. Keep Table 1 and main results first, then mechanism, heterogeneity, robustness, and appendix tables as applicable. A raw long-form estimate dataset can be retained under `output/raw/` for audit, but cannot replace the model-by-column table.

Do not create a separate XLSX for every table by default. Do not also export CSV, Word, or TeX by default; produce those only when requested or required by a downstream draft/submission step. When another format is requested, render it from the same stored estimates and table specification, then check labels, displayed values, statistics, and notes against the workbook. An explicit user or project convention takes precedence over this default.

## Summary-statistics table

Use the analytic sample relevant to the reported regressions and state the unit of observation and sample period. Default columns: `Variable`, `N`, `Mean`, `SD`, `Min`, `P25`, `Median`, `P75`, `Max`. Add `Zero share` or treated/control group columns only when they clarify the data; define their denominators. Use readable variable names with units or transformations, group outcome/treatment/control variables with light section labels when useful, and retain variable-specific `N` where missingness differs. A balance table is separate from ordinary summary statistics and should show group definitions and the difference/inference method.

Put notes directly below the table: analytic sample, observation unit, period, weights if any, variable transformations, treatment/control definitions if shown, and the meaning of missing or zero values. Do not invent or silently harmonize `N` across variables.

## Regression-table content

Use one canonical model-by-column layout within each regression sheet. If a paper-facing table hides controls for readability, retain the complete requested raw regression table separately and state what was hidden.

1. Put a descriptive title above the table. Number model columns `(1)`, `(2)`, etc. Identify the dependent variable; label estimator or sample in the header when columns differ.
2. Show every focal estimated coefficient with its standard error in parentheses on the following row. Include other estimated terms required for the requested raw table. Do not replace the table with a long coefficient inventory.
3. Directly below the coefficient and standard-error block, use this default statistics order: `Pre-treatment mean of Y`, `Number of Clusters`, `Final Observations`, then `R-squared` (or a clearly named estimator-appropriate fit statistic). Add `Initial Observations` when a sample-flow comparison is meaningful; define how both counts were obtained. If the design has no well-defined pre-treatment period, label the first row `Mean of Y` instead. If inference is not clustered, omit the cluster row. Do not invent an ordinary R-squared for PPML or another estimator that does not report one; use an explicitly defined pseudo R-squared only when available, otherwise omit that row.
4. After the statistics, show per-column specification rows for controls, fixed effects, sample restrictions, weights, and clustering level when they vary or help interpret the columns. Use `Yes`, `No`, or `N/A` accurately. Add design-specific statistics, such as first-stage F or RD bandwidth, where needed.
5. Put complete notes below the bottom rule. Open with a concrete sentence of the form `Note: This table presents [estimator] estimates of the effect of [X] on [Y].` Then define the dependent variable, treatment/exposure and timing, sample and period, estimator, standard-error method and clustering level, weights and key restrictions where relevant, and significance thresholds. Notes must describe the actual columns, not tell the reader to fill in a template. See [the concrete note example](09-table-examples.md).

Calculate `Pre-treatment mean of Y` separately within each model's estimation sample (`e(sample)`) restricted to a pre-treatment period defined by the actual design. State that period in the note when it is not obvious. If no pre-treatment period is defined, calculate and label `Mean of Y` on the full model estimation sample. Use the model's dependent-variable definition and analytic weights where applicable. For a binary outcome, report the 0–1 mean; explain percentage-point interpretations in the note. Obtain `Number of Clusters` from the fitted estimator's metadata or count distinct nonmissing cluster IDs in that model's estimation sample, and check agreement with the variance estimator. With multiple cluster dimensions, label and report each dimension. Never use zero or a copied value for an unavailable statistic; use a blank or `N/A` cell with an explanatory note.

Use a consistent display rule across models and formats: normally three decimal places for coefficients and standard errors, more where the outcome scale requires it; standard errors directly below coefficients; `*** p<0.01`, `** p<0.05`, `* p<0.10`. Keep unrounded model results available for regeneration. Do not infer significance from rounded displayed values.

## Workbook layout and optional formats

- **Default XLSX:** Use one workbook for the run. Give every sheet a short, stable table name (Excel's 31-character limit). Place a clear title, model or statistic headers, table body, footer statistics, and ordinary-cell notes below the table. Use a three-line table: a top horizontal rule above the header, a middle rule below the header, and a bottom rule below the table body and above the note. Use whitespace for section separation; avoid vertical borders and full-cell grids. Align numeric columns, use consistent number formats and readable widths. Keep numerical summary statistics as numbers; coefficient display cells may contain significance stars, while unrounded estimates remain in the stored results. Check each sheet at normal zoom and in print layout.
- **CSV, when requested:** Export each table as a rectangular file with its title/header, coefficient and parenthesized-SE rows or descriptive-statistic rows, footer statistics, and a `Notes` row or paired notes file. Quote cells correctly; use UTF-8 with BOM if opened directly in Windows Excel. A CSV cannot hold multiple sheets, so name files to map clearly to the workbook sheets.
- **Word, when requested:** Produce a genuine, openable `.docx` or `.doc` table with title and notes, aligned model columns, and the same three horizontal rules, without vertical borders. Inspect the rendered page. Do not give TeX or RTF content a Word extension.
- **TeX, when requested:** Produce a compilable `booktabs` table or tabular snippet consistent with the draft's input convention, using `\toprule`, `\midrule`, and `\bottomrule`, with title/caption and notes. Escape special characters and verify the table after compilation.

Check that every requested output has the same table count, model columns, row labels, key displayed cells, sample statistics, and notes. If an optional format fails, report that file as incomplete rather than silently substituting another format.

## Stata implementation

Attach statistics immediately after each fitted model, before another estimation replaces `e(sample)`. Adapt for weighted estimates, transformed outcomes, and estimator-specific `e()` returns. For example:

```stata
quietly reghdfe outcome treatment, absorb(unit_id year) vce(cluster unit_id)
* pre_period == 1 must be defined from the actual treatment timing.
quietly summarize outcome if e(sample) & pre_period == 1, meanonly
estadd scalar pre_mean_y = r(mean)
* Check the estimator's stored cluster count before using it.
estadd scalar n_clusters = e(N_clust)
estimates store m1
```

`esttab`/`estout` can stage a model-by-column CSV under `output/raw/` with `stats(pre_mean_y n_clusters N r2, labels("Pre-treatment mean of Y" "Number of Clusters" "Final Observations" "R-squared"))` for a model where those statistics apply. If no pre-treatment period exists, replace `pre_mean_y` and its label with a correctly computed full-sample `mean_y` and `Mean of Y`. Build the consolidated XLSX from staged results and Table 1 data; confirm one complete three-line table and concrete note per sheet. Use `esttab` TeX export or a genuine Word writer/converter only if those formats are requested. Changing a filename extension does not convert a file format; do not use `outreg2 ..., tex` with a `.doc` filename.

## Figures

Use `coefplot`, `binscatter`, `marginsplot`, `rdplot`, or clean `twoway` graphs as appropriate. Keep readable labels, white backgrounds, grayscale legibility, stable names, and PDF/PNG exports when downstream workflows need both.
