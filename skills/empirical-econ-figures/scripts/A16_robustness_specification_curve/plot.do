* Sorted result curve with spec-ID-locked binary choice matrix on one canvas.
version 19.0
args input output lang showtitle
if `"`input'"'=="" local input "demo.csv"
if `"`output'"'=="" {
    display as error "output PNG path required"
    exit 198
}
if `"`lang'"'=="" local lang "en"
if `"`showtitle'"'=="" local showtitle "0"
if !inlist(`"`lang'"',"en","zh") exit 198
* CONFIG: result means mean t-statistic across experiments for this example.
local resultmin -1
local resultmax 6
local options "baseline regional first_round exclude_municipalities pool_one_site logarithm gdp gdp_per_capita population fiscal_income fiscal_expenditure"
assert `resultmin'<`resultmax'
local yminplot 13
local ymaxplot 20
local yzero=`yminplot'+(`ymaxplot'-`yminplot')*(0-`resultmin')/(`resultmax'-`resultmin')
if `"`lang'"'=="zh" {
    local ylabels `"1 "财政支出" 2 "财政收入" 3 "人口" 4 "人均GDP" 5 "GDP" 6 "对数形式" 7 "合并单点政策" 8 "排除直辖市" 9 "仅首轮试点" 10 "纳入区域政策" 11 "基准设定""'
    local resultlabel "各实验t统计量的均值"
    local xlab "按结果排序的模型设定"
    local heading "模型设定曲线"
}
else {
    local ylabels `"1 "Fiscal expenditure" 2 "Fiscal income" 3 "Population" 4 "GDP per capita" 5 "GDP" 6 "Logarithm" 7 "One-site policies pooled" 8 "Municipalities excluded" 9 "First round only" 10 "Regional policies included" 11 "Baseline""'
    local resultlabel "Mean t-statistic across experiments"
    local xlab "Specifications sorted by result"
    local heading "Specification curve"
}
local ylabels `"`ylabels' `yminplot' `"`resultmin'"' `ymaxplot' `"`resultmax'"'"'
local zeroline ""
if `resultmin'<0 & 0<`resultmax' {
    local ylabels `"`ylabels' `yzero' `"0"'"'
    local zeroline "yline(`yzero',lcolor(gs9) lpattern(dash))"
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
import delimited using `"`input'"',clear varnames(1) stringcols(_all) encoding(UTF-8)
confirm variable spec_id result
assert !missing(spec_id,result)
isid spec_id
assert _N>=5
local nspec=_N
capture confirm variable ci_low
local haslow=(_rc==0)
capture confirm variable ci_high
local hashigh=(_rc==0)
assert `haslow'==`hashigh'
if !`haslow' {
    generate str1 ci_low=""
    generate str1 ci_high=""
}
generate double result_num=real(result)
generate double lo_num=real(ci_low)
generate double hi_num=real(ci_high)
assert ci_low=="" | !missing(lo_num)
assert ci_high=="" | !missing(hi_num)
drop result ci_low ci_high
rename result_num result
rename lo_num ci_low
rename hi_num ci_high
assert !missing(result)
assert missing(ci_low)==missing(ci_high)
assert ci_low<=result & result<=ci_high if !missing(ci_low)
assert inrange(result,`resultmin',`resultmax')
assert inrange(ci_low,`resultmin',`resultmax') & inrange(ci_high,`resultmin',`resultmax') if !missing(ci_low)
local expectedopts ""
foreach opt of local options {
    local expectedopts "`expectedopts' opt_`opt'"
}
ds opt_*
local allopts `r(varlist)'
local extraopts : list allopts - expectedopts
if `"`extraopts'"'!="" {
    display as error "unconfigured option columns: `extraopts'"
    exit 9
}
foreach opt of local options {
    confirm variable opt_`opt'
    assert inlist(opt_`opt',"0","1")
    generate byte temp_`opt'=real(opt_`opt')
    drop opt_`opt'
    rename temp_`opt' opt_`opt'
}
sort result spec_id
generate long rank=_n
local stem=regexr(`"`output'"',"[.]png$","")
export delimited using `"`stem'_ordered.csv"',replace
reshape long opt_,i(spec_id) j(option) string
generate byte row=.
replace row=11 if option=="baseline"
replace row=10 if option=="regional"
replace row=9 if option=="first_round"
replace row=8 if option=="exclude_municipalities"
replace row=7 if option=="pool_one_site"
replace row=6 if option=="logarithm"
replace row=5 if option=="gdp"
replace row=4 if option=="gdp_per_capita"
replace row=3 if option=="population"
replace row=2 if option=="fiscal_income"
replace row=1 if option=="fiscal_expenditure"
assert !missing(row) & inlist(opt_,0,1)
bysort spec_id: assert _N==11
generate double result_y=`yminplot'+(`ymaxplot'-`yminplot')*(result-`resultmin')/(`resultmax'-`resultmin')
generate double lo_y=`yminplot'+(`ymaxplot'-`yminplot')*(ci_low-`resultmin')/(`resultmax'-`resultmin')
generate double hi_y=`yminplot'+(`ymaxplot'-`yminplot')*(ci_high-`resultmin')/(`resultmax'-`resultmin')
local xticks "1"
forvalues i=2/`nspec' {
    if mod(`i',10)==0 local xticks "`xticks' `i'"
}
if mod(`nspec',10)!=0 local xticks "`xticks' `nspec'"
local maintitle ""
if `"`showtitle'"'=="1" local maintitle `"title(`"`heading'"',size(medium))"'
twoway ///
    (rcap hi_y lo_y rank if row==11 & !missing(ci_low),lcolor(maroon) lwidth(vthin)) ///
    (scatter result_y rank if row==11,msymbol(O) mcolor(maroon) msize(small)) ///
    (scatter row rank if opt_==0,msymbol(O) mcolor(gs12) msize(vsmall)) ///
    (scatter row rank if opt_==1,msymbol(O) mcolor(black) msize(vsmall)), ///
    xscale(range(.3 `=`nspec'+.7') noextend) xlabel(`xticks',labsize(small)) ///
    yscale(range(.4 20.7) noextend) ylabel(`ylabels',angle(0) labsize(vsmall) noticks) ///
    `zeroline' yline(12.3,lcolor(gs12) lwidth(thin)) ///
    text(20.45 1 `"`resultlabel'"',placement(e) size(vsmall) color(gs5)) ///
    xtitle(`"`xlab'"',size(small)) ytitle("") `maintitle' legend(off) ///
    graphregion(color(white) margin(small)) plotregion(color(white)) scheme(s1color) ///
    xsize(12.6) ysize(7.6)
graph export `"`output'"',width(2772) replace
local pdf=regexr(`"`output'"',"[.]png$",".pdf")
graph export `"`pdf'"',replace
quietly count if row==11 & !missing(ci_low)
local ci_n=r(N)
display "STATA_COMPLETE specs=`nspec' choices=11 ci_specs=`ci_n' output=`output'"
