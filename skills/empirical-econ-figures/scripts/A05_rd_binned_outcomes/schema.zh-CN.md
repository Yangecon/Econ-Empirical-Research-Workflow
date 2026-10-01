# 输入与计算约定

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV 列：`panel`（配置的 ID）、`id`（面板内唯一）、`running`（距零断点的数值距离）以及 `outcome`（`[0,1]` 内的数值概率或二元结果）。必须包含两个配置面板。ID 和全部数值均不得缺失；running/outcome 必须有限。面板 `[-bandwidth,+bandwidth]` 窗口外的行计入排除数，不参与分箱或拟合。零属于**右侧**；`-bandwidth` 保留在左侧第一个箱，`+bandwidth` 保留在右侧最后一个箱。

每侧分别计算等宽箱序号：`x<0` 时为 `min(floor((x+bandwidth)/(bandwidth/B)),B-1)+1`，`x>=0` 时为 `min(floor(x/(bandwidth/B)),B-1)+1`。B 是配置的每侧箱数。箱间边界归入右侧的箱。每箱至少需要两条观测。绘图坐标为箱内原始 x 和结果的样本均值。另外，每侧在该侧**全部窗口内原始观测**上以不加权 OLS 拟合 `outcome = intercept + slope × running`；拟合线的两个端点均检查是否在配置的纵轴范围内。不计算标准误、p 值、带宽选择、协变量调整或 RD 有效性检验。

`_bins.csv`、`_fits.csv` 和 `_sample.csv` 输出公开这些计算。x=0 的拟合截距是各侧描述性外推值。模拟示例有意使 Outcome A 的水平差大于 Outcome B；这不是论文数据或结果。
