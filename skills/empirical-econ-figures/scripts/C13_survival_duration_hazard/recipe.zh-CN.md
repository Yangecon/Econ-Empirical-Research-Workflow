# C13 · 离散持续时间的条件风险率面板

[English](recipe.md) · [中文](recipe.zh-CN.md)

`discrete_duration_hazard_panels` · C13

以事件数除以当期风险集的离散 hazard；保留缺失月份间隔，默认用条形表达期间条件概率。

分类依据：按持续月份比较条件风险率，必须输入事件数与当期风险集；原始频数或累计发生率不是 hazard。

标签：持续时间, 风险率, 风险集

## 来源与范围

[Aggregate Nominal Wage Adjustments: New Evidence from Administrative Payroll Data (2021)](<https://doi.org/10.1257/aer.20190318>); 3; PDF p.21

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

三种来源变体共用同一份 Python CLI，仅统计适配与输入不同。在本模板目录运行：

```shell
python plot.py discrete_duration_hazard_panels --input f38_hazard.csv  --output-prefix YOUR_PROJECT/figures/f38
```

`--title "标题"` 开启可选标题；`--xlabel` / `--ylabel` 自定义轴名。默认无标题与底部 notes。另输出 `_checked.csv` 供核对；不自动添加原论文统计检验。当前 Summary 变体只验收 Python。三份便携目录的 plot.py 为同一实现的同步镜像，不是三套独立折线算法。

共享绘图依赖：保持本目录与相邻 `_shared/line_geometry.py` 的关系；复制到研究项目时同时复制共享模块。导入按脚本位置解析，可从不同工作目录运行。共享模块只画给定折线或右连续阶梯，归一化、累计份额、拟合区间、风险集与 Greenwood 区间仍由各适配器处理。


将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

Python 实际执行并由主 agent 视检；共享适配器通过手算风险集、同刻失败/删失、Greenwood、全失败、缺失月份、非法输入检查。独立便携目录重跑 rc=0；不声称复现原论文数值。 续作共享折线／阶梯几何后，从不同工作目录重跑，默认导出坐标与原验收结果在1e-10容差内一致；统计适配保留，F38条形不变。 另修复 argparse 帮助文本百分号导致 --help 失败的问题；仅文字改变，帮助命令已执行通过。

统一图名：`survival_duration_hazard`
