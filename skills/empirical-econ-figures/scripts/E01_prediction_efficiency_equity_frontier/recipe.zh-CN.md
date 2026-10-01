# E01 · 效率—公平政策路径与操作点

[English](recipe.md) · [中文](recipe.zh-CN.md)

`efficiency_equity_frontier` · E01

比较政策参数变化下的效率与群体差距，显示给定的不确定区间、操作点和现状基准。

分类依据：NRP 样本按真实漏报或 random forest 预测漏报排序，改变审计率后重新汇总检出额和差异；固定数据上的算法绩效评估，不求解行为反应或经济结构均衡。

标签：政策比较, 效率与公平, 运行点, 算法评估, 随机森林, 政策排序, 折线图

## 来源与范围

[Measuring and Mitigating Racial Disparities in Tax Audits (2025)](<https://doi.org/10.1093/qje/qjae027>); Figure VIII; PDF p.35

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在本模板目录中运行：

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/frontier.png --lang en
```

Stata 使用：

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/frontier_stata.png" "en" "0"
```

Python `--title` 或 Stata 最后参数 `1` 才开启标题；`zh` 切换中文。同步修改两份代码顶部的算法ID、文字与坐标单位。黑点表示输入指定的操作点，不是显著性编码；红叉和参考线来自唯一现状行。

连线顺序由 `policy_rate` 决定。当前简单模板要求各算法效率随该参数严格递增，因此**仅支持单调效率路径**；原文部分路径可局部回折，不能声称完整复现这些回折段。差距可为负，输入CI直接用于纵向阴影，不重新做bootstrap或计算横坐标不确定性。现状行两个CI端点必须都为空。

名称中的“前沿”表示政策路径比较，不代表代码计算了帕累托前沿、最优政策或支配关系。原文横轴为年化查获少报额（百万美元）、纵轴为概率差距（百分点）；其年度化、权重、抽查排序及95%bootstrap区间均由上游模型完成。演示仅用模拟数量和给定区间。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

69行模拟输入：4条各17点的路径和1个现状点。Python/Stata中英文均实际执行并视检；解析数值最大差8.89e-16。Stata仅一端填写现状CI的异常输入按预期在导出前返回r(9)，两语言均检查区间完整性、操作点唯一性及路径顺序。

统一图名：`prediction_efficiency_equity_frontier`
