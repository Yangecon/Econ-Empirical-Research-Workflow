# A03 · 多估计器 staggered DID 事件研究比较

[English](recipe.md) · [中文](recipe.zh-CN.md)

`staggered_event_study_estimator_comparison` · A03

六条实际 Stata 估计路线（含 jwdid）共用模拟面板，导出共同结果后由 Python、原生 twoway、event_plot 提取加 twoway 叠加绘制。

分类依据：六个实际 Stata 估计命令（含 jwdid）的结果提取、事件时间与支持范围对齐；Stata 和 Python 读取同一实际估计结果。论文图作为画法来源，不声称取得原作者 Analysis do-files 或复现原始数值。

标签：DID, 交错实施, 事件研究, 估计器比较, 稳健性, 点与区间, event_plot, jwdid, ETWFE, 模拟数据

## 来源与范围

[Braghieri, Luca, Ro'ee Levy, and Alexey Makarin, Social Media and Mental Health (2022)](<https://doi.org/10.1257/aer.20211218>); Figure 2; PDF p.19

原论文 Figure 2、PDF p19 及用户截图已核对；作者档案已定位但原分析 do-file 未取得，另核方法作者示例。

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

读取 schema.md 和 methods.md，先创建研究项目输出目录。默认无标题、无底部 notes；Python 不独立估计六种方法（含 jwdid）。

Python 绘制已保存的估计表：

```shell
python plot_python.py --input audited_estimates.csv --output-stem YOUR_PROJECT/figures/staggered_python
```

原生 Stata（`PATH_TO_TEMPLATE` 为本模板目录）：

```stata
do "PATH_TO_TEMPLATE/run_plot_twoway.do" "PATH_TO_TEMPLATE" "YOUR_PROJECT/estimates.csv" "YOUR_PROJECT/figures/staggered_twoway"
```

包与原生命令组合版本：

```stata
do "PATH_TO_TEMPLATE/plot_event_plot.do" "PATH_TO_TEMPLATE" "YOUR_PROJECT/estimates.csv" "YOUR_PROJECT/figures/staggered_event_plot" "" "YOUR_PROJECT/figures/event_plot_extracted.csv"
```

Python `--title "标题"` 或 Stata 输出路径之后的标题参数可开启标题；组合版本的空字符串是默认无标题。`event_plot` 负责矩阵解析、坐标和区间，`twoway` 负责同一估计器内实心/空心点，不能把它称作未经修改的纯 event_plot 成图。

若重跑估计示例，先把整个模板复制到研究项目 work 目录、按 dependency_manifest.json 配置项目 Stata 依赖，再从该副本运行 estimate_all.do。不要在已安装 skill 中生成模拟数据或图像。读入真实结果时保留估计支持、聚类、不同pretrend定义及两个归一化参考，不能将未支持期补零。

事件时间 −1 的归一化基准用空心圆点显示，不绘制置信区间；它不是估计效应，也不计入处理前后均值。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

六种Stata命令在300单位×15期模拟面板实际执行，dCDH使用199次单位聚类bootstrap。共同表61行（59条估计/检验、2条归一化参考）；jwdid实际提取k=0..5和完整6×6协方差，不补造处理前系数。三种绘图输入一致，event_plot区间最大差小于1.35e-7；主agent视检通过。Python只重绘Stata导出表；不同pre-period含义和estimand不完全相同。全新Stata安装未重建；保留依赖和已测环境。

统一图名：`event_study_staggered_estimator_comparison`
