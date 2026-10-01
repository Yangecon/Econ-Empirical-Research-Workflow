# 给定零假设抽取的输入与尾部规则

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV，每个给定零假设抽取一行。必需列：`panel`（稳定 ID）、`panel_order`（1–4 连续整数）、`panel_label_en`、`panel_label_zh`、`draw_id`（面板内唯一）、有限数值 `null_stat`、有限数值 `observed_stat`（面板内常量）。面板 ID、顺序、标签和观察统计量须一致；列顺序无关。示例统计量是份额，因此默认绘图范围为 0–1。其他统计量须在两命令中设置范围和箱宽。箱宽须恰好整除绘图范围。各直方柱高度为箱计数除以该面板给定抽取总数。

`--tail right` 计数 `null_stat >= observed_stat`；`left` 计数 `<=`。双侧检验须显式给定零假设中心 `c`，计数 `abs(null_stat-c) >= abs(observed_stat-c)`。Stata 参数用 `right`、`left` 或 `two-sided`，第五位置为 `nullcenter`。相等也计入极端事件。给定 `B` 个零假设抽取和 `E` 个极端事件，两程序在输出前缀 `_results.csv` 中报告有限置换 Monte Carlo 修正 `(E+1)/(B+1)`。给定抽取被视为不包含实际观察到的分配。不用正态近似。

程序**绘制并计数既有抽取**，不构建分配机制、生成有效置换、验证可交换性，也不证明该尾部/中心对应研究假设。上游研究须论证随机化设计、统计量、条件集和尾部选择。原图分别对处理市场和控制市场做随机化检验；模拟示例采用通用设置，不声称复现来源数据或数值。
