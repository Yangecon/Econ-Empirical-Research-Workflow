/*******************************************************************************
04_tables.do

Table 1 plus publication-ready table bundle.
*******************************************************************************/

do "code/00_setup.do"

local required_packages "estpost esttab reghdfe balancetable eststo"
do "$CODE/_write_version_log.do" "04_tables.do" "`required_packages'"

use "$DATA/final_sample.dta", clear

local y_var       outcome
local x_var       treatment
local id_var      unit_id
local time_var    year
local cluster_var unit_id

capture which esttab
if _rc != 0 {
    di as error "Package estout/esttab is not installed."
    exit 199
}

capture which reghdfe
if _rc != 0 {
    di as error "Package reghdfe is not installed."
    exit 199
}

capture which balancetable
local has_balancetable = (_rc == 0)

if `has_balancetable' {
    balancetable `y_var' `x_var' using "$TABLES/table1_balance.tex", replace
}
else {
    estpost tabstat `y_var' `x_var', statistics(n mean sd p50 min max)
    esttab . using "$TABLES/table1_summary.tex", replace ///
        cells("count mean sd p50 min max") nonumber nomtitle ///
        title("Summary Statistics")
}

eststo clear
quietly eststo m1: reg `y_var' `x_var', vce(cluster `cluster_var')
quietly eststo m2: reg `y_var' `x_var' i.`time_var', vce(cluster `cluster_var')
quietly eststo m3: reg `y_var' `x_var' i.`time_var' c.`x_var'#c.`x_var', vce(cluster `cluster_var')
quietly eststo m4: reghdfe `y_var' `x_var', absorb(`id_var') vce(cluster `cluster_var')
quietly eststo m5: reghdfe `y_var' `x_var', absorb(`id_var' `time_var') vce(cluster `cluster_var')
quietly eststo m6: reghdfe `y_var' `x_var', absorb(`id_var' `time_var') vce(cluster `cluster_var')

* Attach statistics from each model's own estimation sample before export.
foreach model in m1 m2 m3 m4 m5 m6 {
    estimates restore `model'
    quietly summarize `y_var' if e(sample), meanonly
    estadd scalar mean_y = r(mean)
    estadd scalar n_clusters = e(N_clust)
    estimates store `model', replace
}

esttab m1 m2 m3 m4 m5 m6 using "$TABLES/table2_main_results.tex", replace ///
    booktabs se star(* 0.10 ** 0.05 *** 0.01) ///
    label compress ///
    mtitles("M1" "M2" "M3" "M4" "M5" "M6") ///
    title("Main Results") ///
    stats(N mean_y n_clusters r2, fmt(0 3 0 3) ///
        labels("Observations" "Mean of Y" "Num. of clusters" "R-squared")) ///
    addnotes("Update this note with the actual outcome, sample, estimator, fixed effects, weights, and clustering level.", ///
        "*** p<0.01, ** p<0.05, * p<0.10.")

* Follow skills/empirical-analysis-stata/references/08-tables-plots.md:
* export the same complete table to CSV, XLSX, and genuine DOC before delivery.

log close

