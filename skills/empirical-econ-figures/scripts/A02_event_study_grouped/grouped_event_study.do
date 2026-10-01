version 19.0

capture program drop grouped_event_study
program define grouped_event_study
    version 19.0
    syntax, INPUT(string) OUTPUT(string) [REFERENCE(real -1) POLICYTIME(real 0) LEVEL(real 95) LANGuage(string) TITLE(string)]

    if (`level' <= 0 | `level' >= 100) {
        display as error "level() must be between 0 and 100"
        exit 198
    }
    if "`language'" == "" local language "en"
    if !inlist("`language'", "en", "zh") {
        display as error "language() must be en or zh"
        exit 198
    }

    import delimited using "`input'", varnames(1) clear stringcols(_all)
    foreach v in event_time group estimate {
        capture confirm variable `v'
        if _rc {
            display as error "Missing required column: `v'"
            exit 111
        }
    }
    destring event_time estimate, replace
    capture confirm string variable group
    if _rc {
        display as error "group must be text"
        exit 109
    }
    assert !missing(event_time, group)
    assert !missing(estimate) if event_time != `reference'
    isid group event_time

    capture confirm variable ci_low
    local haslo = (_rc == 0)
    capture confirm variable ci_high
    local hashi = (_rc == 0)
    if (`haslo' != `hashi') {
        display as error "Supply both ci_low and ci_high"
        exit 111
    }
    if !`haslo' {
        capture confirm variable se
        if _rc {
            display as error "Supply se or both ci_low and ci_high"
            exit 111
        }
        destring se, replace
        assert !missing(se) & se >= 0 if event_time != `reference'
        local z = invnormal(0.5 + `level'/200)
        generate double ci_low = estimate - `z' * se
        generate double ci_high = estimate + `z' * se
    }
    else {
        destring ci_low ci_high, replace
    }
    assert !missing(ci_low, ci_high) if event_time != `reference'
    assert ci_low <= estimate & estimate <= ci_high if event_time != `reference'
    drop if event_time == `reference'
    count
    local n_est = r(N)
    if `n_est' == 0 {
        display as error "No non-reference estimates"
        exit 2000
    }
    generate long source_row = _n
    bysort group (source_row): generate long first_row = source_row[1]
    egen group_id = group(first_row)
    sort source_row
    quietly summarize group_id, meanonly
    local ng = r(max)
    if `ng' < 2 {
        display as error "At least two groups are required"
        exit 2000
    }
    generate byte significant = (ci_low > 0 | ci_high < 0)
    count if significant
    local n_sig = r(N)
    quietly summarize event_time, meanonly
    local min_time = min(r(min), `reference')
    local max_time = max(r(max), `reference')
    preserve
    keep event_time
    duplicates drop
    local extra = _N + 1
    set obs `extra'
    replace event_time = `reference' in `extra'
    duplicates drop
    sort event_time
    generate double gap = event_time - event_time[_n-1] if _n > 1
    quietly summarize gap, meanonly
    local min_gap = r(min)
    restore
    if missing(`min_gap') | `min_gap' <= 0 local min_gap = 1
    local span = 0.26 * `min_gap'
    generate double xplot = .
    forvalues i=1/`ng' {
        local offset = ((`i'-1)/(`ng'-1)-0.5)*`span'
        replace xplot = event_time + `offset' if group_id == `i'
    }
    local ref_row = _N + 1
    set obs `ref_row'
    replace event_time = `reference' in `ref_row'
    replace xplot = `reference' in `ref_row'
    replace estimate = 0 in `ref_row'
    generate byte normalized_reference = (_n == `ref_row')

    local color1 "0 136 55"
    local color2 "197 27 43"
    local color3 "43 108 176"
    local color4 "142 68 173"
    local color5 "179 107 0"
    local color6 "0 125 138"
    local symbols "D O S T V P X"
    local plots ""
    local legend_order ""
    local layer = 0
    forvalues i=1/`ng' {
        local color_index = mod(`i'-1, 6) + 1
        local color "`color`color_index''"
        local symbol_index = mod(`i'-1, 7) + 1
        local symbol : word `symbol_index' of `symbols'
        quietly summarize source_row if group_id == `i', meanonly
        local first_obs = r(min)
        local group_name = group[`first_obs']
        local plots `"`plots' (rcap ci_high ci_low xplot if group_id == `i' & !normalized_reference, lcolor("`color'") lwidth(medthin))"'
        local layer = `layer' + 1
        local plots `"`plots' (scatter estimate xplot if group_id == `i' & significant, msymbol(`symbol') mcolor("`color'") msize(medsmall))"'
        local layer = `layer' + 1
        local legend_order `"`legend_order' `layer' "`group_name'""'
        local plots `"`plots' (scatter estimate xplot if group_id == `i' & !significant, msymbol(`symbol') mfcolor(white) mlcolor("`color'") msize(medsmall))"'
        local layer = `layer' + 1
    }
    local plots `"`plots' (scatter estimate xplot if normalized_reference, msymbol(O) mfcolor(white) mlcolor(gs7) msize(medsmall))"'
    local layer = `layer' + 1
    if "`language'" == "zh" {
        local xtitle "相对政策时点"
        local ytitle "估计效应（`level'% 置信区间）"
        local ref_label "归一化参考期"
    }
    else {
        local xtitle "Event time relative to intervention"
        local ytitle "Estimated effect (`level'% CI)"
        local ref_label "Normalized reference"
    }
    local legend_order `"`legend_order' `layer' "`ref_label'""'
    quietly summarize event_time if event_time < `policytime', meanonly
    local policy_line = cond(r(N) > 0, (r(max) + `policytime')/2, `policytime')
    local title_opt ""
    if `"`title'"' != "" local title_opt `"title("`title'")"'
    local ticks ""
    levelsof event_time, local(observed_times)
    foreach t of local observed_times {
        local ticks "`ticks' `t'"
    }
    local plots `"`plots'"'
    twoway `plots', ///
        yline(0, lcolor(gs8) lwidth(thin)) ///
        xline(`policy_line', lcolor(gs9) lpattern(dash) lwidth(thin)) ///
        xlabel(`ticks', nogrid) ylabel(, grid glcolor(gs15)) ///
        xtitle("`xtitle'") ytitle("`ytitle'") ///
        legend(order(`legend_order') position(6) rows(1) region(lcolor(none))) ///
        `title_opt' graphregion(color(white)) plotregion(color(white))
    graph export "`output'.png", replace width(2700)
    graph export "`output'.pdf", replace
    display as result "GROUPED_EVENT_STUDY_STATA_OK rows=`n_est' groups=`ng' significant=`n_sig'"
end
