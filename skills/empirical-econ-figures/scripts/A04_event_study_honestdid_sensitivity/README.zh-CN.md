# A04 · HonestDiD 敏感性图

[English](README.md) · [中文](README.zh-CN.md)

这两张图是 [HonestDiD 官方 Stata 示例](https://github.com/mcaceresb/stata-honestdid) 的已实际执行、设定随机种子的**模拟数据演示**，不复现任何发表论文的数据或估计。相对幅度图改变界限 \(\bar M\)，平滑性图改变 \(M\)。两图均展示 `honestdid` 1.3.0 根据 Stata 事件研究及其完整聚类协方差矩阵计算的真实稳健置信区间。图形由原生 `honestdid, cached coefplot` 绘图器生成；没有手工填写系数或区间。

## 输出

| 图形 | PNG | PDF | 数值区间 |
|---|---|---|---|
| 相对幅度，DeltaRM | `honestdid_relative_magnitude.png` | `honestdid_relative_magnitude.pdf` | `rm_intervals.csv` |
| 平滑性，DeltaSD | `honestdid_smoothness.png` | `honestdid_smoothness.pdf` | `sd_intervals.csv` |

Stata 图默认无标题和底部说明。运行 `do build.do "<this folder>" "A title"` 可添加标题；可选第三个参数（如 `_titled`）为图形文件名附加后缀。两个变体保持独立。按 HonestDiD 实现，每个稳健敏感性网格旁均显示 `Original` 常规区间。它在横轴上的独立位置是类别位置，不是数值 M。

## 估计内容

`build.do` 生成320个单位、九期观测（2,880行）。前160个单位从第5期起接受处理。结果包含个体分量、共同时间趋势、个体斜率噪声、事件时间 \(k\geq0\) 时的处理效应 `0.18 + 0.055 k`，以及正态分布噪声。随机生成采用 `set seed 29092026`。拟合的 `xtreg, fe vce(cluster id)` 模型包含时期效应和处理状态与事件时间的交互指示变量，包括提前期−4、−3、−2与滞后期0至4。事件时间−1是唯一省略参考期。全部已观测处理后时期均进入模型。

提取的 `b` 有八个系数，顺序为−4、−3、−2、0、1、2、3、4。`V` 是来自单位聚类事件研究的完整8乘8协方差子矩阵，包括非对角项。`event_study_coefficients.csv` 与 `event_study_covariance.csv` 保留这些结果。HonestDiD 使用 `pre(1/3) post(4/8)` 与 `l_vec(1,0,0,0,0)'`，所以目标是事件时间0的第一个处理后对比。相对幅度运行使用 `delta(rm) method(C-LF)`，网格为 \(\bar M=0,0.25,\ldots,2\)。平滑性运行使用 `delta(sd) method(FLCI)`，网格为 \(M=0,0.025,\ldots,0.2\)。这些是 HonestDiD 的95%稳健区间。原生 `cionly` 图仅画区间条，不呈现新的点估计。

RM 限制以最大的处理前平行趋势偏离为尺度，约束处理后偏离。即使估计了处理前偏离，RM 在 \(\bar M=0\) 时仍施加精确的处理后平行趋势。SD 限制约束偏离斜率的变化；SD 在 \(M=0\) 时允许处理前趋势线性延续，因此不必等于常规区间。增加任一界限均放松限制。本模拟例中，RM 区间在 \(\bar M=0.75\) 时首次包含零；SD 区间在 \(M=0\) 时已包含零。这些是生成样本的性质，不是实证政策发现。

## 运行与验证

在 Windows 的 Stata 19 中，将 Stata 工作目录切换至本目录并运行 `do build.do`。批处理示例为 `StataMP-64.exe -b do build.do`。默认执行日志为 `build.log`，包含 `EVENT_STUDY_N=2880`、`RM_COMPLETE`、`SD_COMPLETE` 及最终 `HONESTDID_BUILD_COMPLETE` 标记。仅构建时使用的数值验证程序检查 CSV、协方差对称性与正定性、本固定示例的敏感性界限、PNG/PDF 文件签名及输出尺寸。成功结果保留在图库验证记录；验证程序与原始日志留在来源 work 档案，不包含于已安装 skill。PNG 已按原始导出尺寸视检标签碰撞、裁切以及不需要的标题/底部说明。

`packages/` 目录包含任务本地的 HonestDiD 1.3.0 Stata ado/帮助文件、Windows OSQP/ECOS 插件、Mata 库，以及 `coefplot` 1.8.8 和其上游 MIT 许可。`build.do` 将这些路径放到 Stata ado 搜索路径前部。没有修改全局 Stata 安装。`dependency_manifest.json` 记录精确哈希、原始安装路径、上游URL及许可状态。Stata 本身须另行提供。随附插件是 Windows 二进制文件；其他系统需要匹配二进制文件，并可能按[官方 HonestDiD 说明](https://github.com/mcaceresb/stata-honestdid#compiling)重新编译。

`schema.md` 描述所有 CSV。`source_metadata.json` 标识方法来源，并明确说明没有复现来源图像或论文图。`portable_files.json` 列出检查与重跑实现所需文件。

统一图名：`event_study_honestdid_sensitivity`
