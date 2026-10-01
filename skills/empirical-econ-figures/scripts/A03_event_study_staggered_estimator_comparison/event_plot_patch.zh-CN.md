# 本地 `event_plot` 补丁

[English](event_plot_patch.md) · [中文](event_plot_patch.zh-CN.md)

运行时副本 `packages/e/event_plot.ado` 基于2021年6月1日的方法作者命令，仅有两处局部修改。未修改的 SSC 副本、当前 GitHub 副本、帮助文件及 GPL-3.0 许可保存在同一目录。SHA-256 与来源位置记录在 `dependency_manifest.json`。

1. 在两处后备变量名前缀比较中为 `e(cmd)` 加引号。仅有系数/方差矩阵而无活动估计结果时，未修改的表达式可能引发类型不匹配错误。
2. 在滞后数量检查中，将未定义的裸 `coef` 宏替换为带模型索引的 `coef` 宏。这修正以矩阵提供的序列的有效滞后数量。

`plot_event_plot.do` 仅用此命令进行 `savecoef noplot` 提取，随后以原生 `twoway` 绘制提取结果，使实心/空心符号可以表示同一估计器内的显著性。补丁不改变提取系数值或方差公式。已执行的验证将每个提取系数和区间与审计后的 Stata 表逐一比较。
