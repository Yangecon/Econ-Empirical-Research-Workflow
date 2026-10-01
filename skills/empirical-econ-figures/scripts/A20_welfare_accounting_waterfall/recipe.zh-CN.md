# A20 · 并列核算瀑布图与独立比值

[English](recipe.md) · [中文](recipe.zh-CN.md)

`paired_accounting_waterfall` · A20

在分组面板中分别核算两套金额分量、小计和合计，并单独标注无量纲比值。

分类依据：直接审计收入与支出、随机审计结合匹配对照估计的长期威慑收入，再加 IRS 调查的金钱/时间成本构造 MVPF。是基于实证效应的充分统计量式福利核算，不是原始数据概貌，也不是完整结构模型输出。

标签：福利, 成本收益核算, 瀑布图, 分解, 充分统计量

## 来源与范围

[A Welfare Analysis of Tax Audits Across the Income Distribution (2025)](<https://doi.org/10.1093/qje/qjae037>); Figure VIII; PDF p.41

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在模板目录运行：

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/waterfall.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/waterfall_stata.png" "en" "0"
```

Stata运行前须建立输出父目录。Python `--title` 或Stata最后参数 `1` 开启标题；`zh` 切换中文。两个组面板使用各自的纵轴范围，应按轴刻度和打印金额比较，不能跨面板只比柱高。

`component` 按带符号金额增加余额，画成旧余额到新余额之间的浮动柱；`subtotal` 与最终 `total` 从零画到余额，并核验输入值，不重复累加。组间对应步骤必须一致。例子额外加入一个阶段小计，原文没有这一柱。

本来源的MVPF为纳税人避免审计的支付意愿除以政府净收入。金额单位为每增加1美元审计支出的美元金额；MVPF无量纲，单独标注。代码要求净收入分母为正，不能套用其他政策MVPF的净成本或无穷值规则。收入账本中的audit_cost列已经带负号，直接与两项正收入相加。支付意愿和收入的模型估计在上游完成，本例只用模拟数字示范核算与画法。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

两组18个账目步骤，中英文Python/Stata均实际运行并视检，另检查标题开关。浮动柱边界、运行余额和两组比值的跨语言最大差2.22e-16。Python拒绝不平衡合计、缺账本、错误条目归属和断号；Stata不平衡小计测试返回r(9)。

统一图名：`welfare_accounting_waterfall`
