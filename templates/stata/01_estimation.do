/*******************************************************************************
01_estimation.do

Baseline modeling and core diagnostic template.
*******************************************************************************/

do "code/00_setup.do"

local required_packages "reghdfe eststo esttab"
do "$CODE/_write_version_log.do" "01_estimation.do" "`required_packages'"

use "$DATA/final_sample.dta", clear

local y_var       outcome
local x_var       treatment
local id_var      unit_id
local time_var    year
local cluster_var unit_id

capture confirm variable `y_var'
if _rc != 0 {
    di as error "Outcome variable `y_var' is missing. Update the template placeholders."
    exit 111
}

capture confirm variable `x_var'
if _rc != 0 {
    di as error "Treatment variable `x_var' is missing. Update the template placeholders."
    exit 111
}

capture which reghdfe
if _rc != 0 {
    di as error "Package reghdfe is not installed. Install before running this template."
    exit 199
}

capture which esttab
if _rc != 0 {
    di as error "Package estout/esttab is not installed. Install before running this template."
    exit 199
}

* Step 4 diagnostics. Extend to the frozen design in the project notes.
capture noisily summarize `y_var' `x_var'
capture noisily misstable summarize `y_var' `x_var'
capture noisily corr `y_var' `x_var'

eststo clear

quietly eststo m1: reg `y_var' `x_var', vce(cluster `cluster_var')
quietly eststo m2: reg `y_var' `x_var' i.`time_var', vce(cluster `cluster_var')
quietly eststo m3: reg `y_var' `x_var' i.`time_var' c.`x_var'#c.`x_var', vce(cluster `cluster_var')
quietly eststo m4: reghdfe `y_var' `x_var', absorb(`id_var') vce(cluster `cluster_var')
quietly eststo m5: reghdfe `y_var' `x_var', absorb(`id_var' `time_var') vce(cluster `cluster_var')
quietly eststo m6: reghdfe `y_var' `x_var', absorb(`id_var' `time_var') vce(cluster `cluster_var')

esttab m1 m2 m3 m4 m5 m6 using "$TABLES/table2_main_results.tex", replace ///
    booktabs se star(* 0.10 ** 0.05 *** 0.01) ///
    label compress ///
    mtitles("M1" "M2" "M3" "M4" "M5" "M6") ///
    title("Main Results") ///
    addnotes("Replace placeholder controls with project-specific controls and fixed effects.", "Standard errors clustered by `cluster_var'.")

log close
