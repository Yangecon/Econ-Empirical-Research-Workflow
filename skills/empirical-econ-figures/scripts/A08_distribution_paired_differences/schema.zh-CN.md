# 输入与输出结构

[English](schema.md) · [中文](schema.zh-CN.md)

宽格式 CSV：`pair_id,black_contacts,white_contacts`；每行是一个真实孪生配对。配对 ID 必须唯一且非空。结果是有限的非负整数联系人数。至少需要三个完整配对；代码拒绝缺失或重复 ID，绝不静默删除配对中的一方。抖动后的横坐标仅取决于排序后的配对 ID，并随结果导出，纵坐标保留输入值。

核验后的配对 CSV：原始值、`difference_white_minus_black`、`x_black`、`x_white`。汇总 CSV：组均值与正态近似 95% 区间，以及配对差异的均值和标准误。密度平滑仅用于展示，不改变联系人数、配对关系、均值或区间。
