# C12 · 历史事件标注的时间趋势（变体）

[English](recipe.md) · [中文](recipe.zh-CN.md)

`historical_policy_timeline` · C12

带真实日期间距、明确缺失断线和历史事件标注的趋势；共享 line family 绘图入口。

分类依据：QJE Figure III 是带历史事件标注的多序列真实工资趋势，归为 multi_series_time_trend 的待开发注释变体；AER日历图另列 monitoring_calendar，二者不混称同一模板。

标签：时间序列, 历史事件注释, 图形系列变体

## 来源与范围

[Minimum Wages and Racial Inequality (2021)](<https://doi.org/10.1093/qje/qjaa031>); III; PDF p.14

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

三种来源变体共用同一份 Python CLI，仅统计适配与输入不同。在本模板目录运行：

```shell
python plot.py historical_policy_timeline --input f37_trend.csv --events f37_events.csv --output-prefix YOUR_PROJECT/figures/f37
```

`--title "标题"` 开启可选标题；`--xlabel` / `--ylabel` 自定义轴名。默认无标题与底部 notes。另输出 `_checked.csv` 供核对；不自动添加原论文统计检验。当前 Summary 变体只验收 Python。三份便携目录的 plot.py 为同一实现的同步镜像，不是三套独立折线算法。

共享绘图依赖：保持本目录与相邻 `_shared/line_geometry.py` 的关系；复制到研究项目时同时复制共享模块。导入按脚本位置解析，可从不同工作目录运行。共享模块只画给定折线或右连续阶梯，归一化、累计份额、拟合区间、风险集与 Greenwood 区间仍由各适配器处理。


将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

Python 实际执行并由主 agent 视检；共享适配器通过手算风险集、同刻失败/删失、Greenwood、全失败、缺失月份、非法输入检查。独立便携目录重跑 rc=0；不声称复现原论文数值。 续作共享折线／阶梯几何后，从不同工作目录重跑，默认导出坐标与原验收结果在1e-10容差内一致；统计适配保留，F38条形不变。 另修复 argparse 帮助文本百分号导致 --help 失败的问题；仅文字改变，帮助命令已执行通过。

统一图名：`line_historical_annotations`
