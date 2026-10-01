# C13 CSV 结构

[English](schema.md) · [中文](schema.zh-CN.md)

长格式 CSV 列为 `panel`、`series`、`duration`、`events`、`risk_set`。每个面板—序列—正整数持续期一行。`events` 与 `risk_set` 为整数计数，满足 `0 <= events <= risk_set` 且 `risk_set > 0`。适配器按持续期排序、拒绝重复键，并计算 `hazard = events / risk_set`。缺失持续期保留为空柱位置，绝不赋零或插值。绘图器将此比率乘100，用于百分比轴。

每行计数应采用一致的风险定义、事件窗口和人群。适配器无法验证上游队列进入、删失、竞争事件，或连续风险集是否来自有效纵向样本。使用真实数据时请记录这些选择。
