# C14 CSV schema

[English](schema.md) · [中文](schema.zh-CN.md)

Individual-spell CSV columns: `panel`, `series`, `duration`, `event`; optional `id`. Each row is one spell. When `id` is supplied it must be nonblank and unique within panel-series; the same person may appear in separate comparison panels. `duration` is a finite nonnegative number in one documented unit, measured from cohort entry. `event` is 1 when the target event occurs at that duration and 0 for right censoring. At tied times, failures occur before censoring for the risk-set calculation. No left truncation, delayed entry, weights, or competing risks are supported; prepare or choose a different estimator if these matter.

Within group, at event time `t`, survival multiplies by `1 - d_t/n_t`, where `n_t` is the risk set immediately before `t`; censoring only removes spells from later risk sets. The curve starts at 1 at time zero and uses a right-continuous step, carrying the last value to the final observed time. Optional pointwise Greenwood standard error is `S(t) * sqrt(sum[d_j/(n_j(n_j-d_j))])`, clipped normal interval `S(t) +/- 1.96 SE` to [0,1]. An all-fail time yields survival 0 and CI [0,0].
