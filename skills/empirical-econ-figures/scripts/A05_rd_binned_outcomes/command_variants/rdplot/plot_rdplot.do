* Official rdrobust/rdplot variant of the two-panel synthetic RD display.
version 19
args input output lang showtitle
if `"`input'"'=="" | `"`output'"'=="" | !inlist(`"`lang'"',"en","zh") | !inlist(`"`showtitle'"',"0","1") exit 198
capture which rdplot
if _rc {
    display as error "Official rdrobust package with rdplot is required; see README.md"
    exit 499
}
which rdplot

* Same synthetic input and two illustrative windows as the manual template.
local panel1 "outcome_a"
local panel2 "outcome_b"
local bw1 16
local bw2 25
local nb1 10
local nb2 10
if `"`lang'"'=="zh" {
    local name1 "（A）结果 A"
    local name2 "（B）结果 B"
    local xlab "相对断点的运行变量"
    local ylab "结果发生概率"
    local heading "断点两侧的分箱结果"
}
else {
    local name1 "(A) Outcome A"
    local name2 "(B) Outcome B"
    local xlab "Running variable relative to cutoff"
    local ylab "Outcome probability"
    local heading "Binned outcomes around a cutoff"
}
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
import delimited using `"`input'"', clear varnames(1) stringcols(_all) encoding(UTF-8)
confirm variable panel id running outcome
assert !missing(panel,id,running,outcome)
assert inlist(panel,"`panel1'","`panel2'")
isid panel id
gen double running_num=real(running)
gen double outcome_num=real(outcome)
drop running outcome
rename running_num running
rename outcome_num outcome
assert !missing(running,outcome) & inrange(outcome,0,1)
local stem=regexr(`"`output'"',"[.]png$","")
tempname fitfile
file open `fitfile' using `"`stem'_rdplot_fits.csv"', write replace text
file write `fitfile' "panel,side,n,intercept_at_cutoff,slope,fit_x_min,fit_x_max" _n
forvalues i=1/2 {
    preserve
    keep if panel=="`panel`i''" & abs(running)<=`bw`i''
    assert _N>=6*`nb`i''
    local gopts `"title("`name`i''", size(medsmall)) xtitle("`xlab'") ytitle("`ylab'") legend(off) graphregion(color(white)) plotregion(color(white)) scheme(s1mono)"'
    rdplot outcome running, c(0) p(1) kernel(uniform) ///
        h(`bw`i'' `bw`i'') support(-`bw`i'' `bw`i'') ///
        nbins(`nb`i'' `nb`i'') binselect(es) genvars graph_options(`gopts')
    display "RDPLOT_PANEL=`panel`i'' N=" e(N) " N_h_l=" e(N_h_l) " N_h_r=" e(N_h_r) ///
        " J_l=" e(J_star_l) " J_r=" e(J_star_r) " p=" e(p) " binselect=" e(binselect)
    matrix fit_l=e(coef_l)
    matrix fit_r=e(coef_r)
    local nl=e(N_l)
    local nr=e(N_r)
    local al : display %21.15g el(fit_l,1,1)
    local bl : display %21.15g el(fit_l,2,1)
    local ar : display %21.15g el(fit_r,1,1)
    local br : display %21.15g el(fit_r,2,1)
    file write `fitfile' "`panel`i'',left,`nl',`al',`bl',-`bw`i'',0" _n
    file write `fitfile' "`panel`i'',right,`nr',`ar',`br',0,`bw`i''" _n
    graph rename g`i', replace
    keep if !missing(rdplot_mean_y)
    bysort rdplot_id: keep if _n==1
    assert _N==2*`nb`i''
    export delimited rdplot_id rdplot_N rdplot_min_bin rdplot_max_bin ///
        rdplot_mean_bin rdplot_mean_x rdplot_mean_y using `"`stem'_`panel`i''_rdplot_bins.csv"', replace
    restore
}
file close `fitfile'
local maintitle ""
if `"`showtitle'"'=="1" local maintitle `"title("`heading'", size(medium))"'
graph combine g1 g2, cols(1) `maintitle' graphregion(color(white)) xsize(7.4) ysize(8.8)
graph export `"`output'"', width(1628) replace
local pdf=regexr(`"`output'"',"[.]png$",".pdf")
graph export `"`pdf'"', replace
display "RDPLOT_COMPLETE output=`output'"
