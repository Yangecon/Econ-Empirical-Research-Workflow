* Histogram of supplied permutation draws plus observed statistic.
* No permutations are generated here. Tail counts use inclusive thresholds.
version 19.0
args input output lang tail nullcenter xmin xmax binwidth showtitle
if `"`input'"' == "" local input "demo.csv"
if `"`output'"' == "" {
    display as error "output PNG path is required"
    exit 198
}
if `"`lang'"' == "" local lang "en"
if `"`tail'"' == "" local tail "right"
if `"`xmin'"' == "" local xmin "0"
if `"`xmax'"' == "" local xmax "1"
if `"`binwidth'"' == "" local binwidth ".01"
if `"`showtitle'"' == "" local showtitle "0"
if !inlist(`"`lang'"', "en", "zh") exit 198
if !inlist(`"`tail'"', "right", "left", "two-sided") exit 198
if `"`tail'"' == "two-sided" & `"`nullcenter'"' == "" {
    display as error "two-sided tail requires explicit nullcenter"
    exit 198
}
if `xmin' >= `xmax' | `binwidth' <= 0 exit 198
local nbin = (`xmax'-`xmin')/`binwidth'
if abs(`nbin'-round(`nbin')) > 1e-8 exit 198

if `"`lang'"' == "zh" {
    local xtext "统计量"
    local ytext "置换所占比例"
    local titletext "置换零分布"
}
else {
    local xtext "Statistic"
    local ytext "Share of permutations"
    local titletext "Permutation null distribution"
}

capture log close perm
log using "permutation_null_distribution_stata.log", text replace name(perm)
import delimited using `"`input'"', clear varnames(1) stringcols(_all) encoding(UTF-8)
confirm variable panel panel_order panel_label_en panel_label_zh draw_id null_stat observed_stat
assert !missing(panel, panel_label_en, panel_label_zh, draw_id)
isid panel draw_id
destring panel_order null_stat observed_stat, replace
assert !missing(panel_order, null_stat, observed_stat)
assert panel_order == floor(panel_order) & panel_order >= 1
assert inrange(null_stat, `xmin', `xmax') & inrange(observed_stat, `xmin', `xmax')
bysort panel: assert panel_order == panel_order[1] & observed_stat == observed_stat[1] & panel_label_en == panel_label_en[1] & panel_label_zh == panel_label_zh[1]
bysort panel_order: assert panel == panel[1]
quietly summarize panel_order
local np = r(max)
assert r(min) == 1
assert inrange(`np', 1, 4)
forvalues j = 1/`np' {
    quietly count if panel_order == `j'
    assert r(N) > 0
}

local resultoutput = subinstr(`"`output'"', ".png", "_results.csv", .)
file open results using `"`resultoutput'"', write replace text
file write results "panel,panel_order,draws,extreme,observed_stat,tail,null_center,p_finite" _n
local graphs ""
forvalues j = 1/`np' {
    preserve
    keep if panel_order == `j'
    local draws = _N
    local panel_id = panel[1]
    local panel_label = panel_label_`lang'[1]
    local observed = observed_stat[1]
    if `"`tail'"' == "right" generate byte extreme = null_stat >= `observed'
    else if `"`tail'"' == "left" generate byte extreme = null_stat <= `observed'
    else generate byte extreme = abs(null_stat-`nullcenter') >= abs(`observed'-`nullcenter')
    quietly count if extreme
    local extreme_n = r(N)
    local p = (`extreme_n'+1)/(`draws'+1)
    local centerfield ""
    if `"`tail'"' == "two-sided" local centerfield `"`nullcenter'"'
    file write results `"`panel_id',`j',`draws',`extreme_n',`observed',`tail',`centerfield',`p'"' _n
    local paneltitle ""
    if `np' > 1 local paneltitle `"title(`"`panel_label'"', size(small))"'
    histogram null_stat, fraction start(`xmin') width(`binwidth') ///
        fcolor(gs8) lcolor(gs8) xline(`observed', lcolor(red) lpattern(dash) lwidth(medium)) ///
        xscale(range(`xmin' `xmax')) xlabel(`xmin'(.2)`xmax') ///
        xtitle(`"`xtext'"') ytitle(`"`ytext'"') ///
        ylabel(, angle(0)) `paneltitle' graphregion(color(white)) ///
        plotregion(color(white)) scheme(s1mono) name(perm_`j', replace)
    local graphs "`graphs' perm_`j'"
    display "PANEL `panel_id' draws=`draws' extreme=`extreme_n' p_finite=`p'"
    restore
}
file close results
local titleoption ""
if `"`showtitle'"' == "1" local titleoption `"title(`"`titletext'"', size(medium))"'
graph combine `graphs', cols(`np') xsize(`=max(7.5,4.2*`np')') ysize(4.5) ///
    graphregion(color(white)) `titleoption'
graph export `"`output'"', as(png) width(2200) replace
local pdfoutput = subinstr(`"`output'"', ".png", ".pdf", .)
graph export `"`pdfoutput'"', as(pdf) replace
display "STATA_COMPLETE panels=`np' tail=`tail' output=`output'"
log close perm
