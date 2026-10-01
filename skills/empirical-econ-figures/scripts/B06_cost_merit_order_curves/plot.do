version 19
args input output showtitle
clear all
set more off
if "`input'"=="" | "`output'"=="" | !inlist("`showtitle'","0","1") {
    display as error "Usage: plot.do input.csv output.png showtitle(0|1)"
    exit 198
}
local base=subinstr("`output'",".png","",.)
capture log close _all
log using "`base'_run.log", replace text
import delimited using "`input'", clear varnames(1) stringcols(1 2) encoding(UTF-8)
assert !missing(scenario,unit_id,marginal_cost,dispatched_mwh)
replace scenario=strtrim(scenario)
replace unit_id=strtrim(unit_id)
assert scenario!="" & unit_id!=""
isid scenario unit_id
destring marginal_cost dispatched_mwh, replace
assert marginal_cost>=0 & dispatched_mwh>0
egen byte group=group(scenario)
quietly summarize group, meanonly
assert r(max)==2
bysort scenario: egen double demand_mwh=total(dispatched_mwh)
quietly summarize demand_mwh, meanonly
assert abs(r(max)-r(min))<1e-8
local demand=r(max)
sort scenario marginal_cost unit_id
by scenario: gen double x_end=sum(dispatched_mwh)
gen double x_start=x_end-dispatched_mwh
assert x_start>=0 & x_end>x_start
export delimited using "`base'_steps.csv", replace
local name1=scenario[1]
local name2=scenario[_N]
preserve
    gen long originalrow=_n
    expand 2
    bysort originalrow: gen byte endpoint=_n-1
    gen double x_mwh=cond(endpoint==0,x_start,x_end)
    sort scenario marginal_cost unit_id endpoint
    export delimited using "`base'_coordinates.csv", replace
    local ttl ""
    if "`showtitle'"=="1" local ttl `"title("Dispatched marginal costs")"'
    twoway ///
        (line marginal_cost x_mwh if group==1, lcolor(black) lwidth(medthick)) ///
        (line marginal_cost x_mwh if group==2, lcolor(gs8) lwidth(medthick)), ///
        xscale(range(0 `demand')) ///
        xlabel(, grid glcolor(gs14)) ylabel(, grid glcolor(gs14)) ///
        xtitle("Cumulative dispatched energy (MWh)") ytitle("Marginal cost (currency/MWh)") ///
        legend(order(1 "`name1'" 2 "`name2'") position(11) ring(0) ///
               cols(1) size(small) region(lcolor(none))) ///
        graphregion(color(white)) plotregion(color(white)) `ttl'
    graph export "`output'", replace width(2400)
    graph export "`base'.pdf", replace
restore
display "F23_STATA_OK units=" _N " demand_mwh=`demand'"
log close
