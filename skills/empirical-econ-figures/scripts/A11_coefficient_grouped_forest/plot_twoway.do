* Coefficient-interval plot: 1-4 panels; horizontal or vertical.
* Edit the CONFIG section for another study. CI limits are input data.
version 19.0
args input output lang variant orientation showtitle
if `"`input'"' == "" local input "demo.csv"
if `"`output'"' == "" local output "robustness_horizontal_stata_en.png"
if `"`lang'"' == "" local lang "en"
if `"`variant'"' == "" local variant "robustness"
if `"`orientation'"' == "" local orientation "horizontal"
if `"`showtitle'"' == "" local showtitle "0"
if !inlist(`"`lang'"', "en", "zh") exit 198
if !inlist(`"`orientation'"', "horizontal", "vertical") exit 198

* CONFIG: ordered panel IDs and ordered group IDs. Edit counts to 1-4 / 1-3.
if `"`variant'"' == "robustness" {
    local np 4
    local panel1 "mortality"
    local panel2 "difficulty"
    local panel3 "transfer"
    local panel4 "employment"
    local ng 1
    local group1 "main"
    local preferred "preferred"
    if `"`lang'"' == "zh" {
        local panel_label1 "死亡率对数"
        local panel_label2 "行动困难"
        local panel_label3 "残障补助"
        local panel_label4 "年度就业"
        local unit1 "对数点效应"
        local unit2 "指数点效应"
        local unit3 "补助效应"
        local unit4 "百分点效应"
        local group_label1 "估计值"
        local wholetitle "不同规格的估计结果"
    }
    else {
        local panel_label1 "Log mortality"
        local panel_label2 "Ambulatory difficulty"
        local panel_label3 "Disability transfer"
        local panel_label4 "Annual employment"
        local unit1 "Log-point effect"
        local unit2 "Index-point effect"
        local unit3 "Transfer effect"
        local unit4 "Percentage-point effect"
        local group_label1 "Estimate"
        local wholetitle "Specification sensitivity"
    }
}
else if `"`variant'"' == "subgroup" {
    local np 1
    local panel1 "education"
    local ng 2
    local group1 "group_a"
    local group2 "group_b"
    local preferred ""
    if `"`lang'"' == "zh" {
        local panel_label1 "教育结果"
        local unit1 "估计效应"
        local group_label1 "甲组"
        local group_label2 "乙组"
        local wholetitle "分组效应"
    }
    else {
        local panel_label1 "Educational attainment"
        local unit1 "Estimated effect"
        local group_label1 "Group A"
        local group_label2 "Group B"
        local wholetitle "Effects by group"
    }
}
else {
    display as error "variant must match a configured variant"
    exit 198
}
if !inrange(`np', 1, 4) | !inrange(`ng', 1, 3) exit 198

capture log close forest
log using "grouped_coefficient_forest_stata.log", text replace name(forest)
import delimited using `"`input'"', clear varnames(1) stringcols(_all) encoding(UTF-8)
confirm variable variant panel panel_order term term_order term_label_en term_label_zh group group_order estimate ci_low ci_high
capture confirm variable se
if _rc generate str1 se = ""
keep if variant == `"`variant'"'
assert _N > 0
destring panel_order term_order group_order estimate ci_low ci_high se, replace
generate byte both_missing = missing(ci_low) & missing(ci_high)
assert missing(ci_low) == missing(ci_high)
replace ci_low = estimate - 1.96*se if both_missing & !missing(se) & se >= 0
replace ci_high = estimate + 1.96*se if both_missing & !missing(se) & se >= 0
drop both_missing
assert !missing(panel, group, term, panel_order, term_order, group_order, estimate, ci_low, ci_high)
assert ci_low <= estimate & estimate <= ci_high
isid panel term group
generate byte valid_panel = 0
generate byte valid_group = 0
forvalues j = 1/`np' {
    replace valid_panel = 1 if panel == `"`panel`j''"' & panel_order == `j'
}
forvalues k = 1/`ng' {
    replace valid_group = 1 if group == `"`group`k''"' & group_order == `k'
}
assert valid_panel == 1 & valid_group == 1
drop valid_panel valid_group

