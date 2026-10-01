# A08 · 配对结果与差值分布

[English](recipe.md) · [中文](recipe.zh-CN.md)

`paired_difference_distribution` · A08

真实配对 ID 连接个体结果，展示边际密度、组均值及配对差异；不会按结果排序猜测配对。

分类依据：随机设置种族信号的 twin profiles 得到联系人数，图中配对个体和组均值/区间用于呈现实验处理差异；归 RCT 结果展示而非仅按散点外观分类。

标签：随机对照试验, 配对结果, 差值分布

## 来源与范围

[LinkedOut? A Field Experiment on Discrimination in Job Network Formation (2025)](<https://doi.org/10.1093/qje/qjae035>); Figure III; PDF p.22

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在所选模板目录运行 Python；输出到研究项目：

```shell
python plot.py --input demo_pairs.csv --output-prefix YOUR_PROJECT/figures/paired_difference_distribution
```

Stata 从本模板目录以显式参数运行：

```stata
do plot.do "demo_pairs.csv" "YOUR_PROJECT/figures/paired.png" 0
```

Python 可加 `--title "标题"`；Stata 最后参数从0改1可开启示例标题。默认无标题和底部 notes。输入字段及统计边界见 schema.md。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

已核手算配对样例、同一配对坐标、组均值及配对差异标准误的 Python/Stata 一致性。两种密度平滑配置不同，未宣称密度曲线数值一致；均值95%区间为1.96正态近似。 两语言实跑和主 agent 成图视检已通过；示例不等于原论文数值复现。

统一图名：`distribution_paired_differences`
