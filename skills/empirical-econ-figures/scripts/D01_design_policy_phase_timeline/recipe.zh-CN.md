# D01 · 分批政策的过渡、执行与终止时间线

[English](recipe.md) · [中文](recipe.zh-CN.md)

`staggered_policy_phase_timeline` · D01

按队列展示月度政策阶段、样本数和共同终止时点；保留未实施政策的比较组。

分类依据：分批政策的自愿过渡、强制执行与结束时点需要阶段区间输入；纯制度说明可只用 Python。

标签：政策分步实施, 交错时点, DID 设计背景

## 来源与范围

[Prabhat Barnwal, Curbing Leakage in Public Programs: Evidence from India's Direct Benefit Transfer Policy (2024)](<https://doi.org/10.1257/aer.20161864>); Figure 3; PDF p.10

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在本模板目录中运行：

```shell
python plot.py --input demo.csv --lang en --output YOUR_PROJECT/figures/policy_timeline.png
```

`--title` 开启标题；`--lang zh` 切换中文。自动导出同名 PDF。输入采用真实可解析的月初日期与显式队列顺序，坐标按月份计算。

阶段为左闭右开区间，例如 `[2020-04-01, 2020-08-01)` 表示四月至七月，八月可紧接强制执行。终止线可省略；所有队列的非空 termination_month 必须一致。显示的 n 是用户定义的群体计数，含义写在图外。

演示采用虚构的 2020–2021 年日期与人数，不是源论文的印度政策历史时点。源论文同一阶段内存在执行例外，队列条带不能当作个体资格或实际遵从的证明。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

Python 3.12 中英文 PNG 实际执行并视检，另导出 PDF。示例为 3 个政策队列与 1 个非政策组；五种错误时点输入被拒绝，包括区间重叠、倒置、越过终止、非月初日期和非政策组带区间。

统一图名：`design_policy_phase_timeline`
