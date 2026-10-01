# 输入结构与检查

[English](schema.md) · [中文](schema.zh-CN.md)

节点 CSV 必需列为 `id,label,region,exam_group,label_show`，可选成对 `x,y`。`id` 必须唯一，全部文本字段须非空；`label_show` 为0或1。黑白填充最多支持两种区域标签。若提供坐标，则所有节点的坐标均须有限且完整；否则绘图器计算稳定的考试群组示意位置。

边 CSV 为 `source,target,type,directed`。端点须为已列节点ID。支持的 type 值为 `blood`（点划线）、`provincial_exam`（点线）和 `national_exam`（实线）。`directed` 为0/1。拒绝自环和重复同类型关系；无向关系反向重复也算重复，有向关系则尊重方向。单独列出时，同一节点对可有不同类型的连接。不自动添加任何缺失节点对，包括同一考试群组中的人。
