* Supplied medians and nested 68/90 percent posterior uncertainty regions.
version 19.0
args input output lang showtitle
if `"`input'"' == "" local input "demo.csv"
if `"`output'"' == "" {
    display as error "output PNG path is required"
    exit 198
}
if `"`lang'"' == "" local lang "en"
if `"`showtitle'"' == "" local showtitle "0"
if !inlist(`"`lang'"', "en", "zh") exit 198

* CONFIG: panel IDs, row-specific units/limits and labels parallel plot.py.
local row1 "activity"
local row2 "prices"
local row3 "rate"
local row4 "household_credit"
local row5 "business_credit"
local col1 "monetary"
local col2 "household"
local col3 "firm"
local col4 "stress_a"
local col5 "stress_b"
local ymin1 -.011
local ymax1 .008
local ymin2 -.009
local ymax2 .008
local ymin3 -.004
local ymax3 .006
local ymin4 -.03
local ymax4 .015
local ymin5 -.03
local ymax5 .018
local yticks1 "-.010 0 .005"
local yticks2 "-.008 0 .008"
local yticks3 "-.004 0 .006"
local yticks4 "-.030 0 .015"
local yticks5 "-.030 0 .015"
if `"`lang'"' == "zh" {
    local rowlab1 "经济活动（对数点）"
    local rowlab2 "价格（对数点）"
    local rowlab3 "利率（百分点）"
    local rowlab4 "家庭信贷（对数点）"
    local rowlab5 "企业信贷（对数点）"
    local collab1 "货币政策"
    local collab2 "家庭信贷"
    local collab3 "企业信贷"
    local collab4 "压力冲击 A"
    local collab5 "压力冲击 B"
    local xlab "冲击后的月数"
    local heading "脉冲响应"
}
else {
    local rowlab1 "Activity (log points)"
    local rowlab2 "Prices (log points)"
    local rowlab3 "Rate (percentage points)"
    local rowlab4 "Household credit (log points)"
    local rowlab5 "Business credit (log points)"
    local collab1 "Monetary"
    local collab2 "Household credit"
    local collab3 "Firm credit"
    local collab4 "Stress A"
    local collab5 "Stress B"
    local xlab "Months after shock"
    local heading "Impulse responses"
}

local normalized = subinstr(`"`output'"', "\", "/", .)
local lastslash = strrpos(`"`normalized'"', "/")
if `lastslash' > 0 {
    local outdir = substr(`"`normalized'"', 1, `lastslash'-1)
    forvalues k = 1/`=strlen(`"`outdir'"')' {
        if substr(`"`outdir'"', `k', 1) == "/" {
            local prefix = substr(`"`outdir'"', 1, `k'-1)
            capture mkdir `"`prefix'"'
        }
    }
    capture mkdir `"`outdir'"'
}

import delimited using `"`input'"', clear varnames(1) stringcols(_all) encoding(UTF-8)
confirm variable response shock horizon median lo68 hi68 lo90 hi90
assert !missing(response, shock, horizon, median, lo68, hi68, lo90, hi90)
destring horizon median lo68 hi68 lo90 hi90, replace
assert !missing(horizon, median, lo68, hi68, lo90, hi90)
assert horizon >= 0 & horizon == floor(horizon)
assert lo90 <= lo68 & lo68 <= median & median <= hi68 & hi68 <= hi90
assert inlist(response, "`row1'", "`row2'", "`row3'", "`row4'", "`row5'")
assert inlist(shock, "`col1'", "`col2'", "`col3'", "`col4'", "`col5'")
isid response shock horizon
sort response shock horizon
by response shock: generate int hindex = _n
bysort hindex: egen double minh = min(horizon)
bysort hindex: egen double maxh = max(horizon)
assert minh == maxh
drop minh maxh
quietly summarize horizon, meanonly
local xmax = r(max)
local xmid = floor(`xmax'/2)
generate byte outer_excludes_zero = lo90 > 0 | hi90 < 0
local totalrows = _N
local checked = regexr(`"`output'"', "[.]png$", "_checked.csv")
tempfile raw
save `raw'

local panels ""
local expectedN 0
forvalues i = 1/5 {
    forvalues j = 1/5 {
        use `raw', clear
        keep if response == `"`row`i''"' & shock == `"`col`j''"'
        assert _N >= 3
        if `expectedN' == 0 local expectedN = _N
        assert _N == `expectedN'
        assert horizon[1] == 0
        assert lo90 >= `ymin`i'' & hi90 <= `ymax`i''
        sort horizon
        generate byte mark = inlist(horizon, 0, 12, 24, 36, 48, 60)
        local titleopt ""
        if `i' == 1 local titleopt `"title(`"`collab`j''"', size(small))"'
        local ytitleopt `"ytitle("")"'
        if `j' == 1 local ytitleopt `"ytitle(`"`rowlab`i''"', size(vsmall))"'
        local ylabelopt "ylabel(`yticks`i'', angle(0) labsize(vsmall) format(%7.3f) labelminlen(6) grid glcolor(gs14))"
        local xlabelopt `"xlabel(0 `xmid' `xmax', nolabel noticks) xtitle("")"'
        if `i' == 5 local xlabelopt `"xlabel(0 `xmid' `xmax', labsize(vsmall)) xtitle(`"`xlab'"', size(vsmall))"'
        twoway ///
            (rarea lo90 hi90 horizon, fcolor(eltblue%55) lcolor(eltblue%55) lwidth(none)) ///
            (rarea lo68 hi68 horizon, fcolor(blue%55) lcolor(blue%55) lwidth(none)) ///
            (line median horizon, lcolor(black) lwidth(thin)) ///
            (scatter median horizon if mark & outer_excludes_zero, mcolor(black) msymbol(O) msize(vsmall)) ///
            (scatter median horizon if mark & !outer_excludes_zero, mfcolor(white) mlcolor(black) msymbol(O) msize(vsmall)), ///
            xscale(range(0 `xmax') noextend) yscale(range(`ymin`i'' `ymax`i'') noextend) ///
            yline(0, lcolor(gs4) lwidth(thin)) `xlabelopt' `ylabelopt' `ytitleopt' `titleopt' ///
            legend(off) graphregion(color(white) margin(zero)) plotregion(color(white) margin(small)) scheme(s1color) ///
            name(g`i'`j', replace)
        local panels "`panels' g`i'`j'"
    }
}
assert `totalrows' == 25*`expectedN'
use `raw', clear
export delimited response shock horizon median lo68 hi68 lo90 hi90 outer_excludes_zero using `"`checked'"', replace
local maintitle ""
if `"`showtitle'"' == "1" local maintitle `"title(`"`heading'"', size(medsmall))"'
graph combine `panels', cols(5) imargin(small) `maintitle' graphregion(color(white)) xsize(14.5) ysize(11.5)
graph export `"`output'"', width(3190) replace
local pdf = regexr(`"`output'"', "[.]png$", ".pdf")
graph export `"`pdf'"', replace
display "STATA_COMPLETE rows=`totalrows' panels=25 output=`output'"
