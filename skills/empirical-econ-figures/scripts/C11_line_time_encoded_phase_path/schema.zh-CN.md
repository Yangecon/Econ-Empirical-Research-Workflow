# 输入约定

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV，列顺序任意：`year`（示例中为有限、严格递增的整数）、`x` 与 `y`（已处于预期显示尺度的有限数值）、`phase`（默认 `early`、`middle`、`late`，或可选 `--config` 的ID），以及 `year_label`（为空或与当年相同的待标注整数年份）。每个配置阶段至少需要两条观测，默认三阶段共至少六条。阶段内观测须连续，各阶段按配置顺序仅出现一次。跨阶段边界的线段采用**新**阶段的颜色，不按 `x` 对点排序。

来源样式中，`x` 为人口对数，`y` 为实际工资对数。用于其他场景时请提供配置轴文字与单位。来源年份为1250–1860；模拟 `demo.csv` 覆盖这些年份，但数值与阶段区间均为虚构，仅展示视觉结构。输入坐标可按时间不规则分布，不暗示中间存在观测点。

可选 JSON 配置：`phases` 为非空有序数组，包含唯一 `id`、`label_en`、`label_zh`、有效 Matplotlib `color`，以及可选的 `linestyle`（取自 `-`、`--`、`:`、`-.`）。`axes.en` 与 `axes.zh` 均须包含非空 `x`、`y` 与 `title`。Stata 默认仍固定为三个阶段；自定义配置仅用于 Python。此 Python 模板须保留相邻 `../_shared/line_geometry.py`。
