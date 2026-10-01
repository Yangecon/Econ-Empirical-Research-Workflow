# 输入与输出结构

[English](schema.md) · [中文](schema.zh-CN.md)

输入 CSV 的每行对应一个**匹配受试者与任务**，包含 `subject_id`、`task`、`first` 和 `second`。后两个字段只能为 `0`、`1` 或空值。`subject_id` 和 `task` 不得为空，且 `(subject_id, task)` 必须唯一。同一受试者可以出现在多个任务中。任一状态为空的观测从该任务的四状态分母中剔除；输出 `n_rows`、`n_complete`、`n_excluded_unpaired`、`n_missing_first`、`n_missing_second` 和 `n_missing_both`。两值均缺失时，`n_missing_first` 与 `n_missing_second` 重叠，因此其和不一定等于 `n_excluded_unpaired`。

每个任务的互斥联合计数为 `n_both_1`（`1,1`）、`n_one_to_zero`（`1,0`）、`n_zero_to_one`（`0,1`）和 `n_both_0`（`0,0`）。各绘图 `pct_*` 为 `100 × n_state / n_complete`；包括零分量在内的四个百分比之和为100。自下而上的堆叠顺序为 `both_0`、`zero_to_one`、`one_to_zero`、`both_1`，与来源类别顺序一致。只有高度至少8%的区段显示标签。

摘要 CSV 另行报告 `p_one_to_zero_given_start_1 = n_one_to_zero / n_start_1`，其中 `n_start_1 = n_both_1 + n_one_to_zero`；以及 `p_zero_to_one_given_start_0 = n_zero_to_one / n_start_0`，其中 `n_start_0 = n_both_0 + n_zero_to_one`。起始组为零时，该比率**未定义**，输出为空白 CSV 单元格，绝不记为零。这些条件比率不决定100%柱的高度。

四个联合计数需要真实匹配观测或明确提供的联合表。两个独立横截面的边际比例无法恢复状态转移。本实现仅接受配对受试者—任务行。
