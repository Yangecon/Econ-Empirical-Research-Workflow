# A18 · 联合 Bootstrap 置信区域

[English](recipe.md) · [中文](recipe.zh-CN.md)

`joint_bootstrap_region_display` · A18

读取外部二维网格与嵌套90/95/99%联合区域，叠加点估计及 x+y=0.5 判别线。

分类依据：收益与期权数据构造的股权溢价贡献估计及 block bootstrap 联合抽样分布；原文下一节才与资产定价理论模型比较。

标签：自助法, 联合不确定性, 嵌套区域, 推断, 等高线区域

## 来源与范围

[Dissecting the Equity Premium (2022)](<https://doi.org/10.1086/720396>); Figure 3; PDF p.11

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在所选模板目录运行 Python；输出到研究项目：

```shell
python plot.py --grid demo_joint_grid.csv --point demo_point.csv --output-prefix YOUR_PROJECT/figures/joint_bootstrap_region_display
```

Stata 从本模板目录以显式参数运行：

```stata
do plot.do "demo_joint_grid.csv" "demo_point.csv" "YOUR_PROJECT/figures/joint_region.png" 0
```

Python 可加 `--title "标题"`；Stata 最后参数从0改1可开启示例标题。默认无标题和底部 notes。输入字段及统计边界见 schema.md。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

已核网格完整性、区间嵌套、非法格点拒绝以及每格区域的 Python/Stata 一致性。示例区域由模拟网格给定，不实施原文 block bootstrap，也不以边际矩形/正态椭圆代替联合区域；边界接触需检查截断。 两语言实跑和主 agent 成图视检已通过；示例不等于原论文数值复现。

统一图名：`inference_joint_bootstrap_regions`
