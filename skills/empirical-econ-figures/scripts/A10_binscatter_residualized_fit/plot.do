* Equal-count bins of supplied residuals; OLS fit uses underlying observations.
version 19.0
args input output lang bins showtitle
if `"`input'"' == "" local input "demo.csv"
if `"`output'"' == "" local output "residualized_binned_stata_en.png"
if `"`lang'"' == "" local lang "en"
if `"`bins'"' == "" local bins 50
if `"`showtitle'"' == "" local showtitle "0"
if !inlist(`"`lang'"', "en", "zh") exit 198

* Edit labels for another pair of already-residualized variables.
if `"`lang'"' == "zh" {
    local xlab "距离×1994年缓冲带降雨量的残差"
    local ylab "民兵活动对数的残差"
    local wholetitle "分箱后的第一阶段关系"
}
else {
    local xlab "Residualized distance × rainfall, 1994"
    local ylab "Residualized log militia activity"
    local wholetitle "Binned first-stage relationship"
}

capture log close binned_scatter
log using "residualized_binned_scatter_stata.log", text replace name(binned_scatter)
import delimited using `"`input'"', clear varnames(1) stringcols(_all) encoding(UTF-8)
confirm variable id rx ry
destring rx ry, replace
assert !missing(id, rx, ry)
isid id
local n = _N
assert inrange(`bins', 2, `n')
quietly summarize rx
local xmin = r(min)
local xmax = r(max)
assert `xmax' > `xmin'
quietly regress ry rx
local intercept = _b[_cons]
local slope = _b[rx]
display "OBSERVATION_FIT N=`n' intercept=" %12.8f `intercept' " slope=" %12.8f `slope'

* Tie rule: sort by numeric rx, then unique text ID; rank r gets
* bin floor((r-1)*B/N)+1. The same complete rows supplied the OLS fit.
sort rx id
generate int bin = floor((_n-1)*`bins'/`n')+1
collapse (mean) x_mean=rx y_mean=ry (count) n=ry, by(bin)
quietly count
assert r(N) == `bins'
quietly summarize n
local minn = r(min)
local maxn = r(max)
assert `maxn' - `minn' <= 1
export delimited using "bin_summary_stata_`lang'.csv", replace

local titleoption ""
if `"`showtitle'"' == "1" local titleoption `"title(`"`wholetitle'"', size(medium))"'
twoway ///
    (function y=`intercept'+`slope'*x, range(`xmin' `xmax') lcolor(black) lwidth(medium)) ///
    (scatter y_mean x_mean, msymbol(D) mcolor(gs7) msize(medsmall)), ///
    legend(off) yline(0, lcolor(gs12) lwidth(thin)) ylabel(, angle(0)) ///
    xtitle(`"`xlab'"', size(small)) ytitle(`"`ylab'"', size(small)) ///
    graphregion(color(white)) plotregion(color(white)) scheme(s1mono) ///
    xsize(8.2) ysize(4.7) `titleoption'
graph export `"`output'"', as(png) width(1804) replace
local pdfoutput = subinstr(`"`output'"', ".png", ".pdf", .)
graph export `"`pdfoutput'"', as(pdf) replace
display "STATA_COMPLETE lang=`lang' N=`n' bins=`bins' min_bin_n=`minn' max_bin_n=`maxn' output=`output' pdf=`pdfoutput'"
log close binned_scatter
