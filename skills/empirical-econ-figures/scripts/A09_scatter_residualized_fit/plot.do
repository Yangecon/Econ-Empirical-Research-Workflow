* Two-panel residualized scatter. Edit CONFIG blocks for another study.
version 19.0
args input output lang showtitle
if `"`input'"' == "" local input "demo.csv"
if `"`output'"' == "" local output "residualized_scatter_stata_en.png"
if `"`lang'"' == "" local lang "en"
if `"`showtitle'"' == "" local showtitle "0"
if !inlist(`"`lang'"', "en", "zh") exit 198

* CONFIG: exactly two panels, with two or three groups each.
* List highlighted groups first and gray background group last.
local panel1 "all_fields"
local panel1_group_count 2
local panel1_group1 "medicine"
local panel1_group2 "other"
local panel1_group3 ""
local panel2 "computer_science"
local panel2_group_count 3
local panel2_group1 "ai_late"
local panel2_group2 "ai_early"
local panel2_group3 "other"

* CONFIG: display labels and axes. Match IDs above to the input CSV.
if `"`lang'"' == "zh" {
    local xlab "X 的残差"
    local ylab "Y 的残差"
    local title1 "(a) 样本 A"
    local title2 "(b) 样本 B"
    local label11 "组 A"
    local label12 "其他组"
    local label13 ""
    local label21 "组 A"
    local label22 "组 B"
    local label23 "其他组"
    local wholetitle "X 与 Y 的残差关系"
}
else {
    local xlab "Residualized X"
    local ylab "Residualized Y"
    local title1 "(a) Sample A"
    local title2 "(b) Sample B"
    local label11 "Group A"
    local label12 "Other groups"
    local label13 ""
    local label21 "Group A"
    local label22 "Group B"
    local label23 "Other groups"
    local wholetitle "Residualized X and Y"
}

capture log close residual_scatter
log using "residualized_scatter_stata.log", text replace name(residual_scatter)
import delimited using `"`input'"', clear varnames(1) stringcols(_all) encoding(UTF-8)
confirm variable panel group rx ry
destring rx ry, replace
assert !missing(panel, group, rx, ry)
assert inlist(panel, `"`panel1'"', `"`panel2'"')

generate byte valid_group = 0
forvalues j = 1/2 {
    local ng = `panel`j'_group_count'
    assert inrange(`ng', 2, 3)
    forvalues k = 1/`ng' {
        local gid `"`panel`j'_group`k''"'
        replace valid_group = 1 if panel == `"`panel`j''"' & group == `"`gid'"'
        quietly count if panel == `"`panel`j''"' & group == `"`gid'"'
        assert r(N) > 0
    }
}
assert valid_group == 1
drop valid_group

forvalues j = 1/2 {
    preserve
    keep if panel == `"`panel`j''"'
    quietly count
    local n`j' = r(N)
    assert r(N) >= 3
    quietly summarize rx
    local xmin = r(min)
    local xmax = r(max)
    assert `xmax' > `xmin'
    quietly summarize ry
    local ymin = r(min)
    local ymax = r(max)
    quietly regress ry rx
    local intercept = _b[_cons]
    local slope = _b[rx]
    local eq "y = `=string(`intercept',"%6.3f")' `=cond(`slope'<0,"-","+")' `=string(abs(`slope'),"%5.3f")'x"
    local tx = `xmin' + .04*(`xmax'-`xmin')
    local ty = `ymax' - .04*(`ymax'-`ymin')
    display "PANEL `panel`j'' N=`n`j'' intercept=" %10.6f `intercept' " slope=" %10.6f `slope'

    local ng = `panel`j'_group_count'
    local layers `"(function y=`intercept'+`slope'*x, range(`xmin' `xmax') lcolor(gs10) lpattern(dash) lwidth(medthin))"'
    local legend_items ""
    forvalues k = `ng'(-1)1 {
        local gid `"`panel`j'_group`k''"'
        if `k' == `ng' local color "gs13"
        else if `k' == 1 local color "maroon"
        else local color "black"
        local layers `"`layers' (scatter ry rx if group == `"`gid'"', msymbol(plus) mcolor(`color') msize(small))"'
        local plotnum = `ng' - `k' + 2
        local legend_items `"`plotnum' `"`label`j'`k''"' `legend_items'"'
    }
    twoway `layers', ///
        legend(order(`legend_items') rows(1) size(vsmall) region(lcolor(gs8))) ///
        xtitle(`"`xlab'"', size(small)) ytitle(`"`ylab'"', size(small)) ///
        subtitle(`"`title`j''"', size(medsmall)) ///
        text(`ty' `tx' `"`eq'"', placement(e) size(small) color(black)) ///
        graphregion(color(white)) plotregion(color(white)) scheme(s1mono) ///
        name(resid_`j', replace)
    restore
}

local titleoption ""
if `"`showtitle'"' == "1" local titleoption `"title(`"`wholetitle'"', size(medium))"'
graph combine resid_1 resid_2, cols(2) xsize(11.2) ysize(5.2) ///
    graphregion(color(white)) `titleoption'
graph export `"`output'"', as(png) width(2240) replace
local pdfoutput = subinstr(`"`output'"', ".png", ".pdf", .)
graph export `"`pdfoutput'"', as(pdf) replace
display "STATA_COMPLETE N1=`n1' N2=`n2' output=`output' pdf=`pdfoutput'"
log close residual_scatter
