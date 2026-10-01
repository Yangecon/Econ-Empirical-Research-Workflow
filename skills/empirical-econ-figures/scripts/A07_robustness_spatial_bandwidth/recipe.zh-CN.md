# A07 · 带宽敏感性曲线与两种推断区间

[English](recipe.md) · [中文](recipe.zh-CN.md)

`bandwidth_sensitivity_profile` · A07

比较改变回归样本带宽后的系数，以灰带和虚线区分同一覆盖率下的两种推断方法。

分类依据：六结果的空间带宽稳健性剖面：横轴为每次回归允许的距边界最大公里数，不是个体运行变量；每结果61次回归。灰带是census-block聚类稳健95%CI，点线是Conley95%CI，两种推断方法而非68/95双置信水平。输入明确方法名与给定区间，不代做聚类/Conley；可选基准线需用户给明含义，原文蓝虚线不自行猜测。

标签：带宽敏感性, 空间推断, 稳健性, 折线图

## 来源与范围

[Multinationals, Monopsony, and Local Development: Evidence From the United Fruit Company (2022)](<https://doi.org/10.3982/ECTA19514>); Figure 3; PDF p.13

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在模板目录运行：

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/bandwidth.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/bandwidth_stata.png" "en" "0"
```

Stata需预先建立输出父目录。Python `--title` 或Stata最后参数 `1` 开启总标题；`zh` 切换中文。结果名称、单位和顺序在两脚本中同步配置。各结果使用自己的纵轴范围；原文总未满足需求数为数量差，其余五个结果为概率差。

横轴是每次回归纳入的距边界最大距离；原文从5到20公里、每次增加0.25公里，共61个样本带宽。它不等于个体运行变量，也不等于Conley空间相关截断距离（原文另设2公里）。示例保留网格但使用模拟系数与区间。

灰带与点线分别表示同一估计值的聚类稳健95%区间和Conley95%区间。不能改称68%/95%双层区间，也不能要求两种方法互相嵌套。`qa_crossing.csv`提供两种区间交叉的有效例子。脚本读取预计算结果，不估计标准误或推断因果识别。

原图蓝色虚线的准确含义未由图注核实，因此模板省略它；需要基准线时必须先指定其数值和含义。Python使用共享图例，Stata在各面板下显示同样的两种方法，版式允许不同。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

6个结果各61个带宽，共366行；Python与Stata中英文、标题和交叉区间版本实际运行并视检，输出数字最大差0。有效fixture中的两种95%区间相互交叉而均包含估计值，两语言均接受。Python另核验共同带宽网格、重复键、负带宽和无效区间。

统一图名：`robustness_spatial_bandwidth`
