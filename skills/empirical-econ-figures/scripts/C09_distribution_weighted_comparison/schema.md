# Input schema and checks

[English](schema.md) · [中文](schema.zh-CN.md)

Long establishment CSV: `year`, `industry`, `establishment_id`, `labor_share`, `value_added`. One unique establishment within each industry-year. Labor share must be finite and nonnegative; values above 1 are allowed, as in the source figure. Value added must be finite and nonnegative; individual zeros are allowed, but **each included industry-year total must be strictly positive**. Negative VA or a zero-total industry would make the annual industry weight or within-industry VA distribution inappropriate, so the adapter rejects it. Missing and duplicate identifiers are rejected.

Common bins default to `[0, 1.4]` at width `.1`, with an observation exactly on 1.4 included in the last bin. `--bin-min`, `--bin-max` and `--bin-width` jointly change all panels. Out-of-range labor shares are rejected rather than dropped. Each within-industry distribution sums to 1 and industry-year weights sum to 1 within year. Both displayed distributions consequently sum to 1 within year. The output has one bin row per year.
