# C14 · Kaplan–Meier 生存曲线面板

[English](recipe.md) · [中文](recipe.zh-CN.md)

`kaplan_meier_survival_panels` · C14

从持续时间与右删失状态计算 Kaplan–Meier 阶梯生存曲线，可显示点态 Greenwood 正态区间。

分类依据：原始任职 spell 的分组生存曲线：包括 referral 分组和随机处理组比较，图注按入职日显示存活；不把邻近正文的控制变量 hazard 回归自动当成该图的输入。可加 RCT context 标签，若另画回归调整后的处理效应应走 Reduced-form。

标签：生存分析, Kaplan–Meier, 删失

## 来源与范围

[What Do Employee Referral Programs Do? Measuring the Direct and Overall Effects of a Management Practice (2023)](<https://doi.org/10.1086/721735>); 3; PDF p.20

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

三种来源变体共用同一份 Python CLI，仅统计适配与输入不同。在本模板目录运行：

```shell
python plot.py kaplan_meier_survival_panels --input f39_spells.csv --ci --output-prefix YOUR_PROJECT/figures/f39
```

`--title "标题"` 开启可选标题；`--xlabel` / `--ylabel` 自定义轴名。默认无标题与底部 notes。另输出 `_checked.csv` 供核对；不自动添加原论文统计检验。当前 Summary 变体只验收 Python。三份便携目录的 plot.py 为同一实现的同步镜像，不是三套独立折线算法。

共享绘图依赖：保持本目录与相邻 `_shared/line_geometry.py` 的关系；复制到研究项目时同时复制共享模块。导入按脚本位置解析，可从不同工作目录运行。共享模块只画给定折线或右连续阶梯，归一化、累计份额、拟合区间、风险集与 Greenwood 区间仍由各适配器处理。


将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

Python 实际执行并由主 agent 视检；共享适配器通过手算风险集、同刻失败/删失、Greenwood、全失败、缺失月份、非法输入检查。独立便携目录重跑 rc=0；不声称复现原论文数值。 续作共享折线／阶梯几何后，从不同工作目录重跑，默认导出坐标与原验收结果在1e-10容差内一致；统计适配保留，F38条形不变。 另修复 argparse 帮助文本百分号导致 --help 失败的问题；仅文字改变，帮助命令已执行通过。

统一图名：`survival_kaplan_meier`
