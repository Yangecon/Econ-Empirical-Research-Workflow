# 输入与计算约定

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV 列：`panel`（四个配置 ID 之一）、`id`（面板内唯一）、原始单位的数值 `running` 和数值 `outcome`。值不得缺失且必须有限。选定窗口包含两端 `[XMIN,XMAX]`，当前为 `[500,1200]`，内部阈值当前为 850。窗口外行计数后从分箱与拟合中排除。混合结果可使用不同单位，因此各面板明确配置独立的纵轴显示范围；两种实现均拒绝超出范围的箱均值或拟合线端点。

每个面板在**全部窗口内原始行**上拟合 `outcome = level_at_threshold + slope_left × (running-threshold) + slope_change × max(running-threshold,0)`。因此右侧斜率为 `slope_left+slope_change`，拟合水平连续。每个面板共需至少 `6×B` 条窗口内观测、满秩拟合，并在每个 `2×B` 箱中至少有两条观测。左右样本数可不同。这些是无标准误或 p 值的描述性不加权 OLS 系数。若无单独的设计假设、设定与推断，不得将斜率变化作因果解释。

分箱散点在每侧使用 B 个等宽箱，与拟合分开计算。`running<threshold` 属左侧；`running>=threshold` 属右侧。左端点归左侧第 1 箱，精确阈值归右侧第 1 箱，右端点归右侧第 B 箱；内部箱边界归其右侧的箱。每箱至少两条观测。`_bins.csv` 报告箱样本均值和 n；`_fits.csv` 报告连续折点系数；`_sample.csv` 报告纳入和排除数量。绘图脚本不推导研究特定的行政工资/福利规则，也不进行残差化。
