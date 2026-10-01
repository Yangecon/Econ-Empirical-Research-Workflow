version 19
capture program drop plot_staggered_twoway
program define plot_staggered_twoway
    version 19
    syntax, INPUT(string) OUTPUT(string) [TITLE(string)]
    import delimited using "`input'", varnames(1) clear
    foreach v in estimator event_time b se ci_low ci_high status {
        confirm variable `v'
    }
    isid estimator event_time
    assert !missing(event_time) & event_time==floor(event_time)
    assert inlist(status,"estimated","pretrend_test","placebo_test","normalized_reference")
    assert !missing(b,se,ci_low,ci_high) if status!="normalized_reference"
    assert se>0 if status!="normalized_reference"
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
    generate byte group_id=.
    replace group_id=1 if estimator=="TWFE OLS"
    replace group_id=2 if estimator=="Sun-Abraham"
    replace group_id=3 if estimator=="Callaway-Santanna"
    replace group_id=4 if estimator=="dCDH dynamic"
    replace group_id=5 if estimator=="BJS imputation"
    replace group_id=6 if estimator=="Wooldridge jwdid"
    assert !missing(group_id)
    forvalues i=1/6 {
        count if group_id==`i' & status!="normalized_reference"
        assert r(N)>0
    }
    generate double xplot=event_time+(group_id-3.5)*.12
    generate byte significant=(ci_low>0 | ci_high<0) if status!="normalized_reference"
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
        local color "`color`i''"
        local symbol "`symbol`i''"
        local plots `"`plots' (rcap ci_high ci_low xplot if group_id==`i' & status!="normalized_reference", lcolor("`color'") lwidth(thin))"'
        local layer=`layer'+1
        local plots `"`plots' (scatter b xplot if group_id==`i' & significant==1, msymbol(`symbol') mcolor("`color'") msize(medsmall))"'
        local layer=`layer'+1
        local legend_order `"`legend_order' `layer' "`name`i''""'
        local plots `"`plots' (scatter b xplot if group_id==`i' & significant==0, msymbol(`symbol') mfcolor(white) mlcolor("`color'") msize(medsmall))"'
        local layer=`layer'+1
        local plots `"`plots' (scatter b xplot if group_id==`i' & status=="normalized_reference", msymbol(O) mfcolor(white) mlcolor("`color'") msize(medsmall))"'
        local layer=`layer'+1
    }
    local title_opt ""
    if `"`title'"'!="" local title_opt `"title("`title'")"'
    quietly summarize event_time, meanonly
    local xmin=floor(r(min))
    local xmax=ceil(r(max))
    twoway `plots', ///
        yline(0, lcolor(gs8) lwidth(thin)) ///
        xline(-.5, lcolor(gs11) lpattern(dash) lwidth(thin)) ///
        xlabel(`xmin'(1)`xmax', nogrid) ylabel(, grid glcolor(gs15)) ///
        xtitle("Periods relative to adoption") ytitle("Estimated effect (95% CI)") ///
        legend(order(`legend_order') position(6) rows(2) size(small) region(lcolor(none))) ///
        `title_opt' graphregion(color(white)) plotregion(color(white))
    graph export "`output'.png", replace width(2700)
    graph export "`output'.pdf", replace
    count if status!="normalized_reference"
    display as result "STAGGERED_TWOWAY_OK estimates=" r(N)
end
