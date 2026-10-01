# A12 · 分组估计效应与样本分布组合图

[English](recipe.md) · [中文](recipe.zh-CN.md)

`binned_effect_with_support_histogram` · A12

上方展示分组估计值与区间，下方展示同一横轴变量的无条件样本分布；效应和样本数量分别输入。

分类依据：左列为各网络支持分组的平均迁移率和 Wilson 区间，右列为固定效应回归的异质性 beta 与双向聚类区间；复合图以右列实证估计归类，同时标记 Summary overlay，不是结构模型输出。

标签：异质性, 分箱效应, 样本支持, 汇总叠加, 固定效应

## 来源与范围

[Migration and the Value of Social Networks (2025)](<https://doi.org/10.1093/restud/rdad113>); Figure 6; PDF p.20

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在本模板目录中运行：

```shell
python plot.py --effect effect_demo.csv --support support_demo.csv --output YOUR_PROJECT/figures/effect_support.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/effect_demo.csv" "PATH_TO_TEMPLATE/support_demo.csv" "YOUR_PROJECT/figures/effect_support.png" en 0
```

Python `--title` 或 Stata 最后一项 `1` 开启标题；`zh` 切换中文。两语言的 CONFIG 区定义面板 ID、范围、刻度及单位，换数据时一并修改。默认区间来自输入，不计算 Wilson、聚类标准误或新的回归。

下方 count 来自指定的无条件总体，不自动等于上方每个估计值的回归样本数。两部分必须使用相同横轴变量及单位。更改 Stata 刻度文字长度或图形组合后，重新检查上下绘图区对齐。

参考论文左侧面板为迁移率及 Wilson 95% 区间，右侧为固定效应条件下的模型系数及双向聚类 95% 区间；这是来源说明，不是模板自动实现的估计程序。Python 采用较矮的直方图区；Stata 保留对齐和数字刻度，但上下区域高度相近。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

Python/Stata 中英文 PNG/PDF 实际执行并视检；4 面板、80 个估计点、80 个直方图区间。Stata 经修正保留数字纵轴并对齐上下横轴；新建嵌套输出目录测试通过。两语言共享给定估计、CI 与计数，不重估模型。版式差异：Stata 上下区域高度相近，Python 下方直方图较矮。

统一图名：`heterogeneity_binned_effects_support`
