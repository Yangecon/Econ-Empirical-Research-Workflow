version 19
args input output lang showtitle
clear all
set more off
if "`input'"=="" | "`output'"=="" | !inlist("`lang'","en","zh") | !inlist("`showtitle'","0","1") exit 198
import delimited using "`input'", clear varnames(1) stringcols(_all) encoding(UTF-8)
foreach v in bin_low bin_high relative_price relative_productivity relative_sales_per_worker {
    assert `v'!=""
    destring `v', replace
    assert !missing(`v')
}
quietly count
assert r(N)>=3
sort bin_low
gen double width=bin_high-bin_low
assert width>0 & bin_low>=0 & bin_high<=1
assert abs(width-width[1])<1e-9
assert abs(bin_low-bin_high[_n-1])<1e-9 if _n>1
assert abs(relative_price+relative_productivity-relative_sales_per_worker)<=2e-6
gen double mid=(bin_low+bin_high)/2
gen double price_low=min(0,relative_price)
gen double price_high=max(0,relative_price)
gen double prod_low=cond(relative_productivity<0,min(0,relative_price)+relative_productivity,max(0,relative_price))
gen double prod_high=cond(relative_productivity<0,min(0,relative_price),max(0,relative_price)+relative_productivity)
local base=subinstr("`output'",".png","",.)
export delimited using "`base'_checked.csv", replace
if "`lang'"=="zh" {
    local xt "劳动份额"
    local yt "相对对数分量"
    local price "相对价格"
    local prod "相对实物劳动生产率"
    local heading "相对人均销售额的分解"
}
else {
    local xt "Labor share"
    local yt "Relative log components"
    local price "Relative prices"
    local prod "Relative physical labor productivity"
    local heading "Components of relative sales per worker"
}
local w=width[1]*.96
local opt ""
if "`showtitle'"=="1" local opt "title(`heading',size(medsmall))"
twoway (rbar price_low price_high mid, barw(`w') color("115 119 123") fintensity(100) lcolor(white) lwidth(vthin)) ///
       (rbar prod_low prod_high mid, barw(`w') color("198 201 203") fintensity(100) lcolor(white) lwidth(vthin)), ///
       xscale(range(0 1) noextend) xlabel(0(.1)1,labsize(small) nogrid) ///
       yline(0,lcolor(gs5) lwidth(thin)) ylabel(,angle(horizontal) nogrid) ///
       xtitle("`xt'") ytitle("`yt'") ///
       legend(order(1 "`price'" 2 "`prod'") position(1) ring(0) rows(2) region(color(white)) size(small)) ///
       graphregion(color(white)) xsize(10.5) ysize(5.5) `opt'
graph export "`output'", replace width(2200)
graph export "`base'.pdf", replace
display "SIGNED_DECOMP_STATA_COMPLETE bins=" _N
