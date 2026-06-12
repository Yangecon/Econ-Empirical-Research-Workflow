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

esttab r1 r2 r3 using "$TABLES/table5_robustness.tex", replace ///
    booktabs se star(* 0.10 ** 0.05 *** 0.01) ///
    label compress ///
    mtitles("Baseline" "Robust SE" "Alt Cluster") ///
    title("Robustness Checks") ///
    addnotes("Extend with design-specific commands such as boottest, ritest, bacondecomp, honestdid, rwolf, or psacalc.")

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
