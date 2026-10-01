# C05 · 成对二元状态的四类转换堆叠图

[English](recipe.md) · [中文](recipe.zh-CN.md)

`paired_binary_transition_stacks` · C05

从个体配对观测计算四种状态转换，以共同完整配对分母画百分比堆叠柱。

分类依据：配对二元状态的四类联合分布：两次均为1、1转0、0转1、两次均为0，按任务画100%堆叠柱。核心选描述性柱层，不含原图底部p值与检验表，不声称完整复制整张结果图。以匹配个体为共同分母，条件转移率另用起始状态人数作分母；不能由两个独立横截面边际比例恢复转移。缺失配对需明确处理和报告，零分量保留、窄段标签避免挤压。

标签：配对状态, 转变份额, 堆叠柱状图

## 来源与范围

[Contingent Thinking and the Sure-Thing Principle: Revisiting Classic Anomalies in the Laboratory (2024)](<https://doi.org/10.1093/restud/rdad102>); Figure 7, upper descriptive bars only; PDF p.16

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在模板目录运行：

```shell
python plot.py --input figures/demo_pairs.csv --output YOUR_PROJECT/figures/paired_states
```

生成英文 PNG/PDF以及数值摘要。可用 `--title-en "Title"` 开启英文标题，默认无标题和底部notes。

四个组成是00、01、10、11，各任务共同分母为其完整配对数，不能混用初始状态组作为柱高分母。摘要另外提供以初始0或1为分母的条件转换率；空组记缺失而非0。个体与任务组合必须唯一，缺失配对会按任务报告。0/1含义、任务简称及顺序需按研究修改。

只实现原Figure 7上部描述性堆叠柱；原图底部假设检验和p值未复现。全部示例数据为模拟值。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

5项任务200行模拟观测，194个完整配对、6个未配对剔除；每根柱总和100%。零组成保留，初始状态组为空时条件转换率保持未定义。中英文实际运行并视检；原图及图注已核对。 主验收修复可选标题顶部裁切，中英文标题版重新执行，代表图视检通过。

统一图名：`bar_binary_transitions`
