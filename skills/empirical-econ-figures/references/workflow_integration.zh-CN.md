# 图形 skill 接入

[English](workflow_integration.md) · [中文](workflow_integration.zh-CN.md)

Workflow 现包含 [empirical-econ-figures](../README.zh-CN.md)：50 个已验收条目、40 个归并目标。先浏览 [PNG 画廊](https://github.com/Yangecon/Econ-Empirical-Research-Workflow/blob/main/gallery/empirical-econ-figures/README.zh-CN.md)，再按图中数字来源、方法和现有输入选择模板。A 为约化式、B 结构、C summary、D research design、E 预测与算法评估；图形几何、heterogeneity 和 robustness 用标签表达。

## 估计—绘图—draft

| 任务 | 负责 skill | 项目产物 |
|---|---|---|
| 构造样本、估计并导出结果 | research-empirics / empirical-analysis-stata | data、code、output/raw |
| 选择模板并保留推断规则 | empirical-econ-figures | code/03_figures.do 或项目绘图入口、output/figures、notes/figure_log.csv |
| 标题、来源、统计注释与资产同步 | research-writing / output-draft-overleaf-sync | draft/images、draft/figures、draft/main.tex |

已有观测或保存估计的独立绘图请求可以直接调用绘图 skill。出图本身不冻结识别设计，也不代表全部 output ready。缺少估计或协方差时回到估计步骤。探索性的样本诊断按宿主规则先保存在 `work/<slug>/`，再决定是否纳入正式输出。

整个研究项目统一一个 Python 环境。在仓库中执行 `python -m pip install -r requirements-figures.txt`；安装后的独立 skill 使用其 `requirements.txt`，仍装入同一项目环境。Stata 包版本见 skill 的依赖页；绘图不会自动安装或更新全局 ado 包。

在仓库根目录筛选模板：

```shell
python scripts/figure_catalog.py --category reduced_form --tag "Event study"
python scripts/figure_catalog.py --id A01 --json
python scripts/figure_catalog.py --category summary --code-language python
```

目录工具只展示已支持接口，不提供万能绘图命令。读所选 recipe 的输入和参数。独立安装 skill 时，没有仓库辅助工具也可以直接读 `references/catalog.json` 与 `figure_naming.json`。将选中的脚本和必要辅助文件复制到项目，或用明确路径调用安装脚本。共享折线渲染器需要保留相邻的 `scripts/_shared` 目录。

## 可运行的 A01 示例

```shell
python skills/empirical-econ-figures/scripts/A01_event_study_pre_post_averages/event_study_with_pre_post_averages.py --output YOUR_PROJECT/work/figure_demo
```

替换 YOUR_PROJECT，含空格的路径加引号。Python 会实际估计随包的 980 行模拟面板，Stata demo 模式从同一面板独立估计。−1 保持空心归一化零值，并计入前期六期的分母；在本例平衡面板同期处理设定下，后期八期均值减前均值等于静态 DID。对比区间用完整协方差；此等式不直接推广到其他设定，示例值不能作为项目实证结果。

A03 实际运行包括 jwdid 的六种 Stata 交错 DID 估计器，导出系数供 Python 重绘。A04 用 Stata HonestDiD 生成相对幅度和光滑性约束区间。按相应 recipe 操作，不得假设系数，也不能将敏感性区间中点解释为新的稳健点估计。

## 发表约定与验证

默认英文标签、无总标题和底部 notes，可显式开启标题。保留坐标、单位、面板标签和图例。在图外记录估计器、estimand、样本、权重、基准期、聚类、协方差与区间含义。文献来源和统计注释放在 draft；参考论文提供画法灵感，不是项目数值的数据来源。

画廊含 97 张英文生成 PNG、56 张原文/原始参考 PNG 和可点击的双语总览，示例图与参考图分列。代码集中保存在 skill；论文完整 PDF 继续保存在本地材料归档。第三方组件继续保留各自声明，见 skill 的许可页；根 workflow 的许可不替代这些署名和第三方边界。

执行 `python scripts/validate_figures.py --smoke --output-dir YOUR_PROJECT/work/figure_validation`，检查目录路径、双语文档、PNG 包装和哈希清单，并运行 A01、共享折线及已保存估计的重绘示例；同时验证目录筛选与语言不可用的情况。CI 不声称重新运行 Stata；保留的来源验证区分了实际 Stata 运行和仅静态检查的包命令入口。
