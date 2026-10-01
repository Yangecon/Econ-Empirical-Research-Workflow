# 计数输入与比例定义

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV，每个已配置的 `category × group` 组合恰有一行且唯一。必需字段为 `category`、`group`、`numerator` 和 `denominator`。类别及组别ID、顺序、双语标签和条形样式在 `plot.py` 顶部附近配置；并列条形布局要求**恰好两组**，完整笛卡尔组合须各出现一次。计数须为有限整数，每行满足 `denominator > 0` 和 `0 <= numerator <= denominator`。`proportion = numerator / denominator` 在各类别—组别单元格内独立计算；分母是**该单元格的合格观测数**，而非跨组汇总人数。`_rates.csv` 附表保留分子、分母及计算比例。

横轴从零开始。条形表示描述性单元格比例；脚本不计算标准误、检验、处理效应、调整后的入学率或因果对比。类别顺序按配置设置，不按字母或柱高排序。黑色实心与空心样式用于灰度区分两组。
