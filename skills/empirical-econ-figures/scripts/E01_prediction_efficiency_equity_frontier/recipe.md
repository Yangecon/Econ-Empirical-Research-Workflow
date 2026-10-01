# E01 · Efficiency–equity policy paths

[English](recipe.md) · [中文](recipe.zh-CN.md)

`efficiency_equity_frontier` · E01

Compare efficiency and group disparities as a policy parameter varies, showing supplied uncertainty intervals, operating points and the status quo.

Classification: The NRP sample is ranked by actual underreporting or random-forest predictions; detected amounts and disparities are recomputed as audit rates vary. This evaluates algorithm performance on fixed data without solving behavioral responses or an economic structural equilibrium.

Tags: Policy comparison, Efficiency–equity, Operating points, Algorithm evaluation, Random forest, Policy ranking, Line plot

## Sources and scope

[Measuring and Mitigating Racial Disparities in Tax Audits (2025)](<https://doi.org/10.1093/qje/qjae027>); Figure VIII; PDF p.35

The original page image and PDF caption were checked; synthetic data demonstrate only the drawing method.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run inside this template directory:

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/frontier.png --lang en
```

In Stata:

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/frontier_stata.png" "en" "0"
```

Python `--title` or the last Stata argument `1` enables a title; `zh` switches to Chinese. Update algorithm IDs, text and axis units at the top of both scripts together. Black dots are input-specified operating points, not significance coding. The red cross and reference lines come from the unique status-quo row.

Connections follow `policy_rate`. This simple template requires each algorithm’s efficiency to increase strictly with that parameter and thus **supports only monotone-efficiency paths**. Some original paths locally turn back; complete reproduction of those segments cannot be claimed. Disparities may be negative. Supplied CIs directly form vertical bands; no new bootstrap or x uncertainty is calculated. Both CI endpoints must be blank for the status-quo row.

“Frontier” in the family name denotes policy-path comparison, not calculation of Pareto frontiers, optimal policies or dominance. The source x axis is annualized detected underreporting in millions of dollars and y is a probability disparity in percentage points. Annualization, weights, audit ranking and 95% bootstrap intervals are all upstream. The demonstration uses only synthetic quantities and supplied intervals.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Sixty-nine synthetic rows: four 17-point paths and one status-quo point. English/Chinese Python/Stata versions were executed and inspected; maximum analytical numerical difference is 8.89e-16. A malformed Stata status-quo CI with only one endpoint returns r(9) before export. Both languages check complete intervals, unique operating points and path order.

Canonical figure name: `prediction_efficiency_equity_frontier`
