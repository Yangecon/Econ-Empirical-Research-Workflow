# C02 · 加权分布叠图、阈值与区间份额

[English](recipe.md) · [中文](recipe.zh-CN.md)

`distribution_overlay_with_thresholds` · C02

比较多组分布，在明确阈值以下填充完整分箱，并标注使用全样本权重分母计算的份额。

分类依据：按年份比较收入分布，标注共同或年份阈值及其下方质量；保留密度归一化和权重定义。

标签：加权分布, 阈值份额, 直方图

## 来源与范围

[Evaluating the Success of the War on Poverty since 1963 Using an Absolute Full-Income Poverty Measure (2024)](<https://doi.org/10.1086/725705>); Figure 10; PDF p.37

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在本模板目录中运行：

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/distributions.png --lang en --xmax 120000 --binwidth 1000
```

`--lang zh` 切换中文，`--title` 显式开启标题。脚本顶部配置组别、阈值、标签、配色及各组填充至哪个阈值；同一组全部 threshold 的份额会另存 shares.csv。轴单位也在配置中修改。

本模板接受非负数值，左界固定为 0；阈值必须落在箱边界。阴影按整箱边界延伸到阈值，精确份额采用 value<threshold，阈值并列值留在上侧。所有可见箱为左闭右开；恰等于 xmax 或更大的观测不画出，但仍计入权重分母。

纵轴是每个等宽箱的加权百分比，不是核密度。改变箱宽会改变曲线高度。它不自动进行通胀调整、家庭规模等价化、贫困线推算或调查抽样推断；这些步骤应由上游分析完成。来源图另包含中位数参照线，本通用例保留分布、阈值和份额的核心画法。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

Python 中英文 PNG/PDF 实际执行并视检。14,000 条模拟观测；每组每个阈值的加权份额与完整分箱质量核对一致。另测试恰等于阈值及横轴上界的观测、非零左界拒绝和新建嵌套输出目录。右侧被截去的 597 条后期观测仍在分母内，可见质量约 91.4856%，不重新归一化成 100%。

统一图名：`distribution_threshold_overlay`
