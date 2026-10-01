# Local `event_plot` patch

[English](event_plot_patch.md) · [中文](event_plot_patch.zh-CN.md)

The runtime copy `packages/e/event_plot.ado` is the June 1, 2021 method-author command with two narrow edits. The unmodified SSC copy, current GitHub copy, help, and GPL-3.0 license are preserved in the same directory. SHA-256 values and source locations are recorded in `dependency_manifest.json`.

1. Quote `e(cmd)` in two fallback-stub comparisons. With coefficient/variance matrices and no active estimation results, the unmodified expression can raise a type-mismatch error.
2. In the lag count check, replace the undefined bare `coef` macro with the model-indexed `coef` macro. This fixes the valid-lag count for matrix-supplied series.

`plot_event_plot.do` uses this command only for `savecoef noplot` extraction and renders the extracted estimates with native `twoway`, so filled versus hollow markers can represent significance within each estimator. The patch does not change the extracted coefficient values or variance formula. The executed validation compares every extracted coefficient and interval with the audited Stata table.
