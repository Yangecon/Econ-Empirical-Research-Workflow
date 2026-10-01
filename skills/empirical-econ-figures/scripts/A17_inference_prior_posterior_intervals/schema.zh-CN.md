# 输入 CSV

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV，列可任意排序：`panel`、`source`、`kind`、`median`、`low`、`high`。数值必须有限并满足 `low <= median <= high`。`median` 对 Bayesian 行表示分布中位数，对 ITT 行表示**点估计**，不把 ITT 估计器变为中位数。每个 `(panel,source,kind)` 三元组必须恰出现一次；给定四面板配置共 40 行。

面板：`export_2019`、`variety_2019`、`export_2020`、`variety_2020`。出口面板衡量出口概率/比例变化（0–1 尺度）；种类面板衡量产品—国家种类数量变化。每个面板根据输入区间独立设置横轴范围。

**每个面板**包含：`diffuse/posterior`；`literature`、`firm`、`policymaker`、`academic` 各有 `posterior` 与 `prior`；以及 `itt/itt`。同一来源的先验与后验行相邻并按配对解释，但代码不强制数值更新关系。`low/high` 在 `kind=prior` 时为 95% **先验区间**，`kind=posterior` 时为 95% **后验区间**，`kind=itt` 时为 95% 频率派**置信区间**。区间类型完全由 `kind` 决定，绘图代码绝不从端点推导。

示例是绘图测试数据，不是数值复现，也不是实质推断数据。数值为演示独立生成。
