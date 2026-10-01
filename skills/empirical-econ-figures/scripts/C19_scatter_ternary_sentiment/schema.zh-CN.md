# 输入结构

[English](schema.md) · [中文](schema.zh-CN.md)

CSV 每行一本书。必需字段：唯一非空 `book_id`；整数 `year`；数值份额 `religion`、`political_economy`、`science`，各在 [0,1] 内且在1e-7容差内加总为1；以及**预先计算**、位于 [0,1] 的数值 `sentiment_percentile`。必需字段均不得缺失或非有限。每个指定中心年份的包含端点窗口内至少须有一本书。坐标变换为 `x = science + 0.5 × religion`、`y = (sqrt(3)/2) × religion`。
