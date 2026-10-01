# A05 · 断点两侧的分箱均值与局部线性拟合

[English](recipe.md) · [中文](recipe.zh-CN.md)

`regression_discontinuity_binned_outcomes` · A05

分别在断点两侧计算等宽分箱均值，并用窗口内原始观测拟合两条直线，展示水平跳跃。

分类依据：断点两侧分箱和拟合，重点为水平跳跃；与已排队的政策 kink 斜率变化图分别说明识别和输入，不能由图形外观推出设计有效。

标签：RD, 分箱散点图, 局部线性拟合

## 来源与范围

[Political Foundations of Racial Violence in the Post-Reconstruction South (2026)](<https://doi.org/10.1093/qje/qjaf045>); Figure V; PDF p.26

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在本模板目录中运行：

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/rd.png --lang en
```

Stata 使用：

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/rd_stata.png" "en" "0"
```

Python `--title` 或 Stata 最后参数 `1` 开启总标题，`zh` 切换中文。两份脚本顶部同步设置面板、变量标签、窗口、每侧箱数和显示范围。默认两个结果面板各10箱/侧，发生概率使用共同纵轴尺度；更换数据后应同时调整纵轴范围及刻度，代码会拒绝超界点或拟合端点。

输入运行变量已减去断点，零进入右侧；窗口两端均保留。每侧各自等宽分箱，不允许箱跨过零，每箱至少两条观测。线在所有窗口内观测上做等权OLS，绝不在分箱均值上回归。随图输出分箱、两侧系数和样本计数CSV。

原文包括选举期和州固定效应、经纬度二次项，窗口来自Table II最优带宽。这里仅复现画法，以模拟二元结果、手定窗口和无控制项的两侧OLS演示；不恢复原文调整、不选择最优带宽，也不计算RD标准误、p值或识别有效性。结果字段限于[0,1]，不能直接代入可能越界的残差。

### Stata package command variant

原生版本为 `plot_twoway.do`（与原入口 `plot.do` 逐字节一致）；新增 `rdplot` 版本为 `command_variants/rdplot/plot_rdplot.do`，读取同一份显式输入 CSV。先读 [rdplot 的方法与区别](<command_variants/rdplot/README.zh-CN.md>)，再运行：

```stata
do "PATH_TO_TEMPLATE/command_variants/rdplot/run_demo.do" "PATH_TO_TEMPLATE/command_variants/rdplot" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/rdplot"
```

`PATH_TO_TEMPLATE` 指本模板的绝对目录；输出目录应属于研究项目。此 runner 生成默认版与可选标题示例。直接调用 `plot_rdplot.do` 时，最后的标题开关设为 `0`（参数顺序见对应 README）。

需将官方 rdrobust 套件装入项目本地 ado 目录；runner 可接收第 4 个参数指定该目录。默认结果不显示 RD 置信区间；包版横坐标使用箱中点，原生版使用箱内样本 x 均值。


将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

5,900行模拟输入，40个分箱、4条两侧OLS拟合；Python/Stata中英文实际执行并视检，数值最大差4.57e-11以内。已检查窗口端点和断点归属、窗口外样本计数、重复/未知ID、概率范围；合法但超出显示范围的高概率输入在两语言都被拒绝，Stata返回r(9)，避免静默裁图。 rdplot 11.1.0 命令版 EN/ZH 默认及可选标题四次 Stata 运行通过；40 个 bin 的计数和均值与原生版一致（误差<2.14e-14），4 条拟合线误差<3.11e-15。箱中点与样本均值横坐标区别已保留。

统一图名：`rd_binned_outcomes`
