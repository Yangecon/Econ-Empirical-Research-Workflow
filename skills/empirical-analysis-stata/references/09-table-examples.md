# Table layout examples

These examples illustrate workbook structure. All numbers are illustrative and must never be used as research results. The layout draws on the supplied four-column regression screenshot and two inspected project patterns: a multi-sheet regression workbook with one model-by-column table per sheet, and a summary-statistics workbook reporting variable-level `N`, moments, and percentiles. The example adds a defined pre-treatment mean, model statistics, concrete notes, and three-line formatting.

## One XLSX results workbook

`output/tables/results_tables.xlsx`:

| Sheet | Contents |
| --- | --- |
| `Table 1 Summary` | One summary-statistics table and its note |
| `Table 2 Main` | One main regression table and its note |
| `Table 3 Mechanism` | One mechanism table, if estimated |
| `Table 4 Heterogeneity` | One heterogeneity table, if estimated |
| `Table 5 Robustness` | One robustness table, if estimated |

Add or omit sheets to match the actual analysis. Keep the sheet names short and stable. Do not fill a sheet with several unrelated tables or replace `Table 2 Main` with a long list of coefficient records.

## Example: `Table 1 Summary`

**Table 1. Summary statistics for author-year observations** (illustrative numbers)

| Variable | N | Mean | SD | Min | P25 | Median | P75 | Max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Papers published per year | 5,000 | 1.500 | 0.800 | 0.000 | 0.900 | 1.400 | 2.000 | 4.800 |
| Housing-shock exposure | 5,000 | 0.250 | 0.160 | 0.000 | 0.120 | 0.220 | 0.340 | 0.950 |
| Years since doctorate | 4,920 | 12.300 | 3.100 | 2.000 | 10.000 | 12.000 | 14.000 | 23.000 |

**Note:** This table summarizes author-year observations from 2000 to 2019 in the illustrative housing-shock study. Papers published per year counts each author's publications in a calendar year. Housing-shock exposure is the cumulative 2007–2008 growth in the FHFA House Price Index for the author's residence ZIP code at home purchase. Years since doctorate is measured at the observation year. `N` is the number of nonmissing observations for each variable; no weights are applied. These invented descriptive figures are independent of the regression example below.

In XLSX, place a top horizontal rule above the column headings, a middle rule below them, and a bottom rule below the final variable row. Put the note in visible cells beneath that bottom rule; do not use vertical borders or the default Excel grid as the table's borders.

## Example: `Table 2 Main`

**Table 2. Housing shocks and annual publication counts** (illustrative PPML numbers)

| VARIABLES | (1) | (2) | (3) | (4) |
| --- | ---: | ---: | ---: | ---: |
| Dependent variable | Papers_Total | Papers_Total | Papers_Total | Papers_Total |
| Exposure × I_Post | -0.024*** | -0.022*** | -0.019*** | -0.020*** |
|  | (0.002) | (0.002) | (0.002) | (0.003) |
| Pre-treatment mean of Y | 0.396 | 0.396 | 0.152 | 0.156 |
| Number of Clusters | 57,124 | 57,124 | 57,124 | 57,024 |
| Final Observations | 824,261 | 824,261 | 1,142,354 | 1,123,152 |
| Pseudo R-squared | 0.041 | 0.043 | 0.056 | 0.059 |
| Initial Observations | 1,357,860 | 1,357,860 | 1,357,860 | 1,357,860 |
| Author × Years of Holding FE | Yes | Yes | Yes | Yes |
| Year FE | Yes | No | No | No |
| Field-Year FE | No | Yes | Yes | No |
| State-Year FE | No | No | Yes | No |
| County-Year FE | No | No | No | Yes |
| Cluster level | Author | Author | Author | Author |

**Note:** This table presents Poisson pseudo-maximum likelihood (PPML) estimates of the effect of housing shocks on authors' annual publication counts. The dependent variable, `Papers_Total`, is the number of papers an author published in a given year. `Exposure` is ZIP-code-level cumulative growth in the FHFA House Price Index from 2007 to 2008, matched to the author's residence ZIP code at home purchase. `I_Post` equals one after 2008, so the displayed coefficient is on their interaction. The sample contains author-year observations from 2000 to 2019. The pre-treatment mean is calculated within each column's estimation sample using observations through 2008. `Initial Observations` counts eligible author-year rows before model-specific missing-value and singleton exclusions; `Final Observations` is the fitted sample. Pseudo R-squared denotes the estimator-reported fit measure. Standard errors are clustered at the author level and reported in parentheses. No weights are applied. `***`, `**`, and `*` denote significance at the 1%, 5%, and 10% levels, respectively.

This example follows the screenshot's column and row structure; the numbers, including pseudo R-squared, are illustrative and do not establish that the screenshot's PPML output reported this fit measure. In an actual PPML table, verify and name the estimator's fit measure or omit the row when none is appropriate. In XLSX, place the top rule above `(1)`–`(4)`, the middle rule below the dependent-variable header, and the bottom rule below `Cluster level`; place the note beneath it.

For an actual workbook, put the title above the table and notes beneath it as ordinary visible cells. Keep full-precision model results in reproducible source outputs; display precision in the workbook should not change stored estimates. If the paper table suppresses controls, retain the requested complete regression table as a separate sheet or output, and label the difference.
