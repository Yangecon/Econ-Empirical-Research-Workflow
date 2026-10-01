# 输入与变换

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 长格式 CSV，必需字段为 `date`、`series` 与 `value`。日期严格使用 ISO `YYYY-MM-DD`；`--frequency annual`（默认）要求1月1日，`--frequency monthly` 要求每月1日。每个序列—日期一行；序列ID须精确匹配默认 `SERIES` 配置，或可选 `--config` JSON 中的全部ID。`value` 须有限且非负。每个序列至少需要两个已观测时期。示例值是**已构造的比率**（虚构的每销售单位年度计数）。绘图代码不计算或推断原始分母、年度销售样本或样本筛选条件。

默认直接显示 `value`。`--normalize-base YYYY-MM-DD` 是显式可选变换：各序列分别计算 `index_t = 100 × value_t / value_base`；每个序列均须在同一指定基准日期有严格为正的已观测值。不以第一个可用时期替代。`_plotted.csv` 附表同时保留输入 `value` 和显示 `plot_value`。

横轴使用真实日历日期，间距随经过时间变化。各已观测区间内部缺失的年度或月份插入空值，以**断开折线**而非跨缺口插值。不暗示结果估计、不确定性区间或因果对比。

可选 JSON 配置：`series` 为非空数组，包含唯一 `id`、`label_en`、`label_zh`、有效 Matplotlib `color`，以及取自 `-`、`--`、`:`、`-.` 的 `linestyle`。`axes.en` 和 `axes.zh` 均须提供非空 `x_annual`、`x_monthly`、`y_raw_annual`、`y_raw_monthly`、`y_index` 与 `title`。配置ID影响标签及绘图顺序，不改变日历或归一化规则。此 Python 模板须保留相邻 `../_shared/line_geometry.py`。
