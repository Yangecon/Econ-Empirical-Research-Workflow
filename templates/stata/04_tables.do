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

esttab m1 m2 m3 m4 m5 m6 using "$TABLES/table2_main_results.tex", replace ///
    booktabs se star(* 0.10 ** 0.05 *** 0.01) ///
    label compress ///
    mtitles("M1" "M2" "M3" "M4" "M5" "M6") ///
    title("Main Results") ///
    addnotes("Replace placeholder controls with project-specific controls and fixed effects.")

log close
