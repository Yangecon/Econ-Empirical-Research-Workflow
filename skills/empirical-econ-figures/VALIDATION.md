# Validation scope

[English](VALIDATION.md) · [中文](VALIDATION.zh-CN.md)

The source library contains 50 accepted drawing variants organized into 40 drawing targets: 30 Python + Stata, 19 Python-only, and 1 Stata-only. The accepted source was tested with Python 3.12.14 and Stata 19. Released scripts and inputs match their accepted source versions. Later numerical revisions are explicitly recorded in each recipe and its validation evidence; packaging checks do not replace estimator validation. Raw machine logs, environments, caches and full source papers are not shipped. The release is limited to accepted implementations. All candidate suggestions were declined by user decision; candidate suggestions and previews are excluded, with none pending.


Numerical checks and limitations are retained in each recipe; gallery items additionally carry sanitized JSON/CSV validation records. RELEASE_CHECKS.json records this export's link, hash, path and smoke checks. SHA256SUMS.txt records all released files except itself. The complete original work archive remains outside these repositories.

The shared line family preserved default pixels and checked coordinates. Its 14 published entrypoints passed import/help checks, and custom examples were executed from both skill and gallery. A10 passed fresh-output-directory checks with unchanged bins and fit. Native and package Stata versions were executed in the source environment; a clean-room Stata installation has not been rebuilt for this export.

A03 estimates six methods (including jwdid) in Stata and plots a common exported table in both languages; Python redraws actual exported estimates rather than independently estimating these models. A04 estimates simulated panel data and passes the full event-study covariance to HonestDiD for relative-magnitude and smoothness sensitivity intervals; Stata draws both. event_plot uses a documented patch and native twoway rendering. C17 uses real modern boundaries with synthetic values, not the original historical geography. A18 renders supplied bootstrap-region membership; it does not implement the source paper's bootstrap algorithm.

Defaults omit the overall title and bottom notes; panel labels and axes remain. Optional title switches are documented by template. Source-reference screenshots retain their original appearance.


English-only default update: four Python plotting entrypoints and seven demo generators were executed in isolated output directories; numerical outputs match the accepted references byte for byte. Two Stata package-demo runners were statically checked only: the Stata MCP security guard rejected the wrapper execution. Their underlying plotting routines and accepted English PNGs are unchanged. See [English output checks](ENGLISH_OUTPUT_CHECKS.json).


A01 was revised to actual estimates from a 980-row, 70-unit balanced common-timing panel. Python and Stata independently estimate static DID and the event study. The normalized reference zero enters the six-period pre denominator, and the eight-period post mean minus pre mean agrees with static DID within 1e-12. Unit-cluster CR0 covariance and normal intervals are matched explicitly; an independent unit-change calculation also agrees. This identity is scoped to the documented design.
