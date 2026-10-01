# A15 · 置换零分布与观察统计量

[English](recipe.md) · [中文](recipe.zh-CN.md)

`permutation_null_distribution` · A15

并列展示给定的随机化零分布与观察值，显式定义单侧或双侧极端事件和 Monte Carlo p 值。

分类依据：置换零分布与观察统计量是推断诊断，保留双语言；尾部规则和置换 p 值必须显式定义。

标签：随机化推断, 置换, 零假设分布, 推断, 直方图

## 来源与范围

[An Experimental Evaluation of Deferred Acceptance: Evidence from Over 100 Army Officer Labor Markets (2026)](<https://doi.org/10.3982/ecta22160>); Figure 1; PDF p.19

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在本模板目录中运行：

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/permutation.png --lang en --tail right --xmin 0 --xmax 1 --binwidth .01
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/permutation.png" en right "" 0 1 .01 0
```

Stata 参数依次为输入、输出、语言、尾部规则、零假设中心、横轴下界、上界、箱宽和标题开关。Python `--title` 或 Stata 最后一项 `1` 开启标题。`zh` 切换中文。

输入 B 次抽取不包含观察到的分配本身；p=(E+1)/(B+1)。右尾取 null>=observed，左尾取 null<=observed；双侧需显式指定中心 c，以 |null-c|>=|observed-c| 判断。等号属于极端事件。这是 Monte Carlo 抽取的加一规则，不适用于已经包含观察分配的完整枚举计数。

每根柱高是箱内抽取次数/B，不是概率密度。p 值和计数另存 results.csv，图内不写检验 notes。模板不会构造有效的随机分配机制；真实应用必须先根据实验或准实验设计生成零分布，不能把普通 bootstrap 抽取直接称为随机化检验。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

Python 与 Stata 中英文 PNG/PDF 实际运行并视检；单面板默认无上方名称，多面板保留标签，Stata 纵轴刻度横排。2 个面板各 2,500 次模拟抽取；右尾、左尾、显式中心双侧规则的极端计数一致，p 值最大差小于 5.2e-14。

统一图名：`inference_permutation_null`
