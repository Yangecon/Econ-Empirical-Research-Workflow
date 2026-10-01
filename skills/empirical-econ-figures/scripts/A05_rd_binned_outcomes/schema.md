# Input and calculation contract

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV columns: `panel` (configured ID), `id` (unique within panel), `running` (numeric distance from zero cutoff), and `outcome` (numeric probability or binary outcome in `[0,1]`). Two configured panels are required. IDs and all numeric values must be nonmissing; running/outcome must be finite. Rows outside a panel's `[-bandwidth,+bandwidth]` window are counted as excluded and do not enter bins or fits. Zero belongs to the **right** side; `-bandwidth` is retained in the first left bin and `+bandwidth` in the last right bin.

Within each side, equal-width bin index is `min(floor((x+bandwidth)/(bandwidth/B)),B-1)+1` for `x<0`, and `min(floor(x/(bandwidth/B)),B-1)+1` for `x>=0`. B is configured bins per side. A boundary between bins enters the bin to its right. Every bin needs at least two observations. The plotted bin coordinate is the raw sample mean of x and outcome. Separately, each side fits `outcome = intercept + slope × running` by unweighted OLS on **all underlying in-window observations** for that side; both fitted line endpoints are checked against configured y limits. No SE, p-value, bandwidth selection, covariate adjustment, or RD validity test is computed.

The `_bins.csv`, `_fits.csv`, and `_sample.csv` outputs expose the calculations. The fitted intercept at x=0 is a descriptive side-specific extrapolation. The synthetic demo intentionally shows a larger level gap in Outcome A than Outcome B; it is not the paper's data or result.
