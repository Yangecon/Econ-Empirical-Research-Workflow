# C09 · 按行业聚合的加权分布比较

[English](recipe.md) · [中文](recipe.zh-CN.md)

`weighted_distribution_comparison` · C09

先在行业内计算企业数份额和增加值份额，再按行业增加值加权；共同分箱和纵轴尺度。

分类依据：PDF Figure I 图注已核对：先在每个3位行业计算企业数份额和增加值份额，再用该年行业增加值权重平均。区别于对全体企业直接加权；同一横轴两个明确分母，采用共同尺度分面/叠图避免任意双轴缩放。

标签：加权份额, 行业聚合, 分布

## 来源与范围

[The Micro-Level Anatomy of the Labor Share Decline (2021)](<https://doi.org/10.1093/qje/qjab002>); Figure I; PDF p.3

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在本模板目录运行：

```shell
python plot.py --input demo.csv --output-prefix YOUR_PROJECT/figures/weighted_distribution_comparison
```

`--title "标题"` 可显式添加标题，默认无标题和底部 notes。输入字段、排除条件及显示含义见 schema.md；输出 PNG、PDF 与核算 CSV。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

已核行业内两类分母、行业年度权重、总份额为一、共同箱端点和非法分箱；Python 实跑并视检。 所有示例数值及关系为模拟，不是原论文结果复现。

统一图名：`distribution_weighted_comparison`
