# A13 · 双维分组效果热图与独立色阶

[English](recipe.md) · [中文](recipe.zh-CN.md)

`bivariate_effect_heatmap` · A13

在两个分组维度的网格上展示已估计结果，分别标示各结果的单位、色档与缺失单元。

分类依据：按规则与裁量分数分组，用估计处理效应与协变量均值计算异质性，再乘企业规模、汇总并除以补贴金额构造成本效果；归实证效应及其派生核算。

标签：异质性, 交互作用, 热图, 成本效果

## 来源与范围

[Making Subsidies Work: Rules versus Discretion (2025)](<https://doi.org/10.3982/ecta21319>); Figure 8; PDF p.25

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在模板目录运行：

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/heatmap.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/heatmap_stata.png" "en" "0"
```

Stata需预先建立输出父目录。Python `--title` 或Stata最后参数 `1` 开启总标题；`zh` 切换中文。坐标为五分位类别，横轴SR、纵轴SD，每面板完整25格；无估计时保留该行并将value留空，不能以0代替，也不能省略整行。

两语言共用十个RGB色档，按各面板独立范围生成边界并统一舍入至12位小数。每档含下界、不含上界，最末档含上界。Python采用阶梯色条，Stata采用逐档图例；统计输入与色档相同，版式并非逐像素相同。

原文两个对象分别为六年企业就业对数变化的处理效应、每10万欧元补贴带来的新增岗位数；同色在不同面板不代表相同数值。估计、企业规模加权岗位数及补贴总额的构造均属于上游分析，脚本只读取已保存结果。图中不画置信区间或显著性星号；原文90%聚类bootstrap区间位于另表，不能从颜色推断。示例完全模拟。

`qa_boundaries_missing.csv`展示色档边界、灰色缺失与真实零值。更换结果时同步修改两脚本的单位、面板ID和色阶范围，不要只改显示文字。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

两面板50格，Python/Stata实际运行中英文、标题和缺失值版本并视检。输入估计值、缺失标记和色档逐格一致；测试每个面板全部11个色档边界，0.125的就业效应归第6档，最大值归第10档。省略坐标行在两语言均被拒绝；空值灰色与数值零分开。

统一图名：`heterogeneity_effect_heatmap`
