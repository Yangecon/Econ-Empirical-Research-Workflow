version 19
clear all
set more off
set seed 29092026
args root title_text figure_suffix
if `"`root'"' == "" local root "`c(pwd)'"
if `"`figure_suffix'"' == "" local figure_suffix ""
cd `"`root'"'
adopath ++ "`root'/packages/h"
adopath ++ "`root'/packages/l"
adopath ++ "`root'/packages/c"
display "HONESTDID_BEGIN"
which honestdid
which coefplot
honestdid _plugin_check

* Balanced synthetic panel: 320 units x 9 periods. Treatment starts at t=5.
set obs 2880
gen int id = floor((_n-1)/9)+1
gen byte t = mod(_n-1,9)+1
gen byte treated = id<=160
gen int k = t-5
gen double unit_fe = rnormal(0,0.8) if t==1
bysort id (t): replace unit_fe = unit_fe[1]
gen double slope = rnormal(0,0.012) if t==1
bysort id (t): replace slope = slope[1]
gen double tau = cond(treated & k>=0,0.18+0.055*k,0)
gen double y = unit_fe + 0.06*t + slope*t + tau + rnormal(0,0.25)
forvalues j=2/4 {
    gen byte lead`j' = treated & k==-`j'
}
forvalues j=0/4 {
    gen byte lag`j' = treated & k==`j'
}
xtset id t
save "synthetic_panel.dta", replace

* The sole omitted event period is k=-1. Lead order -4,-3,-2; post 0..4.
xtreg y lead4 lead3 lead2 lag0 lag1 lag2 lag3 lag4 i.t, fe vce(cluster id)
assert e(N)==2880
display "EVENT_STUDY_N=" e(N)
matrix eb = e(b)
matrix ev = e(V)
matrix b = eb[1,1..8]
matrix V = ev[1..8,1..8]
matrix colnames b = lead4 lead3 lead2 lag0 lag1 lag2 lag3 lag4
matrix rownames V = lead4 lead3 lead2 lag0 lag1 lag2 lag3 lag4
matrix colnames V = lead4 lead3 lead2 lag0 lag1 lag2 lag3 lag4
mata: st_matrix("V_min_eigen",min(Re(eigenvalues(st_matrix("V")))))
assert V_min_eigen[1,1]>0
matrix list b
matrix list V

* Export every estimated coefficient and every covariance entry.
matrix bt = b'
preserve
clear
svmat double bt, names(b)
gen int event_time = .
replace event_time = -4 in 1
replace event_time = -3 in 2
replace event_time = -2 in 3
replace event_time = 0 in 4
replace event_time = 1 in 5
replace event_time = 2 in 6
replace event_time = 3 in 7
replace event_time = 4 in 8
rename b1 estimate
order event_time estimate
export delimited using "event_study_coefficients.csv", replace
restore
preserve
clear
svmat double V, names(col)
gen str10 row_name = ""
local i=1
foreach n in lead4 lead3 lead2 lag0 lag1 lag2 lag3 lag4 {
    replace row_name = "`n'" in `i'
    local i=`i'+1
}
order row_name
export delimited using "event_study_covariance.csv", replace
restore

* First post-treatment effect, lag0. The explicit contrast selects it.
matrix target = (1 \ 0 \ 0 \ 0 \ 0)
honestdid, b(b) vcov(V) pre(1/3) post(4/8) l_vec(target) ///
    mvec(0(0.25)2) delta(rm) method(C-LF)
mata: st_matrix("RM_CI",HonestEventStudy.CI)
preserve
clear
svmat double RM_CI, names(rmci)
rename rmci1 bound_M
rename rmci2 ci_low
rename rmci3 ci_high
gen str12 restriction = "DeltaRM"
order restriction bound_M ci_low ci_high
export delimited using "rm_intervals.csv", replace
restore
local plotopts `"xtitle("Relative magnitude bound (M-bar)") ytitle("95% robust confidence interval") graphregion(color(white)) plotregion(color(white)) ylabel(,angle(0) nogrid)"'
if `"`title_text'"' != "" local plotopts `"`plotopts' title("`title_text' — relative magnitudes")"'
honestdid, cached coefplot `plotopts'
graph export "honestdid_relative_magnitude`figure_suffix'.png", width(2200) replace
graph export "honestdid_relative_magnitude`figure_suffix'.pdf", replace
display "RM_COMPLETE"

honestdid, b(b) vcov(V) pre(1/3) post(4/8) l_vec(target) ///
    mvec(0(0.025)0.2) delta(sd) method(FLCI)
mata: st_matrix("SD_CI",HonestEventStudy.CI)
preserve
clear
svmat double SD_CI, names(sdci)
rename sdci1 bound_M
rename sdci2 ci_low
rename sdci3 ci_high
gen str12 restriction = "DeltaSD"
order restriction bound_M ci_low ci_high
export delimited using "sd_intervals.csv", replace
restore
local plotopts `"xtitle("Smoothness bound (M)") ytitle("95% robust confidence interval") graphregion(color(white)) plotregion(color(white)) ylabel(,angle(0) nogrid)"'
if `"`title_text'"' != "" local plotopts `"`plotopts' title("`title_text' — smoothness")"'
honestdid, cached coefplot `plotopts'
graph export "honestdid_smoothness`figure_suffix'.png", width(2200) replace
graph export "honestdid_smoothness`figure_suffix'.pdf", replace
display "SD_COMPLETE"
display "HONESTDID_BUILD_COMPLETE"
