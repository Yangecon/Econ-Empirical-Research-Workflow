version 19
args input output lang showtitle
clear all
set more off
if "`input'"=="" | "`output'"=="" | !inlist("`lang'","en","zh") | !inlist("`showtitle'","0","1") exit 198
import delimited using "`input'", clear varnames(1) stringcols(_all) encoding(UTF-8)
foreach v in year x y {
    assert `v'!=""
    destring `v', replace
    assert !missing(`v')
}
assert _N>=6
assert year>year[_n-1] if _n>1
isid year
assert inlist(phase,"early","middle","late")
gen byte phase_num=cond(phase=="early",1,cond(phase=="middle",2,3))
assert phase_num>=phase_num[_n-1] if _n>1
foreach p in early middle late {
    quietly count if phase=="`p'"
    assert r(N)>=2
}
assert year==floor(year) if year_label!=""
assert year_label==strtrim(string(year,"%12.0f")) if year_label!=""
local base=subinstr("`output'",".png","",.)
export delimited year x y phase year_label using "`base'_checked.csv", replace
foreach p in early middle late {
    gen double x_`p'=x if phase=="`p'" | phase[_n+1]=="`p'"
    gen double y_`p'=y if phase=="`p'" | phase[_n+1]=="`p'"
}
local titleopt ""
if "`lang'"=="zh" {
    local xlab "人口的对数"
    local ylab "实际工资的对数"
    local l1 "早期"
    local l2 "中期"
    local l3 "后期"
    if "`showtitle'"=="1" local titleopt `"title("实际工资与人口的时间轨迹")"'
}
else {
    local xlab "Log population"
    local ylab "Log real wage"
    local l1 "Early"
    local l2 "Middle"
    local l3 "Late"
    if "`showtitle'"=="1" local titleopt `"title("Real wages and population over time")"'
}
twoway (line y_early x_early, lcolor("99 99 99") lwidth(medthick)) ///
       (line y_middle x_middle, lcolor("188 188 188") lwidth(medthick)) ///
       (line y_late x_late, lcolor("17 17 17") lwidth(medthick)) ///
       (scatter y x if phase=="early", mcolor("99 99 99") msymbol(O) msize(medium)) ///
       (scatter y x if phase=="middle", mcolor("188 188 188") msymbol(O) msize(medium)) ///
       (scatter y x if phase=="late", mcolor("17 17 17") msymbol(O) msize(medium)) ///
       (scatter y x if year_label!="", msymbol(i) mlabel(year_label) mlabposition(2) mlabsize(small) mlabcolor(black)), ///
       xtitle("`xlab'") ytitle("`ylab'") xlabel(,nogrid) ylabel(,angle(horizontal) nogrid) ///
       legend(order(1 "`l1'" 2 "`l2'" 3 "`l3'") position(6) ring(1) rows(1) size(small) region(lcolor(none))) ///
       graphregion(color(white)) plotregion(color(white)) `titleopt'
graph export "`output'", width(1900) replace
graph export "`base'.pdf", replace
