# 输入约定

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV，列顺序任意，包含 `panel,kind,x,y,count,reference_label`。本版要求 `panel` ID 为 `r1` 和 `r200`，每个面板至少有一个正频数气泡。`kind=bubble` 行要求 `count` 为非负整数（可为零）、参照标签为空，且 `(panel,x,y)` 唯一。`kind=benchmark` 行要求 count 为空，并提供已配置的 `reference_label` ID（`bayesian` 或 `perfect_brn`）；两份脚本均将这些ID映射为英文或中文显示文字。按来源百分比尺度，坐标须有限且位于0–100。使用其他尺度时须配置两份脚本的轴标签与边界。未出现的组合无需行；显式零计数允许且保留，但不绘制。

一个气泡表示给定 `x,y` 组合的**联合人数**。来源先将个体信念舍入至3的倍数再计数；该步骤属于上游处理。`x` 是负信号条件下的信念，`y` 是正信号条件下的信念，均为百分比。两个面板分别表示第1轮与第200轮。基准行是用于解释的参照坐标；模拟值不视为论文估计值。

计数为 `n` 时，气泡直径为 `27 sqrt(n/max_count)` 打印点，因此其面积除以最大气泡面积为 `n/max_count`。`max_count` 在全部面板中共同计算。Stata 输出八位小数直径，仅引入可忽略的舍入误差。核对 CSV 包含 `bubble_area_ratio` 供审计；基准行该字段为空。
