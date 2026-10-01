# A11 · `coefplot` 包版本

[English](README.md) · [中文](README.zh-CN.md)

这是 Ben Jann 的 `coefplot` 对已验收手工分组系数森林图的替代实现。二者读取同一模拟 CSV 中的给定估计和置信端点，均不估计模型。包文档语法 `coefplot matrix(B), ci((2 3))` 从三个矩阵行分别读取估计、下端点和上端点。代码遵循[作者仓库和帮助](https://github.com/benjann/coefplot)，使用 1.8.8 版本（2025 年 8 月 22 日）。未修改的 ado、帮助及许可证随项目本地 `packages/c` 保存；package_manifest.json（`package_manifest.json`）记录 SHA-256 哈希及来源。未进行全局包安装。

plot_coefplot.do（`plot_coefplot.do`）接收 `input.csv output.png en|zh robustness|subgroup horizontal|vertical 0|1 [package-dir]`。输入和输出必填。run_demo.do（`run_demo.do`）接收模板根目录、**显式输入 CSV 路径**和输出目录。runner 写出英文稳健性与分组 PNG/PDF 图，并生成带标题的英文分组示例。默认无总标题或底部注释；多面板稳健性图保留面板标题，单面板分组图无多余副标题。效应单位、类别标签、零线及分组图例保留。与手工图一致，首选稳健性估计和区间为红色，做法是将首选条目拆成相同位置的第二条 `coefplot` 矩阵序列。

五次原生 Stata 运行均以 `COEFPLOT_COMPLETE` 完成，最终图经过视检。验证文件（`validation.json`）检查 38 条输入（32 条稳健性和六条分组）、一条给定 SE 行的准确区间回退、完整面板/组覆盖、输出文件及终止日志。包接收与手工图相同的数值估计和区间。绘制坐标通过视检核查，未另导出做独立数值坐标比较。示例仍为模拟，不复现来源论文估计。输入约定和矩阵映射见 schema.md（`schema.md`）。

示例图与执行证据存档在图册；安装的 skill 仅包含代码与输入。应向 run_demo.do 显式提供上级模板的 demo.csv。

统一图名：`coefficient_grouped_forest`
