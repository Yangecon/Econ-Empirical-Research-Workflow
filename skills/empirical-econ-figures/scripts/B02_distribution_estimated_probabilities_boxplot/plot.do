* Raw-observation grouped boxplot; type-7 quartiles and 1.5-IQR whiskers.
version 19.0
args input output lang showtitle ymin ymax
if `"`input'"' == "" local input "demo.csv"
if `"`output'"' == "" local output "boxplot_stata_en.png"
if `"`lang'"' == "" local lang "en"
if `"`showtitle'"' == "" local showtitle "0"
if `"`ymin'"' == "" local ymin "0"
if `"`ymax'"' == "" local ymax "1"
if !inlist(`"`lang'"', "en", "zh") exit 198
if `ymin' >= `ymax' exit 198

if `"`lang'"' == "zh" {
    local xlabel "敏锐度十分位"
    local ylabel "注意概率"
    local titletext "各十分位的注意概率"
}
else {
    local xlabel "Acuity decile"
    local ylabel "Attention probability"
    local titletext "Probability by acuity decile"
}

capture log close boxplot
log using "quantile_group_boxplot_stata.log", text replace name(boxplot)
import delimited using `"`input'"', clear varnames(1) stringcols(_all) encoding(UTF-8)
confirm variable id group group_order group_label_en group_label_zh value
assert !missing(id, group, group_label_en, group_label_zh)
isid id
destring group_order value, replace
assert !missing(group_order, value)
assert group_order == floor(group_order) & group_order >= 1
assert inrange(value, `ymin', `ymax')
bysort group: assert group_order == group_order[1]
bysort group_order: assert group == group[1] & group_label_en == group_label_en[1] & group_label_zh == group_label_zh[1]
quietly summarize group_order
local ng = r(max)
assert r(min) == 1
forvalues g = 1/`ng' {
    quietly count if group_order == `g'
    assert r(N) > 0
    quietly levelsof group if group_order == `g', local(groupid) clean
    local nw : word count `groupid'
    assert `nw' == 1
    quietly levelsof group_label_`lang' if group_order == `g', local(groupname) clean
    local xticks `"`xticks' `g' `"`groupname'"'"'
}

sort group_order value id
generate double q1 = .
generate double median = .
generate double q3 = .
generate long n = .
forvalues g = 1/`ng' {
    preserve
    keep if group_order == `g'
    sort value id
    local count = _N
    foreach pair in "q1 .25" "median .5" "q3 .75" {
        tokenize `"`pair'"'
        local key `"`1'"'
        local prob = `2'
        local h = 1 + (`count'-1)*`prob'
        local lower = floor(`h')
        local upper = ceil(`h')
        local weight = `h'-`lower'
        local result_`key' = (1-`weight')*value[`lower'] + `weight'*value[`upper']
    }
    restore
    replace n = `count' if group_order == `g'
    replace q1 = `result_q1' if group_order == `g'
    replace median = `result_median' if group_order == `g'
    replace q3 = `result_q3' if group_order == `g'
}
generate double fence_low = q1 - 1.5*(q3-q1)
generate double fence_high = q3 + 1.5*(q3-q1)
generate byte outlier = value < fence_low | value > fence_high
generate byte inside = !outlier
bysort group_order: egen double whisker_low = min(cond(inside, value, .))
bysort group_order: egen double whisker_high = max(cond(inside, value, .))
bysort group_order: egen long outlier_n = total(outlier)
assert !missing(whisker_low, whisker_high)
egen byte tag = tag(group_order)
preserve
keep if tag
keep group group_order n q1 median q3 whisker_low whisker_high outlier_n
sort group_order
export delimited using "summary_stata_`lang'.csv", replace
restore

generate double xleft = group_order - .29
generate double xright = group_order + .29
generate double capleft = group_order - .14
generate double capright = group_order + .14
local titleoption ""
if `"`showtitle'"' == "1" local titleoption `"title(`"`titletext'"')"'
twoway ///
    (rbar q1 q3 group_order if tag, barwidth(.58) fcolor(white) lcolor(gs7) lwidth(medium)) ///
    (pcspike median xleft median xright if tag, lcolor(gs3) lwidth(medthick)) ///
    (pcspike whisker_low group_order q1 group_order if tag, lcolor(gs7) lwidth(medium)) ///
    (pcspike q3 group_order whisker_high group_order if tag, lcolor(gs7) lwidth(medium)) ///
    (pcspike whisker_low capleft whisker_low capright if tag, lcolor(gs7) lwidth(medium)) ///
    (pcspike whisker_high capleft whisker_high capright if tag, lcolor(gs7) lwidth(medium)) ///
    (scatter value group_order if outlier, mcolor(gs8) msymbol(O) msize(tiny)), ///
    xlabel(`xticks') xtitle(`"`xlabel'"') ytitle(`"`ylabel'"') ///
    xscale(range(.4 `=`ng'+.6')) yscale(range(`ymin' `ymax')) ///
    ylabel(, angle(0) grid glcolor(gs14)) legend(off) `titleoption' ///
    graphregion(color(white)) plotregion(color(white)) scheme(s1mono) xsize(9.2) ysize(5.4)
graph export `"`output'"', as(png) width(2200) replace
local pdfoutput = subinstr(`"`output'"', ".png", ".pdf", .)
graph export `"`pdfoutput'"', as(pdf) replace
quietly count if outlier
display "STATA_COMPLETE rows=" _N " groups=`ng' outliers=" r(N) " output=`output'"
log close boxplot
