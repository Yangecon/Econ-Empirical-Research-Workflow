# A17 · 多来源先验、后验与频率派估计比较

[English](recipe.md) · [中文](recipe.zh-CN.md)

`prior_posterior_interval_comparison` · A17

按来源成对排列先验与后验中位数及其区间，并单独展示ITT点估计与置信区间。

分类依据：RCT 的 ITT 与实验数据更新后的后验；Bayesian 是推断方法，原图不估计经济行为结构参数。

标签：贝叶斯推断, 先验与后验, 区间比较, 随机对照试验, 推断, 点区间图

## 来源与范围

[Bayesian Impact Evaluation with Informative Priors: An Application to a Colombian Management and Export Improvement Program (2025)](<https://doi.org/10.3982/ECTA21567>); Figure 2; PDF p.15

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在模板目录运行：

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/prior_posterior.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/prior_posterior_stata.png" "en" "0"
```

Stata需预先建立输出父目录。Python `--title` 或Stata最后参数 `1` 开启总标题；`zh` 切换中文。保留面板结果与年份标签，默认无总标题和底部notes。

输入按面板、来源和区间类型唯一识别。学者、政策制定者、企业、文献四种来源各有先验与后验两行，另列弥散先验对应的后验和频率派ITT；目前四个面板共40行。需要改变面板/来源配置时同步修改两语言脚本中的配置与行数检查。

`median`列对Bayesian行表示中位数，对ITT行表示点估计；这个列名不把ITT估计器变为中位数。`low/high`分别保存95%先验区间、95%后验区间或95%频率派置信区间。脚本只读取已存数值，不进行Bayesian更新，不要求后验一定嵌套于先验，也不把后验排除零解释为频率派显著性。

原文左列出口参与的单位为概率差，右列产品—国家种类为数量差；两类不能共用同一结果单位。各面板独立设置横轴范围。示例值单独生成，仅演示布局与类型区分，不重现原文更新结果。Python用共享图例，Stata用逐行标签和线型区别；区间含义同时保留在本说明中。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

4面板共40行，按panel/source/kind逐项对照两语言数值完全一致。两语言拒绝无效区间和缺失配对，调整CSV列顺序后数值一致。英中默认与标题版本实际运行并视检；Stata行标签经可读性调整后再核对。

统一图名：`inference_prior_posterior_intervals`
