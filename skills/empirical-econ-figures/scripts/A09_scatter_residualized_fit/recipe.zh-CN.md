# A09 · 残差散点、拟合线与分组突出

[English](recipe.md) · [中文](recipe.zh-CN.md)

`residualized_scatter_panels` · A09

多面板残差散点、灰色比较组、重点组突出与输入数据计算的拟合线。

分类依据：多面板残差散点、灰色比较组、重点组突出与输入数据计算的拟合线。

标签：残差化, 散点图, 组别突出显示

## 来源与范围

本地参考；原图文献身份未确认; Figure 1

补充相近画法: [Population Aging and Structural Transformation](<https://doi.org/10.3386/w26327>); Figure A6; PDF p.38

截图显示 Figure 1；论文身份待主材料核实

NBER Figure A6 有三个行业行，左列为原始观测、右列为残差化观测，没有突出组别。截图有两个残差面板，突出医学/AI 子集，并比较科研经费与科研产出。不声称截图 Figure 1 出自该 NBER 论文。

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在模板目录中运行，指定项目输出位置：

```shell
python plot.py --input demo.csv --lang en --output YOUR_PROJECT/figures/residual_scatter.png
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/residual_scatter.png" en 0
```

Python `--title` 或 Stata 最后一个参数 `1` 打开整体标题；默认关闭。`zh` 切换中文。两个实现自动导出同名 PDF。

调整自己的两面板与每面板 2–3 组：修改 Python 顶部 PANEL_GROUPS/GROUP_STYLES/TEXT，或 Stata 顶部 panel/group IDs 和标签 locals；主体绘图循环无需改动。模型拟合使用每面板全部显示点，灰色比较组也计入。此模板读取已经残差化的 rx/ry，不替用户选择固定效应或生成残差。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

2026-09-29 通用标签修订：Python 3.12 与 Stata 19 英中四张图均实跑并视检，PNG/PDF 完整。样本仍为 440/200，输入 CSV 哈希未变，两套实现的截距与斜率保持原验收值并一致到六位小数。

统一图名：`scatter_residualized_fit`
