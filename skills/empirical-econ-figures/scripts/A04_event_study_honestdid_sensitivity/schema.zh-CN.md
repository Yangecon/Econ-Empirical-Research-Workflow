# 数据结构

[English](schema.md) · [中文](schema.zh-CN.md)

`synthetic_panel.dta`：2,880条观测，每个 `id`（1–320）× `t`（1–9）一条。`treated` 表示160个处理单位，`k=t-5` 为事件时间，`tau` 为生成的处理分量，`y` 为模拟结果变量。`lead4`、`lead3`、`lead2` 和 `lag0`–`lag4` 是处理状态与事件时间交互指示变量。事件时间−1没有指示变量，作为参考期。

`event_study_coefficients.csv`：每个纳入的事件时间一行。`event_time` 为相对处理起始的整数时期，`estimate` 为固定效应事件研究系数。顺序为−4、−3、−2、0、1、2、3、4。省略的−1不在表中，不作为估计零值保存。

`event_study_covariance.csv`：八行、八个数值列，依次为 `lead4`、`lead3`、`lead2`、`lag0`、`lag1`、`lag2`、`lag3`、`lag4`。`row_name` 标识协方差行。数值为完整、对称的聚类协方差子矩阵，而非仅标准误。

`rm_intervals.csv` 与 `sd_intervals.csv`：各十行。`restriction` 标识 `DeltaRM` 或 `DeltaSD`；常规 `Original` 行的 `bound_M` 为空，其余九种限制强度为数值；`ci_low` 与 `ci_high` 是包计算的95%区间下上端点。每次实际 `honestdid` 运行后直接从 `HonestEventStudy.CI` 保存。空白表示不适用，不是零。
