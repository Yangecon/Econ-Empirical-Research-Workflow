/*******************************************************************************
03_figures.do

Publication-ready figure templates for the main empirical results.
*******************************************************************************/

do "code/00_setup.do"

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

capture which coefplot
local has_coefplot = (_rc == 0)

capture which binscatter
local has_binscatter = (_rc == 0)

eststo clear
quietly eststo fig_main: reghdfe `y_var' `x_var', absorb(`id_var' `time_var') vce(cluster `cluster_var')

if `has_coefplot' {
    coefplot fig_main, ///
        keep(`x_var') ///
        xline(0, lpattern(dash)) ///
        title("Main Treatment Effect") ///
        ytitle("Coefficient") ///
        graphregion(color(white))
    graph export "$FIGURES/figure_main_coefplot.pdf", replace
    graph export "$FIGURES/figure_main_coefplot.png", replace width(2400)
}

if `has_binscatter' {
    binscatter `y_var' `x_var', ///
        title("Binned Relationship Between Treatment and Outcome") ///
        graphregion(color(white))
    graph export "$FIGURES/figure_binscatter.pdf", replace
    graph export "$FIGURES/figure_binscatter.png", replace width(2400)
}

log close
