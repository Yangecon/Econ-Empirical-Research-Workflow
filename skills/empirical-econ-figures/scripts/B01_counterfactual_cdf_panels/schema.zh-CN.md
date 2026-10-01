# 输入 CSV 约定

[English](schema.md) · [中文](schema.zh-CN.md)

每行是情景/组别 CDF 上一个已观测或给定点。UTF-8 CSV，以下表头可任意排序：

| 列 | 含义 |
| --- | --- |
| `panel` | 配置的情景 ID；示例为 `forced_attention`、`no_switching_costs`。 |
| `panel_order` | 明确显示顺序，1 或 2。 |
| `group` | 配置曲线 ID；示例为低、中、高敏锐度 `low`、`medium`、`high`。 |
| `group_order` | 明确图例顺序，1–3。 |
| `x_reduction` | 超额支出的货币减少量，可为负。更换数量或单位须修改轴标签。 |
| `cdf` | 在 `x_reduction` 处的累计份额，介于 0 和 1。 |

六条配置面板/组曲线各至少两点。值必须有限；曲线内 `x_reduction` 唯一；按 `x_reduction` 排序后 `cdf` 必须在 `[0,1]` 内非递减。给定 x 端点处不要求曲线恰好达到 0 或 1，因为显示范围可能截断分布尾部。两实现直接使用给定 CDF 点，不从观测计算 CDF、不估计反事实模型，也不将 `cdf` 解释为注意概率。
