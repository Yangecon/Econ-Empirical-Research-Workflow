# A14 · 分位数回归系数曲线

[English](recipe.md) · [中文](recipe.zh-CN.md)

`quantile_coefficient_profile` · A14

沿数值分位位置连接预估系数，并绘制各分位给定的置信区间。

分类依据：结果分布不同分位上的回归系数与预计算区间；原文为标准化PSAT分数对BNI的无条件分位数回归，99%CI，ZIP聚类。保留数值分位位置与区间水平；不是按x分位分组的均值，也不能自动改称分位处理效应。模板不把qreg当作无条件分位估计器。

标签：分位数系数, UQR, 置信区间, 异质性, 系数图

## 来源与范围

[Distinctively Black Names and Educational Outcomes (2023)](<https://doi.org/10.1086/722093>); Figure 4; PDF p.15

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在模板目录运行：

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/quantile.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/quantile_stata.png" "en" "0"
```

Stata需预先建立输出父目录。Python `--title` 或Stata最后参数 `1` 开启总标题；`zh` 切换中文。默认没有总标题和底部notes。

横轴是结果分布的数值分位（0到100之间），输入按分位严格递增排列；连线只辅助阅读。纵轴系数和区间直接读取，不估计回归或标准误。修改脚本中的标签以表达真实单位，并在正文记录区间水平与推断方法。

原文是标准化PSAT分数对BNI的无条件分位数回归，使用ZIP层级聚类的99%置信区间。示例9个分位使用模拟系数和示意区间。不能把普通Stata `qreg` 自动当作无条件分位估计，也不能无条件把该系数改称分位处理效应。它不同于按解释变量分箱后计算结果均值的图。

两语言按数值横轴放置点，自动刻度和留白有所不同；CSV输出可逐项核对。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

9个分位数的Python与Stata导出数值完全一致。两语言实际拒绝不含点估计的区间和未排序分位，CSV列顺序调整后数值仍一致；中英文默认图和标题版本运行通过，默认图经主agent视检。

统一图名：`coefficient_quantile_profile`
