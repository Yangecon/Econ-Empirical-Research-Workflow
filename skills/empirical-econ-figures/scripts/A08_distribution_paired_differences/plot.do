version 19
args input output showtitle
clear all
set more off
if "`input'"=="" | "`output'"=="" | !inlist("`showtitle'","0","1") {
    display as error "Usage: plot.do input.csv output.png showtitle(0|1)"
    exit 198
}
local base=subinstr("`output'",".png","",.)
capture log close _all
log using "`base'_run.log", replace text
import delimited using "`input'", clear varnames(1) stringcols(1) encoding(UTF-8)
foreach v in pair_id black_contacts white_contacts {
    assert !missing(`v')
}
replace pair_id=strtrim(pair_id)
assert pair_id!=""
isid pair_id
destring black_contacts white_contacts, replace
assert black_contacts>=0 & white_contacts>=0
assert black_contacts==floor(black_contacts) & white_contacts==floor(white_contacts)
quietly count
assert r(N)>=3
sort pair_id
gen double difference_white_minus_black=white_contacts-black_contacts
gen double x_black=1+(mod(_n*37,101)/100-.5)*.13
gen double x_white=x_black+1
export delimited using "`base'_pairs_checked.csv", replace

quietly summarize black_contacts
local mb=r(mean)
local seb=r(sd)/sqrt(r(N))
quietly summarize white_contacts
local mw=r(mean)
local sew=r(sd)/sqrt(r(N))
quietly summarize difference_white_minus_black
local md=r(mean)
local sed=r(sd)/sqrt(r(N))
local n=r(N)
quietly ttest white_contacts == black_contacts
local paired_t=r(t)
local paired_p=r(p)
preserve
    clear
    set obs 3
    gen str40 measure=""
    replace measure="Black" in 1
    replace measure="White" in 2
    replace measure="White minus Black, paired" in 3
    gen int pairs=`n'
    gen double mean=.
    replace mean=`mb' in 1
    replace mean=`mw' in 2
    replace mean=`md' in 3
    gen double se=.
    replace se=`seb' in 1
    replace se=`sew' in 2
    replace se=`sed' in 3
    gen double ci_low=mean-1.96*se
    gen double ci_high=mean+1.96*se
    gen double paired_t=`paired_t' if _n==3
    gen double paired_p=`paired_p' if _n==3
    export delimited using "`base'_summary.csv", replace
restore

gen double x_mean_black=.78 if _n==1
gen double x_mean_white=2.22 if _n==1
gen double mean_black=`mb' if _n==1
gen double mean_white=`mw' if _n==1
gen double lo_black=`mb'-1.96*`seb' if _n==1
gen double hi_black=`mb'+1.96*`seb' if _n==1
gen double lo_white=`mw'-1.96*`sew' if _n==1
gen double hi_white=`mw'+1.96*`sew' if _n==1

local ttl ""
if "`showtitle'"=="1" local ttl `"title("Twin-profile contact outcomes")"'
twoway ///
    (pcspike white_contacts x_white black_contacts x_black if difference_white_minus_black>=0, lcolor("230 120 95%35") lwidth(vthin)) ///
    (pcspike white_contacts x_white black_contacts x_black if difference_white_minus_black<0, lcolor("65 110 180%35") lwidth(vthin)) ///
    (scatter black_contacts x_black, mcolor("1 115 178") msize(vsmall)) ///
    (scatter white_contacts x_white, mcolor("213 94 0") msize(vsmall)) ///
    (rcap hi_black lo_black x_mean_black, lcolor("1 115 178")) ///
    (rcap hi_white lo_white x_mean_white, lcolor("213 94 0")) ///
    (scatter mean_black x_mean_black, mcolor("1 115 178") msize(medium)) ///
    (scatter mean_white x_mean_white, mcolor("213 94 0") msize(medium)), ///
    xlabel(1 "Black profile" 2 "White profile") xscale(range(.67 2.35)) ///
    ytitle("Number of contacts") xtitle("") ylabel(, grid glcolor(gs14)) ///
    legend(off) graphregion(color(white)) plotregion(color(white)) `ttl' name(pairs, replace)

* Side density uses the same outcomes, plotted vertically beside the pair panel.
quietly kdensity black_contacts, generate(grid_black density_black) n(`n')
quietly kdensity white_contacts, generate(grid_white density_white) n(`n')
gen double neg_density_black=-density_black
twoway ///
    (line grid_black neg_density_black, lcolor("1 115 178") lwidth(medthick)) ///
    (line grid_white density_white, lcolor("213 94 0") lwidth(medthick)), ///
    ytitle("") xtitle("Marginal density") xlabel(, nolabel noticks) ///
    ylabel(, grid glcolor(gs14)) legend(off) ///
    graphregion(color(white)) plotregion(color(white)) name(density, replace)
graph combine density pairs, cols(2) ycommon graphregion(color(white))
graph export "`output'", replace width(2400)
graph export "`base'.pdf", replace
display "F05_STATA_OK n=`n' paired_gap=`md'"
log close