local graphs ""
forvalues j = 1/`np' {
    preserve
    keep if panel == `"`panel`j''"'
    quietly count
    local n`j' = r(N)
    assert r(N) > 0
    quietly summarize term_order
    local nt = r(max)
    assert r(min) == 1
    forvalues t = 1/`nt' {
        quietly count if term_order == `t' & group_order == 1
        assert r(N) == 1
        forvalues k = 1/`ng' {
            quietly count if term_order == `t' & group_order == `k'
            assert r(N) == 1
        }
    }
    if `"`orientation'"' == "horizontal" {
        local current_terms ""
        forvalues t = 1/`nt' {
            quietly levelsof term if term_order == `t' & group_order == 1, local(termid) clean
            local current_terms `"`current_terms'|`termid'"'
        }
        if `j' == 1 local common_terms `"`current_terms'"'
        else if `"`current_terms'"' != `"`common_terms'"' {
            display as error "horizontal panels must have identical ordered term IDs"
            exit 459
        }
    }
    quietly summarize ci_low
    local low = min(0, r(min))
    quietly summarize ci_high
    local high = max(0, r(max))
    local pad = max((`high'-`low')*.12, .001)
    local lower = `low'-`pad'
    local upper = `high'+`pad'
    local ticks ""
    forvalues t = 1/`nt' {
        if `"`lang'"' == "zh" quietly levelsof term_label_zh if term_order == `t', local(tlabel) clean
        else quietly levelsof term_label_en if term_order == `t', local(tlabel) clean
        if `"`orientation'"' == "horizontal" local tickpos = `nt'+1-`t'
        else local tickpos = `t'
        local ticks `"`ticks' `tickpos' `"`tlabel'"'"'
    }

    local layers ""
    local legend_items ""
    local plotnum 0
    forvalues k = 1/`ng' {
        local gid `"`group`k''"'
        if `k' == 1 local color "black"
        else if `k' == 2 local color "gs8"
        else local color "navy"
        if `k' == 1 local symbol "O"
        else if `k' == 2 local symbol "Th"
        else local symbol "S"
        local offset = (`k'-(`ng'+1)/2)*.22
        if `"`orientation'"' == "horizontal" {
            generate double ypos`k' = `nt'+1-term_order+`offset' if group_order == `k'
            if `"`preferred'"' != "" {
                local layers `"`layers' (rcap ci_low ci_high ypos`k' if group == `"`gid'"' & term != `"`preferred'"', horizontal lcolor(`color') lwidth(medthin))"'
                local layers `"`layers' (rcap ci_low ci_high ypos`k' if group == `"`gid'"' & term == `"`preferred'"', horizontal lcolor(red) lwidth(medthin))"'
                local plotnum = `plotnum'+2
            }
            else {
                local layers `"`layers' (rcap ci_low ci_high ypos`k' if group == `"`gid'"', horizontal lcolor(`color') lwidth(medthin))"'
                local plotnum = `plotnum'+1
            }
            local layers `"`layers' (scatter ypos`k' estimate if group == `"`gid'"' & term != `"`preferred'"', msymbol(`symbol') mcolor(white) mlcolor(`color') msize(medsmall))"'
            local plotnum = `plotnum'+1
            if `"`preferred'"' != "" {
                local layers `"`layers' (scatter ypos`k' estimate if group == `"`gid'"' & term == `"`preferred'"', msymbol(O) mcolor(red) mlcolor(red) msize(medsmall))"'
                local plotnum = `plotnum'+1
            }
        }
        else {
            generate double xpos`k' = term_order+`offset' if group_order == `k'
            local layers `"`layers' (rcap ci_low ci_high xpos`k' if group == `"`gid'"', lcolor(gs9) lwidth(medthin))"'
            local plotnum = `plotnum'+1
            local layers `"`layers' (scatter estimate xpos`k' if group == `"`gid'"', msymbol(`symbol') mcolor(`=cond(`k'==1,"black","white")') mlcolor(`color') msize(medium))"'
            local plotnum = `plotnum'+1
        }
        if `ng' > 1 local legend_items `"`legend_items' `plotnum' `"`group_label`k''"'"'
    }
    if `"`orientation'"' == "horizontal" {
        if `ng' == 1 local legendoption "legend(off)"
        else local legendoption `"legend(order(`legend_items') rows(1) size(vsmall))"'
        if `j' == 1 local ylabeloption `"ylabel(`ticks', angle(0) labsize(small))"'
        else local ylabeloption "ylabel(none)"
        local prefline ""
        if `"`preferred'"' != "" {
            quietly summarize estimate if term == `"`preferred'"' & group_order == 1
            if r(N) == 1 local prefline `"xline(`=r(mean)', lcolor(gs8) lpattern(dash) lwidth(thin))"'
        }
        twoway `layers', xline(0, lcolor(gs5) lwidth(thin)) `prefline' ///
            xscale(range(`lower' `upper')) yscale(range(.5 `=`nt'+.5')) ///
            `ylabeloption' `legendoption' ///
            xtitle(`"`unit`j''"', size(small)) ytitle("") subtitle(`"`panel_label`j''"', size(small)) ///
            graphregion(color(white)) plotregion(color(white)) scheme(s1mono) ///
            name(forest_`j', replace)
    }
    else {
        if `ng' == 1 local legendoption "legend(off)"
        else local legendoption `"legend(order(`legend_items') rows(1) size(vsmall))"'
        local subtitleoption ""
        if `np' > 1 local subtitleoption `"subtitle(`"`panel_label`j''"', size(small))"'
        twoway `layers', yline(0, lcolor(gs5) lwidth(thin)) ///
            yscale(range(`lower' `upper')) xscale(range(.5 `=`nt'+.5')) ///
            xlabel(`ticks', labsize(vsmall)) ylabel(, angle(0)) `legendoption' ///
            ytitle(`"`unit`j''"', size(small)) `subtitleoption' ///
            graphregion(color(white)) plotregion(color(white)) scheme(s1mono) ///
            name(forest_`j', replace)
    }
    local graphs "`graphs' forest_`j'"
    display "PANEL `panel`j'' N=`n`j'' terms=`nt' groups=`ng'"
    restore
}
local titleoption ""
if `"`showtitle'"' == "1" local titleoption `"title(`"`wholetitle'"', size(medium))"'
graph combine `graphs', cols(`np') xsize(`=max(7.5,3.0*`np'+2.5)') ysize(5.1) ///
    graphregion(color(white)) `titleoption'
graph export `"`output'"', as(png) width(2400) replace
local pdfoutput = subinstr(`"`output'"', ".png", ".pdf", .)
graph export `"`pdfoutput'"', as(pdf) replace
display "STATA_COMPLETE variant=`variant' orientation=`orientation' lang=`lang' panels=`np' output=`output' pdf=`pdfoutput'"
log close forest
