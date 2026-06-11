---
name: research-identification
description: Freeze the estimand, empirical design, assumptions, data requirements, robustness plan, and PAP for a selected empirical economics research question. Use when the user asks to choose between DID, IV, RD, shift-share, or another design, write an identification memo, define treatment and outcome, pre-specify robustness, or move a topic from idea stage into a frozen empirical design. Triggers: identification strategy, estimand, design memo, PAP, assumptions, robustness plan, freeze design, applied econometrics design.
---

# Research Identification

## Purpose

Use this skill after the topic gate returns `go`.

## Trigger phrases

- identification strategy
- freeze the design
- estimand
- assumptions
- robustness plan
- write PAP
- DID or IV or RD
- empirical design memo

## Folder

Use flat files under:

```text
notes/
```

Do not create:

```text
design/
notes/identification/
```

## Required outputs

```text
notes/identification.md
notes/estimand_registry.csv
notes/assumption_register.csv
notes/data_requirements.yaml
notes/robustness_plan.csv
notes/pap.md
notes/identification_status.json
```

## Required tasks

1. Define estimand.
2. Define unit of analysis.
3. Define treatment, shock, or exposure.
4. Define outcome variables.
5. Select design family.
6. State identifying variation.
7. Create assumption register.
8. Create data requirements file.
9. Pre-specify robustness, placebo, mechanism, and heterogeneity checks.
10. Draft PAP.
11. Set identification status.

## Status values

Use only:

```text
freeze
redesign
park
```

## Minimum checks by design family

### Difference-in-differences

- treatment timing
- comparison group
- no anticipation
- parallel-trends evidence
- event-study plan
- cohort heterogeneity plan
- alternative control groups

### Instrumental variables

- instrument relevance
- exclusion restriction
- first-stage plan
- weak-IV robust inference
- placebo outcomes
- complier interpretation

### Regression discontinuity

- running variable
- cutoff
- sorting threat
- density test
- covariate balance
- bandwidth grid
- donut check
- placebo cutoffs

### Shift-share

- shares
- shocks
- identifying variation
- leave-one-out construction
- shock-level inference
- placebo shocks

### Non-standard design

- exact identifying variation
- most likely confounders
- falsification checks
- alternative samples
- sensitivity analysis

## Handoff

If status is `freeze`, hand off to `research-empirics` or `empirical-analysis-stata` with:

- final estimand
- main specification
- data requirements
- robustness plan
- required outputs
