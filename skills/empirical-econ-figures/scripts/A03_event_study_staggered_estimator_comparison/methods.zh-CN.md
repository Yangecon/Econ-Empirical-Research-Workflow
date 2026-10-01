# 分期处理事件研究估计器比较

[English](methods.md) · [中文](methods.zh-CN.md)

本目录为已实际执行的**模拟面板演示**，画法参考 Braghieri, Levy, and Makarin 的 *Social Media and Mental Health* Figure 2（[AER 论文](https://doi.org/10.1257/aer.20211218)）。它**不**复现该论文的估计或样本。本地来源审查未取得原始分析 do-files；已定位[官方档案](https://doi.org/10.3886/E175582V1)，但未获取分析文件。五种估计路线遵循 [Borusyak 的方法作者示例](https://github.com/borusyak/did_imputation/blob/main/five_estimators_example.do)；第六种使用作者维护的 [`jwdid`](https://github.com/friosavila/stpackages/tree/main/jwdid)。

## 结果

`estimate_all.do` 在同一个设定随机种子的300单位 × 15期模拟面板上运行六种实际 Stata 估计器：`reghdfe`、`did_imputation`、`eventstudyinteract`、`csdid` 后接 `estat event`、`did_multiplegt_old`，以及 `jwdid` 后接 `estat event`。处理开始于第10–16期。结果变量包含单位与时间分量、随日历时期变化的处理效应及正态噪声。命令和数据定义见 do-file。有意采用旧版 de Chaisemartin–d'Haultfoeuille 命令：当前 `did_multiplegt` 是语法已改变的包装命令，而方法作者示例使用历史动态路线。本演示在该路线使用设定种子的199次 bootstrap 重复。

输出 audited_estimates.csv（`audited_estimates.csv`）含61行：44条处理后或常规提前项估计、10条其他处理前趋势检验、5条动态安慰剂检验，以及2条归一化参考标记。总体显示事件时间−5至+5。`jwdid` 提供0至+5共六个处理后值。**共同绘图表**中的全部逐点95%区间使用 `b ± invnormal(.975) × se`；这使绘图器可比较，但 TWFE 表的区间是正态近似，而非其命令报告的 t 分布区间。动态估计器的 `se` 来自单位聚类 bootstrap 方差；`jwdid` 基于单位聚类拟合报告 delta 方法事件标准误。实心符号表示绘图区间不含零；空心符号表示含零或省略参考期。颜色和形状标识估计器。

| 估计器 | 处理前时期解释 | 参考期及远期提前项 |
|---|---|---|
| TWFE OLS | 估计的提前项系数 | −1归一化；`K <= -6` 作为一个干扰分箱纳入，因此更早时期不会悄悄归入参考期。 |
| Sun–Abraham | 交互加权提前项系数 | −1归一化；设定纳入−2至−14提前项，由最后处理队列提供对照。 |
| Callaway–Sant’Anna | 来自 `estat event` 的处理前趋势对比 | −1期 `Tm1` 是对比，不是强制零值。 |
| de Chaisemartin–d’Haultfoeuille | `Placebo_1` 至 `Placebo_5` | −1值是安慰剂检验，不是强制零值。 |
| Borusyak–Jaravel–Spiess | `pre1` 至 `pre5` 插补处理前趋势检验 | −1值是检验，不是强制零值。 |
| Wooldridge `jwdid` | 在此所有单位最终均处理的面板上，默认尚未处理对照不输出处理前时期 | `estat event, window(0 5)` 仅提供处理后 ATT；不添加−1符号。 |

61行**不是**61个定义相同的动态 ATT 估计。显示支持范围和各命令可取得的 `e(N)` 见 estimator_support.csv（`estimator_support.csv`）。`csdid` 和 `did_multiplegt_old` 在导出的估计状态中未返回 `e(N)`，因此该字段保留缺失。完整输入有4,500单位—时期行；各期限的估计器特定人数并非一致可得，不从原始相对时间人数推算。未来真实数据提取中缺席的期限应继续缺席，不补零。完整 `jwdid` 事件协方差矩阵按0–5事件顺序保存在 jwdid_event_covariance.csv（`jwdid_event_covariance.csv`）。

## 图形与一致性

- Stata 手工 twoway PNG（`staggered_comparison_stata.png`）与 PDF（`staggered_comparison_stata.pdf`）来自 `plot_twoway.do`。可复用 `plot_staggered_twoway` 程序接受 `input()`、`output()` 及可选 `title()`；`run_plot_twoway.do` 是项目运行入口。
- Python PNG（`staggered_comparison_python.png`）与 PDF（`staggered_comparison_python.pdf`）来自 `plot_python.py`，读取**同一份 Stata 导出 CSV**，接受可选 `--title`。不执行独立的 Python 估计。
- `event_plot` 组合 PNG（`staggered_comparison_event_plot_hybrid.png`）与 PDF（`staggered_comparison_event_plot_hybrid.pdf`）来自 `plot_event_plot.do`。`event_plot` 解析全部六套系数/方差矩阵，通过 `savecoef noplot` 生成坐标和区间；原生 `twoway` 图层再实现同一估计器内的实心/空心显著性规则。event_plot_extracted.csv（`event_plot_extracted.csv`）保留包的输出。2021版包的直接绘图器每个序列只有一种符号样式，因此最终显著性编码使用原生图层。

三张已验收图默认均无标题和底部说明。论文图的配套图注须解释模拟样本、各估计器处理前时期的不同含义、−1标记、单位聚类、95%逐点区间及不同的估计目标。来源论文的处理后支持仅为0–2；本模拟窗口延伸到+5，不扩展该论文的证据。

验证报告（`validation.json`）将全部59条估计/检验行与组合 `event_plot` 提取比较，并检查两条省略参考行及完成标记。实际系数和区间差异见报告。重新生成后的最终手工、Python 和组合 PNG 均进行了裁切与图例重叠视检。

## 重跑与依赖

在 Stata 19 中切换至本模板目录，依次运行 `estimate_all.do`、`run_plot_twoway.do` 和 `plot_event_plot.do`。若 Stata 工作目录在其他位置，每个 do-file 均接受本目录绝对路径作为首个参数。`run_plot_twoway.do` 另外接受输入 CSV、输出文件名前缀及可选标题；`plot_event_plot.do` 接受输入 CSV、输出文件名前缀、可选标题及提取 CSV 路径。估计 do-file 先写出设定种子的面板及审计表，绘图器随后读取。使用共享 Python 环境运行 `plot_python.py`。仅构建时使用的验证代码及完整日志保留在原始 work 档案；图库验证记录包含数值检查。已保存的 `audited_estimates.csv` 支持只重绘、不重估计。

全部绘图器根据实际存在的整数事件时间确定横轴范围。估计器可以缺少某个期限；矩阵和图均不以零补齐。输入约定要求恰好两条归一化参考（TWFE 和 Sun–Abraham 的−1期）、其他行均有正标准误，以及与给定估计和标准误一致的95%正态区间。归档的便携性检查（`portability_check.json`）属于此前五估计器版本，尚未针对本扩展重跑。

项目本地 `packages/` 包含 `avar`、`drdid`、`did_imputation`、`eventstudyinteract` 和 `did_multiplegt_old` 的 SSC 副本，附带其提供的帮助文件。作者维护的 `jwdid` 源码和帮助文件位于 `packages/j`；`packages/h` 下本地 `hdfe.ado` 副本满足依赖检查。`avar` 调用 `livreg2.mlib` Mata 库；估计运行入口通过 `packages/l` 暴露随附副本。记录执行时，既有 Stata PLUS 还安装了 `ivreg2`，因此未独立验证缺少该安装时的便携性。记录运行所用 `reghdfe`、`ftools` 和 `csdid` 来自既有 Stata PLUS；其他 Stata 环境应在项目本地 PLUS 目录安装。组合版本使用方法作者 [`event_plot.ado`](https://github.com/borusyak/did_imputation/blob/main/event_plot.ado) 的本地副本，并对无活动 `e()` 状态的纯矩阵调用及缺失的带索引系数宏作两处明确记录的局部修复。未修改的已安装副本、当前 GitHub 副本、帮助文件和上游 GPL-3.0 许可均保存在补丁文件旁。dependency_manifest.json（`dependency_manifest.json`）记录来源路径、已声明版本及 SHA-256；event_plot_patch.md（`event_plot_patch.md`）记录补丁。此任务未进行全局 Stata 包安装。

执行证据：当前估计日志（`estimate_all.log`）以 `STAGGERED_ESTIMATION_COMPLETE` 和 `AUDITED_ESTIMATE_ROWS=61` 结束。当前手工 Stata 日志（`run_plot_twoway.log`）、组合日志（`plot_event_plot.log`）、Python 日志（`plot_python.log`）与验证日志（`validation.log`）均有完成标记且无终止 Stata 错误码。验证（`validation.json`）将全部59条包提取的非参考行与审计后的 Stata 表比较。便携 do-files 默认使用当前模板目录。


事件时间 −1 的归一化基准用空心圆点显示，不绘制置信区间；它不是估计效应，也不计入处理前后均值。
