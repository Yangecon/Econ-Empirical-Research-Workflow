/*******************************************************************************
02_robustness.do

Robustness gauntlet template.
*******************************************************************************/

do "code/00_setup.do"

local required_packages "reghdfe eststo esttab boottest ritest"
do "$CODE/_write_version_log.do" "02_robustness.do" "`required_packages'"

use "$DATA/final_sample.dta", clear

local y_var       outcome
local x_var       treatment
local id_var      unit_id
local time_var    year
local cluster_var unit_id

capture which reghdfe
if _rc != 0 {
    di as error "Package reghdfe is not installed."
    exit 199
}

capture which esttab
if _rc != 0 {
    di as error "Package estout/esttab is not installed."
    exit 199
}

eststo clear

quietly eststo r1: reghdfe `y_var' `x_var', absorb(`id_var' `time_var') vce(cluster `cluster_var')
quietly eststo r2: reghdfe `y_var' `x_var' if !missing(`y_var', `x_var'), absorb(`id_var' `time_var') vce(robust)
quietly eststo r3: reghdfe `y_var' `x_var', absorb(`id_var' `time_var') vce(cluster `id_var')

foreach model in r1 r2 r3 {
    estimates restore `model'
    quietly summarize `y_var' if e(sample), meanonly
    estadd scalar mean_y = r(mean)
    if "`model'" == "r2" {
        estadd scalar n_clusters = .
    }
    else {
        estadd scalar n_clusters = e(N_clust)
    }
    estimates store `model', replace
}

esttab r1 r2 r3 using "$OUTPUT/raw/table5_robustness.csv", replace csv ///
    se star(* 0.10 ** 0.05 *** 0.01) ///
    label compress ///
    mtitles("Baseline" "Robust SE" "Alt Cluster") ///
    title("Robustness Checks") ///
    stats(N mean_y n_clusters r2, fmt(0 3 0 3) ///
        labels("Observations" "Mean of Y" "Num. of clusters" "R-squared")) ///
    addnotes("Column 2 uses unclustered robust standard errors; its cluster count is not applicable.", ///
        "Replace this note with the actual sample, estimator, fixed effects, weights, and inference details.")

* Stage this table as a separate sheet in results_tables.xlsx when applicable.

capture which boottest
if _rc == 0 {
    quietly reghdfe `y_var' `x_var', absorb(`id_var' `time_var') vce(cluster `cluster_var')
    capture noisily boottest `x_var'
}

capture which ritest
if _rc == 0 {
    capture noisily ritest `x_var' _b[`x_var'], reps(100): ///
        reghdfe `y_var' `x_var', absorb(`id_var' `time_var') vce(cluster `cluster_var')
}

log close
