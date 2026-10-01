# 输入结构与解释

[English](schema.md) · [中文](schema.zh-CN.md)

输入 CSV 每行对应一个国家或类别，行顺序严格为预期的**自上而下顺序**。必需列为 `category`、`actual_pct` 与 `perceived_pct`。`category_zh` 为可选且完整的中文标签；不提供时，中文图直接使用 `category`。类别须唯一且非空。

全部数值采用**0–100尺度的百分比单位**，不是比例小数：`12` 表示12%，而非0.12。实际值与感知值须有限且位于此范围。感知值可低于、等于或高于实际值。输出增加 `gap_pct_points = perceived_pct - actual_pct`；负值表示低估。脚本绘制两个给定值及其连接线，绝不按任何一个值排序。

可选置信区间列为 `perceived_ci_low_pct` 与 `perceived_ci_high_pct`。须**两列均提供且每行均有限，或两列均不提供**。这些列应为外部计算的95%置信限；代码能检查边界及是否包含均值，但不能验证覆盖水平。部分缺失区间或不包含感知均值的区间会被拒绝。阴影区间**仅适用于感知均值**；实际值不画区间。脚本不推导标准误，也不重新估计区间。

随附 [`figures/demo_values.csv`](figures/demo_values.csv) 含六个虚构例子。Sweden 的差值为负、France 的差值为零，用于检查连线方向及符号重叠。所有数值均非来源论文估计。
