# A05 · `rdplot` 包版本

[English](README.md) · [中文](README.zh-CN.md)

这是已验收手工双面板模拟 RD 图的 Stata `rdplot` 替代版本。它读取同一显式输入 CSV，使用断点 0、均匀核一阶拟合，Outcome A 和 B 的左右带宽分别固定为 16 和 25，每侧十个等距箱。窗口和箱数是示意选择，不是数据驱动带宽或推断性 RD 估计。语法遵循[作者的 Stata 示例](https://github.com/rdpackages/rdrobust/blob/main/stata/rdplot_illustration.do)。实际运行 `rdplot` 版本为 11.1.0（2026 年 5 月 22 日）；源文件哈希见 package_manifest.json（`package_manifest.json`）。命令来自既有 Stata PLUS，本任务未进行全局安装。可移植环境应将官方 `rdrobust` 套件安装到项目本地 ado 目录，并将该目录传给 runner。

runner 仅生成英文图：`rdplot_en.png` 保留面板标题，但无总标题或底部注释；`rdplot_en_title.png` 示范标题选项。旧验证曾检查中文版，但当前 demo runner 不再生成，画廊也不再收录。代码为 plot_rdplot.do（`plot_rdplot.do`）；run_demo.do（`run_demo.do`）接收模板根目录、**显式输入 CSV 路径**、输出目录和可选本地 ado 目录。绘图文件本身接收 `input.csv output.png en|zh 0|1`。

包版本每面板导出一个分箱表（`*_rdplot_bins.csv`），另导出四行的侧别拟合表（`*_rdplot_fits.csv`）。此模拟示例的 40 个包分箱与手工 Stata 版的箱计数及 x/y 样本均值一致，均值最大差为 `2.14e-14`。四条侧别拟合的截距、斜率及范围均在 `3.11e-15` 内一致。`rdplot` 显示**箱中点**，手工图显示每箱**运行变量样本均值**；本例横坐标最大差为 `0.104`。因此即使成员和均值一致，图中点仍会有水平位置差异。两图均为描述性，不提供 RD 置信区间或因果推断。验证文件（`validation.json`）记录数值比较，schema.md（`schema.md`）说明生成列。

四份最终 Stata 日志与验证日志（`validation.log`）含完成标记。中英文默认版和标题版均经视检。结果使用模拟观测，不是来源论文数据。

示例图与执行证据存档在图册；安装的 skill 仅包含代码与输入。应向 run_demo.do 显式提供上级模板的 demo.csv。

统一图名：`rd_binned_outcomes`
