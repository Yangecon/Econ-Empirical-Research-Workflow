# Step 8 - Regression Tables and Plots

Export complete regression tables from stored model results. Apply this contract to main, mechanism, heterogeneity, and robustness tables. A coefficient-only summary, screenshot, or copied Results-window text does not satisfy the table deliverable.

## Required table content

By default, export each regression table as CSV, XLSX, DOC, and TeX from one canonical layout. All formats must have the same model columns, row order, displayed values, significance marks, and substantive notes. Follow an explicit narrower format request when the user specifies one.

1. Put a descriptive title above the table. Number model columns `(1)`, `(2)`, etc. Identify the dependent variable; label estimator or sample in the header when columns differ.
2. Show every focal estimated coefficient with its standard error in parentheses on the following row. Include other estimated terms required for the requested **raw** table. If a shorter paper table hides controls, retain a separately named full regression table and state which terms were hidden.
3. Show per-column specification rows for controls, fixed effects, sample restrictions, and weights when they vary. Use `Yes`, `No`, or `N/A` accurately.
4. Show per-column `Observations` and `Mean of Y`. Show `Num. of clusters` whenever standard errors are clustered. Add `R-squared` or an appropriate model-fit measure only where meaningful. Add design-specific statistics, such as first-stage F or RD bandwidth, where needed to interpret the results.
5. Put complete notes below the table. State outcome units or transformation, estimation sample and restrictions, estimator, standard-error method and clustering level, fixed effects, weights when used, significance thresholds, and relevant omitted category or design detail. Define abbreviations. Notes must describe the actual columns, not a generic template.

Calculate `Mean of Y` separately on each model's estimation sample (`e(sample)`), using that model's dependent-variable definition and analytic weights where applicable. For a binary outcome, report the 0–1 mean; explain percentage-point interpretations in the note. Obtain `Num. of clusters` from the fitted estimator's metadata or count distinct nonmissing cluster IDs in that model's estimation sample, and check agreement with the variance estimator. With multiple cluster dimensions, label and report each dimension. Never use zero or a copied value for an unavailable statistic; use a blank or `N/A` cell with an explanatory note.

Use a consistent display rule across models and formats: normally three decimal places for coefficients and standard errors, more where the outcome scale requires it; standard errors directly below coefficients; `*** p<0.01`, `** p<0.05`, `* p<0.10`. Keep unrounded model results available for regeneration. Do not infer significance from rounded displayed values.

## Format-specific requirements

- **CSV:** A rectangular regression table with one row-label column and one column per model. Keep coefficients and parenthesized standard errors on separate rows, followed by specification and statistic rows. Put the full note in a final `Notes` row or a clearly paired notes CSV. Quote cells correctly; use UTF-8 with BOM when the file is intended for direct opening in Windows Excel.
- **XLSX:** A visible table sheet with the same rows and columns, title, and notes. Use readable widths, aligned model columns, and a print area that keeps the table legible. A long tidy coefficient dataset may be supplied as an extra sheet, but does not replace the regression table.
- **Word:** Produce a genuine, openable Word table. Use `.doc` when requested; `.docx` may supplement it. Include title and notes, align model columns, avoid vertical borders, and inspect the rendered page. Do not give TeX or RTF content a `.doc` extension.
- **TeX:** Produce a compilable `booktabs` table or tabular snippet consistent with the draft's input convention. Include title or caption and notes, escape special characters, and verify the rows after compilation.

Deliver the four default formats from the same stored estimates and canonical table data. Check that the model count, row labels, key cells, sample statistics, and notes match across exports before marking the bundle complete. If one format fails, repair or explicitly report that format as incomplete.

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

`esttab`/`estout` can generate matching TeX and CSV views using `stats(N mean_y n_clusters r2, labels("Observations" "Mean of Y" "Num. of clusters" "R-squared"))` when those statistics are applicable. Use a real spreadsheet writer for XLSX and Word or LibreOffice conversion for a genuine DOC; changing the filename extension does not convert the format. Do not use `outreg2 ..., tex` with a `.doc` filename.

## Figures

Use `coefplot`, `binscatter`, `marginsplot`, `rdplot`, or clean `twoway` graphs as appropriate. Keep readable labels, white backgrounds, grayscale legibility, stable names, and PDF/PNG exports when downstream workflows need both.

