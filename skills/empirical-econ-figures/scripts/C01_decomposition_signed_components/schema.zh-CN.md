# 输入约定

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV，包含 `bin_low,bin_high,relative_price,relative_productivity,relative_sales_per_worker`。每行对应一个劳动份额分箱。分箱**宽度**须严格为正、相等、连续，且分箱位于 `[0,1]` 内；允许 `bin_low=0`，至少需要三个分箱。分量和总量须为有限的有符号数值，采用相同的相对对数单位。每行须在 `2e-6` 容差内满足 `relative_sales_per_worker = relative_price + relative_productivity`，以容纳 CSV 六位小数舍入。

两个分量柱**在零轴上方和下方分别堆叠**。正分量从当前正向堆叠高度开始；负分量从当前负向深度开始。总量为代数和，分量异号时可落在正负两端之间。`_checked.csv` 提供 `price_low/price_high`、`prod_low/prod_high` 和原始总量，供数值核查。两分量均不是以100为分母的百分比，这也不是100%堆叠图。来源将相对实物劳动生产率定义为相对人均销售额减去相对价格；模板读取三个已保存值并验证恒等式，不估计它们。
