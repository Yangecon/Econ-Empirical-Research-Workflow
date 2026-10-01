version 19
args input output lang showtitle
clear all
set more off
if "`input'"=="" | "`output'"=="" | !inlist("`lang'","en","zh") | !inlist("`showtitle'","0","1") exit 198
local notch 1000
local exclude_low 880
local exclude_high 1200
import delimited using "`input'", clear varnames(1) stringcols(_all) encoding(UTF-8)
foreach v in bin_center observed_count counterfactual_count {
    assert `v'!=""
    destring `v', replace
    assert !missing(`v')
}
assert _N>=10
assert observed_count>=0 & counterfactual_count>=0
assert bin_center>bin_center[_n-1] if _n>1
quietly summarize bin_center
local xmin=r(min)
local xmax=r(max)
assert `xmin'<`exclude_low' & `exclude_low'<`notch' & `notch'<`exclude_high' & `exclude_high'<`xmax'
local spacing=bin_center[2]-bin_center[1]
assert abs((bin_center-bin_center[_n-1])-`spacing')<=1e-9+abs(`spacing')*1e-9 if _n>1
local base=subinstr("`output'",".png","",.)
export delimited using "`base'_checked.csv", replace
quietly summarize observed_count
local ymax=r(max)
quietly summarize counterfactual_count
local ymax=max(`ymax',r(max))*1.08
local titleopt ""
if "`lang'"=="zh" {
    local xlab "运行变量"
    local ylab "样本数"
    local obs "实际人数"
    local cf "给定的反事实"
    local notchlab "税收跳跃门槛"
    local boundlab "排除区间边界"
    if "`showtitle'"=="1" local titleopt `"title("门槛附近的分布")"'
}
else {
    local xlab "Running variable"
    local ylab "Number of observations"
    local obs "Observed count"
    local cf "Supplied counterfactual"
    local notchlab "Notch"
    local boundlab "Exclusion bounds"
    if "`showtitle'"=="1" local titleopt `"title("Distribution around a notch")"'
}
twoway (line counterfactual_count bin_center, lcolor(gs7) lwidth(medium)) ///
       (connected observed_count bin_center, lcolor("36 84 125") mcolor("36 84 125") msize(tiny) lwidth(medthin)) ///
       (pci 0 `exclude_low' `ymax' `exclude_low', lcolor(gs6) lpattern(dash)) ///
       (pci 0 `exclude_high' `ymax' `exclude_high', lcolor(gs6) lpattern(dash)) ///
       (pci 0 `notch' `ymax' `notch', lcolor(red) lpattern(dot)), ///
       xscale(range(`xmin' `xmax') noextend) yscale(range(0 `ymax') noextend) ///
       xtitle("`xlab'") ytitle("`ylab'") ylabel(,angle(horizontal) nogrid) ///
       legend(order(2 "`obs'" 1 "`cf'" 3 "`boundlab'" 5 "`notchlab'") position(6) ring(1) rows(1) size(small) region(lcolor(none))) ///
       graphregion(color(white)) plotregion(color(white)) `titleopt'
graph export "`output'", width(1800) replace
graph export "`base'.pdf", replace
