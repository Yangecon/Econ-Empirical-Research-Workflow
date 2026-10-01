# Input CSV

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV, columns in any order: `panel`, `source`, `kind`, `median`, `low`, `high`. Numeric values must be finite and satisfy `low <= median <= high`. The label `median` is a distribution median for Bayesian rows and the **point estimate** for the ITT row; it does not make the ITT estimator a median. Each `(panel,source,kind)` triple must appear exactly once, 40 rows total with the supplied four-panel configuration.

Panels: `export_2019`, `variety_2019`, `export_2020`, `variety_2020`. Export panels measure changes in exporting probability/proportion (values on 0–1 scale); variety panels measure changes in number of product-country varieties. Each panel independently sets its horizontal range from input intervals.

Within **each panel**, rows are: `diffuse/posterior`; `literature`, `firm`, `policymaker`, and `academic` each with both `posterior` and `prior`; and `itt/itt`. Source prior and posterior rows are adjacent and interpreted as paired, but the code does not enforce a numerical updating relationship. `low/high` mean 95% **prior interval** for `kind=prior`, 95% **posterior interval** for `kind=posterior`, and 95% frequentist **confidence interval** for `kind=itt`. The interval type is determined solely by `kind`; the plotting code never derives it from endpoints.

The demo is a drawing fixture, not a numerical replication or data for substantive inference. Its numbers were generated independently for illustration.
