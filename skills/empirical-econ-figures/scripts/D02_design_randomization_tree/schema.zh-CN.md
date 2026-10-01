# 设计输入与概率含义

[English](schema.md) · [中文](schema.zh-CN.md)

通过 `--spec` 传入的可选 JSON 包含四个说明性参数，以及按以下顺序排列的五条路径：`A1_F1_U1`、`A1_F0_U1`、`A0_F1_U0`、`A0_F0_U1`、`A0_F0_U0`。`A` 是买方的**初始选择**，`F` 表示**保留合同要求**，`U` 为**最终选择**；1按适用情况表示接受或保留。来源图在样本中买方未改变初始选择的分支省略后续决策节点：初始接受者在两种合同条件下最终均接受，初始拒绝者在保留要求时最终均拒绝。这是观测样本的简化，**不是实验设计的逻辑限制**。模板固定这些来源图的五个叶节点，仅在 `A=0,F=0` 时绘制进一步接受/拒绝节点。

`p_initial_accept` 是买方初始接受的说明性份额/概率；来源中的初始选择**不是**随机化的。`p_contract_maintained_given_initial_accept` 与 `p_contract_maintained_given_initial_reject` 必须相等，因为来源将合同要求独立于初始选择进行随机分配。它们分别以对应 `A` 分支为条件；共同值为说明性随机化概率，非 Figure 1 提供的数值。`p_ultimate_accept_given_initial_reject_and_lifted` 以**同时**初始拒绝且取消要求为条件，代表说明性的后续行为，不是随机分配。全部概率须有限且位于 `[0,1]`。

输出 `illustrative_leaf_probabilities.csv` 给出各路径的联合概率、最终分支的条件分母及最终支付分支。例如 `P(A=0,F=0,U=1) = (1-p_initial_accept) × (1-p_contract_maintained_given_initial_reject) × p_ultimate_accept_given_initial_reject_and_lifted`。五条路径概率之和为1。图中有意不显示数值概率，因为来源 Figure 1 未提供这些概率。模拟概率只演示路径核算，不是估计值或来源数值。
