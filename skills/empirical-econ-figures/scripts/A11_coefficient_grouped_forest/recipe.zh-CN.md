# A11 · 分组系数与稳健性森林图

[English](recipe.md) · [中文](recipe.zh-CN.md)

`grouped_coefficient_forest` · A11

横向多结果规格比较与纵向分组系数两种变体；按结果保留独立单位、置信区间和明确显示顺序。

分类依据：用同一可配置图族支持横向设定比较和纵向分组结果系数，保留各结果单位与区间含义。

标签：异质性, 系数图, 模型设定比较, 稳健性, 森林图

## 来源与范围

[Andrew Goodman-Bacon, The Long-Run Effects of Childhood Insurance Coverage: Medicaid Implementation, Adult Health, and Labor Market Outcomes (2021)](<https://doi.org/10.1257/aer.20171671>); Figure 8; PDF p.31

补充参考: [Desmond Ang, The Effects of Police Violence on Inner-City Students](<https://doi.org/10.1093/qje/qjaa027>); Figure VIII; PDF p.44

原始页图与 PDF 图注已核对；第一来源为 IV 规格比较，另一来源为 DD 分组结果，估计含义不合并

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在本模板目录中运行，指定项目输出路径：

```shell
python plot.py --input demo.csv --variant robustness --orientation horizontal --lang en --output YOUR_PROJECT/figures/forest.png
python plot.py --input demo.csv --variant subgroup --orientation vertical --lang en --output YOUR_PROJECT/figures/grouped_coefficients.png
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/forest.png" en robustness horizontal 0
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/grouped_coefficients.png" en subgroup vertical 0
```

Python `--title` / Stata 最后参数 `1` 开启标题；`zh` 切换中文。自动导出同名 PDF。顶部 CONFIG 或 Stata 对应 locals 配置 1–4 面板、1–3 组、各面板单位及基准规格；CSV 显式提供 term/panel/group 顺序。横向面板共享规格行，不强行共享不同量纲的效应轴。

优先读取显式 CI；仅当两端同时缺失时用 estimate ± 1.96×se。该回退是正态近似，真实分析请传入估计器实际区间。实心/空心在此比较模板代表规格或组别；它不是事件研究模板的显著性编码。

### Stata package command variant

原生版本为 `plot_twoway.do`（与原入口 `plot.do` 逐字节一致）；新增 `coefplot` 版本为 `command_variants/coefplot/plot_coefplot.do`，读取同一份显式输入 CSV。先读 [coefplot 的方法与区别](<command_variants/coefplot/README.zh-CN.md>)，再运行：

```stata
do "PATH_TO_TEMPLATE/command_variants/coefplot/run_demo.do" "PATH_TO_TEMPLATE/command_variants/coefplot" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/coefplot"
```

`PATH_TO_TEMPLATE` 指本模板的绝对目录；输出目录应属于研究项目。此 runner 生成默认版与可选标题示例。直接调用 `plot_coefplot.do` 时，最后的标题开关设为 `0`（参数顺序见对应 README）。

coefplot 1.8.8 的未修改 ado/help/license 随模板保存，runner 仅添加该项目本地包目录。图仅展示输入估计量及区间，不进行回归。


将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

Python 3.12 与 Stata 19 的两个方向、中英文八张 PNG 均实际运行并视检；四面板横向示例 32 行，单面板纵向示例 6 行，包含一行 SE 回退。Stata 四份日志有完成标记。单面板默认无顶部名称，多面板保留结果标签。 Additional Stata checks reject a one-sided missing CI (expected rc=9) and inconsistent horizontal term order (expected rc=459); all four valid demo runs were repeated successfully after repair. coefplot 1.8.8 命令版五次 Stata 运行通过，38 行输入及区间回填规则经核对，首选规格以红色点和区间突出。成图已视检；未另导出包版绘制坐标做独立数值对照。单面板默认无标题，多面板保留必要面板名。

统一图名：`coefficient_grouped_forest`
