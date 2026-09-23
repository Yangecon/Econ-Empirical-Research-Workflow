# Table layout examples

These examples illustrate workbook structure; the numbers below are invented and must never be used as research results. The layout draws on two inspected project patterns: a multi-sheet regression workbook with one model-by-column table per sheet, and a summary-statistics workbook reporting variable-level `N`, moments, and percentiles. The inspected regression sheets did not consistently include `Mean of Y` or a full note, so the example adds those required elements.

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

**Table 1. Summary statistics for the analytic panel** (illustrative numbers)

| Variable | N | Mean | SD | Min | P25 | Median | P75 | Max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Outcome (units) | 5,000 | 1.500 | 0.800 | 0.000 | 0.900 | 1.400 | 2.000 | 4.800 |
| Treatment share | 5,000 | 0.250 | 0.160 | 0.000 | 0.120 | 0.220 | 0.340 | 0.950 |
| Baseline covariate (years) | 4,920 | 12.300 | 3.100 | 2.000 | 10.000 | 12.000 | 14.000 | 23.000 |

**Notes:** Unit of observation: unit-year. State the actual years, restrictions, variable definitions, transformations, and weights for the project. `N` is nonmissing observations for each variable; it need not be identical across rows. If adding `Zero share`, define its denominator. Do not infer the regression sample size from this table unless both samples are constructed identically.

## Example: `Table 2 Main`

**Table 2. Effect on outcome** (illustrative numbers)

|  | (1) | (2) | (3) |
| --- | ---: | ---: | ---: |
| Dependent variable | Outcome | Outcome | Outcome |
| Treatment | 0.120*** | 0.105** | 0.098* |
|  | (0.040) | (0.050) | (0.052) |
| Baseline covariate |  | 0.080** | 0.075* |
|  |  | (0.040) | (0.040) |
| Basic controls | No | Yes | Yes |
| Unit FE | No | Yes | Yes |
| Year FE | No | No | Yes |
| Observations | 5,000 | 4,920 | 4,920 |
| Mean of Y | 1.500 | 1.470 | 1.470 |
| Num. of clusters | 100 | 98 | 98 |
| R-squared | 0.040 | 0.220 | 0.310 |

**Notes:** Replace this example with the actual outcome definition and units, analytic sample, estimator, weight choice, and clustering level. Standard errors are in parentheses and clustered at the unit level in this example. `Mean of Y` and cluster counts refer to each column's estimation sample. `*** p<0.01`, `** p<0.05`, `* p<0.10`. Identify any omitted category or estimator-specific statistic needed to read the actual table.

For an actual workbook, put the title above the table and notes beneath it as ordinary visible cells. Keep the full-precision model results in reproducible source outputs; display precision in the workbook should not change the stored estimates. If the paper table suppresses controls, retain the requested complete regression table as a separate sheet or output, and label the difference.
