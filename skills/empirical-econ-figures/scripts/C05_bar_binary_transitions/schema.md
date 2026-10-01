# Input and output schema

[English](schema.md) · [中文](schema.zh-CN.md)

Input is one CSV row for each **matched subject and task**, with `subject_id`, `task`, `first`, and `second`. The last two fields must be `0`, `1`, or blank. `subject_id` and `task` cannot be blank, and `(subject_id, task)` must be unique. The same subject can appear in several tasks. An observation with either status blank is excluded from that task's four-state denominator; `n_rows`, `n_complete`, `n_excluded_unpaired`, `n_missing_first`, `n_missing_second`, and `n_missing_both` are exported. `n_missing_first` and `n_missing_second` overlap when both values are missing, so their sum need not equal `n_excluded_unpaired`.

For each task, the mutually exclusive joint counts are `n_both_1` (`1,1`), `n_one_to_zero` (`1,0`), `n_zero_to_one` (`0,1`), and `n_both_0` (`0,0`). Each plotted `pct_*` is `100 × n_state / n_complete`; the four percentages sum to 100, including any zero components. The display stacks from bottom to top as `both_0`, `zero_to_one`, `one_to_zero`, `both_1`, matching the source's category order. Segment labels appear only when a segment is at least 8% tall.

The summary CSV separately reports `p_one_to_zero_given_start_1 = n_one_to_zero / n_start_1`, where `n_start_1 = n_both_1 + n_one_to_zero`, and `p_zero_to_one_given_start_0 = n_zero_to_one / n_start_0`, where `n_start_0 = n_both_0 + n_zero_to_one`. A rate with a zero starting group is **undefined** and exported as a blank CSV cell, never as zero. These conditional rates do not determine the 100% bar heights.

Four joint counts require actual matched observations or an explicitly supplied joint table. Two independent cross-sectional marginal rates cannot recover transitions. This implementation accepts paired subject-task rows only.
