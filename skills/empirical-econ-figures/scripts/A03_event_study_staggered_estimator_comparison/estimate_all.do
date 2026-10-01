version 19
clear all
set more off
args root
if `"`root'"'=="" local root "`c(pwd)'"
set seed 10
adopath ++ "`root'/packages/d"
adopath ++ "`root'/packages/e"
adopath ++ "`root'/packages/_"
adopath ++ "`root'/packages/a"
adopath ++ "`root'/packages/l"
adopath ++ "`root'/packages/h"
adopath ++ "`root'/packages/j"
set obs 4500
gen long i = int((_n-1)/15)+1
gen byte t = mod(_n-1,15)+1
xtset i t
gen byte Ei = ceil(runiform()*7)+9 if t==1
bys i (t): replace Ei = Ei[1]
gen int K = t-Ei
gen byte D = K>=0
gen double tau = cond(D, t-12.5, 0)
gen double Y = i + 3*t + tau*D + rnormal()
save "`root'/synthetic_panel.dta", replace
postfile h str32 estimator int event_time double b se ci_low ci_high ///
    str24 status double sample_n str24 command str32 inference ///
    using "`root'/estimate_rows.dta", replace
local z=invnormal(.975)
forvalues l=0/5 {
    gen byte L`l'event = K==`l'
}
forvalues l=2/15 {
    gen byte F`l'event = K==-`l'
}
gen byte F6plus = K<=-6

