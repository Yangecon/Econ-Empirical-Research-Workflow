version 19
args gridinput pointinput output showtitle
clear all
set more off
if "`gridinput'"=="" | "`pointinput'"=="" | "`output'"=="" | !inlist("`showtitle'","0","1") {
    display as error "Usage: plot.do grid.csv point.csv output.png showtitle(0|1)"
    exit 198
}
local base=subinstr("`output'",".png","",.)
capture log close _all
log using "`base'_run.log", replace text
import delimited using "`gridinput'", clear varnames(1) encoding(UTF-8)
foreach v in x_center y_center x_lo x_hi y_lo y_hi in90 in95 in99 {
    assert !missing(`v')
}
isid x_center y_center
assert x_lo<x_center & x_center<x_hi & y_lo<y_center & y_center<y_hi
assert inlist(in90,0,1) & inlist(in95,0,1) & inlist(in99,0,1)
assert in90<=in95 & in95<=in99
gen double dx=x_hi-x_lo
gen double dy=y_hi-y_lo
assert abs(dx-dx[1])<1e-7 & abs(dy-dy[1])<1e-7
assert abs(x_center-(x_lo+x_hi)/2)<1e-7
assert abs(y_center-(y_lo+y_hi)/2)<1e-7
egen byte tagx=tag(x_center)
egen byte tagy=tag(y_center)
quietly count if tagx
local nx=r(N)
quietly count if tagy
local ny=r(N)
assert `nx'>=2 & `ny'>=2 & _N==`nx'*`ny'
local width=dx[1]
local height=dy[1]
sort x_center y_center
by x_center: assert _N==`ny'
by x_center: assert abs(y_center-y_center[_n-1]-`height')<1e-7 if _n>1
preserve
    keep if tagx
    sort x_center
    assert abs(x_center-x_center[_n-1]-`width')<1e-7 if _n>1
restore
gen byte region=cond(in90==1,90,cond(in95==1,95,cond(in99==1,99,0)))
export delimited using "`base'_checked.csv", replace
quietly summarize x_lo, meanonly
local xmin=r(min)
quietly summarize x_hi, meanonly
local xmax=r(max)
quietly summarize y_lo, meanonly
local ymin=r(min)
quietly summarize y_hi, meanonly
local ymax=r(max)
local line_lo=max(`xmin',.5-`ymax')
local line_hi=min(`xmax',.5-`ymin')

preserve
    import delimited using "`pointinput'", clear varnames(1) encoding(UTF-8)
    assert _N==1 & !missing(x,y)
    local px=x[1]
    local py=y[1]
restore
gen double point_x=`px' if _n==1
gen double point_y=`py' if _n==1
local ttl ""
if "`showtitle'"=="1" local ttl `"title("Joint bootstrap regions")"'
twoway ///
    (rbar y_hi y_lo x_center if region==99, barwidth(`width') color(gs14) lcolor(gs14)) ///
    (rbar y_hi y_lo x_center if region==95, barwidth(`width') color(gs11) lcolor(gs11)) ///
    (rbar y_hi y_lo x_center if region==90, barwidth(`width') color(gs7) lcolor(gs7)) ///
    (function y=.5-x, range(`line_lo' `line_hi') lcolor(black) lwidth(medthin)) ///
    (scatter point_y point_x, mcolor(black) msize(medium)), ///
    xlabel(, grid glcolor(gs14)) ylabel(, grid glcolor(gs14)) ///
    xscale(range(`xmin' `xmax')) yscale(range(`ymin' `ymax')) ///
    xtitle("EP(-10%) - EP(-30%)") ytitle("EP(-30%)") ///
    legend(order(1 "99% joint region" 2 "95% joint region" 3 "90% joint region" ///
                 4 "x + y = 0.5" 5 "Point estimate") cols(1) position(5) ring(0) ///
           size(vsmall) region(lcolor(none))) ///
    graphregion(color(white)) plotregion(color(white)) `ttl'
graph export "`output'", replace width(2400)
graph export "`base'.pdf", replace
display "F16_STATA_OK cells=" _N " point_x=`px' point_y=`py'"
log close
