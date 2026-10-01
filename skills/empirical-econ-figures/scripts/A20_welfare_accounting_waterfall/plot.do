version 19
args input output lang showtitle
clear all
set more off
if "`input'"=="" | "`output'"=="" | !inlist("`lang'","en","zh") | !inlist("`showtitle'","0","1") {
    display as error "Usage: plot.do input output lang(en|zh) showtitle(0|1)"
    exit 198
}
local group_a_en "Group A"
local group_b_en "Group B"
local group_a_zh "组 A"
local group_b_zh "组 B"
import delimited using "`input'", clear varnames(1) stringcols(_all) encoding(UTF-8)
foreach v in group ledger seq item kind value {
    assert `v'!=""
}
assert inlist(group,"group_a","group_b")
assert inlist(ledger,"revenue","wtp")
assert inlist(kind,"component","subtotal","total")
assert inlist(item,"audit_cost","upfront_revenue","interim_revenue","deterrence_revenue","net_revenue","upfront_taxes","deterrence_taxes","response_burden","net_wtp")
assert inlist(item,"audit_cost","upfront_revenue","interim_revenue","deterrence_revenue","net_revenue") if ledger=="revenue"
assert inlist(item,"upfront_taxes","deterrence_taxes","response_burden","net_wtp") if ledger=="wtp"
destring seq value, replace
assert !missing(seq,value) & seq>=1 & seq==floor(seq)
egen byte pair=group(group ledger)
assert !missing(pair)
egen byte pairtag=tag(group ledger)
quietly count if pairtag
assert r(N)==4
sort group ledger seq
by group ledger: assert seq==_n
by group ledger: assert _N>=3
by group ledger: assert kind[_N]=="total"
by group ledger: assert item[_N]==cond(ledger=="revenue","net_revenue","net_wtp")
by group ledger: egen byte ntotal=total(kind=="total")
assert ntotal==1
isid group ledger item
preserve
    keep group ledger seq item kind
    reshape wide seq kind, i(ledger item) j(group) string
    assert seqgroup_a==seqgroup_b & kindgroup_a==kindgroup_b
restore
by group ledger (seq): gen double running=sum(cond(kind=="component",value,0))
by group ledger (seq): gen double prior=running-cond(kind=="component",value,0)
assert abs(value-running)<1e-8 if kind!="component"
gen double bottom=cond(kind=="component",min(prior,running),min(0,value))
gen double top=cond(kind=="component",max(prior,running),max(0,value))
quietly summarize seq if ledger=="revenue", meanonly
local revmax=r(max)
quietly summarize seq if ledger=="wtp", meanonly
local wtpmax=r(max)
local offset=`revmax'+1
local xmax=`offset'+`wtpmax'
gen double x=seq+cond(ledger=="wtp",`offset',0)
gen double label_y=cond(value>=0,top+.15,bottom-.15)
gen str12 value_label=string(value,"%4.2f")
gen str35 label_en=""
gen str35 label_zh=""
replace label_en="Audit cost" if item=="audit_cost"
replace label_zh="审计成本" if item=="audit_cost"
replace label_en="Upfront revenue" if item=="upfront_revenue"
replace label_zh="当期收入" if item=="upfront_revenue"
replace label_en="Interim revenue" if item=="interim_revenue"
replace label_zh="阶段收入" if item=="interim_revenue"
replace label_en="Deterrence revenue" if item=="deterrence_revenue"
replace label_zh="威慑收入" if item=="deterrence_revenue"
replace label_en="Net revenue" if item=="net_revenue"
replace label_zh="净收入" if item=="net_revenue"
replace label_en="Upfront taxes" if item=="upfront_taxes"
replace label_zh="当期税款" if item=="upfront_taxes"
replace label_en="Deterrence taxes" if item=="deterrence_taxes"
replace label_zh="威慑税款" if item=="deterrence_taxes"
replace label_en="Response burden" if item=="response_burden"
replace label_zh="应对负担" if item=="response_burden"
replace label_en="Net WTP" if item=="net_wtp"
replace label_zh="净支付意愿" if item=="net_wtp"
assert label_en!="" & label_zh!=""
local base=subinstr("`output'",".png","",.)
export delimited using "`base'_checked.csv", replace
preserve
    keep if kind=="total"
    keep group ledger value
    reshape wide value, i(group) j(ledger) string
    assert valuerevenue>0
    gen double mvpf=valuewtp/valuerevenue
    export delimited using "`base'_ratios.csv", replace
restore
if "`lang'"=="zh" {
    local axis "金额（美元 / 每1美元审计支出）"
    local ratio "MVPF = 支付意愿 / 政府净收入"
    local title "边际审计的福利核算"
    local labelvar label_zh
}
else {
    local axis "USD per $1 audit spending"
    local ratio "MVPF = WTP / net revenue"
    local title "Accounting for marginal audits"
    local labelvar label_en
}
forvalues j=1/2 {
    local g=cond(`j'==1,"group_a","group_b")
    if `j'==1 local groupname=cond("`lang'"=="zh","组 A","Group A")
    else local groupname=cond("`lang'"=="zh","组 B","Group B")
    quietly summarize top if group=="`g'", meanonly
    local ymax=ceil(r(max)*1.18)
    quietly summarize bottom if group=="`g'", meanonly
    local ymin=min(-2,floor(r(min)-.7))
    quietly summarize value if group=="`g'" & ledger=="revenue" & kind=="total", meanonly
    local revenue=r(mean)
    quietly summarize value if group=="`g'" & ledger=="wtp" & kind=="total", meanonly
    local wtp=r(mean)
    local mvpf: display %4.2f (`wtp'/`revenue')
    local xl ""
    forvalues k=1/`xmax' {
        if `k'!=`offset' {
            quietly levelsof `labelvar' if group=="`g'" & x==`k', local(lab) clean
            local xl `"`xl' `k' "`lab'""'
        }
    }
    twoway (rbar bottom top x if group=="`g'" & kind=="component", barw(.65) color(gs11) lcolor(white)) ///
           (rbar bottom top x if group=="`g'" & kind=="subtotal", barw(.65) color(eltblue) lcolor(white)) ///
           (rbar bottom top x if group=="`g'" & kind=="total", barw(.65) color("64 109 145") lcolor(white)) ///
           (scatter label_y x if group=="`g'" & value>=0, msymbol(none) mlabel(value_label) mlabposition(12) mlabsize(tiny) mlabcolor(gs4)) ///
           (scatter label_y x if group=="`g'" & value<0, msymbol(none) mlabel(value_label) mlabposition(6) mlabsize(tiny) mlabcolor(gs4)), ///
           xlabel(`xl', labsize(vsmall) angle(35) nogrid) xscale(range(.3 `=`xmax'+.7') noextend) xtitle("") ///
           ylabel(, angle(horizontal) labsize(small) nogrid) yscale(range(`ymin' `ymax') noextend) ///
           yline(0,lcolor(gs8) lwidth(thin)) ///
           text(-.9 `offset' "`ratio': `mvpf'", size(vsmall) color(black)) ///
           subtitle("`groupname'", size(medsmall) position(11)) ///
           ytitle("`axis'", size(small)) legend(off) name(p`j',replace) graphregion(color(white)) plotregion(margin(small))
}
local opt ""
if "`showtitle'"=="1" local opt "title(`title',size(medsmall))"
graph combine p1 p2, cols(1) xsize(11.5) ysize(8.6) graphregion(color(white)) `opt'
graph export "`output'", replace width(2200)
graph export "`base'.pdf", replace
display "WATERFALL_STATA_COMPLETE groups=2 rows=" _N
