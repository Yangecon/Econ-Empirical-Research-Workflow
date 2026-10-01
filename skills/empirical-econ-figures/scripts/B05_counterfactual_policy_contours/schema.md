# Input contract

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV, columns in any order:

| Column | Meaning |
|---|---|
| `fee_change_pct` | Fee percentage change on horizontal axis. |
| `denial_change_pct` | Relative percentage change in denial probability on vertical axis. |
| `acceptance_change` | Change in Medicaid acceptance from observed baseline, with 0 denoting no change. |
| `payment_change_usd` | Change in per-visit physician payments, **US dollars**. |

Every value must be finite. Grid coordinates must be unique. The Cartesian product of at least five unique x and five unique y coordinates must be completely observed; both languages sort numerical axes, regardless of input row order. `(0,0)` must occur exactly once, with both outcome surfaces zero there within `1e-9`. The acceptance surface must span zero, and the payment surface must span every configured contour level. The output `*_checked.csv` records the validated grid; `*_contours.csv` records rendered contour points/segments for geometry QA. Missing grid cells are rejected rather than interpolated. `demo.csv` is synthetic; it does not contain the paper's model outputs.
