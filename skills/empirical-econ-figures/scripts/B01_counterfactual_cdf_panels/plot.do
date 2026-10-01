* Two scenario panels with three supplied CDF curves per panel.
* Edit CONFIG IDs and labels for another application.
version 19.0
args input output lang showtitle
if `"`input'"' == "" local input "demo.csv"
if `"`output'"' == "" local output "scenario_cdf_stata_en.png"
if `"`lang'"' == "" local lang "en"
if `"`showtitle'"' == "" local showtitle "0"
if !inlist(`"`lang'"', "en", "zh") exit 198

* CONFIG: order and IDs. Match these to the CSV, not alphabetic sorting.
local panel1 "forced_attention"
local panel2 "no_switching_costs"
local group1 "low"
local group2 "medium"
local group3 "high"
if `"`lang'"' == "zh" {
    local panel_label1 "面板A：强制关注"
    local panel_label2 "面板B：无转换成本"
    local group_label1 "低需求"
    local group_label2 "中需求"
    local group_label3 "高需求"
    local legend_label "健康需求程度"
    local xlab "超额支出减少额（美元）"
    local ylab "累计比例（CDF）"
    local wholetitle "反事实情景下的超额支出减少额"
}
else {
    local panel_label1 "Panel A. Forced attention"
    local panel_label2 "Panel B. No switching costs"
    local group_label1 "Low acuity"
    local group_label2 "Medium acuity"
    local group_label3 "High acuity"
    local legend_label "Acuity level"
    local xlab "Reduction in overspending ($)"
    local ylab "Cumulative share (CDF)"
    local wholetitle "Counterfactual reductions in overspending"
}

capture log close scenario_cdf
log using "scenario_cdf_stata.log", text replace name(scenario_cdf)
import delimited using `"`input'"', clear varnames(1) stringcols(_all) encoding(UTF-8)
confirm variable panel panel_order group group_order x_reduction cdf
destring panel_order group_order x_reduction cdf, replace
assert !missing(panel, group, panel_order, group_order, x_reduction, cdf)
assert inrange(cdf, 0, 1)
isid panel group x_reduction
generate byte valid = 0
forvalues j = 1/2 {
    forvalues k = 1/3 {
        replace valid = 1 if panel == `"`panel`j''"' & panel_order == `j' & ///
            group == `"`group`k''"' & group_order == `k'
        quietly count if panel == `"`panel`j''"' & group == `"`group`k''"'
        assert r(N) >= 2
    }
}
assert valid == 1
drop valid
sort panel group x_reduction
by panel group: assert x_reduction > x_reduction[_n-1] if _n > 1
by panel group: assert cdf >= cdf[_n-1] - 1e-9 if _n > 1
quietly summarize x_reduction
local xmin = r(min)
local xmax = r(max)

forvalues j = 1/2 {
    quietly count if panel == `"`panel`j''"'
    local n`j' = r(N)
    twoway ///
        (line cdf x_reduction if panel == `"`panel`j''"' & group == `"`group1'"', sort lcolor(black) lpattern(solid) lwidth(medthick)) ///
        (line cdf x_reduction if panel == `"`panel`j''"' & group == `"`group2'"', sort lcolor(gs7) lpattern(dash) lwidth(medthick)) ///
        (line cdf x_reduction if panel == `"`panel`j''"' & group == `"`group3'"', sort lcolor(gs11) lpattern(shortdash_dot) lwidth(medthick)), ///
        legend(order(1 `"`group_label1'"' 2 `"`group_label2'"' 3 `"`group_label3'"') ///
               title(`"`legend_label'"', size(small)) position(5) ring(0) ///
               rows(3) size(small) region(lcolor(gs8) fcolor(white))) ///
        subtitle(`"`panel_label`j''"', position(11) size(medium)) ///
        xtitle(`"`xlab'"', size(small)) ytitle(`"`ylab'"', size(small)) ///
        xlabel(, labsize(small)) ylabel(0(.25)1, angle(0) labsize(small)) ///
        yscale(range(0 1)) xscale(range(`xmin' `xmax')) ///
        graphregion(color(white)) plotregion(color(white)) scheme(s1mono) ///
        name(cdf_`j', replace)
    display "PANEL `panel`j'' N=`n`j'' groups=3"
}
local titleoption ""
if `"`showtitle'"' == "1" local titleoption `"title(`"`wholetitle'"', size(medium))"'
graph combine cdf_1 cdf_2, cols(1) xsize(8.5) ysize(7) ///
    graphregion(color(white)) `titleoption'
graph export `"`output'"', as(png) width(1870) replace
local pdfoutput = subinstr(`"`output'"', ".png", ".pdf", .)
graph export `"`pdfoutput'"', as(pdf) replace
display "STATA_COMPLETE N1=`n1' N2=`n2' output=`output' pdf=`pdfoutput'"
log close scenario_cdf
