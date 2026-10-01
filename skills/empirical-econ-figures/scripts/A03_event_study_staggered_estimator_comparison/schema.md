# Six-estimator event-study estimate table

[English](schema.md) · [中文](schema.zh-CN.md)

The UTF-8 CSV has one row per `estimator` × integer `event_time`, with unique keys. Rows may be absent when a horizon is unsupported; absent horizons must never be supplied as zero effects. The demo table contains six estimator labels exactly as listed below and event times −5 through +5 overall. The `jwdid` series contains only 0 through +5. A different application should review each estimator's horizon meaning and extraction before using the renderer.

| Column | Meaning |
| --- | --- |
| `estimator` | One of `TWFE OLS`, `Sun-Abraham`, `Callaway-Santanna`, `dCDH dynamic`, `BJS imputation`, `Wooldridge jwdid`. The labels map to distinct colors and shapes. |
| `event_time` | Signed integer period relative to adoption, sorted numerically for plotting. |
| `b` | Command-exported estimate or an explicitly normalized zero reference. |
| `se` | Command-exported standard error; blank for a normalized reference. |
| `ci_low`, `ci_high` | Pointwise 95% normal-approximation endpoints `b ± invnormal(.975) × se`; blank for a normalized reference. |
| `status` | `estimated`, `pretrend_test`, `placebo_test`, or `normalized_reference`. A reference row is plotted hollow without an interval and is never counted as an estimate. |
| `sample_n` | `e(N)` returned by the estimator, if present. Missing means the command did not return an accessible `e(N)` in this extraction; it is not zero. |
| `command` | Stata command that produced the source estimate. |
| `inference` | Unit-cluster normal approximation or unit-cluster bootstrap normal approximation used for this display. |

The six-series demonstration has two imposed −1 reference rows, for TWFE OLS and Sun–Abraham. BJS `pre1`, Callaway–Sant’Anna `Tm1`, and de Chaisemartin–d’Haultfoeuille `Placebo_1` are tests or contrasts at −1, not normalized zeros. The `jwdid` default uses not-yet-treated controls and reports post-treatment event ATTs only; the synthetic panel has no never-treated cohort, so this series has no preperiod values or −1 marker. Its `estat event, window(0 5)` outputs are extracted from `r(b)` and `r(V)`. The full six-by-six variance matrix is saved in `jwdid_event_covariance.csv` with rows and columns ordered by events 0 through +5. The TWFE regression includes a `K <= -6` nuisance bin and estimates leads −5 through −2; Sun–Abraham includes earlier lead dummies through −14 but plots only −5 through −2. This comparison does not assume identical cohort support, samples, weights, or estimands across methods. The [estimator support table](estimator_support.csv) documents what is actually reported.

Filled markers denote intervals excluding zero. Hollow markers denote intervals including zero or normalized reference rows. The legend identifies estimator by color and shape; the caption must explain the reference, pretrend statuses, pointwise interval rule, clustering, outcome, unit, time period, and sample. The plot has no title or bottom notes by default; the manual Stata program and Python renderer accept an optional title.


The normalized reference at event time −1 is displayed as a hollow circle with no confidence interval. It is not an estimated effect and is excluded from pre/post averages.
