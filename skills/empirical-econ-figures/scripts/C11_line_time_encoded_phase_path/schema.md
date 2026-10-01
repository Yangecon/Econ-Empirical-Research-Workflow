# Input contract

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV columns (in any order): `year` (finite, strictly increasing integer in the demonstration), `x` and `y` (finite numeric values already on the intended display scale), `phase` (`early`, `middle`, `late` by default, or IDs from optional `--config`), and `year_label` (blank or the same integer year to annotate). At least two observations per configured phase are needed, six for the default three phases. Each phase needs contiguous observations; phases appear once in configured order. The line crossing a phase boundary takes the color of the **new** phase, and no point is sorted by `x`.

For the source-style chart, `x` is log population and `y` is log real wage. For other applications, supply config axis text and units. The source years run 1250–1860; synthetic `demo.csv` spans these years but contains invented values and phase intervals only to show the visual structure. Input coordinates can be irregularly spaced in time; no intermediate point is implied.

Optional JSON config: `phases` is a nonempty ordered array of unique `id`, `label_en`, `label_zh`, valid Matplotlib `color`, and optional `linestyle` from `-`, `--`, `:`, `-.`. `axes.en` and `axes.zh` each require nonblank `x`, `y`, and `title`. The Stata default remains fixed to three phases; custom config is Python-only. Keep sibling `../_shared/line_geometry.py` with this Python template.
