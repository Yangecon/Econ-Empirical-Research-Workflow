* Binned RD display: equal-width bins and side-local OLS on underlying observations.
version 19.0
args input output lang showtitle
if `"`input'"' == "" local input "demo.csv"
if `"`output'"' == "" {
    display as error "output PNG path required"
    exit 198
}
if `"`lang'"' == "" local lang "en"
if `"`showtitle'"' == "" local showtitle "0"
if !inlist(`"`lang'"', "en", "zh") exit 198

* CONFIG: parallel to plot.py. Units and windows may differ across panels.
local panel1 "outcome_a"
local panel2 "outcome_b"
local bw1 16
local bw2 25
local nb1 10
local nb2 10
local xticks1 "-15(5)15"
local xticks2 "-20(10)20"
local ymin1 -.008
local ymin2 -.008
local ymax1 .26
local ymax2 .26
if `"`lang'"' == "zh" {
    local name1 "（A）结果 A"
    local name2 "（B）结果 B"
    local xlab "相对断点的运行变量"
    local ylab "结果发生概率"
    local heading "断点两侧的分箱结果"
}
else {
    local name1 "(A) Outcome A"
    local name2 "(B) Outcome B"
    local xlab "Running variable relative to cutoff"
    local ylab "Outcome probability"
    local heading "Binned outcomes around a cutoff"
}

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
confirm variable panel id running outcome
assert !missing(panel, id, running, outcome)
assert inlist(panel, "`panel1'", "`panel2'")
isid panel id
generate double running_num = real(running)
generate double outcome_num = real(outcome)
drop running outcome
rename running_num running
rename outcome_num outcome
assert !missing(running, outcome) & inrange(outcome, 0, 1)
generate double bw = cond(panel=="`panel1'", `bw1', `bw2')
generate int nb = cond(panel=="`panel1'", `nb1', `nb2')
assert bw > 0 & nb >= 3
generate byte selected = abs(running) <= bw
generate byte cutoff_zero = selected & running==0
local total_input_n = _N
local stem = regexr(`"`output'"', "[.]png$", "")
preserve
collapse (count) total_input_n=outcome (sum) window_n=selected cutoff_zero_n=cutoff_zero, by(panel)
assert _N == 2
generate long excluded_outside_bandwidth_n = total_input_n-window_n
export delimited using `"`stem'_sample.csv"', replace
restore
keep if selected
local window_n = _N
generate str5 side = cond(running<0, "left", "right")
bysort panel side: assert _N >= 3*nb
bysort panel side: egen double minx = min(running)
bysort panel side: egen double maxx = max(running)
assert maxx > minx
drop minx maxx
generate double width = bw/nb
generate int bin = min(floor(cond(side=="left", (running+bw)/width, running/width)), nb-1)+1
assert inrange(bin, 1, nb)
tempfile window
save `window'

tempname fitpost
tempfile fits
postfile `fitpost' str32 panel str5 side double n double intercept_at_cutoff double slope double fit_x_min double fit_x_max using `fits', replace
forvalues i = 1/2 {
    foreach side in left right {
        use `window', clear
        keep if panel=="`panel`i''" & side=="`side'"
        assert _N >= 3*`nb`i''
        local n = _N
        quietly regress outcome running
        local b0 = _b[_cons]
        local b1 = _b[running]
        local xmin = cond("`side'"=="left", -`bw`i'', 0)
        local xmax = cond("`side'"=="left", 0, `bw`i'')
        assert inrange(`b0'+`b1'*`xmin', `ymin`i'', `ymax`i'')
        assert inrange(`b0'+`b1'*`xmax', `ymin`i'', `ymax`i'')
        post `fitpost' ("`panel`i''") ("`side'") (`n') (`b0') (`b1') (`xmin') (`xmax')
        local a`i'_`side' = `b0'
        local b`i'_`side' = `b1'
    }
}
postclose `fitpost'
use `fits', clear
export delimited using `"`stem'_fits.csv"', replace

use `window', clear
collapse (mean) x_mean=running y_mean=outcome (count) n=outcome, by(panel side bin)
forvalues i = 1/2 {
    foreach side in left right {
        quietly count if panel=="`panel`i''" & side=="`side'"
        assert r(N) == `nb`i''
    }
}
assert n >= 2
forvalues i = 1/2 {
    assert inrange(y_mean, `ymin`i'', `ymax`i'') if panel=="`panel`i''"
}
export delimited using `"`stem'_bins.csv"', replace
local bin_n = _N
forvalues i = 1/2 {
    local titleopt `"title(`"`name`i''"', size(medsmall))"'
    twoway ///
        (function y=`a`i'_left'+`b`i'_left'*x, range(-`bw`i'' 0) lcolor(black) lwidth(medium)) ///
        (function y=`a`i'_right'+`b`i'_right'*x, range(0 `bw`i'') lcolor(black) lwidth(medium)) ///
        (scatter y_mean x_mean if panel=="`panel`i''", msymbol(O) mcolor(gs7) msize(medsmall)), ///
        xline(0, lcolor(black) lpattern(dash) lwidth(thin)) ///
        yline(0, lcolor(red) lpattern(dash) lwidth(thin)) ///
        xscale(range(-`bw`i'' `bw`i'') noextend) yscale(range(`ymin`i'' `ymax`i'') noextend) ///
        xlabel(`xticks`i'', labsize(small)) ///
        ylabel(0(.05).25, angle(0) labsize(small) grid glcolor(gs14)) ///
        xtitle(`"`xlab'"', size(small)) ytitle(`"`ylab'"', size(small)) `titleopt' ///
        legend(off) graphregion(color(white) margin(small)) plotregion(color(white)) scheme(s1mono) ///
        name(g`i', replace)
}
local maintitle ""
if `"`showtitle'"' == "1" local maintitle `"title(`"`heading'"', size(medium))"'
graph combine g1 g2, cols(1) `maintitle' graphregion(color(white)) xsize(7.4) ysize(8.8)
graph export `"`output'"', width(1628) replace
local pdf = regexr(`"`output'"', "[.]png$", ".pdf")
graph export `"`pdf'"', replace
display "STATA_COMPLETE input_rows=`total_input_n' window_rows=`window_n' bins=`bin_n' fits=4 output=`output'"
