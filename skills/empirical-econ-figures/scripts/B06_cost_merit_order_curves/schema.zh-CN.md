# 输入与绘图约定

[English](schema.md) · [中文](schema.zh-CN.md)

CSV：`scenario,unit_id,marginal_cost,dispatched_mwh`。恰好两个非空情景名，每情景机组 ID 唯一，边际成本有限非负，**实际调度** MWh 严格为正。两情景调度 MWh 总和须在数值容差内一致。零调度机组不贡献宽度，应省略；成本允许为零。机组先按边际成本排序，并列按机组 ID；每级阶梯从该机组之前的累计调度量延伸到加入该机组之后的累计量。

核验阶梯 CSV：原始列加 `x_start,x_end`；坐标 CSV：每机组两点，`endpoint=0/1`、`x_mwh`、`marginal_cost`。相同需求是本图的可比性规则，不是绘图器施加的优化约束。不得从机组 ID 或成本排序推断容量或调度决策。
