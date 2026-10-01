# C16 · 区分关系类型的群组网络

[English](recipe.md) · [中文](recipe.zh-CN.md)

`typed_edge_community_network` · C16

考试群组作示意布局，区域以节点填充分辨，明确输入的关系以线型分辨；只绘制列出的边。

分类依据：按考试群组布置的精英关系网络，边线型区分关系种类、节点填充区分地区。读取节点、类型边和明确分组/坐标；布局位置不是地理距离或因果距离，环形节点排列不自动创建不存在的边。

标签：网络, 边的类型, 社群

## 来源与范围

[Web of Power: How Elite Networks Shaped War and Politics in China (2023)](<https://doi.org/10.1093/qje/qjac041>); Figure I; PDF p.14

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在本模板目录运行：

```shell
python plot.py --nodes demo_nodes.csv --edges demo_edges.csv --output-prefix YOUR_PROJECT/figures/typed_edge_community_network
```

`--title "标题"` 可显式添加标题，默认无标题和底部 notes。输入字段、排除条件及显示含义见 schema.md；输出 PNG、PDF 与核算 CSV。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

已核节点与端点、类型、方向、重复无向边、显式坐标和仅绘六条给定边；Python 实跑并视检。布局不是地理或因果距离。 所有示例数值及关系为模拟，不是原论文结果复现。

统一图名：`network_typed_communities`
