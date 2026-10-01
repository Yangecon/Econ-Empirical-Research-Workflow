/***************************************************************************
 Event study with pre- and post-treatment coefficient averages.
 Stata 15.1+; native commands only. Bundled demo_panel.csv is required.

 QUICK START:
   cd "D:/your_path"
   Execute this file in Stata.

 REAL RESULTS:
   1. Run your event-study estimator first.
   2. Change MODE to "estimation" and edit TIMES / COEFS below, or
      use MODE "csv" with estimates/covariance CSVs matching Python.
   3. Run this file. It reads e(b), e(V) without clearing estimation results.
      Results in r(), or estimator-specific matrices, need an adapted input block.

 The demo estimates the SAME bundled balanced panel as the Python file.
 Real data and e() are not replaced; preserve/restore protects the dataset.
 Both languages estimate the same 980 observations in demo_panel.csv.

 Interpretation:
   - Pre mean is a placebo summary, NOT an ATT or a joint pre-trend test.
   - Post mean height is not the static DID under reference -1.
   - Post minus pre is the static DID in this balanced common-timing demo.
   - Means use fixed, nonnegative weights normalized within each window.
   - SE(mean) = sqrt(w' V w), including all off-diagonal covariances.
   - Horizontal ribbons are CIs for two scalar means, NOT uniform bands.
   - Averaging biased TWFE coefficients does not remove the underlying bias.
***************************************************************************/
version 15.1
set more off

* =========================== USER SETTINGS ===========================
local MODE "demo"                  // "csv", "demo", or "estimation"
local POST_IS_ATT 0                 // Deprecated: 1 is rejected under -1 normalization
local OUT "figures_stata"
local ESTIMATES_CSV "demo_estimates.csv"
local COVARIANCE_CSV "demo_covariance.csv"
local PANEL_CSV "demo_panel.csv"
local TITLE ""                       // Optional; blank by default
local LEVEL 95
local DF .                         // . = normal; set to e(df_r) for model-based t CIs
local REFERENCE -1
local FIRST_TREATED 0

* These two labels are created ENTIRELY by the graph code.
local PRE_TEXT "Pre-treatment"
local POST_TEXT "Post-treatment"
local LABEL_Y_FRACTION .065         // Fraction of the displayed vertical range

* APPEARANCE ONLY: these settings never change any estimate or interval.
local CI_STYLE "bar"               // "bar" (source-like) or "cap"
local CI_WIDTH_FRACTION .22         // Width of vertical CI bar / min time gap
local CONNECT 0                    // 1 adds faint dashed links within windows
local PERIOD_SPACING .43            // Lower = denser auto-width figure
local FIG_WIDTH .                   // . = automatic, otherwise inches (>=5)
local FIG_WIDTH_MIN 6.2
local FIG_WIDTH_MAX 11
local FIG_WIDTH_OVERHEAD 1.25
local FIG_HEIGHT 4.15

* List coefficients in increasing event-time order. REF is a placeholder,
* not an actual coefficient name. Qualify equation names when necessary.
local TIMES "-6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6 7"
local COEFS "lead6 lead5 lead4 lead3 lead2 REF lag0 lag1 lag2 lag3 lag4 lag5 lag6 lag7"
local WEIGHTS ""                   // Blank = equal weights; otherwise one per TIMES entry
* ====================================================================

