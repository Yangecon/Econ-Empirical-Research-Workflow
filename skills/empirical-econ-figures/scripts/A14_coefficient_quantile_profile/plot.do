version 19
args input output lang showtitle
clear all
set more off
if "`input'"=="" | "`output'"=="" | !inlist("`lang'","en","zh") | !inlist("`showtitle'","0","1") exit 198
import delimited using "`input'", clear varnames(1) stringcols(_all) encoding(UTF-8)
foreach v in quantile_percent estimate ci_low ci_high {
    assert `v'!=""
    destring `v', replace
    assert !missing(`v')
}
assert _N>=3
assert quantile_percent>0 & quantile_percent<100
assert ci_low<=estimate & estimate<=ci_high
assert quantile_percent>quantile_percent[_n-1] if _n>1
isid quantile_percent
local base=subinstr("`output'",".png","",.)
export delimited using "`base'_checked.csv", replace
quietly summarize quantile_percent
local xmin=max(0,r(min)-5)
local xmax=min(100,r(max)+5)
quietly summarize ci_low
local ymin=r(min)
quietly summarize ci_high
local ymax=r(max)
local pad=max((`ymax'-`ymin')*.065,.015)
local ymin=`ymin'-`pad'
local ymax=`ymax'+`pad'
local titleopt ""
if "`lang'"=="zh" {
    local xlab "结果分布分位数"
    local ylab "回归系数"
    if "`showtitle'"=="1" local titleopt `"title("不同分位数的回归系数")"'
}
else {
    local xlab "Quantile of outcome distribution"
    local ylab "Coefficient"
    if "`showtitle'"=="1" local titleopt `"title("Coefficient across quantiles")"'
}
twoway (rcap ci_low ci_high quantile_percent, lcolor(gs7) lwidth(medium)) ///
       (connected estimate quantile_percent, lcolor(black) mcolor(gs6) msymbol(O) msize(medium) lwidth(medthick)), ///
       xscale(range(`xmin' `xmax') noextend) yscale(range(`ymin' `ymax') noextend) ///
       xlabel(,nogrid) ylabel(,angle(horizontal) nogrid) ///
       xtitle("`xlab'") ytitle("`ylab'") legend(off) `titleopt' ///
       graphregion(color(white)) plotregion(color(white))
graph export "`output'", width(1800) replace
graph export "`base'.pdf", replace
