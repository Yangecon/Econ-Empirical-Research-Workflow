# C19 · 按时间分面的三元主题与情绪散点

[English](recipe.md) · [中文](recipe.zh-CN.md)

`time_faceted_ternary_sentiment_scatter` · C19

每点一本书，三份额组成三元坐标；按时间分面并使用跨面板共同情绪百分位颜色。

分类依据：每点为一本书，主题份额和情绪百分位是文本测度，按年份分面；测量模型不等于经济结构模型。

标签：文本指标, 三元组成, 时间分面, 组成, 三元散点图, 分面

## 来源与范围

[Enlightenment Ideals and Belief in Progress in the Run-up to the Industrial Revolution: A Textual Analysis (2026)](<https://doi.org/10.1093/qje/qjaf054>); Figure VI; PDF p.30

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在模板目录运行，下列输出目录应属于研究项目：

```shell
python plot.py demo_books.csv YOUR_PROJECT/figures/ternary.png --centers 1550 1600 1650 1700 1750 1800 1850 --half-window 10
```

`--title "标题"` 显式开启标题，默认无标题/底部notes。字段、统计对象及显示限制见schema.md。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

已核顶点坐标、非负份额及和为1、书目ID、百分位范围和含端点的时间窗口。颜色输入是上游百分位，不在面板内重新排序；最大值用可见浅灰，不用白底白点。 Python已实跑，主agent已视检；绘图示例不等于原论文数值复现。

统一图名：`scatter_ternary_sentiment`
