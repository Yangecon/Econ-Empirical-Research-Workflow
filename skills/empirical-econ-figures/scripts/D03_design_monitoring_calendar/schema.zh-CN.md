# 输入结构与检查

[English](schema.md) · [中文](schema.zh-CN.md)

必需命令行参数为 `--year` 与 `--output-prefix`。仅选择一种日程来源：带 `date,schedule` 列的 `--schedule` CSV，或 `--anchor-3` 和/或 `--anchor-6`。日程值须为 `3_day` 或 `6_day`；日期与锚点严格采用 ISO `YYYY-MM-DD`。锚点根据 `(date - anchor).days mod 3/6 == 0` 在指定年份内设置按日历天连续的周期，不推断星期周期。锚点对齐时，来源的每六日一次可为每三日一次的子集；对任意给定日期不预设此关系。

可选 `--observed` CSV 使用相同 `date,schedule` 列。实际观测日期可偏离计划，仍独立标记。重复日期—日程行、指定年份外日期、未知日程类型、无效日期、缺少日程来源，以及文件与锚点来源冲突均被拒绝。日历天依据标准公历，包括闰日。
