# Step 2 - Variable Construction in Stata

Goal: construct the analysis variables that the identification design actually needs, with transparent transformations and reusable code.

## Use this reference for

- `gen` and `egen`
- winsorization
- quantile bins
- panel lags and leads
- interactions
- treatment timing variables

## Default checklist

1. Define the treatment, timing, and outcome variables exactly as written in the identification memo.
2. Build control variables in reproducible blocks.
3. Create missingness flags when imputing.
4. Winsorize only when justified and document the rule.
5. Construct event-time or cohort variables for DID.
6. Use `xtset` before lags and leads.

## Canonical commands

```stata
gen treated = exposure > 0 if !missing(exposure)
gen post = year >= policy_year if !missing(policy_year)
gen treat_post = treated * post

egen ln_assets = ln(assets)
gen log_wage = ln(wage)

winsor2 wage assets, cuts(1 99) replace
xtile size_decile = firm_size, nq(10)

xtset unit_id year
gen L1_outcome = L.outcome
gen F1_outcome = F.outcome
gen D_outcome  = D.outcome

gen rel_time = year - first_treat_year
replace rel_time = -5 if rel_time < -5 & !missing(rel_time)
replace rel_time = 5 if rel_time > 5 & !missing(rel_time)
```

## Hard rules

- Do not invent transformed variables that are not tied to the identification story.
- Do not winsorize by habit; state why.
- Do not create interactions without deciding the reference group and interpretation.
- Keep naming stable enough that tables and plots can reuse the same variables.

## Common outputs

- treatment timing variables
- event-time bins
- transformed outcomes
- control blocks ready for Step 5
