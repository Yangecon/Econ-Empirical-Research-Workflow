# 六估计器事件研究估计表

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV 每个 `estimator` × 整数 `event_time` 一行，键唯一。不支持的期限可以缺席；缺席期限绝不能以零效应提供。示例表含下列六种精确的估计器标签，总体事件时间为−5至+5。`jwdid` 序列仅含0至+5。用于其他场景前，应检查每个估计器的期限含义与提取方式。

| 列 | 含义 |
| --- | --- |
| `estimator` | `TWFE OLS`、`Sun-Abraham`、`Callaway-Santanna`、`dCDH dynamic`、`BJS imputation`、`Wooldridge jwdid` 之一。标签映射至不同颜色与形状。 |
| `event_time` | 相对实施时点的有符号整数时期，绘图按数值排序。 |
| `b` | 命令导出的估计，或显式归一化的零参考。 |
| `se` | 命令导出的标准误；归一化参考为空。 |
| `ci_low`, `ci_high` | 逐点95%正态近似端点 `b ± invnormal(.975) × se`；归一化参考为空。 |
| `status` | `estimated`、`pretrend_test`、`placebo_test` 或 `normalized_reference`。参考行以空心符号绘制、无区间，绝不计为估计。 |
| `sample_n` | 若估计器返回 `e(N)` 则记录；缺失表示本次提取无法取得命令返回的 `e(N)`，不是零。 |
| `command` | 产生来源估计的 Stata 命令。 |
| `inference` | 本图使用的单位聚类正态近似，或单位聚类 bootstrap 正态近似。 |

六序列示例有两条强制−1参考行，分别用于 TWFE OLS 与 Sun–Abraham。BJS 的 `pre1`、Callaway–Sant’Anna 的 `Tm1`、de Chaisemartin–d’Haultfoeuille 的 `Placebo_1` 是−1期检验或对比，不是归一化零值。`jwdid` 默认使用尚未处理对照，仅报告处理后事件 ATT；模拟面板没有从未处理队列，因此该序列没有处理前值或−1符号。其 `estat event, window(0 5)` 输出从 `r(b)` 与 `r(V)` 提取。完整六乘六方差矩阵保存在 `jwdid_event_covariance.csv`，行列均按事件0至+5排序。TWFE 回归包含 `K <= -6` 干扰分箱，并估计−5至−2期提前项；Sun–Abraham 纳入更早至−14期的提前虚拟变量，但仅绘制−5至−2。本比较不假设各方法的队列支持、样本、权重或估计目标相同。[估计器支持表](estimator_support.csv) 记录实际报告内容。

实心符号表示区间不含零；空心表示区间含零或归一化参考行。图例以颜色与形状标识估计器；图注必须解释参考期、处理前趋势状态、逐点区间规则、聚类、结果变量、单位、时期和样本。默认无标题或底部说明；手工 Stata 程序与 Python 绘图器接受可选标题。


事件时间 −1 的归一化基准用空心圆点显示，不绘制置信区间；它不是估计效应，也不计入处理前后均值。
