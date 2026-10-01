# B02 · 分位组箱线图与边界观测

[English](recipe.md) · [中文](recipe.zh-CN.md)

`quantile_group_boxplot` · B02

按已定义的分位组比较个体估计值分布，明确四分位插值、箱须与异常值规则。

分类依据：同一行为模型 V 估计的个体注意概率，按潜在 acuity 十分位展示；不是原始观测概率的普通箱线图。

标签：估计概率, 分位数组, 箱线图, 异质性

## 来源与范围

[Heiss et al., Inattention and Switching Costs as Sources of Inertia in Medicare Part D (2021)](<https://doi.org/10.1257/aer.20170471>); Figure 1; PDF p.29

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在本模板目录中运行：

```shell
python plot.py --input demo.csv --lang en --output YOUR_PROJECT/figures/grouped_boxplot.png
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/grouped_boxplot.png" en 0 0 1
```

Stata 最后三个参数依次为标题开关、输入下界、输入上界。Python `--title` 开启标题；`--ymin` / `--ymax` 调整输入范围。两语言用 `zh` 切换中文，另输出各自的分组统计 CSV。

采用显式 Hyndman–Fan type 7 四分位数和 1.5×IQR 箱须；这是为两语言一致性选择的规则，不冒称论文原代码默认值。箱须不是置信区间，箱须外点不等于错误数据。概率为 1 的边界观测不能因为显得极端就删除。

模板读取已定义的 group 与 value，不自动构造 acuity decile 或估计注意力概率。若换成其他变量，必须同时更改范围、单位和轴标签。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

Python/Stata 中英文 PNG/PDF 实际运行并视检。700 行含并列值的模拟数据、10 组、21 个箱须外观测；两语言组计数、箱须和异常值数量一致，四分位数最大差约 1.11e-16。Python 已另验证新建嵌套输出目录，0/1 边界点可完整显示。

统一图名：`distribution_estimated_probabilities_boxplot`
