# B05 · 二维政策反事实与等结果线

[English](recipe.md) · [中文](recipe.zh-CN.md)

`policy_counterfactual_contours` · B05

在费用和拒付概率的政策网格上，叠加接受率不变线与每次就诊支付变化的等值线。

分类依据：最优重新提交索赔的 Bellman 决策模型与估计成本，再结合 Medicaid acceptance 的估计效应；属于结构与约化式混合输入的政策模拟。

标签：反事实, 政策网格, 等高线, 结构式与简约式混合输入, 等高线图

## 来源与范围

[A Denial a Day Keeps the Doctor Away (2024)](<https://doi.org/10.1093/qje/qjad035>); Figure VIII; PDF p.39

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在模板目录运行：

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/policy_contours.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/policy_contours_stata.png" "en" "0"
```

Stata需预先建立输出父目录。Python `--title` 或Stata最后参数 `1` 开启总标题；`zh` 切换中文。默认无总标题和底部notes。

输入是完整二维政策网格和两个已计算的结果面。横轴为费用百分比变化；纵轴为拒付概率的相对百分比变化，+10代表d变为1.1d，并非增加10个百分点。原点对应观测基准，两结果变化在那里均须为0。黑色实线是接受率变化=0，虚线数值是每次就诊支付变化（美元），不共用结果单位。

输入行顺序可变，脚本按真实数值坐标排序；缺网格拒绝。改支付水平时同步修改Python的PAYMENT_LEVELS、Stata的水平循环与范围检查。代码不估计结构模型或决定政策参数的可行范围。

Python使用Matplotlib轮廓算法；Stata独立按网格边线性插值，鞍点格使用确定性相邻边配对，因此粗网格或强非线性面上的曲线可有差别。Stata对每个线段留小间隙形成虚线，完整未断轮廓另在CSV以plot_style=4保留。数值验证包括解析曲线位置，不把像素一致作为通过条件。

示例为651格模拟结果；原文模型输出和原图数值未恢复。输出_checked.csv为网格，_contours.csv为轮廓证据。新数据应再次查看标签与线交叉处，必要时调整标签位置。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

651格完整网格，两语言输入数值一致；独立提取轮廓与解析曲线的端点残差最大4.08e-5。检查九个支付水平完整且顺序正确、接受率0线过原点；Stata水平等值线fixture保留全部水平。两语言实际拒绝缺网格和未归一化原点。默认中英文及标题版本已运行视检，修复虚线漏段和Python标签碰撞。

统一图名：`counterfactual_policy_contours`
