# Step 8 - Publication-Ready Tables and Plots

Goal: export tables and figures that can move directly into `draft/` and then into Overleaf with minimal cleanup.

## Preferred tools

- `esttab`
- `outreg2`
- `estout`
- `coefplot`
- `binscatter`
- `marginsplot`
- `rdplot`

## Canonical commands

```stata
esttab m1 m2 m3 m4 m5 m6 using "output/tables/table2_main_results.tex", ///
    replace booktabs se star(* 0.10 ** 0.05 *** 0.01) ///
    mtitles("M1" "M2" "M3" "M4" "M5" "M6")

outreg2 using "output/tables/table2_main_results.doc", replace tex

coefplot m1 m2 m3 m4 m5 m6, vertical xline(0)
graph export "output/figures/figure_main_coefplot.pdf", replace

binscatter outcome treatment
graph export "output/figures/figure_binscatter.pdf", replace

rdplot outcome running_var, c(0)
graph export "output/figures/figure_rdplot.pdf", replace
```

## House rules

- Stable file names beat clever names.
- Use readable labels, not raw variable codes, in exported tables when possible.
- Keep figure backgrounds white and lines legible in grayscale.
- Export the same figure to both PDF and PNG when downstream workflows differ.

## Common output set

- `table1_balance.tex`
- `table2_main_results.tex`
- `table3_mechanism.tex`
- `table4_heterogeneity.tex`
- `table5_robustness.tex`
- figure PDFs and PNGs under `output/figures/`
