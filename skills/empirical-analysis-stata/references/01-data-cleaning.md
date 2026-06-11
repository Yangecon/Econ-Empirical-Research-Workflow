# Step 1 - Data Cleaning in Stata

Goal: move from raw source files to an analysis-ready dataset with explicit typing, missingness handling, duplicate resolution, validated merges, and a declared panel structure.

## Use this reference for

- `import delimited`
- `import excel`
- `destring`
- date parsing
- `misstable`
- `duplicates`
- `merge`
- `xtset`

## Default checklist

1. Import the raw file in its native format.
2. Save a raw snapshot before mutating.
3. Inspect types, labels, and key identifiers.
4. Convert string numerics and parse dates.
5. Document missing-value handling.
6. Resolve exact duplicates and key duplicates.
7. Validate merges with hard assertions.
8. Declare panel structure and inspect gaps.

## Canonical commands

```stata
use "data/raw/panel.dta", clear
import delimited "data/raw/panel.csv", clear varnames(1)
import excel "data/raw/panel.xlsx", firstrow clear

describe, short
codebook, compact
misstable summarize
misstable patterns

destring year wage, replace ignore("$,%")
gen hire_date = date(hire_date_str, "YMD")
format hire_date %td
encode industry, gen(industry_n)

duplicates report
duplicates report unit_id year
isid unit_id year

merge m:1 firm_id using "data/raw/firm_chars.dta", ///
    assert(master match) keep(master match)

xtset unit_id year
xtdescribe
```

## Hard rules

- Never use `merge m:m` casually.
- Never drop missing values on the outcome, treatment, or key IDs without logging that decision.
- Never assume the panel key is unique; test it.
- Never move to estimation before confirming row counts after merges.

## Common outputs

- `data/build/final_sample_intermediate.dta`
- `data/final_sample.dta`
- a run log explaining drops, imputations, and merge decisions
