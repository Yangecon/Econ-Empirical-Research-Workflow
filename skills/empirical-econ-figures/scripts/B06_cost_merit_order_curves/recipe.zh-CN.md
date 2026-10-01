# B06 · 按成本排序的调度边际成本曲线

[English](recipe.md) · [中文](recipe.zh-CN.md)

`merit_order_cost_curves` · B06

按边际成本排序，阶梯宽度使用实际调度 MWh；比较满足相同总需求的两套已求解场景。

分类依据：机组热耗/燃料价格构造边际成本、容量数据和核电成本等假设，解最小成本调度并改变空间约束。属于机制/优化模拟，不声称是偏好参数估计。

标签：调度, 边际成本, 反事实, 优化, 校准输入, 阶梯图

## 来源与范围

[Power Flows: Transmission Lines, Allocative Efficiency, and Corporate Profits (2025)](<https://doi.org/10.1257/aer.20240276>); Figure 1; PDF p.10

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在所选模板目录运行 Python；输出到研究项目：

```shell
python plot.py --input demo_dispatch.csv --output-prefix YOUR_PROJECT/figures/merit_order_cost_curves
```

Stata 从本模板目录以显式参数运行：

```stata
do plot.do "demo_dispatch.csv" "YOUR_PROJECT/figures/merit_order.png" 0
```

Python 可加 `--title "标题"`；Stata 最后参数从0改1可开启示例标题。默认无标题和底部 notes。输入字段及统计边界见 schema.md。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

已核零边际成本、共同需求、正调度量以及每个阶梯端点的 Python/Stata 一致性；不把容量当宽度，不在绘图阶段求解调度优化。 两语言实跑和主 agent 成图视检已通过；示例不等于原论文数值复现。

统一图名：`cost_merit_order_curves`
