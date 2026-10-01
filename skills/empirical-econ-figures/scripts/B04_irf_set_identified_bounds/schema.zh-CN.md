# 输入约定

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV，五个有限数值列可任意排序：`horizon`、`admissible_low`、`admissible_high`、`pointwise_median`、`maxg_response`。至少三个严格递增、唯一、非负数值期限。每期限满足 `admissible_low <= admissible_high`，两条给定汇总曲线均须落在其中。允许任何有效数值期限网格；按输入期限顺序连点。来源用第 1–15 季度，第 1 期为冲击期。若其他数据采用不同时间起点，须相应修改横轴标签。`demo.csv` 是确定性模拟数据，不匹配文章数值。

`admissible_low`/`admissible_high` 是**每个期限可容许响应集合**的极值，不是 95% 置信界限。`pointwise_median` 在各期限分别计算；连线是视觉汇总，未必是一条共同可容许候选路径。`maxg_response` 是与选定可容许解关联的给定路径，这里不通过最大化来寻找。其是否满足事件限制须由上游认证。所有值须使用同一结果单位，例如 GDP 同比增长响应的百分点。
