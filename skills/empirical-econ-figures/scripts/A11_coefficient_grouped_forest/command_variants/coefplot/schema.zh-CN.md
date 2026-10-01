# 输入约定

[English](schema.md) · [中文](schema.zh-CN.md)

完全使用[分组系数森林图 CSV 约定](<../../schema.zh-CN.md>)。必需列：`variant`、`panel`、`panel_order`、`term`、`term_order`、双语条目标签、`group`、`group_order`、`estimate` 和 `ci_low`/`ci_high`。若两个端点均缺失，使用与手工 Stata 版相同的 `estimate ± 1.96×se` 回退。仅缺一个端点会失败。CI 必须包含估计。每配置组须包含面板内全部条目；重复的面板—条目—组键失败。此包版本还要求 `term` 是合法 Stata 矩阵列名/系数名。

命令为每个组和面板构建一个 3×N 矩阵，行依次为 `(estimate, ci_low, ci_high)`，列名为按输入排序的条目 ID。作者文档中的 `coefplot matrix(B), ci((2 3))` 从第一行读取估计，从第二、三行读取准确区间端点，**不从方差矩阵重新计算 CI**。`order()` 和 `coeflabels()` 保留明确输入顺序及双语标签。包输出是另一种绘图实现，不重新估计论文系数。

`plot_coefplot.do` 参数为 `input.csv output.png lang variant orientation showtitle [package-dir]`。输入和输出路径必填。`lang` 为 `en`/`zh`；`variant` 为 `robustness`/`subgroup`；`orientation` 为 `horizontal`/`vertical`；`showtitle` 默认为 `0`，可设 `1`。多面板稳健性图保留面板副标题，单面板分组图无副标题。必要时保留轴和图例；默认无总标题或底部注释。PNG 和同名 PDF 写入输出路径。来源示例支持最多四个配置面板和两组；新研究须修改配置块。稳健性面板的 `preferred` 条目拆为偏移零的红色第二矩阵序列。
