# A01 · 事件研究与处理前后均值

[English](recipe.md) · [中文](recipe.zh-CN.md)

`event_study_with_pre_post_averages` · A01

980 行同期处理平衡面板实际估计：逐期效应、包含基准期零值的处理前均值、处理后均值，以及后减前的 DID 对比；区间使用完整协方差。

分类依据：980 行同期处理平衡面板实际估计：逐期效应、包含基准期零值的处理前均值、处理后均值，以及后减前的 DID 对比；区间使用完整协方差。

标签：事件研究, 兼容 DID 的展示, 处理前后均值

## 来源与范围

本地参考；原图文献身份未确认

补充相近画法: [Alleviating Worker Shortages Through Targeted Subsidies: Evidence from Incentive Payments in Healthcare](<https://doi.org/10.3386/w32412>); Figure 5; PDF p.26

用户提供的本地模拟绘图示例；不是已核实论文图

NBER 参考图有六个结果面板、日历日期、灰色置信带，以及排除改革前后若干季度的红色时期均值。本示例用 980 行模拟平衡面板实际估计一个相对时间面板；六期前均值包含归一化基准零值，八期后均值减去前均值，在文档指定的同期处理设定下等于静态 DID。这是相近画法参考，不复现 NBER 论文的估计值、样本、窗口或推断。

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

输入字段与检查规则见代码开头。

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在模板目录中执行，将输出写入研究项目：

```shell
python event_study_with_pre_post_averages.py --output YOUR_PROJECT/figures
```

默认读取随包的 980 行面板，实际估计静态 DID 与事件研究。绘制外部保存的估计时同时传入 `--estimates` 和 `--covariance`。重新生成固定种子面板及数值结果：`estimate_demo_panel.py --output-dir YOUR_PROJECT/example_inputs`。

Stata 将 `PANEL_CSV` 指向随包面板、`OUT` 改为项目输出，保留 `MODE "demo"`，原生 do-file 会独立估计相同模型。未显式设置绝对路径时，以 Stata 当前目录解析。`MODE "csv"` 读取保存的系数与完整协方差；`MODE "estimation"` 读取现有 e(b)/e(V)，按实际估计器设置 TIMES/COEFS。

六期前均值包含 −1 基准零值，八期后均值减去前均值，在本例同期处理平衡面板中等于静态 DID。归一化基准使用空心圆点，没有单独区间。后减前及其完整协方差区间导出到 `_contrast.csv`，不额外画第三条阴影带。假设、协方差修正与数值核对见[方法说明](README.zh-CN.md)。

`--ci-style cap` / `CI_STYLE "cap"` 可改为误差棒，`--connect` / `CONNECT 1` 可连接点。`--title "..."` / `TITLE "..."` 可开启标题，默认无标题或底部注释。`--post-is-att` / `POST_IS_ATT=1` 已弃用并报错。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

980 行、70 个体（35 处理 / 35 对照）的同期处理平衡面板；Python 与 Stata 19 均实际估计静态 DID 和事件研究并出图。前期六期含 -1 零值，后期八期；使用完整协方差、个体聚类 CR0 和正态 95% 区间。两语言均值、后减前及区间误差小于 1e-12；独立个体变化核对通过，PNG 已视检。

统一图名：`event_study_pre_post_averages`
