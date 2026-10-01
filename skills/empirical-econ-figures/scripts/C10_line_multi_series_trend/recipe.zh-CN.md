# C10 · 多序列时间趋势与基期指数

[English](recipe.md) · [中文](recipe.zh-CN.md)

`multi_series_time_trend` · C10

按真实年度或月度间距展示多条趋势，保留缺失期断线，并可按显式共同日期分别归一为100。

分类依据：已有模拟演示，正修正短月度序列的日期刻度与留白；基础年度/月份折线保留真实日期间距、缺失期及显式基期归一化。

标签：时间序列, 趋势, 基期指数

## 来源与范围

[Knowledge Spillovers and Corporate Investment in Scientific Research (2021)](<https://doi.org/10.1257/aer.20171742>); Figure 2; PDF p.5

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在本模板目录中运行：

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/trend.png --normalize-base 1980-01-01 --lang en
python plot.py --input qa_monthly.csv --output YOUR_PROJECT/figures/monthly_trend.png --frequency monthly --lang en
```

省略 `--normalize-base` 直接画输入原单位；开启后，每条序列分别除以该日期的正观测值再乘100，不能用不同日期悄悄替代缺失基期。`--lang zh` 使用中文标签；`--title` 才显示标题。序列ID、文字和单位在脚本顶部配置。

年度日期须为1月1日，月度日期须为每月1日；相同序列/日期不得重复。输入的已观测值必须有限、非负，每条序列至少两期。序列内部缺失期补为空值而断线，不进行插值。序列开始前和结束后不扩展观测。

原文先将年度专利或论文数量除以样本总销售额，再将各比率定基。销售额分母、论文样本条件和年度汇总属于上游数据构造，本模板只做可选定基及绘图。历史事件文字注释尚未实现，不将带复杂注释的所有趋势图都称为已复现。

共享绘图依赖：保持本目录与相邻 `_shared/line_geometry.py` 的关系；复制到研究项目时同时复制共享模块。导入按脚本位置解析，可从不同工作目录运行。共享模块只画给定折线或右连续阶梯，归一化、累计份额、拟合区间、风险集与 Greenwood 区间仍由各适配器处理。

自定义系列／阶段及轴单位时使用随附 JSON；默认不传 `--config` 则兼容原示例：

```shell
python plot.py --input custom_demo.csv --config custom_config.json --output YOUR_PROJECT/figures/custom.png --lang en
```

`--lang zh` 使用中文标签，`--title` 显示配置中的标题。此配置扩展仅限 Python；若本项保留 Stata，其入口仍按原 schema 运行。C10 的有限非负值、日期和明确基期规则保留；C11 按年份顺序连线，不能按横坐标重新排序。


将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

68条模拟年度观测，补齐内部缺失期后72行；两条1980基期均为100。年度中英文、原单位模式和三/六月短序列均实际运行；日期刻度与右侧留白修正后视检通过。月份缺口与缺失基期拒绝检查通过。 续作共享折线／阶梯几何后，从不同工作目录重跑，默认导出坐标与原验收结果在1e-10容差内一致；统计适配保留，F38条形不变。 已执行外部系列/阶段ID、中文标签及可选标题示例，非法值或阶段/年份顺序输入会拒绝。

统一图名：`line_multi_series_trend`
