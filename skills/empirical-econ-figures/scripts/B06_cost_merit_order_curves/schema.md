# Input and drawing contract

[English](schema.md) · [中文](schema.zh-CN.md)

CSV: `scenario,unit_id,marginal_cost,dispatched_mwh`. Exactly two nonblank scenario names, unique unit ID per scenario, finite nonnegative marginal cost and strictly positive **dispatched** MWh. The sum of dispatched MWh must match across scenarios within numerical tolerance. A unit with zero dispatch contributes no width and should be omitted. A cost of zero is allowed. Units are ordered by marginal cost, then unit ID for ties; each step runs from cumulative dispatched quantity before that unit to after it.

Checked steps CSV: original columns plus `x_start,x_end`; coordinate CSV: two points per unit, `endpoint=0/1`, `x_mwh`, `marginal_cost`. Equal demand is a comparability rule for this figure, not an optimization constraint imposed by the plotter. No capacity or dispatch decision is inferred from unit IDs or cost sorting.
