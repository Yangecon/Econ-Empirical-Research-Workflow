# A16 · 规格曲线与模型选择矩阵

[English](recipe.md) · [中文](recipe.zh-CN.md)

`specification_curve_with_choice_matrix` · A16

将预先计算的结果排序，并把每个模型的明确选择项与同一列严格对齐。

分类依据：Figure3 Panel B：按结果值排序的设定曲线，下方逐列对齐二元设定选择矩阵。原图纵轴是各实验的平均t统计量，不是回归系数或单次t检验；不得对均值机械加±1.96阈值。排序后矩阵必须通过spec_id与结果保持一一对应，空设定值不能当作0。Panel A统计量分布属于另一图层，优先复现B的曲线+设定矩阵。

标签：规格曲线, 模型选择, 稳健性

## 来源与范围

[Policy Experimentation in China: The Political Economy of Policy Learning (2025)](<https://doi.org/10.1086/734873>); Figure 3, Panel B: Average t statistics among all experiments; PDF p.21

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在模板目录运行：

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/specification.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/specification_stata.png" "en" "0"
```

Python `--title` 或 Stata 最后参数 `1` 开启总标题；`zh` 使用中文。示例为原文Figure 3的Panel B布局，纵轴是各实验t统计量的均值，不是回归系数或单个检验的t值，因此不画±1.96临界线。数据完全模拟，程序接收结果而不运行原文的实验估计。

按结果和spec_id排序，上图与每个选择项共同使用同一rank。灰点明确表示0、黑点表示1，缺失值不能当作0。需更换模型选择时，同步修改两脚本的选项ID、行次序、标签和结果范围。

`qa_with_ci.csv`展示调用者提供的区间：每行要么两个端点都空，要么同时存在并包含结果。原文Panel B不含这类区间；本模板不推断区间类型、覆盖率或显著性。多结果、聚类和Conley两类95%区间的矩阵变体尚未实现。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

48个模型、11个选择项；两语言排序结果及选择矩阵完全一致，随机打乱输入不改变输出。实际运行并视检中英文、可选区间和标题版本；Stata改变结果范围为[-5,10]后上图与矩阵仍分离。单侧区间、非数值区间和未知选择列均按预期拒绝。

统一图名：`robustness_specification_curve`
