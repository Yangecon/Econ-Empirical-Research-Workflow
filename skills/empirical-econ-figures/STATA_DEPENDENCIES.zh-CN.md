# Stata 依赖与命令变体

[English](STATA_DEPENDENCIES.md) · [中文](STATA_DEPENDENCIES.zh-CN.md)

测试使用 Stata 19。原生 `twoway`、`graph`、数据管理及估计命令随 Stata 提供。下列第三方依赖仅在相应模板或命令变体通过验收后登记。精确文件头、来源、哈希及本地修改保存在 `stata_packages.json` 中。仅有已安装的版本号，不能证明某个具体脚本成功运行。

宿主研究项目统一使用一个 ado 目录。在该次 Stata 会话中，先设置 `sysdir set PLUS "YOUR_PROJECT/stata_packages"`，再安装所需 SSC 包；该设置仅用于本次运行。安装包与绘图是两个独立步骤，画廊不会自动触发安装。请按所选操作说明配置依赖；大部分模板仅需 Stata 原生命令。

交错处理估计器演示包含一份有文档记录的本地 `event_plot` 补丁。不要悄然用上游版本替换后假定行为完全一致；应保留原始源码与补丁记录，或重新执行结果提取和数值检查。Python 绘图依赖仍在共享依赖文件中登记。

| 模板／变体 | 依赖证据 |
|---|---|
| staggered_event_study_estimator_comparison | reghdfe、ftools、csdid、avar、drdid、did_imputation、did_multiplegt_old、eventstudyinteract、event_plot_patched、jwdid、jwdid_estat、jwdid_plot、hdfe；精确记录见 `stata_packages.json` |
| honestdid_sensitivity | honestdid 1.3.0、coefplot 1.8.8、Windows OSQP/ECOS 插件、Mata 库；精确记录见 `stata_packages.json` |
| regression_discontinuity_binned_outcomes / rdplot | rdplot；精确记录见 `stata_packages.json` |
| grouped_coefficient_forest / coefplot | coefplot；精确记录见 `stata_packages.json` |

复制后的技能包和画廊保留这份合并清单，以支持迁移。随包提供资源的清单路径相对于仓库根目录。STATA_PLUS 表示外部 Stata 安装；original-build-record 表示保留在本仓库之外的来源构建记录。画廊条目保留经清理的 JSON/CSV 验证证据。采用新包版本需要新的执行记录，不能在无记录的情况下更新全局安装。
