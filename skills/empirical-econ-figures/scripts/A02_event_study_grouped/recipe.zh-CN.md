# A02 · 分组事件研究动态效应

[English](recipe.md) · [中文](recipe.zh-CN.md)

`grouped_event_study` · A02

多组错位系数与置信区间，以实心/空心区分显著性，保留真实事件时间间距。

分类依据：多组错位系数与置信区间，以实心/空心区分显著性，保留真实事件时间间距。

标签：事件研究, 兼容 DID 的展示, 异质性

## 来源与范围

本地参考；原图文献身份未确认; Figure A3

补充相近画法: [English Language Requirement and Educational Inequality: Evidence from 16 Million College Applicants in China](<https://doi.org/10.3386/w32162>); Figure 1; PDF p.24

截图显示 Figure A3；论文身份待主材料核实

NBER Figure 1 研究英语听力要求与考试结果，有三个面板并采用交互加权估计量。截图研究宽带中国与城乡户口的政治信任，只有一个面板，使用红绿错位估计。二者是不同研究；NBER 论文不能证明截图出处。

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

输入字段与检查规则见代码开头。

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在本模板目录中执行，输出位置改为你的项目目录：

```shell
python grouped_event_study.py --input demo_estimates.csv --output-dir YOUR_PROJECT/figures
```

Stata 先载入程序，再调用：

```stata
do "PATH_TO_TEMPLATE/grouped_event_study.do"
grouped_event_study, input("PATH_TO_TEMPLATE/demo_estimates.csv") output("YOUR_PROJECT/figures/grouped_event_study") reference(-1) level(95) language(en)
```

Python `--title "..."` 或 Stata `title("...")` 可开启标题；默认不绘制标题。真实输入可用 se 或成对 ci_low/ci_high；外部区间需自行确保 level 与其一致。

事件时间 −1 的归一化基准用空心圆点显示，不绘制置信区间；它不是估计效应，也不计入处理前后均值。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

Python 3.12 与 Stata 19 实际运行并视检通过。主示例 26 个估计、2 组、14 个 CI 排除零；另验证列顺序变化、3 组、非等距事件时间及显式区间输入。Python 中文已视检；Stata 中文未单独视检。

统一图名：`event_study_grouped`
