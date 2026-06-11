# Step 6 - Robustness Gauntlet in Stata

Goal: stress-test the identifying claim using the robustness tools that match the design's main threats.

## Default toolkit

- `bacondecomp`
- `honestdid`
- `boottest`
- `ritest`
- `rwolf`
- `psacalc`

## Canonical commands

```stata
bacondecomp outcome treatment

honestdid, pre(1/4) post(5/9) mvec(0(0.1)0.5)

reghdfe outcome treatment, absorb(unit_id year) vce(cluster unit_id)
boottest treatment

ritest treatment _b[treatment], reps(1000): ///
    reghdfe outcome treatment, absorb(unit_id year) vce(cluster unit_id)

rwolf treatment other_coef, indepvars(treatment other_coef) reps(500)

psacalc delta treatment, rmax(1.3)
```

## Common robustness dimensions

- alternative clustering
- alternative sample restrictions
- placebo outcomes
- placebo timing
- bandwidth grids for RD
- donor-pool or pre-period changes for SCM
- control-group variants for DID

## Hard rules

- Do not create a giant robustness appendix before the main estimate is stable.
- Use one robustness table as a bundle, not dozens of disconnected one-column tables.
- Match the robustness choice to the actual critique a referee would raise.
