# Step 7 - Mechanism and Heterogeneity in Stata

Goal: extend the baseline result into economically interpretable channels and subgroup patterns.

## Common tasks

- mechanism outcomes
- subgroup splits
- interaction models
- triple differences
- dynamic treatment effects
- margins-based interpretation

## Canonical commands

```stata
foreach y in invest employment productivity {
    eststo: reghdfe `y' treatment controls, ///
        absorb(unit_id year) vce(cluster unit_id)
}

reghdfe outcome c.treatment##i.female controls, ///
    absorb(unit_id year) vce(cluster unit_id)

margins female, dydx(treatment)
marginsplot

binscatter outcome treatment, by(region)
```

## Interpretation rules

- Mechanisms should connect to an economic story already implied by the paper.
- Heterogeneity should specify the reference group and interaction interpretation.
- Do not report noisy subgroup estimates without a coherent reason to care.

## Common outputs

- mechanism table
- heterogeneity table
- interaction plot
- subgroup binscatter or margins plot
