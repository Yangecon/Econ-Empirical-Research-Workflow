# A20 · Paired accounting waterfalls

[English](recipe.md) · [中文](recipe.zh-CN.md)

`paired_accounting_waterfall` · A20

Account separately for two sets of monetary components, subtotals and totals in grouped panels, with a separately labeled dimensionless ratio.

Classification: MVPF combines direct audit revenue/costs, long-run deterrence revenue estimated using random audits and matched controls, and monetary/time costs from IRS surveys. This is sufficient-statistics-style welfare accounting based on empirical effects, not raw-data description or full structural-model output.

Tags: Welfare, Cost–benefit accounting, Waterfall, Decomposition, Sufficient statistics

## Sources and scope

[A Welfare Analysis of Tax Audits Across the Income Distribution (2025)](<https://doi.org/10.1093/qje/qjae037>); Figure VIII; PDF p.41

The original page image and PDF caption were checked; synthetic data demonstrate only the drawing method.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run inside the template directory:

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/waterfall.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/waterfall_stata.png" "en" "0"
```

Create the output parent directory before running Stata. Python `--title` or the last Stata argument `1` enables a title; `zh` switches to Chinese. The two group panels have their own y ranges. Compare axis ticks and printed amounts, not bar height alone across panels.

`component` adds a signed amount to the balance and draws a floating bar from old to new balance. `subtotal` and final `total` draw from zero to the balance, checking the supplied value without adding it again. Corresponding steps must agree across groups. The example adds an intermediate subtotal absent from the source.

In this source, MVPF is taxpayers’ willingness to pay to avoid an audit divided by government net revenue. Monetary amounts are dollars per additional $1 of audit expenditure; MVPF is dimensionless and labeled separately. The code requires positive net revenue in the denominator; rules for net cost or infinity from other policy MVPFs cannot be applied. The revenue ledger’s audit_cost is already negative and is added directly to two positive revenues. WTP and revenue model estimates are upstream; this example demonstrates accounting and drawing using synthetic numbers.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Eighteen accounting steps across two groups. English/Chinese Python/Stata versions were executed and inspected, including title switches. Floating-bar bounds, running balances and both group ratios have maximum cross-language difference 2.22e-16. Python rejects unbalanced totals, missing ledgers, wrong item assignment and sequence gaps; the Stata unbalanced-subtotal test returns r(9).

Canonical figure name: `welfare_accounting_waterfall`
