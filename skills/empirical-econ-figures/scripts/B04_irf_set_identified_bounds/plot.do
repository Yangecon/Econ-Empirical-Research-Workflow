version 19
args input output lang showtitle
clear all
set more off
if "`input'"=="" | "`output'"=="" | !inlist("`lang'","en","zh") | !inlist("`showtitle'","0","1") exit 198
import delimited using "`input'", clear varnames(1) stringcols(_all) encoding(UTF-8)
foreach v in horizon admissible_low admissible_high pointwise_median maxg_response {
    assert `v'!=""
    destring `v', replace
    assert !missing(`v')
}
assert _N>=3
assert horizon>=0
assert horizon>horizon[_n-1] if _n>1
isid horizon
assert admissible_low<=admissible_high
assert inrange(pointwise_median,admissible_low,admissible_high)
assert inrange(maxg_response,admissible_low,admissible_high)
local base=subinstr("`output'",".png","",.)
export delimited using "`base'_checked.csv", replace
quietly summarize horizon
local xmin=r(min)
local xmax=r(max)
local xstep=(`xmax'-`xmin')/7
local titleopt ""
if "`lang'"=="zh" {
    local xlab "季度（冲击发生于第1期）"
    local ylab "GDP同比增速响应（百分点）"
    local bounds "可容许响应上下界"
    local median "逐期中位数"
    local maxg "给定的maxG路径"
    if "`showtitle'"=="1" local titleopt `"title("不确定性冲击的集合识别响应")"'
}
else {
    local xlab "Quarter (shock in period 1)"
    local ylab "GDP growth response (pp)"
    local bounds "Admissible bounds"
    local median "Pointwise median"
    local maxg "Supplied maxG path"
    if "`showtitle'"=="1" local titleopt `"title("Set-identified response to an uncertainty shock")"'
}
twoway (line admissible_low horizon, lcolor("38 68 155") lwidth(medthick)) ///
       (line admissible_high horizon, lcolor("38 68 155") lwidth(medthick)) ///
       (connected pointwise_median horizon, lcolor("35 138 75") mcolor("35 138 75") msymbol(X) msize(medium) lwidth(medium)) ///
       (connected maxg_response horizon, lcolor("190 48 53") mcolor("190 48 53") msymbol(Oh) msize(medium) lwidth(medium)), ///
       yline(0,lcolor(gs6) lpattern(dash)) xtitle("`xlab'") ytitle("`ylab'") ///
       xscale(range(`xmin' `xmax') noextend) xlabel(`xmin'(`xstep')`xmax',nogrid) ///
       ylabel(,angle(horizontal) nogrid) ///
       legend(order(1 "`bounds'" 3 "`median'" 4 "`maxg'") position(6) ring(1) rows(1) size(small) region(lcolor(none))) ///
       graphregion(color(white)) plotregion(color(white)) `titleopt'
graph export "`output'", width(1900) replace
graph export "`base'.pdf", replace
