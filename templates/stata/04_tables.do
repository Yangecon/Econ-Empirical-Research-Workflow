/*******************************************************************************
04_tables.do

Table 1 plus publication-ready table bundle.
*******************************************************************************/

do "code/00_setup.do"

local required_packages "estpost esttab reghdfe eststo"
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

estpost tabstat `y_var' `x_var', statistics(n mean sd p25 p50 p75 min max)
esttab . using "$OUTPUT/raw/table1_summary.csv", replace csv ///
    cells("count mean sd min p25 p50 p75 max") nonumber nomtitle ///
    title("Summary Statistics")

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

esttab m1 m2 m3 m4 m5 m6 using "$OUTPUT/raw/table2_main_results.csv", replace csv ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    label compress ///
    mtitles("M1" "M2" "M3" "M4" "M5" "M6") ///
    title("Main Results") ///
    stats(N mean_y n_clusters r2, fmt(0 3 0 3) ///
        labels("Observations" "Mean of Y" "Num. of clusters" "R-squared")) ///
    addnotes("Update this note with the actual outcome, sample, estimator, fixed effects, weights, and clustering level.", ///
        "*** p<0.01, ** p<0.05, * p<0.10.")

* These CSVs are staging files. Assemble one results_tables.xlsx workbook
* with a summary-statistics sheet and one complete main-table sheet, including
* the sample, estimator, inference, and significance notes before delivery.

log close

