# Step 4 - Diagnostic Tests in Stata

Goal: run the classical diagnostics that establish whether the preferred estimator is being used on data that roughly meet its assumptions, and record design-specific red flags before claiming results.

## Use this reference for

- normality and distribution checks
- heteroskedasticity tests
- serial-correlation checks
- unit-root checks when relevant
- overidentification and first-stage diagnostics
- panel-model comparison tests

## Canonical commands

```stata
summarize outcome treatment, detail
sktest outcome
swilk outcome

reg outcome treatment controls
hettest
estat imtest, white
vif

xtset unit_id year
xtserial outcome treatment controls
xttest3

dfuller outcome, lags(1)

ivreg2 outcome controls (treatment = z), cluster(unit_id) first
estat overid
estat endogenous
```

## Design-specific reminders

- OLS and HDFE: check leverage, heteroskedasticity, and clustering choice.
- IV: read the first-stage F, Kleibergen-Paap style weak-IV evidence, and overidentification results if applicable.
- DID: pre-trend and event-study diagnostics matter more than generic normality tests.
- RD: density and bandwidth sensitivity are first-order diagnostics.

## Hard rules

- Diagnostics do not replace design logic.
- Do not run every test mechanically; prioritize the ones that speak to the identifying threat.
- Keep a record of failed diagnostics and how the specification responds.
