# Input and transformations

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 long CSV with required `date`, `series`, and `value`. Dates are exact ISO `YYYY-MM-DD`, with January 1 for `--frequency annual` (default) or the first day of month for `--frequency monthly`. One row per series-date; series IDs must exactly match the default `SERIES` configuration or all IDs in optional `--config` JSON. `value` must be finite and nonnegative. Each series needs at least two observed periods. The demo values are **already constructed ratios** (invented annual counts per sales unit). The plotting code does not calculate or infer the original denominator, annual sales sample, or sample conditioning.

By default the plot displays `value` unchanged. `--normalize-base YYYY-MM-DD` is an explicit optional transform: for each series separately, `index_t = 100 × value_t / value_base`; each series must have a strictly positive observed value at that same requested base date. No first-available-period substitution is made. The `_plotted.csv` sidecar preserves both input `value` and displayed `plot_value`.

The x axis uses actual calendar dates, so spacing follows elapsed time. Missing annual or monthly periods within each observed span are inserted as blank values, which **break the line** instead of interpolating over gaps. No outcome estimation, uncertainty interval, or causal contrast is implied.

Optional JSON config: `series` is a nonempty array of unique `id`, `label_en`, `label_zh`, valid Matplotlib `color`, and `linestyle` from `-`, `--`, `:`, `-.`. `axes.en` and `axes.zh` each require nonblank `x_annual`, `x_monthly`, `y_raw_annual`, `y_raw_monthly`, `y_index`, and `title`. Configured IDs affect labels and drawing order, not the calendar or normalization rules. Keep sibling `../_shared/line_geometry.py` with this Python template.
