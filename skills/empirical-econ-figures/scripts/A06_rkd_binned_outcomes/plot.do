* Continuous kink fit on underlying rows; bins used only for plotted summaries.
version 19.0
args input output lang showtitle
if `"`input'"'=="" local input "demo.csv"
if `"`output'"'=="" {
    display as error "output PNG path required"
    exit 198
}
if `"`lang'"'=="" local lang "en"
if `"`showtitle'"'=="" local showtitle "0"
if !inlist(`"`lang'"',"en","zh") exit 198
* CONFIG matches plot.py; all panel y scales are deliberately separate.
local threshold 850
local xmin 500
local xmax 1200
local p1 "replacement"
local p2 "takeup"
local p3 "risk_basic"
local p4 "risk_comprehensive"
local ymin1 .55
local ymax1 .82
local ymin2 .75
local ymax2 .94
local ymin3 1.2
local ymax3 4.1
local ymin4 7.7
local ymax4 10.7
local nb1 12
local nb2 12
local nb3 12
local nb4 12
local yticks1 ".55(.05).80"
local yticks2 ".75(.05).90"
local yticks3 "1.5(.5)4"
local yticks4 "8(.5)10.5"
if `"`lang'"'=="zh" {
    local paneltitle1 "（A）替代率"
    local paneltitle2 "（B）保险购买比例"
    local paneltitle3 "（C）基本保险风险"
    local paneltitle4 "（D）综合保险风险"
    local ylabel1 "日津贴／日工资"
    local ylabel2 "保险购买概率"
    local ylabel3 "预测失业天数"
    local ylabel4 "预测失业天数"
    local xlabeltext "运行变量（示例单位）"
    local heading "政策折点两侧的结果"
}
else {
    local paneltitle1 "(A) Replacement rate"
    local paneltitle2 "(B) Coverage take-up"
    local paneltitle3 "(C) Risk under basic coverage"
    local paneltitle4 "(D) Risk under comprehensive coverage"
    local ylabel1 "Daily benefits / daily wage"
    local ylabel2 "Coverage purchase probability"
    local ylabel3 "Predicted unemployment days"
    local ylabel4 "Predicted unemployment days"
    local xlabeltext "Running variable (illustrative units)"
    local heading "Outcomes around a policy kink"
}
assert `xmin'<`threshold' & `threshold'<`xmax'
local normalized=subinstr(`"`output'"',"\","/",.)
local lastslash=strrpos(`"`normalized'"',"/")
if `lastslash'>0 {
    local outdir=substr(`"`normalized'"',1,`lastslash'-1)
    forvalues k=1/`=strlen(`"`outdir'"')' {
        if substr(`"`outdir'"',`k',1)=="/" {
            local prefix=substr(`"`outdir'"',1,`k'-1)
            capture mkdir `"`prefix'"'
        }
    }
    capture mkdir `"`outdir'"'
}
import delimited using `"`input'"',clear varnames(1) stringcols(_all) encoding(UTF-8)
confirm variable panel id running outcome
assert !missing(panel,id,running,outcome)
assert inlist(panel,"`p1'","`p2'","`p3'","`p4'")
isid panel id
generate double xnum=real(running)
generate double ynum=real(outcome)
drop running outcome
rename xnum running
rename ynum outcome
assert !missing(running,outcome)
local total_input_n=_N
generate byte selected=inrange(running,`xmin',`xmax')
generate byte exact_threshold=selected & running==`threshold'
local stem=regexr(`"`output'"',"[.]png$","")
preserve
collapse (count) total_input_n=outcome (sum) window_n=selected exact_threshold_n=exact_threshold,by(panel)
assert _N==4
generate long excluded_outside_window_n=total_input_n-window_n
export delimited using `"`stem'_sample.csv"',replace
restore
keep if selected
local window_n=_N
generate double centered=running-`threshold'
generate double hinge=max(centered,0)
generate str5 side=cond(running<`threshold',"left","right")
tempfile window fits
save `window'
tempname fitpost
postfile `fitpost' str32 panel double n double level_at_threshold double slope_left double slope_change double slope_right using `fits',replace
forvalues i=1/4 {
    use `window',clear
    keep if panel=="`p`i''"
    assert _N>=6*`nb`i''
    local n=_N
    quietly regress outcome centered hinge
    assert e(df_m)==2
    local a=_b[_cons]
    local bl=_b[centered]
    local delta=_b[hinge]
    local br=`bl'+`delta'
    assert inrange(`a'+`bl'*(`xmin'-`threshold'),`ymin`i'',`ymax`i'')
    assert inrange(`a',`ymin`i'',`ymax`i'')
    assert inrange(`a'+`br'*(`xmax'-`threshold'),`ymin`i'',`ymax`i'')
    post `fitpost' ("`p`i''") (`n') (`a') (`bl') (`delta') (`br')
    local a`i'=`a'
    local bl`i'=`bl'
    local br`i'=`br'
}
postclose `fitpost'
use `fits',clear
export delimited using `"`stem'_fits.csv"',replace

use `window',clear
generate double low=cond(side=="left",`xmin',`threshold')
generate double high=cond(side=="left",`threshold',`xmax')
generate int nb=.
forvalues i=1/4 {
    replace nb=`nb`i'' if panel=="`p`i''"
}
generate double width=(high-low)/nb
generate int bin=min(floor((running-low)/width),nb-1)+1
assert inrange(bin,1,nb)
collapse (mean) x_mean=running y_mean=outcome (count) n=outcome,by(panel side bin)
forvalues i=1/4 {
    foreach s in left right {
        quietly count if panel=="`p`i''" & side=="`s'"
        assert r(N)==`nb`i''
    }
    assert inrange(y_mean,`ymin`i'',`ymax`i'') if panel=="`p`i''"
}
assert n>=2
local bin_n=_N
export delimited using `"`stem'_bins.csv"',replace
forvalues i=1/4 {
    twoway ///
      (function y=`a`i''+`bl`i''*(x-`threshold'),range(`xmin' `threshold') lcolor(red) lwidth(medium)) ///
      (function y=`a`i''+`br`i''*(x-`threshold'),range(`threshold' `xmax') lcolor(red) lwidth(medium)) ///
      (scatter y_mean x_mean if panel=="`p`i''",msymbol(O) mfcolor(white) mlcolor(navy) msize(small)), ///
      xline(`threshold',lcolor(red) lwidth(thin)) ///
      xscale(range(`xmin' `xmax') noextend) xlabel(500(100)1200,labsize(vsmall)) ///
      yscale(range(`ymin`i'' `ymax`i'') noextend) ylabel(`yticks`i'',angle(0) labsize(vsmall) grid glcolor(gs14)) ///
      title(`"`paneltitle`i''"',size(small)) xtitle(`"`xlabeltext'"',size(vsmall)) ///
      ytitle(`"`ylabel`i''"',size(vsmall)) legend(off) ///
      graphregion(color(white) margin(small)) plotregion(color(white)) scheme(s1color) name(g`i',replace)
}
local maintitle ""
if `"`showtitle'"'=="1" local maintitle `"title(`"`heading'"',size(medium))"'
graph combine g1 g2 g3 g4,cols(2) `maintitle' graphregion(color(white)) xsize(12.4) ysize(8.2)
graph export `"`output'"',width(2728) replace
local pdf=regexr(`"`output'"',"[.]png$",".pdf")
graph export `"`pdf'"',replace
display "STATA_COMPLETE input_rows=`total_input_n' window_rows=`window_n' bins=`bin_n' fits=4 output=`output'"
