* Supplied model-output paths and disparity confidence intervals.
version 19.0
args input output lang showtitle
if `"`input'"' == "" local input "demo.csv"
if `"`output'"' == "" {
    display as error "output PNG path is required"
    exit 198
}
if `"`lang'"' == "" local lang "en"
if `"`showtitle'"' == "" local showtitle "0"
if !inlist(`"`lang'"', "en", "zh") exit 198

* CONFIG: these IDs, labels and units correspond to plot.py.
local id1 "credit_prediction"
local id2 "credit_oracle"
local id3 "total_prediction"
local id4 "total_oracle"
local color1 "lavender"
local color2 "teal"
local color3 "purple"
local color4 "navy"
if `"`lang'"' == "zh" {
    local lab1 "抵免额预测"
    local lab2 "抵免额实际值"
    local lab3 "总额预测"
    local lab4 "总额实际值"
    local xlab "查获少报金额（合成单位）"
    local ylab "差距（百分点）"
    local baselab "现状"
    local oplab "执行比例"
    local heading "效率与差距路径"
}
else {
    local lab1 "Credit prediction"
    local lab2 "Credit oracle"
    local lab3 "Total prediction"
    local lab4 "Total oracle"
    local xlab "Detected underreporting (synthetic units)"
    local ylab "Disparity (percentage points)"
    local baselab "Status quo"
    local oplab "Operating rate"
    local heading "Efficiency and disparity paths"
}

* Create every prefix of a new nested output directory.
local normalized = subinstr(`"`output'"', "\", "/", .)
local lastslash = strrpos(`"`normalized'"', "/")
if `lastslash' > 0 {
    local outdir = substr(`"`normalized'"', 1, `lastslash'-1)
    forvalues k = 1/`=strlen(`"`outdir'"')' {
        if substr(`"`outdir'"', `k', 1) == "/" {
            local prefix = substr(`"`outdir'"', 1, `k'-1)
            capture mkdir `"`prefix'"'
        }
    }
    capture mkdir `"`outdir'"'
}

import delimited using `"`input'"', clear varnames(1) stringcols(_all) encoding(UTF-8)
confirm variable algorithm policy_rate efficiency disparity ci_low ci_high operating
assert !missing(algorithm, policy_rate, efficiency, disparity, operating)
destring policy_rate efficiency disparity ci_low ci_high operating, replace
assert !missing(policy_rate, efficiency, disparity, operating)
assert policy_rate >= 0 & efficiency >= 0
assert inlist(operating, 0, 1)
isid algorithm policy_rate
assert inlist(algorithm, "status_quo", "credit_prediction", "credit_oracle", "total_prediction", "total_oracle")
quietly count if algorithm == "status_quo"
assert r(N) == 1
assert missing(ci_low) & missing(ci_high) & operating == 0 if algorithm == "status_quo"
assert !missing(ci_low, ci_high) & ci_low <= disparity & disparity <= ci_high if algorithm != "status_quo"
sort algorithm policy_rate
by algorithm: assert efficiency > efficiency[_n-1] if _n > 1 & algorithm != "status_quo"
forvalues j = 1/4 {
    quietly count if algorithm == `"`id`j''"'
    assert r(N) >= 2
    quietly count if algorithm == `"`id`j''"' & operating == 1
    assert r(N) == 1
}
quietly summarize efficiency if algorithm == "status_quo", meanonly
local basex = r(mean)
quietly summarize disparity if algorithm == "status_quo", meanonly
local basey = r(mean)
local checked = regexr(`"`output'"', "[.]png$", "_checked.csv")
export delimited algorithm policy_rate efficiency disparity ci_low ci_high operating using `"`checked'"', replace
local titleopt ""
if `"`showtitle'"' == "1" local titleopt `"title(`"`heading'"')"'

twoway ///
    (rarea ci_low ci_high efficiency if algorithm==`"`id1'"', fcolor(lavender%45) lcolor(lavender%45) lwidth(none)) ///
    (line disparity efficiency if algorithm==`"`id1'"', lcolor(lavender) lwidth(medthick)) ///
    (rarea ci_low ci_high efficiency if algorithm==`"`id2'"', fcolor(teal%45) lcolor(teal%45) lwidth(none)) ///
    (line disparity efficiency if algorithm==`"`id2'"', lcolor(teal) lwidth(medthick)) ///
    (rarea ci_low ci_high efficiency if algorithm==`"`id3'"', fcolor(purple%45) lcolor(purple%45) lwidth(none)) ///
    (line disparity efficiency if algorithm==`"`id3'"', lcolor(purple) lwidth(medthick)) ///
    (rarea ci_low ci_high efficiency if algorithm==`"`id4'"', fcolor(navy%45) lcolor(navy%45) lwidth(none)) ///
    (line disparity efficiency if algorithm==`"`id4'"', lcolor(navy) lwidth(medthick)) ///
    (scatter disparity efficiency if operating==1, mcolor(black) msymbol(O) msize(small)) ///
    (scatter disparity efficiency if algorithm=="status_quo", mcolor(red) msymbol(X) msize(medlarge)), ///
    xline(`basex', lcolor(red%65) lpattern(dot)) yline(`basey', lcolor(red%65) lpattern(dot)) ///
    yline(0, lcolor(gs10) lwidth(vthin)) ///
    xtitle(`"`xlab'"') ytitle(`"`ylab'"') ///
    ylabel(, angle(0) grid glcolor(gs14)) xlabel(, grid glcolor(gs14)) ///
    legend(order(2 `"`lab1'"' 4 `"`lab2'"' 6 `"`lab3'"' 8 `"`lab4'"' 9 `"`oplab'"' 10 `"`baselab'"') rows(2) size(small) region(lcolor(none))) ///
    `titleopt' graphregion(color(white)) plotregion(color(white)) scheme(s1color) ///
    xsize(10) ysize(6.5)
graph export `"`output'"', width(2400) replace
local pdf = regexr(`"`output'"', "[.]png$", ".pdf")
graph export `"`pdf'"', replace
display "STATA_COMPLETE rows=" _N " curves=4 output=`output'"