display "START_TWFE"
reghdfe Y F2event-F5event F6plus L*event, a(i t) cluster(i)
local N=e(N)
matrix B=e(b)
matrix V=e(V)
forvalues k=2/5 {
    local nm "F`k'event"
    local j=colnumb(B,"`nm'")
    local b=el(B,1,`j')
    local se=sqrt(el(V,`j',`j'))
    post h ("TWFE OLS") (-`k') (`b') (`se') (`b'-`z'*`se') (`b'+`z'*`se') ("estimated") (`N') ("reghdfe") ("unit_cluster_normal")
}
post h ("TWFE OLS") (-1) (0) (.) (.) (.) ("normalized_reference") (`N') ("reghdfe") ("none")
forvalues k=0/5 {
    local nm "L`k'event"
    local j=colnumb(B,"`nm'")
    local b=el(B,1,`j')
    local se=sqrt(el(V,`j',`j'))
    post h ("TWFE OLS") (`k') (`b') (`se') (`b'-`z'*`se') (`b'+`z'*`se') ("estimated") (`N') ("reghdfe") ("unit_cluster_normal")
}
estimates store twfe

display "START_BJS"
did_imputation Y i t Ei, horizons(0/5) pretrends(5) cluster(i)
local N=e(N)
matrix B=e(b)
matrix V=e(V)
forvalues k=1/5 {
    local nm "pre`k'"
    local j=colnumb(B,"`nm'")
    local b=el(B,1,`j')
    local se=sqrt(el(V,`j',`j'))
    post h ("BJS imputation") (-`k') (`b') (`se') (`b'-`z'*`se') (`b'+`z'*`se') ("pretrend_test") (`N') ("did_imputation") ("unit_cluster_normal")
}
forvalues k=0/5 {
    local nm "tau`k'"
    local j=colnumb(B,"`nm'")
    local b=el(B,1,`j')
    local se=sqrt(el(V,`j',`j'))
    post h ("BJS imputation") (`k') (`b') (`se') (`b'-`z'*`se') (`b'+`z'*`se') ("estimated") (`N') ("did_imputation") ("unit_cluster_normal")
}
estimates store bjs

display "START_SA"
egen byte lastcohort = max(Ei), by(i)
quietly summ Ei
replace lastcohort = Ei==r(max)
eventstudyinteract Y L*event F2event-F14event, vce(cluster i) absorb(i t) cohort(Ei) control_cohort(lastcohort)
local N=e(N)
display "SA_RC=" _rc
matrix B=e(b_iw)
matrix V=e(V_iw)
forvalues k=2/5 {
    local nm "F`k'event"
    local j=colnumb(B,"`nm'")
    local b=el(B,1,`j')
    local se=sqrt(el(V,`j',`j'))
    post h ("Sun-Abraham") (-`k') (`b') (`se') (`b'-`z'*`se') (`b'+`z'*`se') ("estimated") (`N') ("eventstudyinteract") ("unit_cluster_normal")
}
post h ("Sun-Abraham") (-1) (0) (.) (.) (.) ("normalized_reference") (`N') ("eventstudyinteract") ("none")
forvalues k=0/5 {
    local nm "L`k'event"
    local j=colnumb(B,"`nm'")
    local b=el(B,1,`j')
    local se=sqrt(el(V,`j',`j'))
    post h ("Sun-Abraham") (`k') (`b') (`se') (`b'-`z'*`se') (`b'+`z'*`se') ("estimated") (`N') ("eventstudyinteract") ("unit_cluster_normal")
}
matrix sa_b=B
matrix sa_v=V

display "START_CS"
gen byte gvar = Ei
csdid Y, ivar(i) time(t) gvar(gvar) notyet
display "CSDID_RC=" _rc
estat event, estore(cs)
display "CS_EVENT_RC=" _rc
estimates restore cs
local N=e(N)
matrix B=e(b)
matrix V=e(V)
forvalues k=1/5 {
    local nm "Tm`k'"
    local j=colnumb(B,"`nm'")
    local b=el(B,1,`j')
    local se=sqrt(el(V,`j',`j'))
    post h ("Callaway-Santanna") (-`k') (`b') (`se') (`b'-`z'*`se') (`b'+`z'*`se') ("pretrend_test") (`N') ("csdid_estat_event") ("unit_cluster_normal")
}
forvalues k=0/5 {
    local nm "Tp`k'"
    local j=colnumb(B,"`nm'")
    local b=el(B,1,`j')
    local se=sqrt(el(V,`j',`j'))
    post h ("Callaway-Santanna") (`k') (`b') (`se') (`b'-`z'*`se') (`b'+`z'*`se') ("estimated") (`N') ("csdid_estat_event") ("unit_cluster_normal")
}

display "START_DCDH"
did_multiplegt_old Y i t D, robust_dynamic dynamic(5) placebo(5) breps(199) cluster(i) seed(10)
display "DCDH_RC=" _rc
matrix B=e(estimates)
matrix V=e(variances)
local N=e(N)
forvalues k=1/5 {
    local nm "Placebo_`k'"
    local j=rownumb(B,"`nm'")
    local b=el(B,`j',1)
    local se=sqrt(el(V,`j',1))
    post h ("dCDH dynamic") (-`k') (`b') (`se') (`b'-`z'*`se') (`b'+`z'*`se') ("placebo_test") (`N') ("did_multiplegt_old") ("unit_bootstrap_normal")
}
forvalues k=0/5 {
    local nm "Effect_`k'"
    local j=rownumb(B,"`nm'")
    local b=el(B,`j',1)
    local se=sqrt(el(V,`j',1))
    post h ("dCDH dynamic") (`k') (`b') (`se') (`b'-`z'*`se') (`b'+`z'*`se') ("estimated") (`N') ("did_multiplegt_old") ("unit_bootstrap_normal")
}
matrix dcdh_b=B'
matrix dcdh_v=V'

display "START_JWDID"
* All cohorts eventually adopt, so the documented default not-yet-treated
* control scheme yields post-treatment event ATT only on this panel.
jwdid Y, ivar(i) tvar(t) gvar(Ei) cluster(i)
local N=e(N)
estat event, window(0 5)
matrix B=r(b)
matrix V=r(V)
assert colsof(B)==6
assert rowsof(V)==6 & colsof(V)==6
preserve
clear
svmat double V, names(v)
gen byte event_time=_n-1
order event_time
export delimited using "`root'/jwdid_event_covariance.csv", replace
restore
forvalues k=0/5 {
    local j=`k'+1
    local b=el(B,1,`j')
    local se=sqrt(el(V,`j',`j'))
    assert !missing(`b',`se') & `se'>0
    post h ("Wooldridge jwdid") (`k') (`b') (`se') (`b'-`z'*`se') (`b'+`z'*`se') ("estimated") (`N') ("jwdid_estat_event") ("unit_cluster_delta_normal")
}
postclose h
preserve
use "`root'/estimate_rows.dta", clear
isid estimator event_time
assert !missing(b, se, ci_low, ci_high) if status!="normalized_reference"
assert se>0 if status!="normalized_reference"
assert missing(se, ci_low, ci_high) if status=="normalized_reference"
sort estimator event_time
export delimited using "`root'/audited_estimates.csv", replace
count
display "AUDITED_ESTIMATE_ROWS=" r(N)
restore
display "STAGGERED_ESTIMATION_COMPLETE"
