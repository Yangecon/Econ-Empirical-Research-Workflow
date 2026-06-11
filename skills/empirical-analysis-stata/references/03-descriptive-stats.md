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
4. Save a publication-ready Table 1 artifact.
5. Keep Table 1 separate from causal claims.

## Canonical commands

```stata
summarize outcome treatment controls
summarize outcome treatment controls, detail

tabstat outcome treatment age edu tenure, ///
    statistics(n mean sd p25 p50 p75 min max) columns(statistics)

estpost tabstat outcome treatment age edu tenure, ///
    statistics(n mean sd p50 min max)
esttab . using "output/tables/table1_summary.tex", replace ///
    cells("count mean sd p50 min max") nonumber nomtitle

balancetable outcome treatment age edu tenure ///
    using "output/tables/table1_balance.tex", replace
```

## Hard rules

- Do not let Table 1 become a dumping ground for every variable in the dataset.
- Prefer variables that define scale, comparability, or sample construction.
- Keep causal interpretation out of Step 3.

## Common outputs

- `table1_summary.tex`
- `table1_balance.tex`
- quick sample diagnostics for the draft
