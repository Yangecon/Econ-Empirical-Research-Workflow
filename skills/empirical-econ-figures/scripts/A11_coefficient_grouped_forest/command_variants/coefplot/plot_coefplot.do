* Package variant of grouped_coefficient_forest. Requires Ben Jann's coefplot.
* CSV has already-calculated endpoints; coefplot receives matrix rows b, ll, ul.
version 19.0
args input output lang variant orientation showtitle packages
if `"`input'"' == "" | `"`output'"' == "" exit 198
if `"`lang'"' == "" local lang "en"
if `"`variant'"' == "" local variant "robustness"
if `"`orientation'"' == "" {
    if `"`variant'"' == "subgroup" local orientation "vertical"
    else local orientation "horizontal"
}
if `"`showtitle'"' == "" local showtitle "0"
if !inlist(`"`lang'"', "en", "zh") exit 198
if !inlist(`"`variant'"', "robustness", "subgroup") exit 198
if !inlist(`"`orientation'"', "horizontal", "vertical") exit 198
if !inlist(`"`showtitle'"', "0", "1") exit 198
if `"`packages'"' != "" adopath ++ `"`packages'"'

capture which coefplot
if _rc {
    display as error "Ben Jann's coefplot is required; install only into project work/stata_packages"
    exit 499
}
if `"`variant'"' == "robustness" {
    local np 4
    local ng 1
    local panel1 "mortality"
    local panel2 "difficulty"
    local panel3 "transfer"
    local panel4 "employment"
    local group1 "main"
    local group_label1 "Estimate"
    if `"`lang'"' == "zh" {
        local panel_label1 "死亡率对数"
        local panel_label2 "行动困难"
        local panel_label3 "残障补助"
        local panel_label4 "年度就业"
        local unit1 "对数点效应"
        local unit2 "指数点效应"
        local unit3 "补助效应"
        local unit4 "百分点效应"
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
        local wholetitle "Specification sensitivity"
    }
}
else {
    local np 1
    local ng 2
    local panel1 "education"
    local group1 "group_a"
    local group2 "group_b"
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
drop valid_panel valid_group both_missing

local graphs ""
forvalues j = 1/`np' {
    preserve
    keep if panel == `"`panel`j''"'
    quietly summarize term_order
    local nt = r(max)
    assert r(min) == 1
    local modelplots ""
    local orderlist ""
    local labellist ""
    forvalues t = 1/`nt' {
        quietly levelsof term if term_order == `t' & group_order == 1, local(termid) clean
        assert `"`termid'"' != ""
        capture confirm name `termid'
        if _rc {
            display as error "term must be a valid Stata coefficient name: `termid'"
            exit 198
        }
        if `"`lang'"' == "zh" quietly levelsof term_label_zh if term_order == `t' & group_order == 1, local(tlabel) clean
        else quietly levelsof term_label_en if term_order == `t' & group_order == 1, local(tlabel) clean
        local term`t' `"`termid'"'
        local labellist `"`labellist' `termid' = `"`tlabel'"'"'
        if `"`orientation'"' == "horizontal" local orderlist `"`termid' `orderlist'"'
        else local orderlist `"`orderlist' `termid'"'
        forvalues k = 1/`ng' {
            quietly count if term_order == `t' & group_order == `k'
            assert r(N) == 1
        }
    }
    forvalues k = 1/`ng' {
        sort term_order
        mkmat estimate ci_low ci_high if group_order == `k', matrix(raw`k')
        matrix B`k' = raw`k''
        local cols ""
        forvalues t = 1/`nt' {
            local cols "`cols' `term`t''"
        }
        matrix colnames B`k' = `cols'
        matrix rownames B`k' = b ll ul
        if `k' == 1 {
            local color "black"
            local symbol "O"
        }
        else {
            local color "gs8"
            local symbol "Th"
        }
        if `"`variant'"' == "robustness" {
            local modelplots `"`modelplots' (matrix(B`k'), ci((2 3)) drop(preferred) offset(0) msymbol(`symbol') mcolor(`color') mlcolor(`color') ciopts(lcolor(`color') lwidth(medthin)))"'
            local modelplots `"`modelplots' (matrix(B`k'), ci((2 3)) keep(preferred) offset(0) msymbol(`symbol') mcolor("197 27 43") mlcolor("197 27 43") ciopts(lcolor("197 27 43") lwidth(medthin)))"'
        }
        else local modelplots `"`modelplots' (matrix(B`k'), ci((2 3)) label(`"`group_label`k''"') msymbol(`symbol') mcolor(`color') mlcolor(`color') ciopts(lcolor(`color') lwidth(medthin)))"'
    }
    quietly summarize ci_low
    local low = min(0, r(min))
    quietly summarize ci_high
    local high = max(0, r(max))
    local pad = max((`high'-`low')*.12, .001)
    local lower = `low'-`pad'
    local upper = `high'+`pad'
    local titleopts ""
    if `np' > 1 local titleopts `"subtitle(`"`panel_label`j''"', size(small))"'
    if `"`orientation'"' == "horizontal" {
        local axisopts `"horizontal xline(0, lcolor(gs5) lwidth(thin)) xscale(range(`lower' `upper')) xtitle(`"`unit`j''"') ytitle("")"'
    }
    else {
        local axisopts `"vertical yline(0, lcolor(gs5) lwidth(thin)) yscale(range(`lower' `upper')) ytitle(`"`unit`j''"') xtitle("")"'
    }
    if `ng' == 1 local leg "legend(off)"
    else local leg "legend(rows(1) size(vsmall))"
    coefplot `modelplots', ciopts(recast(rcap)) order(`orderlist') ///
        coeflabels(`labellist') `axisopts' `titleopts' `leg' ///
        graphregion(color(white)) plotregion(color(white)) scheme(s1mono) ///
        name(coef_panel`j', replace)
    local graphs "`graphs' coef_panel`j'"
    display "COEFPLOT_PANEL `panel`j'' rows=" _N " terms=`nt' groups=`ng'"
    restore
}
local titleoption ""
if `"`showtitle'"' == "1" local titleoption `"title(`"`wholetitle'"', size(medium))"'
graph combine `graphs', cols(`np') xsize(`=max(7.5,3.0*`np'+2.5)') ysize(5.1) ///
    graphregion(color(white)) `titleoption'
graph export `"`output'"', as(png) width(2400) replace
local pdfoutput = subinstr(`"`output'"', ".png", ".pdf", .)
graph export `"`pdfoutput'"', as(pdf) replace
display "COEFPLOT_COMPLETE variant=`variant' orientation=`orientation' lang=`lang' output=`output' pdf=`pdfoutput'"
