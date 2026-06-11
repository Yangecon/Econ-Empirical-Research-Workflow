# Step 5 - Baseline Modeling in Stata

Goal: estimate the main specification with the estimator that matches the frozen identification design.

## Estimator menu

- OLS or HDFE baseline: `reg`, `xtreg`, `reghdfe`
- IV: `ivreg2`, `ivregress`, `ivreghdfe`
- DID: `reghdfe`, `csdid`, `eventstudyinteract`, `did_imputation`, `sdid`
- RD: `rdrobust`
- SCM: `synth`, `synth_runner`
- matching and weighting: `psmatch2`, `teffects`, `ebalance`

## Canonical commands

```stata
reghdfe outcome treatment controls, ///
    absorb(unit_id year) vce(cluster unit_id)

ivreg2 outcome controls (treatment = instrument), ///
    cluster(unit_id) first

ivreghdfe outcome controls (treatment = instrument), ///
    absorb(unit_id year) cluster(unit_id) first

csdid outcome controls, ///
    ivar(unit_id) time(year) gvar(first_treat_year) method(dripw)

eventstudyinteract outcome ib4.rel_p, ///
    cohort(first_treat_year) control_cohort(never_treated) ///
    absorb(i.unit_id i.year) vce(cluster unit_id)

did_imputation outcome unit_id year first_treat_year, ///
    allhorizons pretrend(5) autosample

rdrobust outcome running_var, c(0)

synth outcome controls, trunit(10) trperiod(2010)

teffects psmatch (outcome) (treatment controls), atet
```

## Modeling rules

- Match the estimator to the design memo, not to what is fashionable.
- The main specification should be easy to point to in the paper.
- Keep the preferred clustering choice stable across nearby columns unless a robustness table changes it intentionally.
- Save the core model objects with `eststo` so the reporting layer is painless.
