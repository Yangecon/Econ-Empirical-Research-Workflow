# 输入约定

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV 列：`group,ledger,seq,item,kind,value`。每行是某组某金额账本中的一个有序步骤。当前配置有两个组 ID（`group_a`、`group_b`）及两个账本 ID（`revenue`、`wtp`）；用于其他应用时修改两脚本的双语标签和条目词汇。各组在同一账本内须有相同有序步骤。`seq` 从 1 连续编号。`value` 为有限金额，示例单位是**每增加 1 美元审计支出对应的美元金额**。所有金额行（包括小计和合计）共用此单位。

`kind=component` 将带符号 `value` 加入该账本运行余额，绘为旧余额到新余额间浮动柱。`kind=subtotal` 从零绘至**当前**余额，必须等于此前分量之和。`kind=total` 对最终余额作同样处理；每组—账本恰有一个且必须最后出现。小计和合计仅核验，不重复相加。配置的收入合计条目为 `net_revenue`，支付意愿合计为 `net_wtp`。拒绝缺失或非数值金额、重复条目、不连续步骤、不一致组布局、未知 ID、不平衡小计/合计，以及非正净收入分母。脚本输出含 `bottom,top,running` 的 `_checked.csv`，以及含两项总金额和无量纲 `mvpf` 的 `_ratios.csv`。

来源启发的审计示例中，`net_revenue = audit_cost + upfront_revenue + deterrence_revenue`，其中 `audit_cost` 以**负数**输入。本模拟示例中 `net_wtp = upfront_taxes + deterrence_taxes + response_burden`；税收分量和应对负担均为避免审计的正支付意愿。显示的 `MVPF = net_wtp / net_revenue` 是独立的**无量纲比值**，绝不是金额柱。示例中间收入小计仅演示所支持的小计类型，引用的原始 Figure VIII 中没有该柱。
