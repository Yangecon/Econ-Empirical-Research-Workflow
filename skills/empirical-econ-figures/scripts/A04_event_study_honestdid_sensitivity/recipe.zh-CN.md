# A04 · 平行趋势敏感性区间：相对幅度与平滑性限制

[English](recipe.md) · [中文](recipe.zh-CN.md)

`honestdid_sensitivity` · A04

模拟面板实际估计事件研究及完整协方差；honestdid 分别计算相对幅度和二阶差分平滑性限制下的95%稳健区间，再调用原生 coefplot 选项成图。

分类依据：模拟单位×时间数据，实际估计事件研究 b 与完整 V，再由 honestdid 计算两类限制下目标处理后效应的稳健区间。Stata 命令原生绘图；不手填系数、不把稳健区间中点当作新的效应估计。

标签：DID, 事件研究, 稳健性, 敏感性, 平行趋势, 置信区间, honestdid, 相对幅度, 光滑性

## 来源与范围

[Rambachan and Roth, A More Credible Approach to Parallel Trends (2023)](<https://doi.org/10.1093/restud/rdad018>); 方法文献

补充参考: [Rambachan and Roth (2023), A More Credible Approach to Parallel Trends](<https://doi.org/10.1093/restud/rdad018>); Figure 5; PDF p.31

补充参考: [Rambachan and Roth (2023), A More Credible Approach to Parallel Trends](<https://doi.org/10.1093/restud/rdad018>); Figure 7; PDF p.33

方法来源为 Rambachan–Roth 论文与 HonestDiD 作者命令文档；不对应指定论文 Figure，不附伪造原图。

发表论文中的示例采用不同数据和目标效应；现有模板仍是模拟数据演示。

发表论文中的示例采用不同数据和目标效应；现有模板仍是模拟数据演示。

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

把模板复制到研究项目 work 子目录，在 Stata 中运行：

```stata
do "YOUR_PROJECT/honestdid_sensitivity/build.do" "YOUR_PROJECT/honestdid_sensitivity"
```

从模拟数据生成、固定效应事件研究估计到两类敏感性区间与成图均由 Stata 实际运行。可选标题及独立文件名：

```stata
do "YOUR_PROJECT/honestdid_sensitivity/build.do" "YOUR_PROJECT/honestdid_sensitivity" "Sensitivity analysis" "_titled"
```

读取 schema.md 与 README.md；两张图分别为 honestdid_relative_magnitude 和 honestdid_smoothness。默认无整体标题与底部 notes。不要在已安装 skill 目录运行，以免把输出写回 skill。

本项按用户明确要求仅提供 Stata；CSV 保存真实区间，可供未来 Python 重绘。M与M-bar不可混用，SD的M=0与Original区间不是同一假设。示例目标为第一个处理后效应，替换为平均效应时须修改 l_vec 并保留完整协方差。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

Stata19在320单位×9期模拟面板实际执行xtreg与honestdid；参考期-1，完整8×8单位聚类协方差，目标为k=0。RM/SD各9个限制值与1条Original常规区间；日志成功标记、数值范围/协方差/区间及可选标题检查通过，主agent视检通过。使用已测试HonestDiD1.3.0和Windows插件；未声称验证其他平台或最新版本。

统一图名：`event_study_honestdid_sensitivity`
