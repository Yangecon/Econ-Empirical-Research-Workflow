* Supplied estimates/CIs plus separate pre-binned unconditional support counts.
version 19.0
args effects support output lang showtitle
if `"`effects'"' == "" local effects "effect_demo.csv"
if `"`support'"' == "" local support "support_demo.csv"
if `"`output'"' == "" {
    display as error "output PNG path is required"
    exit 198
}
if `"`lang'"' == "" local lang "en"
if `"`showtitle'"' == "" local showtitle "0"
if !inlist(`"`lang'"', "en", "zh") exit 198

* CONFIG: keep panel IDs, independent x/y units, and bounds aligned with Python.
local np 4
local panel1 "destination_share"
local panel2 "destination_degree"
local panel3 "home_share"
local panel4 "home_degree"
local xmin1 0
local xmax1 1
local ymin1 0
local ymax1 .08
local yticks1 ".02(.02).08"
local countticks1 "0(2000)8000"
local xmin2 .5
local xmax2 20.5
local ymin2 -1
local ymax2 2
local yticks2 "-.5(.5)2"
local countticks2 "0(3000)9000"
local xmin3 0
local xmax3 1
local ymin3 0
local ymax3 .08
local yticks3 ".02(.02).08"
local countticks3 "0(2000)6000"
local xmin4 .5
local xmax4 20.5
local ymin4 -1
local ymax4 2
local yticks4 "-.5(.5)2"
local countticks4 "0(1000)5000"
if `"`lang'"' == "zh" {
    local xlab1 "目的地共同支持比例"
    local xlab2 "目的地网络规模"
    local xlab3 "原居地共同支持比例"
    local xlab4 "原居地网络规模"
    local ylab1 "迁移率"
    local ylab2 "估计效应"
    local ylab3 "迁移率"
    local ylab4 "估计效应"
    local countlabel "样本数"
    local titletext "效应与样本分布"
}
else {
    local xlab1 "Destination support share"
    local xlab2 "Destination network size"
    local xlab3 "Home support share"
    local xlab4 "Home network size"
    local ylab1 "Migration rate"
    local ylab2 "Estimated effect"
    local ylab3 "Migration rate"
    local ylab4 "Estimated effect"
    local countlabel "Count"
    local titletext "Effects and support"
}

* Create every prefix of an output directory, including a new nested path.
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

capture log close supportplot
log using "binned_effect_with_support_histogram_stata.log", text replace name(supportplot)
import delimited using `"`effects'"', clear varnames(1) stringcols(_all) encoding(UTF-8)
confirm variable panel panel_order x estimate ci_low ci_high
assert !missing(panel)
destring panel_order x estimate ci_low ci_high, replace
assert !missing(panel_order, x, estimate, ci_low, ci_high)
assert ci_low <= estimate & estimate <= ci_high
isid panel x
generate byte valid = 0
forvalues j = 1/`np' {
    replace valid = 1 if panel == `"`panel`j''"' & panel_order == `j'
    quietly count if panel == `"`panel`j''"'
    assert r(N) > 0
    assert inrange(x, `xmin`j'', `xmax`j'') & inrange(ci_low, `ymin`j'', `ymax`j'') & inrange(ci_high, `ymin`j'', `ymax`j'') if panel == `"`panel`j''"'
}
assert valid == 1
drop valid
tempfile effectdata supportdata
save `effectdata'

import delimited using `"`support'"', clear varnames(1) stringcols(_all) encoding(UTF-8)
confirm variable panel panel_order x_left x_right count
assert !missing(panel)
destring panel_order x_left x_right count, replace
assert !missing(panel_order, x_left, x_right, count)
assert x_left < x_right & count >= 0 & count == floor(count)
isid panel x_left
generate byte valid = 0
forvalues j = 1/`np' {
    replace valid = 1 if panel == `"`panel`j''"' & panel_order == `j'
    quietly count if panel == `"`panel`j''"'
    assert r(N) > 0
    assert inrange(x_left, `xmin`j'', `xmax`j'') & inrange(x_right, `xmin`j'', `xmax`j'') if panel == `"`panel`j''"'
}
assert valid == 1
drop valid
sort panel_order x_left
by panel_order: assert x_left >= x_right[_n-1]-1e-10 if _n > 1
generate double binwidth = x_right-x_left
bysort panel_order: assert abs(binwidth-binwidth[1]) < 1e-10
generate double xmid = (x_left+x_right)/2
save `supportdata'

local panels ""
forvalues j = 1/`np' {
    use `effectdata', clear
    keep if panel == `"`panel`j''"'
    local heading ""
    if `np' > 1 {
        local letter = char(96+`j')
        local heading `"title("(`letter') `xlab`j''", size(small) position(11))"'
    }
    local zeroline ""
    if `ymin`j'' < 0 & `ymax`j'' > 0 local zeroline "yline(0, lcolor(gs9) lpattern(dash))"
    local xticks "0(.2)1"
    if `j' == 2 | `j' == 4 local xticks "1 5 10 15 20"
    twoway (rcap ci_low ci_high x, lcolor(gs4) lwidth(medthin)) ///
        (scatter estimate x, mcolor(gs2) msymbol(O) msize(small)), ///
        xscale(range(`xmin`j'' `xmax`j'') noextend) yscale(range(`ymin`j'' `ymax`j'') noextend) ///
        xlabel(`xticks', nolabel noticks) xtitle("") ytitle(`"`ylab`j''"', size(small)) ///
        ylabel(`yticks`j'', angle(0) labelminlen(8) labsize(small) grid glcolor(gs14)) ///
        legend(off) `zeroline' `heading' ///
        graphregion(color(white)) plotregion(margin(zero) color(white)) scheme(s1mono) ///
        xsize(5.2) ysize(3.3) name(top_`j', replace)
    use `supportdata', clear
    keep if panel == `"`panel`j''"'
    quietly summarize binwidth
    local bw = r(mean)
    quietly summarize count
    local countmax = ceil(r(max)*1.08/1000)*1000
    twoway (bar count xmid, barwidth(`bw') fcolor(gs9) lcolor(gs7) lwidth(vthin)), ///
        xscale(range(`xmin`j'' `xmax`j'') noextend) yscale(range(0 `countmax') noextend) ///
        xlabel(`xticks') ///
        xtitle(`"`xlab`j''"', size(small)) ytitle(`"`countlabel'"', size(small)) ///
        ylabel(`countticks`j'', angle(0) labelminlen(8) labsize(small) grid glcolor(gs14)) ///
        legend(off) ///
        graphregion(color(white)) plotregion(margin(zero) color(white)) scheme(s1mono) ///
        xsize(5.2) ysize(1.6) name(bottom_`j', replace)
    graph combine top_`j' bottom_`j', cols(1) imargin(0 0 0 0) ///
        graphregion(color(white)) xsize(5.2) ysize(5.0) name(pair_`j', replace)
    local panels "`panels' pair_`j'"
    display "PANEL `panel`j'' effects and support bins rendered"
}
local titleoption ""
if `"`showtitle'"' == "1" local titleoption `"title(`"`titletext'"')"'
local cols = cond(`np'>1, 2, 1)
graph combine `panels', cols(`cols') imargin(0 0 0 0) ///
    graphregion(color(white)) `titleoption' xsize(`=5.2*`cols'') ysize(`=5.0*ceil(`np'/`cols')')
graph export `"`output'"', as(png) width(2400) replace
local pdfoutput = subinstr(`"`output'"', ".png", ".pdf", .)
graph export `"`pdfoutput'"', as(pdf) replace
display "STATA_COMPLETE panels=`np' output=`output'"
log close supportplot
