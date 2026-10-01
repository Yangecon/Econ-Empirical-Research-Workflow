# B06 · Merit-order marginal-cost curves

[English](recipe.md) · [中文](recipe.zh-CN.md)

`merit_order_cost_curves` · B06

Order units by marginal cost and use actual dispatched MWh as step widths, comparing two solved scenarios meeting the same total demand.

Classification: Heat rates/fuel prices, capacity data and assumptions including nuclear costs construct marginal costs; least-cost dispatch is solved under different spatial constraints. This is mechanism/optimization simulation, without claiming preference-parameter estimation.

Tags: Dispatch, Marginal costs, Counterfactual, Optimization, Calibrated inputs, Step plot

## Sources and scope

[Power Flows: Transmission Lines, Allocative Efficiency, and Corporate Profits (2025)](<https://doi.org/10.1257/aer.20240276>); Figure 1; PDF p.10

The original page image and PDF caption were checked; synthetic data demonstrate only the drawing method.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run Python in the selected template directory, writing to the research project:

```shell
python plot.py --input demo_dispatch.csv --output-prefix YOUR_PROJECT/figures/merit_order_cost_curves
```

Run Stata from this template directory with explicit arguments:

```stata
do plot.do "demo_dispatch.csv" "YOUR_PROJECT/figures/merit_order.png" 0
```

Python may add `--title "标题"`; change Stata’s last argument from 0 to 1 to enable the example title. Defaults omit the title and bottom notes. See schema.md for input fields and statistical boundaries.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Zero marginal cost, common demand, positive dispatch and every step endpoint were checked across Python/Stata. Capacity is not used as width, and dispatch optimization is not solved during plotting. Both languages were executed and the lead agent inspected the figures; the example is not a numerical paper replication.

Canonical figure name: `cost_merit_order_curves`
