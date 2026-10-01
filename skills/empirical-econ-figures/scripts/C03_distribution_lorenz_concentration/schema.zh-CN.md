# 输入与计算

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV，每个唯一且非空的 `id` 对应一条观测：`rank_value`、`weight`、`expenditure` 和 `fuel` 均为有限非负数。两个资源曲线的列ID和双语标签在 `plot.py` 中一起配置。至少一个权重须为正，每种资源的加权总量也须为正。允许资源为零及个别权重为零。示例为模拟数据；`weight` 列不声称是调查设计权重。

默认 `--mode concentration` 将两条资源曲线均按**同一** `rank_value` 升序排列。可选 `--mode lorenz` 则将每条资源曲线按**自身**资源值升序排列。两种模式的横坐标均为累计 `weight / total weight`，纵坐标均为累计 `weight × resource / total weighted resource`，均以百分比计。精确排序并列值先聚合再累计，避免虚构并列值内部顺序。包括原点 `(0,0)` 和终点 `(100,100)`；平等线为 `y=x`。集中曲线可穿过平等线，与非负资源按自身排序的洛伦兹曲线不同。`_points.csv` 附表记录全部绘图坐标及模式。

这是描述性的累计份额图，不推断处理效应、置信区间或不平等指数。
