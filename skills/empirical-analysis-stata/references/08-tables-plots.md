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
3. Show per-column specification rows for controls, fixed effects, sample restrictions, and weights when they vary. Use `Yes`, `No`, or `N/A` accurately.
4. Show per-column `Observations` and `Mean of Y`. Show `Num. of clusters` whenever standard errors are clustered. Add `R-squared` or an appropriate model-fit measure only where meaningful. Add design-specific statistics, such as first-stage F or RD bandwidth, where needed to interpret the results.
5. Put complete notes below the table. State outcome units or transformation, estimation sample and restrictions, estimator, standard-error method and clustering level, fixed effects, weights when used, significance thresholds, and relevant omitted category or design detail. Define abbreviations. Notes must describe the actual columns, not a generic template.

Calculate `Mean of Y` separately on each model's estimation sample (`e(sample)`), using that model's dependent-variable definition and analytic weights where applicable. For a binary outcome, report the 0–1 mean; explain percentage-point interpretations in the note. Obtain `Num. of clusters` from the fitted estimator's metadata or count distinct nonmissing cluster IDs in that model's estimation sample, and check agreement with the variance estimator. With multiple cluster dimensions, label and report each dimension. Never use zero or a copied value for an unavailable statistic; use a blank or `N/A` cell with an explanatory note.

Use a consistent display rule across models and formats: normally three decimal places for coefficients and standard errors, more where the outcome scale requires it; standard errors directly below coefficients; `*** p<0.01`, `** p<0.05`, `* p<0.10`. Keep unrounded model results available for regeneration. Do not infer significance from rounded displayed values.

## Workbook layout and optional formats

- **Default XLSX:** Use one workbook for the run. Give every sheet a short, stable table name (Excel's 31-character limit). Place a clear title, model or statistic headers, table body, footer statistics, and ordinary-cell notes below the table. Align numeric columns, use consistent number formats, readable widths, light horizontal rules, and no full-cell grid or unnecessary vertical borders. Keep numerical summary statistics as numbers; coefficient display cells may contain significance stars, while unrounded estimates remain in the stored results. Check each sheet at normal zoom and in print layout.
- **CSV, when requested:** Export each table as a rectangular file with its title/header, coefficient and parenthesized-SE rows or descriptive-statistic rows, footer statistics, and a `Notes` row or paired notes file. Quote cells correctly; use UTF-8 with BOM if opened directly in Windows Excel. A CSV cannot hold multiple sheets, so name files to map clearly to the workbook sheets.
- **Word, when requested:** Produce a genuine, openable `.docx` or `.doc` table with title and notes, aligned model columns, and no vertical borders. Inspect the rendered page. Do not give TeX or RTF content a Word extension.
- **TeX, when requested:** Produce a compilable `booktabs` table or tabular snippet consistent with the draft's input convention, with title/caption and notes. Escape special characters and verify the table after compilation.

Check that every requested output has the same table count, model columns, row labels, key displayed cells, sample statistics, and notes. If an optional format fails, report that file as incomplete rather than silently substituting another format.

## Stata implementation

Attach statistics immediately after each fitted model, before another estimation replaces `e(sample)`. Adapt for weighted estimates, transformed outcomes, and estimator-specific `e()` returns. For example:

```stata
quietly reghdfe outcome treatment, absorb(unit_id year) vce(cluster unit_id)
quietly summarize outcome if e(sample), meanonly
estadd scalar mean_y = r(mean)
* Check the estimator's stored cluster count before using it.
estadd scalar n_clusters = e(N_clust)
estimates store m1
```

`esttab`/`estout` can stage a model-by-column CSV under `output/raw/` using `stats(N mean_y n_clusters r2, labels("Observations" "Mean of Y" "Num. of clusters" "R-squared"))` when those statistics apply. Build the consolidated XLSX from these staged results and the Table 1 data; confirm one complete table and note per sheet. Use `esttab` TeX export or a genuine Word writer/converter only if those formats are requested. Changing a filename extension does not convert a file format; do not use `outreg2 ..., tex` with a `.doc` filename.

## Figures

Use `coefplot`, `binscatter`, `marginsplot`, `rdplot`, or clean `twoway` graphs as appropriate. Keep readable labels, white backgrounds, grayscale legibility, stable names, and PDF/PNG exports when downstream workflows need both.
