# Input and calculation

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV, one observation per unique nonblank `id`: `rank_value`, `weight`, `expenditure`, and `fuel` are finite nonnegative numbers. Column IDs and bilingual labels for the two resource curves are configured together in `plot.py`. At least one positive weight and a positive weighted total for each resource are required. Zero resources and zero individual weights are permitted. The example is synthetic; the `weight` column does not purport to be a survey design weight.

Default `--mode concentration` orders both resource curves by the **same** ascending `rank_value`. Optional `--mode lorenz` instead orders each resource curve by its **own** ascending resource value. For either mode, the x coordinate is cumulative `weight / total weight` and the y coordinate is cumulative `weight × resource / total weighted resource`, both in percent. Exact rank ties are aggregated before cumulation, avoiding a made-up within-tie ordering. An origin `(0,0)` and the endpoint `(100,100)` are included; the equality line is `y=x`. Concentration curves may cross the equality line, unlike nonnegative own-ranked Lorenz curves. The `_points.csv` sidecar records all plotted coordinates and mode.

This is a descriptive cumulative-share graphic. It does not infer treatment effects, confidence intervals, or inequality indices.
