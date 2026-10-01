# 输入约定

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV，每个唯一 `spec_id` 一行（至少五行）。必需：`spec_id`、有限数值 `result`，以及每个已配置 `opt_*` 选择项的明确 `0`/`1` 字段。选择项不得为空；零表示已知选择关闭，不表示“缺失”。当前 11 个字段为 `opt_baseline`、`opt_regional`、`opt_first_round`、`opt_exclude_municipalities`、`opt_pool_one_site`、`opt_logarithm`、`opt_gdp`、`opt_gdp_per_capita`、`opt_population`、`opt_fiscal_income`、`opt_fiscal_expenditure`。用于其他应用时，在两脚本中一起修改 ID 和有序双语标签；额外未配置的 `opt_*` 列会被拒绝。

可选 `ci_low` 与 `ci_high` 必须成对提供。每行要么均为空，要么均有限且满足 `ci_low <= result <= ci_high`；非空非数值文本被拒绝。不假定区间类型或覆盖率。脚本不计算区间或推断显著性。配置的显示范围当前为 −1 到 6，包含结果和区间；若数据超界必须修改，任何点均不得静默裁剪。Stata 将配置范围映射到上方绘图区，即使范围变化也与下方矩阵分离。

确定性排序按 `(result, spec_id)` 升序，并列用文本 ID 打破。`_ordered.csv` 包含排序后的 `rank`、`spec_id`、`result`、可选边界和所有选择项。上方结果曲线与下方矩阵每列使用同一秩。下方灰点表示明确的 `0`，黑点表示明确的 `1`。当前结果标签为“各实验的平均 t 统计量”，对应主要来源；更换估计对象时须修改。零线是描述性参考，不是临界值阈值。
