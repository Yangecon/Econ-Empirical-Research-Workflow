# C08 · 对数密度与尾部斜率比较

[English](recipe.md) · [中文](recipe.zh-CN.md)

`log_density_tail_comparison` · C08

给定密度或对数密度，展示正态基准与显式区间内的左右尾部斜率。

分类依据：原图与 PDF p11 已核对：自然对数密度与正态基准、左右明确区间上的 log-density 直线。读取正密度或显式 log-density 输入；零密度不可强加 epsilon。原图显示斜率 +1.40/-2.18，文中尾指数0.40/1.18，二者不是同一数字；模板仅报告拟合斜率，不能自动把它称为 Pareto 指数。

标签：对数密度, 尾部斜率, 正态分布基准

## 来源与范围

[What Do Data on Millions of U.S. Workers Reveal About Lifecycle Earnings Dynamics? (2021)](<https://doi.org/10.3982/ECTA14603>); Figure 6; PDF p.11

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在模板目录运行，下列输出目录应属于研究项目：

```shell
python plot.py demo_density.csv YOUR_PROJECT/figures/log_density.png --density-column density --left -4 -1.1 --right 1.1 3.5 --normal-sd 0.51
```

`--title "标题"` 显式开启标题，默认无标题/底部notes。字段、统计对象及显示限制见schema.md。

共享绘图依赖：保持本目录与相邻 `_shared/line_geometry.py` 的关系；复制到研究项目时同时复制共享模块。导入按脚本位置解析，可从不同工作目录运行。共享模块只画给定折线或右连续阶梯，归一化、累计份额、拟合区间、风险集与 Greenwood 区间仍由各适配器处理。


将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

已核有限网格示例密度积分为1、左右精确斜率+1.40/-2.18及零密度/重复x拒绝。对数密度斜率不自动等于Pareto指数；用户输入不自动归一化，正态基准仅显示均值±4SD。 Python已实跑，主agent已视检；绘图示例不等于原论文数值复现。 续作共享折线／阶梯几何后，从不同工作目录重跑，默认导出坐标与原验收结果在1e-10容差内一致；统计适配保留，F38条形不变。

统一图名：`distribution_log_density_tails`
