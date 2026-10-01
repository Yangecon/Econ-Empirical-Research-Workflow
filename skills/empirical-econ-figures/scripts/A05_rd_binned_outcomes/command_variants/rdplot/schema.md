# Data and output contract

[English](schema.md) · [中文](schema.zh-CN.md)

Input: UTF-8 CSV with `panel`, `id`, `running`, `outcome`, matching the manual RD template. `panel` is `outcome_a` or `outcome_b`; `id` is unique within panel; `running` and `outcome` are finite; outcomes are in `[0,1]`. The package variant fixes cutoff 0, panel bandwidths 16 and 25, a linear uniform-kernel fit, and ten evenly spaced bins per side. Values outside the specified windows are excluded.

`<output-stem>_<panel>_rdplot_bins.csv` contains `rdplot_id` (negative left, positive right), `rdplot_N`, bin bounds, `rdplot_mean_bin` (bin midpoint plotted by the command), `rdplot_mean_x` (raw sample mean running value), and `rdplot_mean_y` (sample mean outcome). There are 20 rows per panel in the demo. `<output-stem>_rdplot_fits.csv` has `panel`, `side`, `n`, `intercept_at_cutoff`, `slope`, `fit_x_min`, and `fit_x_max`, taken from `rdplot`'s `e(coef_l)` and `e(coef_r)` matrices. The intercept is a descriptive side-specific extrapolation to cutoff zero; the fit is not an RD effect estimate.
