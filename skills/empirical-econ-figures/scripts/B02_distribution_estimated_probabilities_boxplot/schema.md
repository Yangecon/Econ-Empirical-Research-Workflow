# Raw-observation input contract

[English](schema.md) · [中文](schema.zh-CN.md)

One row per observed value in UTF-8 CSV. Required columns: `id` (unique nonblank row key), `group` (stable ID), `group_order` (consecutive positive integer starting at 1), `group_label_en`, `group_label_zh`, and finite numeric `value`. A group has exactly one order and one label per language. Source-model probabilities require values within `[0,1]`; the demo and default axes enforce that bound. For other measures, set `--ymin`/`--ymax` in Python or the final two arguments in Stata to contain all values and edit the axis labels near the top of both scripts. Input column order is irrelevant.

Both implementations calculate quartiles using Hyndman–Fan type 7: sorted values `x_(1)...x_(n)`, position `h = 1 + (n-1)p`, and linear interpolation between `floor(h)` and `ceil(h)` for `p = .25, .5, .75`. Ties remain individual observations. The lower and upper fences are Q1−1.5×IQR and Q3+1.5×IQR. Whiskers stop at the smallest and largest actual observations inside the inclusive fences; values outside are plotted as outliers. This is an explicitly chosen reproducible drawing convention, not a claim about the source paper's software defaults. Both scripts export their own group summary CSV for comparison.

The box plot is descriptive for supplied values. It does not estimate a model, create acuity deciles, or supply sampling uncertainty. If plotting estimates, upstream analysis must calculate those values and groups.
