# 数据与输出约定

[English](schema.md) · [中文](schema.zh-CN.md)

输入为 UTF-8 CSV，列 `panel`、`id`、`running`、`outcome` 与手工 RD 模板相同。`panel` 为 `outcome_a` 或 `outcome_b`；`id` 在面板内唯一；`running` 和 `outcome` 有限，结果位于 `[0,1]`。包版本固定断点为 0、面板带宽为 16 和 25，采用均匀核线性拟合，每侧十个等距箱。指定窗口外的值排除。

`<output-stem>_<panel>_rdplot_bins.csv` 含 `rdplot_id`（左负右正）、`rdplot_N`、箱边界、`rdplot_mean_bin`（命令绘制的箱中点）、`rdplot_mean_x`（原始运行变量样本均值）和 `rdplot_mean_y`（结果样本均值）。示例每面板 20 行。`<output-stem>_rdplot_fits.csv` 含 `panel`、`side`、`n`、`intercept_at_cutoff`、`slope`、`fit_x_min`、`fit_x_max`，来自 `rdplot` 的 `e(coef_l)` 与 `e(coef_r)` 矩阵。截距是各侧向零断点的描述性外推；拟合不是 RD 效应估计。
