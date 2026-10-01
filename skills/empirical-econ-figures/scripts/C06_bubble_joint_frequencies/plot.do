version 19
args input output lang showtitle
clear all
set more off
if "`input'"=="" | "`output'"=="" | !inlist("`lang'","en","zh") | !inlist("`showtitle'","0","1") exit 198
import delimited using "`input'", clear varnames(1) stringcols(_all) encoding(UTF-8)
assert inlist(panel,"r1","r200")
assert inlist(kind,"bubble","benchmark")
foreach v in x y {
    assert `v'!=""
    destring `v', replace
    assert !missing(`v') & inrange(`v',0,100)
}
assert count!="" & reference_label=="" if kind=="bubble"
assert count=="" & inlist(reference_label,"bayesian","perfect_brn") if kind=="benchmark"
destring count, replace
assert !missing(count) & count>=0 & count==floor(count) if kind=="bubble"
bysort panel kind x y: assert _N==1 if kind=="bubble"
foreach p in r1 r200 {
    quietly count if panel=="`p'" & kind=="bubble" & count>0
    assert r(N)>0
}
quietly summarize count if kind=="bubble"
local maxcount=r(max)
gen double bubble_area_ratio=count/`maxcount' if kind=="bubble"
local base=subinstr("`output'",".png","",.)
export delimited panel kind x y count reference_label bubble_area_ratio using "`base'_checked.csv", replace
gen byte panel_id=cond(panel=="r1",1,2)
if "`lang'"=="zh" {
    label define panels 1 "第1轮" 2 "第200轮"
    local xlab "负信号条件下的信念（%）"
    local ylab "正信号条件下的信念（%）"
    local titleopt ""
    if "`showtitle'"=="1" local titleopt `"title("二维信念联合频数")"'
    gen str40 display_label=cond(reference_label=="bayesian","贝叶斯基准",cond(reference_label=="perfect_brn","完全基率忽略",""))
}
else {
    label define panels 1 "Round 1" 2 "Round 200"
    local xlab "Belief conditional on negative signal (%)"
    local ylab "Belief conditional on positive signal (%)"
    local titleopt ""
    if "`showtitle'"=="1" local titleopt `"title("Joint belief frequencies")"'
    gen str40 display_label=cond(reference_label=="bayesian","Bayesian",cond(reference_label=="perfect_brn","Perfect BRN",""))
}
label values panel_id panels
quietly levelsof count if kind=="bubble" & count>0, local(freqs)
local layers ""
foreach n of local freqs {
    local diameter : display %12.8f (27*sqrt(`n'/`maxcount'))
    local diameter=strtrim("`diameter'")
    local layers `"`layers' (scatter y x if kind=="bubble" & count==`n', msymbol(O) msize(`diameter'pt) mcolor("237 103 105") mlwidth(none))"'
}
twoway `layers' ///
    (scatter y x if kind=="benchmark", msymbol(T) msize(medium) mcolor(black) ///
      mlabel(display_label) mlabposition(3) mlabsize(vsmall) mlabcolor(black)), ///
    by(panel_id, cols(2) note("") legend(off) graphregion(color(white)) `titleopt') ///
    xscale(range(0 100) noextend) yscale(range(0 100) noextend) ///
    xlabel(0(20)100,nogrid) ylabel(0(20)100,angle(horizontal) nogrid) ///
    xtitle("`xlab'") ytitle("`ylab'") ///
    graphregion(color(white)) plotregion(color(white))
graph export "`output'", width(2000) replace
graph export "`base'.pdf", replace