if !inlist("`MODE'", "csv", "demo", "estimation") {
    display as error "MODE must be csv, demo, or estimation."
    exit 198
}
if `POST_IS_ATT' {
    display as error "Post mean height is not static DID under -1 normalization; use the contrast."
    exit 198
}
if `LEVEL' <= 0 | `LEVEL' >= 100 {
    display as error "LEVEL must be between 0 and 100."
    exit 198
}
if `DF' < . & `DF' <= 0 {
    display as error "DF must be positive, or missing for normal intervals."
    exit 198
}
if !inlist("`CI_STYLE'", "bar", "cap") {
    display as error "CI_STYLE must be bar or cap."
    exit 198
}
if missing(`CI_WIDTH_FRACTION') | `CI_WIDTH_FRACTION' <= 0 | `CI_WIDTH_FRACTION' > 1 {
    display as error "CI_WIDTH_FRACTION must be in (0,1]."
    exit 198
}
if !inlist(`CONNECT', 0, 1) {
    display as error "CONNECT must be 0 or 1."
    exit 198
}
if missing(`PERIOD_SPACING') | `PERIOD_SPACING' <= 0 {
    display as error "PERIOD_SPACING must be positive."
    exit 198
}
if missing(`FIG_HEIGHT') | `FIG_HEIGHT' < 3 {
    display as error "FIG_HEIGHT must be at least 3 inches."
    exit 198
}
if `FIG_WIDTH' < . & `FIG_WIDTH' < 5 {
    display as error "FIG_WIDTH must be at least 5 inches, or missing for automatic."
    exit 198
}
if `REFERENCE' >= `FIRST_TREATED' {
    display as error "The reference must be before treatment."
    exit 198
}
local CRIT = invnormal(1 - (1 - `LEVEL'/100)/2)
if `DF' < . local CRIT = invttail(`DF', (1 - `LEVEL'/100)/2)

tempname B V TIME RAW_W BFULL VFULL W MEANS VM
local STATIC_DID .
local STATIC_SE .

* ======================= A. INPUT COEFFICIENTS =======================
if "`MODE'" == "demo" {
    local TIMES "-6 -5 -4 -3 -2 -1 0 1 2 3 4 5 6 7"
    local REFERENCE -1
    local FIRST_TREATED 0
    local WEIGHTS ""
    import delimited using "`PANEL_CSV'", clear varnames(1) asdouble
    isid unit event_time
    assert inrange(unit,1,70) & inrange(event_time,-6,7)
    assert inlist(treated,0,1) & post==(event_time>=0)
    count
    assert r(N)==980
    bysort unit: assert _N==14 & treated==treated[1]
    egen byte first_unit = tag(unit)
    count if first_unit & treated
    assert r(N)==35
    drop first_unit
    generate byte did = treated*post
    generate byte time_id = event_time+7
    quietly regress y did i.unit i.time_id
    local KMODEL = e(N)-e(df_r)
    quietly regress y did i.unit i.time_id, vce(cluster unit)
    local NMODEL = e(N)
    local FACTOR = (70/69)*((`NMODEL'-1)/(`NMODEL'-`KMODEL'))
    local STATIC_K = `KMODEL'
    local STATIC_FACTOR = `FACTOR'
    local STATIC_DID = _b[did]
    local STATIC_SE = _se[did]/sqrt(`FACTOR')
    foreach j in 6 5 4 3 2 {
        generate byte lead`j' = treated*(event_time==-`j')
    }
    forvalues j=0/7 {
        generate byte lag`j' = treated*(event_time==`j')
    }
    quietly regress y lead6 lead5 lead4 lead3 lead2 lag0 lag1 lag2 lag3 lag4 lag5 lag6 lag7 ///
        i.unit i.time_id
    local KMODEL = e(N)-e(df_r)
    quietly regress y lead6 lead5 lead4 lead3 lead2 lag0 lag1 lag2 lag3 lag4 lag5 lag6 lag7 ///
        i.unit i.time_id, vce(cluster unit)
    local NMODEL = e(N)
    local FACTOR = (70/69)*((`NMODEL'-1)/(`NMODEL'-`KMODEL'))
    local EVENT_K = `KMODEL'
    local EVENT_FACTOR = `FACTOR'
    matrix `BFULL' = e(b)
    matrix `VFULL' = e(V)/`FACTOR'
    local K : word count `TIMES'
    local COEFS "lead6 lead5 lead4 lead3 lead2 REF lag0 lag1 lag2 lag3 lag4 lag5 lag6 lag7"
    matrix `V' = J(`K', `K', 0)
    matrix `B' = J(1,`K',0)
    forvalues j=1/`K' {
        local cj : word `j' of `COEFS'
        if "`cj'" != "REF" {
            local pj = colnumb(`BFULL',"`cj'")
            matrix `B'[1,`j'] = `BFULL'[1,`pj']
        }
        forvalues k=1/`K' {
            local ck : word `k' of `COEFS'
            if "`cj'" != "REF" & "`ck'" != "REF" {
                local pk = colnumb(`BFULL',"`ck'")
                matrix `V'[`j',`k'] = `VFULL'[`pj',`pk']
            }
        }
    }
}
else if "`MODE'" == "csv" {
    preserve
    import delimited using "`ESTIMATES_CSV'", clear varnames(1)
    confirm variable term
    confirm variable event_time
    confirm variable estimate
    confirm variable is_reference
    capture confirm variable weight
    if _rc generate double weight = 1
    assert !missing(term, event_time, estimate, is_reference, weight)
    assert weight >= 0
    assert event_time == floor(event_time)
    assert inlist(is_reference, 0, 1)
    assert is_reference == (event_time == `REFERENCE')
    count if is_reference
    assert r(N) == 1
    assert estimate == 0 if is_reference
    isid term
    isid event_time
    sort event_time
    local K = _N
    local TIMES ""
    local COEFS ""
    local WEIGHTS ""
    matrix `B' = J(1, `K', 0)
    matrix `V' = J(`K', `K', 0)
    forvalues j=1/`K' {
        local tj = event_time[`j']
        local cj = term[`j']
        local wj = weight[`j']
        local TIMES "`TIMES' `tj'"
        local COEFS "`COEFS' `cj'"
        local WEIGHTS "`WEIGHTS' `wj'"
        matrix `B'[1,`j'] = estimate[`j']
    }
    import delimited using "`COVARIANCE_CSV'", clear varnames(1)
    confirm variable term
    isid term
    count
    assert r(N) == `K'
    forvalues j=1/`K' {
        local cj : word `j' of `COEFS'
        capture confirm variable `cj'
        if _rc {
            display as error "Covariance column missing: `cj'"
            exit 111
        }
        count if term == "`cj'"
        assert r(N) == 1
        forvalues k=1/`K' {
            local ck : word `k' of `COEFS'
            capture confirm variable `ck'
            if _rc {
                display as error "Covariance column missing: `ck'"
                exit 111
            }
            quietly summarize `ck' if term == "`cj'", meanonly
            matrix `V'[`j',`k'] = r(mean)
            if missing(`V'[`j',`k']) {
                display as error "Missing covariance cell: `cj' by `ck'"
                exit 498
            }
        }
    }
    restore
}
else {
    capture matrix `BFULL' = e(b)
    if _rc {
        display as error "No e(b). Run the estimator before using estimation mode."
        exit 301
    }
    capture matrix `VFULL' = e(V)
    if _rc {
        display as error "No e(V). Supply the full covariance, not only SEs."
        exit 301
    }
    local K : word count `TIMES'
    local NC : word count `COEFS'
    if `K' != `NC' {
        display as error "TIMES and COEFS must have equal length."
        exit 198
    }
    matrix `B' = J(1, `K', 0)
    matrix `V' = J(`K', `K', 0)
    forvalues j=1/`K' {
        local cj : word `j' of `COEFS'
        local tj : word `j' of `TIMES'
        if ("`cj'" == "REF") != (`tj' == `REFERENCE') {
            display as error "The REF placeholder must match REFERENCE."
            exit 198
        }
        if "`cj'" != "REF" {
            local pj = colnumb(`BFULL', "`cj'")
            if missing(`pj') | `pj' <= 0 {
                display as error "Coefficient not found in e(b): `cj'"
                exit 111
            }
            matrix `B'[1,`j'] = `BFULL'[1,`pj']
            forvalues k=1/`K' {
                local ck : word `k' of `COEFS'
                if "`ck'" != "REF" {
                    local pk = colnumb(`BFULL', "`ck'")
                    if missing(`pk') | `pk' <= 0 {
                        display as error "Coefficient not found in e(b): `ck'"
                        exit 111
                    }
                    matrix `V'[`j',`k'] = `VFULL'[`pj',`pk']
                }
            }
            if `V'[`j',`j'] <= 0 | missing(`V'[`j',`j']) {
                display as error "Non-reference term has zero/missing variance: `cj'"
                exit 498
            }
        }
    }
}

