version 19
clear all
set more off
args root input output title
if `"`root'"'=="" local root "`c(pwd)'"
if `"`input'"'=="" local input "`root'/audited_estimates.csv"
if `"`output'"'=="" local output "`root'/staggered_comparison_stata"
do "`root'/plot_twoway.do"
plot_staggered_twoway, input("`input'") output("`output'") title(`"`title'"')
display "STAGGERED_TWOWAY_COMPLETE"
