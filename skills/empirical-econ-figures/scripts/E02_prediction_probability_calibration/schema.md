# Input contract

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV with `id,true_prob,predicted_prob` in any column order; extra columns ignored. ID must be unique and nonblank. Both probabilities must be finite and in `[0,1]`. The regular sample is `true_prob<=0.99` (including exact 0.99); the independent tail is `true_prob>0.99` (including exact 1). Require at least 40 regular and four tail observations, so each of the 10 regular rank groups has observations. Each row represents one individual-level prediction, with equal weight. Pre-aggregated bin means cannot be used here.

The ten groups use sort `(true_prob,id)` and `bin = 1+floor(10*(rank−1)/N_regular)`. Ties are broken lexicographically by ID and can span two bins. Bin statistics are unweighted mean true probability, mean predicted probability, and type-7/linear-interpolation 25th and 75th percentiles of individual predictions. Bin 11 is the independent `>0.99` tail. The `_fit.csv` intercept and slope are OLS from all input observations. All values are probabilities, not percentage points. The IQR is descriptive dispersion, not estimation uncertainty.
