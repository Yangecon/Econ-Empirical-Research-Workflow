# Input contract

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV, one row per `outcome × bandwidth_km` regression result. Required columns: `outcome,bandwidth_km,estimate,cluster_low,cluster_high,conley_low,conley_high`. The six configured outcome IDs and bilingual panel labels are in the scripts. Bandwidth is the **maximum allowed distance from the geographic border for that regression's sample**, in kilometers, not an individual observation's signed running variable. Each outcome has the same strictly increasing grid of at least three positive bandwidths, with one unique row per grid point. The synthetic demo has 61 points per outcome, matching the source's count of regressions but not its values.

All numeric fields must be finite. Both supplied intervals are 95% intervals for the **same saved estimate**: each low ≤ estimate ≤ high. Clustered and Conley intervals are different inference methods at the same nominal coverage; neither must contain the other. The scripts do not estimate coefficients, cluster-robust standard errors, Conley errors, or confidence limits. An observed zero or sign change is shown as provided; no significance flag is inferred. The figure omits the original's blue dashed benchmark because its exact meaning was not established from the caption. Users can add a benchmark only after specifying its value and meaning. Per-panel y scales reflect different outcomes; `unmet_needs` has a count difference while the other five are probability differences.

The paper's Conley calculation uses a spatial correlation cutoff distinct from this horizontal sample-bandwidth axis (2 km in its footnote). The drawing template never treats that Conley cutoff as an x value.
