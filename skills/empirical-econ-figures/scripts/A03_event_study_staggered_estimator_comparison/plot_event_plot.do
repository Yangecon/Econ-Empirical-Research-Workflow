version 19
clear all
set more off
args root input output title extract
if `"`root'"'=="" local root "`c(pwd)'"
if `"`input'"'=="" local input "`root'/audited_estimates.csv"
if `"`output'"'=="" local output "`root'/staggered_comparison_event_plot_hybrid"
if `"`extract'"'=="" local extract "`root'/event_plot_extracted.csv"
adopath ++ "`root'/packages/e"
discard
import delimited using "`input'", varnames(1) clear
foreach v in estimator event_time b se ci_low ci_high status {
    confirm variable `v'
}
isid estimator event_time
assert !missing(event_time) & event_time==floor(event_time)
assert inlist(status,"estimated","pretrend_test","placebo_test","normalized_reference")
assert inlist(estimator,"TWFE OLS","Sun-Abraham","Callaway-Santanna","dCDH dynamic","BJS imputation","Wooldridge jwdid")
assert !missing(b,se,ci_low,ci_high) & se>0 if status!="normalized_reference"
assert ci_low<=b & b<=ci_high if status!="normalized_reference"
assert event_time==-1 & b==0 & missing(se) & missing(ci_low) & missing(ci_high) if status=="normalized_reference"
assert inlist(estimator,"TWFE OLS","Sun-Abraham") if status=="normalized_reference"
count if status=="normalized_reference"
assert r(N)==2
count if estimator=="TWFE OLS" & status=="normalized_reference"
assert r(N)==1
count if estimator=="Sun-Abraham" & status=="normalized_reference"
assert r(N)==1
local z=invnormal(.975)
assert abs(ci_low-(b-`z'*se))<1e-6 if status!="normalized_reference"
assert abs(ci_high-(b+`z'*se))<1e-6 if status!="normalized_reference"
generate double variance=se^2
sort event_time
local key1 "TWFE OLS"
local key2 "Sun-Abraham"
local key3 "Callaway-Santanna"
local key4 "dCDH dynamic"
local key5 "BJS imputation"
local key6 "Wooldridge jwdid"
forvalues i=1/6 {
    count if estimator=="`key`i''" & status!="normalized_reference"
    assert r(N)>0
    levelsof event_time if estimator=="`key`i''" & status!="normalized_reference", local(horizons)
    local names ""
    foreach k of local horizons {
        if `k'<0 {
            local lag=abs(`k')
            local names "`names' P`lag'"
        }
        else local names "`names' E`k'"
    }
    mkmat b if estimator=="`key`i''" & status!="normalized_reference", matrix(b`i')
    mkmat variance if estimator=="`key`i''" & status!="normalized_reference", matrix(v`i')
    matrix b`i'=b`i''
    matrix v`i'=v`i''
    matrix colnames b`i'=`names'
    matrix colnames v`i'=`names'
}
quietly summarize event_time, meanonly
local xmin=floor(r(min))
local xmax=ceil(r(max))
local trimlead=max(0,-`xmin')
local trimlag=max(0,`xmax')
* event_plot parses six named coefficient/variance pairs, horizons, CIs, and offsets.
* Its one-style-per-series renderer cannot vary fill by significance, so savecoef
* supplies audited coordinates to the native twoway layers below.
event_plot b1#v1 b2#v2 b3#v3 b4#v4 b5#v5 b6#v6, ///
    stub_lag(E#) stub_lead(P#) trimlag(`trimlag') trimlead(`trimlead') ///
    plottype(scatter) ciplottype(rcap) together perturb(-0.30(0.12)0.30) ///
    savecoef noplot
local color1 "0 136 55"
local color2 "197 27 43"
local color3 "43 108 176"
local color4 "142 68 173"
local color5 "179 107 0"
local color6 "55 55 55"
local symbol1 "D"
local symbol2 "O"
local symbol3 "S"
local symbol4 "T"
local symbol5 "S"
local symbol6 "O"
local name1 "TWFE OLS"
local name2 "Sun-Abraham"
local name3 "Callaway-Sant'Anna"
local name4 "de Chaisemartin-d'Haultfoeuille"
local name5 "Borusyak-Jaravel-Spiess"
local name6 "Wooldridge (jwdid)"
local plots ""
local legend_order ""
local layer=0
forvalues i=1/6 {
    assert !missing(__event_hi`i',__event_lo`i') if !missing(__event_coef`i')
    generate byte sig`i'=(__event_lo`i'>0 | __event_hi`i'<0) if !missing(__event_coef`i')
    local color "`color`i''"
    local symbol "`symbol`i''"
    local plots `"`plots' (rcap __event_hi`i' __event_lo`i' __event_pos`i' if !missing(__event_coef`i'), lcolor("`color'") lwidth(thin))"'
    local layer=`layer'+1
    local plots `"`plots' (scatter __event_coef`i' __event_pos`i' if sig`i'==1, msymbol(`symbol') mcolor("`color'") msize(medsmall))"'
    local layer=`layer'+1
    local legend_order `"`legend_order' `layer' "`name`i''""'
    local plots `"`plots' (scatter __event_coef`i' __event_pos`i' if sig`i'==0, msymbol(`symbol') mfcolor(white) mlcolor("`color'") msize(medsmall))"'
    local layer=`layer'+1
}
generate double ref_twfe=0 if status=="normalized_reference" & estimator=="TWFE OLS"
generate double ref_sa=0 if status=="normalized_reference" & estimator=="Sun-Abraham"
generate double ref_x_twfe=-1-.30 if !missing(ref_twfe)
generate double ref_x_sa=-1-.18 if !missing(ref_sa)
local plots `"`plots' (scatter ref_twfe ref_x_twfe, msymbol(O) mfcolor(white) mlcolor("0 136 55") msize(medsmall))"'
local plots `"`plots' (scatter ref_sa ref_x_sa, msymbol(O) mfcolor(white) mlcolor("197 27 43") msize(medsmall))"'
local title_opt ""
if `"`title'"'!="" local title_opt `"title("`title'")"'
twoway `plots', ///
    yline(0, lcolor(gs8) lwidth(thin)) xline(-.5, lcolor(gs11) lpattern(dash)) ///
    xlabel(`xmin'(1)`xmax', nogrid) ylabel(, grid glcolor(gs15)) ///
    xtitle("Periods relative to adoption") ytitle("Estimated effect (95% CI)") ///
    legend(order(`legend_order') position(6) rows(2) size(small) region(lcolor(none))) ///
    `title_opt' graphregion(color(white)) plotregion(color(white))
graph export "`output'.png", replace width(2700)
graph export "`output'.pdf", replace
preserve
keep __event_H* __event_pos* __event_coef* __event_hi* __event_lo*
generate long rowid=_n
reshape long __event_H __event_pos __event_coef __event_hi __event_lo, i(rowid) j(group_id)
drop if missing(__event_coef)
rename __event_H event_time
rename __event_pos xplot
rename __event_coef b
rename __event_hi ci_high
rename __event_lo ci_low
keep group_id event_time xplot b ci_low ci_high
sort group_id event_time
export delimited using "`extract'", replace
count
display "EVENT_PLOT_EXTRACTED_ROWS=" r(N)
restore
display "STAGGERED_EVENT_PLOT_HYBRID_COMPLETE"
