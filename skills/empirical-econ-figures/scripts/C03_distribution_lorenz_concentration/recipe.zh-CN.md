# C03 · 集中曲线与洛伦兹曲线

[English](recipe.md) · [中文](recipe.zh-CN.md)

`lorenz_concentration_curves` · C03

展示累计人口权重与累计资源份额，区分共同排序变量的集中曲线和按资源自身排序的洛伦兹曲线。

分类依据：人口排序下的累计资源份额与平等线，分母/排序变量与普通 CDF 不同。

标签：洛伦兹曲线, 集中曲线, 不平等

## 来源与范围

[Curbing Leakage in Public Programs: Evidence from India's Direct Benefit Transfer Policy (2024)](<https://doi.org/10.1257/aer.20161864>); Figure 1; PDF p.7

原始页图与 PDF 图注已核对；参考页上半部 Figure 1 对应本模板，下半部另有 Figure 2

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在本模板目录中运行：

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/concentration.png --mode concentration --lang en
```

`--mode lorenz` 改为各条资源曲线按资源自身排序；`--lang zh` 切换中文；`--title` 显式开启与模式匹配的标题。默认不显示标题。配置资源列名、曲线标签和单位时一并修改脚本顶部设置。

每条曲线横轴为累计观测权重/总权重，纵轴为累计 weight×resource/资源的加权总量。相同排序值先聚合再累计，避免任意的并列值内部顺序。数据须非负，权重总量和每类资源加权总量须为正；允许零资源与零个体权重。

原图按同一家庭消费排序展示燃气购买和总支出，属于共同排序的集中曲线。洛伦兹模式是本模板提供的通用变体；它会改变排序，不能把两种模式当成同一个统计对象。点坐标另存 points.csv，不自动生成基尼系数、置信区间或处理效应。

共享绘图依赖：保持本目录与相邻 `_shared/line_geometry.py` 的关系；复制到研究项目时同时复制共享模块。导入按脚本位置解析，可从不同工作目录运行。共享模块只画给定折线或右连续阶梯，归一化、累计份额、拟合区间、风险集与 Greenwood 区间仍由各适配器处理。


将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

900 条模拟家庭观测。Python 中英文集中曲线及英文洛伦兹变体均实际执行、视检；加权起终点、精确并列排序聚合和两种排序的差异通过测试。另运行开启标题的洛伦兹变体，确认标题与模式一致。 续作共享折线／阶梯几何后，从不同工作目录重跑，默认导出坐标与原验收结果在1e-10容差内一致；统计适配保留，F38条形不变。

统一图名：`distribution_lorenz_concentration`
