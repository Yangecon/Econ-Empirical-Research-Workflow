# D03 · 制度监测日历

[English](recipe.md) · [中文](recipe.zh-CN.md)

`monitoring_calendar` · D03

按完整日期与显式周期锚点展示监测计划，独立标记实际观测；保持跨月日程连续。

分类依据：逐日制度日历：真实年月日与星期位置，显式监测日期列表/周期锚点，不把每3天误解为每周三。区分计划日程与实际执行；低于主要结果图的实施优先级。

标签：监测日程, 日历, 制度设计

## 来源与范围

[Unwatched Pollution: The Effect of Intermittent Monitoring on Air Quality (2021)](<https://doi.org/10.1257/aer.20181346>); Figure 1; PDF p.6

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在本模板目录运行：

```shell
python plot.py --year 2024 --anchor-3 2024-01-01 --anchor-6 2024-01-01 --observed demo_observed.csv --output-prefix YOUR_PROJECT/figures/monitoring_calendar
```

`--title "标题"` 可显式添加标题，默认无标题和底部 notes。输入字段、排除条件及显示含义见 schema.md；输出 PNG、PDF 与核算 CSV。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

已核 2024 闰年、日期位置、跨月三日/六日周期和计划/观测分离；Python 实跑并视检。六日边框和三日填色独立编码。 所有示例数值及关系为模拟，不是原论文结果复现。

统一图名：`design_monitoring_calendar`