* ====================== B. WEIGHTED AGGREGATION ======================
local NREF 0
forvalues j=1/`K' {
    local tj : word `j' of `TIMES'
    if `tj' == `REFERENCE' {
        local NREF = `NREF' + 1
        if abs(`B'[1,`j']) > 1e-12 {
            display as error "Reference coefficient must equal zero."
            exit 498
        }
    }
    else if missing(`V'[`j',`j']) | `V'[`j',`j'] <= 0 {
        display as error "Non-reference coefficient needs positive variance."
        exit 498
    }
    forvalues k=1/`K' {
        if missing(`V'[`j',`k']) | abs(`V'[`j',`k'] - `V'[`k',`j']) > 1e-9 {
            display as error "Covariance must be finite and symmetric."
            exit 498
        }
        if `tj' == `REFERENCE' & abs(`V'[`j',`k']) > 1e-12 {
            display as error "Reference covariance row must be zero."
            exit 498
        }
    }
}
if `NREF' != 1 {
    display as error "Exactly one reference at -1 is required."
    exit 198
}
tempname EIGMIN VMAX
mata: st_numscalar("`EIGMIN'", min(symeigenvalues(st_matrix("`V'"))))
mata: st_numscalar("`VMAX'", max(vec(abs(st_matrix("`V'")))))
if `EIGMIN' < -1e-10*max(`VMAX', 1e-15) {
    display as error "Covariance must be positive semidefinite."
    exit 498
}
local NW : word count `WEIGHTS'
if `NW' != 0 & `NW' != `K' {
    display as error "WEIGHTS must be blank or have one entry per event time."
    exit 198
}
matrix `TIME' = J(1, `K', .)
matrix `RAW_W' = J(1, `K', 1)
matrix `W' = J(2, `K', 0)
local SUMPRE 0
local SUMPOST 0
local STEP .
local LAST_PRE .
local FIRST_POST .
local NPRE 0
local NPOST 0
local PRE_MIN .
local PRE_MAX .
local POST_MIN .
local POST_MAX .
forvalues j=1/`K' {
    local tj : word `j' of `TIMES'
    if missing(`tj') {
        display as error "TIMES must contain only finite numeric values."
        exit 198
    }
    matrix `TIME'[1,`j'] = `tj'
    if `j' > 1 {
        local GAP = `tj' - `TIME'[1,`j'-1]
        if `GAP' <= 0 {
            display as error "TIMES must be strictly increasing."
            exit 198
        }
        local STEP = min(`STEP', `GAP')
    }
    local wj 1
    if `NW' > 0 local wj : word `j' of `WEIGHTS'
    if missing(`wj') | `wj' < 0 {
        display as error "Weights must be finite and nonnegative."
        exit 198
    }
    matrix `RAW_W'[1,`j'] = `wj'
    if `tj' < `FIRST_TREATED' local LAST_PRE = `tj'
    if `tj' >= `FIRST_TREATED' & missing(`FIRST_POST') local FIRST_POST = `tj'
    if `tj' < `FIRST_TREATED' {
        local SUMPRE = `SUMPRE' + `wj'
        local NPRE = `NPRE' + 1
        local PRE_MIN = min(`PRE_MIN', `tj')
        local PRE_MAX = `tj'
    }
    if `tj' >= `FIRST_TREATED' {
        local SUMPOST = `SUMPOST' + `wj'
        local NPOST = `NPOST' + 1
        local POST_MIN = min(`POST_MIN', `tj')
        local POST_MAX = `tj'
    }
}
if `SUMPRE' <= 0 | `SUMPOST' <= 0 {
    display as error "Both pre and post windows require positive total weight."
    exit 198
}
forvalues j=1/`K' {
    local tj = `TIME'[1,`j']
    if `tj' < `FIRST_TREATED' ///
        matrix `W'[1,`j'] = `RAW_W'[1,`j']/`SUMPRE'
    if `tj' >= `FIRST_TREATED' ///
        matrix `W'[2,`j'] = `RAW_W'[1,`j']/`SUMPOST'
}
matrix `MEANS' = `W' * `B''
matrix `VM' = `W' * `V' * `W''
if `VM'[1,1] < 0 | `VM'[2,2] < 0 {
    display as error "Negative summary variance. Check the covariance matrix."
    exit 498
}
local PRE_B = `MEANS'[1,1]
local POST_B = `MEANS'[2,1]
local PRE_SE = sqrt(`VM'[1,1])
local POST_SE = sqrt(`VM'[2,2])
local PRE_LO = `PRE_B' - `CRIT'*`PRE_SE'
local PRE_HI = `PRE_B' + `CRIT'*`PRE_SE'
local POST_LO = `POST_B' - `CRIT'*`POST_SE'
local POST_HI = `POST_B' + `CRIT'*`POST_SE'
local PRE_NUMBER : display %6.3f `PRE_B'
local POST_NUMBER : display %6.3f `POST_B'
local POST_LABEL "Post mean"
local SOURCE "Estimation inputs; fixed weights normalized within each window."
if "`MODE'" == "demo" local SOURCE "Synthetic inputs; equal event-time weights. Not the paper's estimates."
if "`MODE'" == "csv" local SOURCE "CSV inputs; inspect provenance before interpreting estimates."

* ========================= C. PLOTTING DATA ==========================
preserve
clear
local N = `K' + 4
quietly set obs `N'
generate byte kind = cond(_n <= `K', 1, 2)
generate double event_time = .
generate double estimate = .
generate double ci_low = .
generate double ci_high = .
generate byte reference = 0
generate byte significant = 0
generate byte group = .
forvalues j=1/`K' {
    quietly replace event_time = `TIME'[1,`j'] in `j'
    quietly replace estimate = `B'[1,`j'] in `j'
    quietly replace ci_low = `B'[1,`j'] - `CRIT'*sqrt(`V'[`j',`j']) in `j'
    quietly replace ci_high = `B'[1,`j'] + `CRIT'*sqrt(`V'[`j',`j']) in `j'
    quietly replace reference = (event_time == `REFERENCE') in `j'
    quietly replace significant = (ci_low > 0 | ci_high < 0) & !reference in `j'
    quietly replace group = cond(event_time < `FIRST_TREATED', 1, 2) in `j'
}
local a = `K' + 1
local b = `K' + 2
local c = `K' + 3
local d = `K' + 4
quietly replace group = 1 in `a'/`b'
quietly replace group = 2 in `c'/`d'
quietly replace event_time = `PRE_MIN' - .42*`STEP' in `a'
quietly replace event_time = `PRE_MAX' + .42*`STEP' in `b'
quietly replace event_time = `POST_MIN' - .42*`STEP' in `c'
quietly replace event_time = `POST_MAX' + .42*`STEP' in `d'
quietly replace estimate = `PRE_B' in `a'/`b'
quietly replace ci_low = `PRE_LO' in `a'/`b'
quietly replace ci_high = `PRE_HI' in `a'/`b'
quietly replace estimate = `POST_B' in `c'/`d'
quietly replace ci_low = `POST_LO' in `c'/`d'
quietly replace ci_high = `POST_HI' in `c'/`d'
generate double band_x = .
quietly replace band_x = (`PRE_MIN'+`PRE_MAX')/2 in `a'
quietly replace band_x = (`POST_MIN'+`POST_MAX')/2 in `c'
local PRE_BAND_WIDTH = `PRE_MAX'-`PRE_MIN'+.84*`STEP'
local POST_BAND_WIDTH = `POST_MAX'-`POST_MIN'+.84*`STEP'

* ================= D. AUTOMATIC LABEL COORDINATES ====================
local DIVIDER = (`LAST_PRE' + `FIRST_POST')/2
local XMIN = `TIME'[1,1] - .6*`STEP'
local XMAX = `TIME'[1,`K'] + .6*`STEP'
local X_PRE = (`XMIN' + `DIVIDER')/2
local X_POST = (`DIVIDER' + `XMAX')/2
quietly summarize ci_low, meanonly
local DATA_LOW = min(r(min), 0)
quietly summarize ci_high, meanonly
local DATA_HIGH = max(r(max), 0)
local SPAN = max(`DATA_HIGH' - `DATA_LOW', .01)
local YMIN = `DATA_LOW' - .23*`SPAN'
local YMAX = `DATA_HIGH' + .13*`SPAN'
local Y_TEXT = `YMIN' + `LABEL_Y_FRACTION'*(`YMAX' - `YMIN')
local BARWIDTH = `CI_WIDTH_FRACTION'*`STEP'

* Auto-width changes the physical display size, NOT the event-time coordinates.
if missing(`FIG_WIDTH') {
    local FIG_WIDTH = min(`FIG_WIDTH_MAX', max(`FIG_WIDTH_MIN', ///
        `FIG_WIDTH_OVERHEAD' + `PERIOD_SPACING'*`K'))
}
local TICK_CAPACITY = max(8, floor(`FIG_WIDTH'*2.2))
local TICK_STRIDE = max(1, ceil(`K'/`TICK_CAPACITY'))
local XTICKS ""
forvalues j=1/`K' {
    local tj = `TIME'[1,`j']
    if mod(`j'-1, `TICK_STRIDE') == 0 | `j' == 1 | `j' == `K' | ///
       `tj' == `REFERENCE' | `tj' == `FIRST_POST' {
        local XTICKS "`XTICKS' `tj'"
    }
}
local EXPORT_WIDTH = round(300*`FIG_WIDTH')

* ===================== E. GRAPH: INCLUDING TEXT ======================
* p1/p2 use the user's current Stata scheme rather than hardcoded group colors.
* PRE_TEXT / POST_TEXT can be edited above; text() takes y FIRST, then x.
capture mkdir "`OUT'"
local TITLE_OPT ""
if `"`TITLE'"' != "" local TITLE_OPT `"title("`TITLE'", size(medsmall))"'
local CI1 "(rbar ci_low ci_high event_time if kind==1 & !reference & !significant, barwidth(`BARWIDTH') fcolor(gs9%25) lcolor(none))"
local CI2 "(rbar ci_low ci_high event_time if kind==1 & significant, barwidth(`BARWIDTH') fcolor(gs9%25) lcolor(none))"
if "`CI_STYLE'" == "cap" {
    local CI1 "(rcap ci_high ci_low event_time if kind==1 & !reference & !significant, lcolor(gs9) lwidth(medthin))"
    local CI2 "(rcap ci_high ci_low event_time if kind==1 & significant, lcolor(gs9) lwidth(medthin))"
}
local CONNECT1 ""
local CONNECT2 ""
local LEG_PRE 7
local LEG_POST 8
if `CONNECT' {
    local CONNECT1 "(line estimate event_time if kind==1 & group==1 & !reference, sort lpattern(shortdash) lcolor(gs8) lwidth(vthin))"
    local CONNECT2 "(line estimate event_time if kind==1 & group==2, sort lpattern(shortdash) lcolor(gs8) lwidth(vthin))"
    local LEG_PRE 9
    local LEG_POST 10
}
twoway ///
    (rbar ci_low ci_high band_x if _n==`a', ///
        barwidth(`PRE_BAND_WIDTH') fcolor("31 119 180%20") lcolor(none)) ///
    (rbar ci_low ci_high band_x if _n==`c', ///
        barwidth(`POST_BAND_WIDTH') fcolor("255 127 14%20") lcolor(none)) ///
    `CI1' ///
    `CI2' ///
    `CONNECT1' ///
    `CONNECT2' ///
    (scatter estimate event_time if kind==1 & !reference & !significant, ///
        msymbol(O) msize(small) mfcolor(white) mlcolor(gs8) mlwidth(medthin)) ///
    (scatter estimate event_time if kind==1 & significant, ///
        msymbol(O) msize(small) mcolor(black)) ///
    (line estimate event_time if kind==2 & group==1, ///
        sort lcolor("31 119 180") lwidth(medthick)) ///
    (line estimate event_time if kind==2 & group==2, ///
        sort lcolor("255 127 14") lwidth(medthick)) ///
    (scatter estimate event_time if kind==1 & reference, ///
        msymbol(O) msize(small) mfcolor(white) mlcolor(gs8)), ///
    xline(`DIVIDER', lpattern(shortdash) lwidth(vthin) lcolor(gs10)) ///
    yline(0, lpattern(shortdash) lwidth(vthin) lcolor(gs10)) ///
    text(`Y_TEXT' `X_PRE' "`PRE_TEXT'" ///
         `Y_TEXT' `X_POST' "`POST_TEXT'", place(c) size(small)) ///
    xlabel(`XTICKS', labsize(small) nogrid) ///
    ylabel(, angle(horizontal) labsize(small) nogrid) ///
    xscale(range(`XMIN' `XMAX') noextend) ///
    yscale(range(`YMIN' `YMAX') noextend) ///
    xtitle("Event time relative to treatment", size(small)) ///
    ytitle("Estimated effect", size(small)) ///
    legend(order(`LEG_PRE' "Pre mean = `PRE_NUMBER'" `LEG_POST' "`POST_LABEL' = `POST_NUMBER'") ///
        rows(1) position(6) size(small) region(lcolor(none))) ///
    `TITLE_OPT' ///
    graphregion(color(white) margin(small)) plotregion(color(white)) ///
    xsize(`FIG_WIDTH') ysize(`FIG_HEIGHT') name(event_aggregate, replace)

local STEM "event_study_with_pre_post_averages_stata"
graph export "`OUT'/`STEM'.png", width(`EXPORT_WIDTH') replace
graph export "`OUT'/`STEM'.pdf", replace
graph export "`OUT'/`STEM'.svg", replace
graph save "`OUT'/`STEM'.gph", replace
restore

* Machine-readable values for Python/Stata parity checks.
preserve
clear
quietly set obs 2
generate str4 group = cond(_n==1, "pre", "post")
generate double estimate = cond(_n==1, `PRE_B', `POST_B')
generate double se = cond(_n==1, `PRE_SE', `POST_SE')
generate double ci_low = cond(_n==1, `PRE_LO', `POST_LO')
generate double ci_high = cond(_n==1, `PRE_HI', `POST_HI')
export delimited using "`OUT'/`STEM'_summaries.csv", replace
restore

* The plotted gap is a separate full-covariance contrast, not a third ribbon.
tempname C VC
matrix `C' = J(1,`K',0)
forvalues j=1/`K' {
    matrix `C'[1,`j'] = `W'[2,`j']-`W'[1,`j']
}
matrix `VC' = `C' * `V' * `C''
local GAP_B = `POST_B'-`PRE_B'
local GAP_SE = sqrt(`VC'[1,1])
local GAP_LO = `GAP_B'-`CRIT'*`GAP_SE'
local GAP_HI = `GAP_B'+`CRIT'*`GAP_SE'
if "`MODE'" == "demo" {
    assert abs(`GAP_B'-`STATIC_DID') < 1e-9
    assert abs(`GAP_SE'-`STATIC_SE') < 1e-9
}
preserve
clear
quietly set obs 1
generate str20 estimand = "post_minus_pre"
generate double estimate = `GAP_B'
generate double se = `GAP_SE'
generate double ci_low = `GAP_LO'
generate double ci_high = `GAP_HI'
export delimited using "`OUT'/`STEM'_contrast.csv", replace
restore
if "`MODE'" == "demo" {
    preserve
    clear
    quietly set obs 1
    generate double static_did = `STATIC_DID'
    generate double static_cr0_se = `STATIC_SE'
    generate int observations = `NMODEL'
    generate int static_parameters = `STATIC_K'
    generate int event_parameters = `EVENT_K'
    generate double static_cluster_factor = `STATIC_FACTOR'
    generate double event_cluster_factor = `EVENT_FACTOR'
    export delimited using "`OUT'/demo_model_checks.csv", replace
    restore
    preserve
    clear
    quietly set obs 14
    generate str8 term = ""
    generate int event_time = .
    generate double estimate = .
    generate byte is_reference = .
    generate byte weight = 1
    forvalues j=1/14 {
        local cj : word `j' of `COEFS'
        quietly replace term = "`cj'" in `j'
        quietly replace event_time = `TIME'[1,`j'] in `j'
        quietly replace estimate = `B'[1,`j'] in `j'
        quietly replace is_reference = (`TIME'[1,`j']==-1) in `j'
    }
    export delimited using "`OUT'/demo_estimates_stata.csv", replace
    clear
    quietly set obs 14
    generate str8 term = ""
    forvalues j=1/14 {
        local cj : word `j' of `COEFS'
        quietly replace term = "`cj'" in `j'
        generate double `cj' = .
        forvalues k=1/14 {
            quietly replace `cj' = `V'[`k',`j'] in `k'
        }
    }
    export delimited using "`OUT'/demo_covariance_stata.csv", replace
    restore
}

display as text "Pre mean: " as result %9.6f `PRE_B' "   SE: " %9.6f `PRE_SE'
display as text "`POST_LABEL': " as result %9.6f `POST_B' "   SE: " %9.6f `POST_SE'
display as text "Post minus pre: " as result %9.6f `GAP_B' "   CR0 SE: " %9.6f `GAP_SE'
display as text "`SOURCE'"
display as text "Figure size (inches): `FIG_WIDTH' x `FIG_HEIGHT'"
display as text "Saved in: `OUT'"
display as result "STATA_EVENT_AVERAGES_COMPLETE"
