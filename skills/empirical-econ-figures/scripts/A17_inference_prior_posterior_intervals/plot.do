version 19
args input output lang showtitle
clear all
set more off
if "`input'"=="" | "`output'"=="" | !inlist("`lang'","en","zh") | !inlist("`showtitle'","0","1") exit 198
local panels "export_2019 variety_2019 export_2020 variety_2020"
import delimited using "`input'", clear varnames(1) stringcols(_all) encoding(UTF-8)
foreach v in panel source kind median low high {
    assert `v'!=""
}
assert inlist(panel,"export_2019","variety_2019","export_2020","variety_2020")
assert inlist(source,"diffuse","literature","firm","policymaker","academic","itt")
assert inlist(kind,"prior","posterior","itt")
assert (source=="diffuse" & kind=="posterior") | (source=="itt" & kind=="itt") | ///
       (inlist(source,"literature","firm","policymaker","academic") & inlist(kind,"prior","posterior"))
foreach v in median low high {
    destring `v', replace
    assert !missing(`v')
}
assert low<=median & median<=high
isid panel source kind
bysort panel: assert _N==10
assert _N==40
generate byte ypos=.
replace ypos=10 if source=="diffuse"
replace ypos=9 if source=="literature" & kind=="posterior"
replace ypos=8 if source=="literature" & kind=="prior"
replace ypos=7 if source=="firm" & kind=="posterior"
replace ypos=6 if source=="firm" & kind=="prior"
replace ypos=5 if source=="policymaker" & kind=="posterior"
replace ypos=4 if source=="policymaker" & kind=="prior"
replace ypos=3 if source=="academic" & kind=="posterior"
replace ypos=2 if source=="academic" & kind=="prior"
replace ypos=1 if source=="itt"
isid panel ypos
local base=subinstr("`output'",".png","",.)
preserve
sort panel ypos
keep panel source kind median low high
export delimited using "`base'_checked.csv", replace
restore
if "`lang'"=="zh" {
    local ylabels `"1 "ITT" 2 "学者先验" 3 "学者后验" 4 "政策制定者先验" 5 "政策制定者后验" 6 "企业先验" 7 "企业后验" 8 "文献先验" 9 "文献后验" 10 "弥散后验""'
    local p1 "出口参与，2019"
    local p2 "产品—国家种类，2019"
    local p3 "出口参与，2020"
    local p4 "产品—国家种类，2020"
    local unit1 "概率差"
    local unit2 "数量差"
    local overall "先验、后验与频率派估计比较"
}
else {
    local ylabels `"1 "ITT" 2 "Academic prior" 3 "Academic posterior" 4 "Policymaker prior" 5 "Policymaker posterior" 6 "Firm prior" 7 "Firm posterior" 8 "Literature prior" 9 "Literature posterior" 10 "Diffuse posterior""'
    local p1 "Exporting, 2019"
    local p2 "Product-country varieties, 2019"
    local p3 "Exporting, 2020"
    local p4 "Product-country varieties, 2020"
    local unit1 "Probability-point effect"
    local unit2 "Count effect"
    local overall "Prior, posterior and frequentist estimates"
}
forvalues j=1/4 {
    local id: word `j' of `panels'
    local axis "`unit1'"
    if mod(`j',2)==0 local axis "`unit2'"
    twoway (rcap low high ypos if panel=="`id'" & kind=="prior", horizontal lcolor("21 149 191") lpattern(dash) lwidth(medium)) ///
           (rcap low high ypos if panel=="`id'" & kind=="posterior", horizontal lcolor("66 94 114") lwidth(medium)) ///
           (rcap low high ypos if panel=="`id'" & kind=="itt", horizontal lcolor("190 35 46") lwidth(thick)) ///
           (scatter ypos median if panel=="`id'", mcolor(black) msize(small)), ///
           ylabel(`ylabels', angle(horizontal) labsize(vsmall) nogrid) yscale(range(.4 10.6) noextend) ///
           xlabel(,nogrid labsize(vsmall)) xtitle("`axis'",size(vsmall)) ytitle("") ///
           subtitle("`p`j''",size(small)) legend(off) graphregion(color(white)) plotregion(color(white)) ///
           name(g`j',replace)
}
local titleopt ""
if "`showtitle'"=="1" local titleopt `"title("`overall'",size(medium))"'
graph combine g1 g2 g3 g4, cols(2) xsize(18) ysize(10) graphregion(color(white)) `titleopt'
graph export "`output'", width(2400) replace
graph export "`base'.pdf", replace
