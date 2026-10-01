version 19
args input output lang showtitle
clear all
set more off
if "`input'"=="" | "`output'"=="" | !inlist("`lang'","en","zh") | !inlist("`showtitle'","0","1") exit 198
import delimited using "`input'", clear varnames(1) stringcols(_all) encoding(UTF-8)
assert id!=""
isid id
foreach v in true_prob predicted_prob {
    assert `v'!=""
    destring `v', replace
    assert !missing(`v') & inrange(`v',0,1)
}
gen byte tail=true_prob>.99
quietly count if tail==0
local nregular=r(N)
assert `nregular'>=40
quietly count if tail==1
assert r(N)>=4
quietly regress predicted_prob true_prob
local intercept=_b[_cons]
local slope=_b[true_prob]
sort tail true_prob id
gen byte bin=1+floor((_n-1)*10/`nregular') if tail==0
replace bin=11 if tail==1
local base=subinstr("`output'",".png","",.)
export delimited id true_prob predicted_prob bin using "`base'_assigned.csv", replace
preserve
clear
set obs 1
gen double intercept=`intercept'
gen double slope=`slope'
export delimited using "`base'_fit.csv", replace
restore
tempfile bintable
postfile ph byte bin long n double mean_true mean_predicted q25 q75 using `bintable', replace
forvalues b=1/11 {
    preserve
    keep if bin==`b'
    local m=_N
    assert `m'>0
    quietly summarize true_prob, meanonly
    local mx=r(mean)
    quietly summarize predicted_prob, meanonly
    local my=r(mean)
    sort predicted_prob id
    local pos25=1+.25*(`m'-1)
    local lo25=floor(`pos25')
    local hi25=ceil(`pos25')
    scalar qlo=predicted_prob[`lo25']+(`pos25'-`lo25')*(predicted_prob[`hi25']-predicted_prob[`lo25'])
    local pos75=1+.75*(`m'-1)
    local lo75=floor(`pos75')
    local hi75=ceil(`pos75')
    scalar qhi=predicted_prob[`lo75']+(`pos75'-`lo75')*(predicted_prob[`hi75']-predicted_prob[`lo75'])
    post ph (`b') (`m') (`mx') (`my') (qlo) (qhi)
    restore
}
postclose ph
use `bintable', clear
export delimited using "`base'_bins.csv", replace
gen double fit=`intercept'+`slope'*mean_true
set obs 13
replace mean_true=0 in 12
replace mean_true=1 in 13
replace fit=`intercept' in 12
replace fit=`intercept'+`slope' in 13
sort mean_true
local titleopt ""
if "`lang'"=="zh" {
    local xlab "真实录取概率"
    local ylab "预测录取概率"
    local meanlab "分箱均值"
    local fitlab "线性拟合"
    local linelab "45度线"
    local iqrlab "条件四分位距"
    if "`showtitle'"=="1" local titleopt `"title("预测概率与真实概率的校准")"'
}
else {
    local xlab "True placement probability"
    local ylab "Predicted placement probability"
    local meanlab "Bin mean"
    local fitlab "Linear fit"
    local linelab "45-degree line"
    local iqrlab "Conditional IQR"
    if "`showtitle'"=="1" local titleopt `"title("Predicted versus true placement probabilities")"'
}
twoway (rarea q75 q25 mean_true, color("219 234 244") lcolor("190 216 233")) ///
       (function y=x, range(0 1) lcolor(black) lpattern(dot) lwidth(medium)) ///
       (line fit mean_true, lcolor("40 121 185") lpattern(dash) lwidth(medthick)) ///
       (scatter mean_predicted mean_true, msymbol(Oh) msize(medium) mcolor("40 121 185")), ///
       xscale(range(0 1) noextend) yscale(range(0 1) noextend) ///
       xlabel(0(.2)1,nogrid) ylabel(0(.2)1,angle(horizontal) nogrid) ///
       xtitle("`xlab'") ytitle("`ylab'") ///
       legend(order(4 "`meanlab'" 3 "`fitlab'" 2 "`linelab'" 1 "`iqrlab'") ///
       position(4) ring(0) rows(4) size(small) region(color(white))) ///
       graphregion(color(white)) plotregion(color(white)) `titleopt'
graph export "`output'", width(1800) replace
graph export "`base'.pdf", replace
