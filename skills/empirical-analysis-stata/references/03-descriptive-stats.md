# Step 3 - Descriptive Statistics and Table 1

Goal: produce a clean descriptive picture of the sample before modeling.

## Use this reference for

- `summarize`
- `tabstat`
- `estpost tabstat`
- `balancetable`
- treated-versus-control comparisons

## Default checklist

1. Show sample size and key variable coverage.
2. Report means, standard deviations, and meaningful percentiles.
3. For treatment designs, compare treated and control groups.
4. Put a complete, labeled Table 1 on its own sheet in the consolidated `output/tables/results_tables.xlsx`.
5. Keep Table 1 separate from causal claims.

Use the summary-statistics layout and notes contract in `references/08-tables-plots.md`; `references/09-table-examples.md` shows an illustrative sheet.

## Canonical commands

```stata
summarize outcome treatment controls
summarize outcome treatment controls, detail

tabstat outcome treatment age edu tenure, ///
    statistics(n mean sd p25 p50 p75 min max) columns(statistics)

estpost tabstat outcome treatment age edu tenure, ///
    statistics(n mean sd p50 min max)
esttab . using "output/raw/table1_summary.csv", replace csv ///
    cells("count mean sd p50 min max") nonumber nomtitle
```

The CSV is a staging file. The default deliverable is the single XLSX results workbook. If the design needs treated-versus-control balance, use `balancetable` or an equivalent method and add that balance table as its own sheet; include group definitions and the difference/inference method.

## Hard rules

- Do not let Table 1 become a dumping ground for every variable in the dataset.
- Prefer variables that define scale, comparability, or sample construction.
- Keep causal interpretation out of Step 3.

## Common outputs

- `results_tables.xlsx` with one `Table 1 Summary` sheet and, if relevant, a separate balance sheet
- reproducible staging data under `output/raw/`
- quick sample diagnostics for the draft
