version 19
args input output lang showtitle
clear all
set more off
if "`input'"=="" | "`output'"=="" | !inlist("`lang'","en","zh") | !inlist("`showtitle'","0","1") exit 198
local ids "poverty unmet_needs housing health education consumption"
local en1 "Poverty probability"
local en2 "Unmet basic needs"
local en3 "Housing dimension"
local en4 "Health dimension"
local en5 "Education dimension"
local en6 "Consumption dimension"
local zh1 "贫困概率"
local zh2 "未满足基本需求"
local zh3 "住房维度"
local zh4 "健康维度"
local zh5 "教育维度"
local zh6 "消费维度"
import delimited using "`input'", clear varnames(1) stringcols(_all) encoding(UTF-8)
foreach v in outcome bandwidth_km estimate cluster_low cluster_high conley_low conley_high {
    assert `v'!=""
}
assert inlist(outcome,"poverty","unmet_needs","housing","health","education","consumption")
foreach v in bandwidth_km estimate cluster_low cluster_high conley_low conley_high {
    destring `v', replace
    assert !missing(`v')
}
assert bandwidth_km>0
isid outcome bandwidth_km
assert cluster_low<=estimate & estimate<=cluster_high
assert conley_low<=estimate & estimate<=conley_high
bysort outcome (bandwidth_km): assert _N>=3
egen byte tag=tag(outcome)
quietly count if tag
assert r(N)==6
bysort bandwidth_km: assert _N==6
local base=subinstr("`output'",".png","",.)
sort outcome bandwidth_km
export delimited using "`base'_checked.csv", replace
if "`lang'"=="zh" {
    local xlab "回归允许的距边界最大距离（公里）"
    local prob "概率差"
    local count "数量差"
    local clust "区块聚类95%区间"
    local conley "Conley95%区间"
    local alltitle "边界距离敏感性"
}
else {
    local xlab "Maximum allowed border distance (km)"
    local prob "Probability difference"
    local count "Count difference"
    local clust "Clustered 95% CI"
    local conley "Conley 95% CI"
    local alltitle "Sensitivity to border distance"
}
forvalues j=1/6 {
    local id: word `j' of `ids'
    if "`lang'"=="en" local name "`en`j''"
    else local name "`zh`j''"
    local unit "`prob'"
    if `j'==2 local unit "`count'"
    twoway (rarea cluster_high cluster_low bandwidth_km if outcome=="`id'", color(gs11) lcolor(gs10)) ///
           (line conley_low bandwidth_km if outcome=="`id'", lcolor(gs5) lpattern(dot) lwidth(thin)) ///
           (line conley_high bandwidth_km if outcome=="`id'", lcolor(gs5) lpattern(dot) lwidth(thin)) ///
           (line estimate bandwidth_km if outcome=="`id'", lcolor(black) lwidth(medthick)), ///
           subtitle("`name'",size(small)) xtitle("`xlab'",size(vsmall)) ytitle("`unit'",size(vsmall)) ///
           xlabel(,labsize(vsmall) nogrid) ylabel(,angle(horizontal) labsize(vsmall) nogrid) ///
           legend(order(1 "`clust'" 2 "`conley'") position(6) ring(1) rows(1) size(tiny) region(lcolor(none))) ///
           graphregion(color(white)) name(g`j',replace)
}
local opt ""
if "`showtitle'"=="1" local opt "title(`alltitle',size(medsmall))"
graph combine g1 g2 g3 g4 g5 g6, cols(2) xsize(11.5) ysize(10) graphregion(color(white)) `opt'
graph export "`output'", replace width(2400)
graph export "`base'.pdf", replace
display "BANDWIDTH_STATA_COMPLETE rows=" _N
