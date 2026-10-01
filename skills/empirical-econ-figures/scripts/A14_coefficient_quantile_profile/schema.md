# Input contract

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV with exactly one row per numerical outcome quantile, in strictly increasing `quantile_percent` order. Required numeric, finite columns:

| Column | Meaning |
|---|---|
| `quantile_percent` | Percentile of the **outcome distribution**, strictly between 0 and 100, e.g. 10, 20, …, 90. |
| `estimate` | Precomputed coefficient at that unconditional quantile. |
| `ci_low` | Precomputed confidence-interval lower endpoint. |
| `ci_high` | Precomputed confidence-interval upper endpoint. |

The input must contain at least three unique quantiles; `ci_low <= estimate <= ci_high`. CSV columns may be in any order. Both languages preserve coefficient units. They do **not** calculate UQR, clustered standard errors, or interval coverage. The source figure reports 99% ZIP-clustered intervals, but another user's supplied interval level should be described outside this CSV; it is not inferred from the endpoints. The synthetic example has nine quantiles and illustrative intervals, not source values.
