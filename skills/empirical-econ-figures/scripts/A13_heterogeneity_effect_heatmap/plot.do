version 19
args input output lang showtitle
clear all
set more off
if "`input'"=="" | "`output'"=="" | !inlist("`lang'","en","zh") | !inlist("`showtitle'","0","1") exit 198
* Edit panel labels, units and scale endpoints together for another application.
local te_min .05
local te_max .20
local jobs_min 0
local jobs_max 1.25
import delimited using "`input'", clear varnames(1) stringcols(_all) encoding(UTF-8)
foreach v in panel sr sd {
    assert `v'!=""
}
assert inlist(panel,"te","jobs")
destring sr sd, replace
assert !missing(sr,sd) & inrange(sr,1,5) & inrange(sd,1,5) & sr==floor(sr) & sd==floor(sd)
isid panel sr sd
gen byte missing_value=value==""
gen double estimate=real(value)
assert !missing(estimate) if missing_value==0
assert inrange(estimate,`te_min',`te_max') if panel=="te" & missing_value==0
assert inrange(estimate,`jobs_min',`jobs_max') if panel=="jobs" & missing_value==0
foreach p in te jobs {
    quietly count if panel=="`p'" & missing_value==0
    assert r(N)>0
    quietly count if panel=="`p'"
    assert r(N)==25
}
gen byte shade=.
replace shade=1 if missing_value==0
forvalues k=1/9 {
    local te_edge=round(`te_min'+`k'*(`te_max'-`te_min')/10,1e-12)
    local jobs_edge=round(`jobs_min'+`k'*(`jobs_max'-`jobs_min')/10,1e-12)
    replace shade=shade+1 if panel=="te" & missing_value==0 & estimate>=`te_edge'
    replace shade=shade+1 if panel=="jobs" & missing_value==0 & estimate>=`jobs_edge'
}
gen double lo=sd-.5
gen double hi=sd+.5
local base=subinstr("`output'",".png","",.)
export delimited using "`base'_checked.csv", replace
if "`lang'"=="zh" {
    local te_title "企业就业增长处理效应"
    local jobs_title "每 €100,000 补贴新增岗位"
    local te_unit "企业就业对数变化"
    local jobs_unit "每 €100,000 补贴新增岗位数"
    local xt "客观规则五分位（SR）"
    local yt "政治裁量五分位（SD）"
    local alltitle "规则与裁量分组效应"
}
else {
    local te_title "Firm employment growth effect"
    local jobs_title "Cost effectiveness"
    local te_unit "Log-change in firm employment"
    local jobs_unit "New jobs per €100,000 subsidy"
    local xt "Objective rules quintile (SR)"
    local yt "Political discretion quintile (SD)"
    local alltitle "Effects by rules and discretion"
}
forvalues j=1/2 {
    local p=cond(`j'==1,"te","jobs")
    local vmin=cond(`j'==1,`te_min',`jobs_min')
    local vmax=cond(`j'==1,`te_max',`jobs_max')
    local c1 "255 255 204"
    local c2 "255 237 160"
    local c3 "254 217 118"
    local c4 "254 178 76"
    local c5 "253 141 60"
    local c6 "252 78 42"
    local c7 "227 26 28"
    local c8 "189 0 38"
    local c9 "153 0 38"
    local c10 "128 0 38"
    local labs ""
    forvalues k=1/10 {
        local lower: display %5.3f (`vmin'+(`k'-1)*(`vmax'-`vmin')/10)
        local upper: display %5.3f (`vmin'+`k'*(`vmax'-`vmin')/10)
        local labs `"`labs' `=`k'+1' "`lower'–`upper'""'
    }
    quietly count if panel=="`p'" & missing_value==1
    local missingplot=r(N)>0
    local legorder "`labs'"
    if `missingplot' & "`lang'"=="zh" local legorder `"`labs' 1 "无估计""'
    if `missingplot' & "`lang'"=="en" local legorder `"`labs' 1 "No estimate""'
    twoway (rbar lo hi sr if panel=="`p'" & missing_value==1, barw(1) color("229 229 229") fintensity(100) lcolor(white) lwidth(vthin)) ///
           (rbar lo hi sr if panel=="`p'" & shade==1, barw(1) color("`c1'") fintensity(100) lcolor(white) lwidth(vthin)) ///
           (rbar lo hi sr if panel=="`p'" & shade==2, barw(1) color("`c2'") fintensity(100) lcolor(white) lwidth(vthin)) ///
           (rbar lo hi sr if panel=="`p'" & shade==3, barw(1) color("`c3'") fintensity(100) lcolor(white) lwidth(vthin)) ///
           (rbar lo hi sr if panel=="`p'" & shade==4, barw(1) color("`c4'") fintensity(100) lcolor(white) lwidth(vthin)) ///
           (rbar lo hi sr if panel=="`p'" & shade==5, barw(1) color("`c5'") fintensity(100) lcolor(white) lwidth(vthin)) ///
           (rbar lo hi sr if panel=="`p'" & shade==6, barw(1) color("`c6'") fintensity(100) lcolor(white) lwidth(vthin)) ///
           (rbar lo hi sr if panel=="`p'" & shade==7, barw(1) color("`c7'") fintensity(100) lcolor(white) lwidth(vthin)) ///
           (rbar lo hi sr if panel=="`p'" & shade==8, barw(1) color("`c8'") fintensity(100) lcolor(white) lwidth(vthin)) ///
           (rbar lo hi sr if panel=="`p'" & shade==9, barw(1) color("`c9'") fintensity(100) lcolor(white) lwidth(vthin)) ///
           (rbar lo hi sr if panel=="`p'" & shade==10, barw(1) color("`c10'") fintensity(100) lcolor(white) lwidth(vthin)), ///
           xlabel(1(1)5,nogrid) ylabel(1(1)5,angle(horizontal) nogrid) ///
           xscale(range(.5 5.5) noextend) yscale(range(.5 5.5) noextend) ///
           xtitle("`xt'",size(small)) ytitle("`yt'",size(small)) ///
           subtitle("``p'_title'",size(medsmall)) ///
           legend(order(`legorder') cols(1) size(tiny) title("``p'_unit'",size(vsmall)) region(lcolor(none))) ///
           aspectratio(1) graphregion(color(white)) plotregion(margin(zero)) name(p`j',replace)
}
local opt ""
if "`showtitle'"=="1" local opt "title(`alltitle',size(medsmall))"
graph combine p1 p2, cols(2) xsize(11.4) ysize(5.8) graphregion(color(white)) `opt'
graph export "`output'", replace width(2200)
graph export "`base'.pdf", replace
display "HEATMAP_STATA_COMPLETE rows=" _N
