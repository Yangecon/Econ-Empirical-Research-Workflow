# E02 · 平台预测概率与事后概率校准图

[English](recipe.md) · [中文](recipe.zh-CN.md)

`probability_belief_calibration` · E02

分箱比较预测与真实概率，显示个体预测的四分位范围、全样本线性拟合和45度基准。

分类依据：对申请名单和优先类型重抽样、抽取 lottery numbers，重复模拟匹配机制 500 次。预测概率使用当前申请和历史外推，事后基准使用实际申请；Figure I A 检验平台预测质量，不是受访者信念，也不是估计偏好/成本参数的结构 calibration。

标签：概率校准, 分箱散点图, 预测, 校准, 匹配模拟, 模型验证

## 来源与范围

[Smart Matching Platforms and Heterogeneous Beliefs in Centralized School Choice (2022)](<https://doi.org/10.1093/qje/qjac013>); Figure I Panel A: Predicted vs. True Placement Probabilities; PDF p.25

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在模板目录运行：

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/calibration.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/calibration_stata.png" "en" "0"
```

Stata需预建输出父目录。Python `--title` 或Stata最后参数 `1` 开启总标题；`zh`生成中文。默认无总标题和底部notes。

x是真实/参考概率，y是预测概率，单位0–1。0至.99（含.99）的观测按x与唯一ID稳定排序后分10个近似等人数箱，>.99单列第11箱；要求常规组至少40行且尾组至少4行。相同x可能按ID拆入不同箱，这是模板的明确约定，不归因于原文。箱内横坐标和纵坐标均为观测均值，四分位数采用位置1+(n-1)p的线性插值。

浅色带为个体预测概率的条件第25至75百分位范围，不是均值置信区间。OLS在全部原始观测上拟合，包含>.99尾组，不以11个分箱点回归；该样本约定由本模板声明，不声称等同原文估计实现。空心圆只是分箱均值样式，不编码显著性。只复现原Figure I的Panel A画法，Panel B直方图未实现；原文预测模型与标准误不在此重算。全部演示值为模拟数据。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

160条模拟观测：10个常规箱各12人，>.99尾组40人。均值、线性插值四分位数和OLS拟合两语言最大差2.5e-8。精确.99归常规箱，>.99归尾组；两语言实际拒绝1.01概率。中英文默认及标题图已执行，默认图视检通过。

统一图名：`prediction_probability_calibration`
