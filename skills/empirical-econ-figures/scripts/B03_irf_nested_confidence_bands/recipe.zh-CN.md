# B03 · 含双层后验区间的脉冲响应矩阵

[English](recipe.md) · [中文](recipe.zh-CN.md)

`impulse_response_matrix_nested_bands` · B03

按响应变量和冲击排列动态中位数及68%/90%后验区间，同一响应行共用纵轴尺度。

分类依据：带 t 分布误差的 SVAR 正交结构冲击及 68%/90% 后验响应区间；不是任意回归动态系数。

标签：脉冲响应, 结构模型, 后验区间带, SVAR, 折线图

## 来源与范围

[Feedbacks, Financial Markets, and Economic Activity (2021)](<https://doi.org/10.1257/aer.20180733>); Figure 1; PDF p.14

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在本模板目录中运行：

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/irf.png --lang en
```

Stata 使用：

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/irf_stata.png" "en" "0"
```

Python `--title` 或 Stata 最后参数 `1` 开启总标题；`zh` 切换中文。冲击列名、响应行名和单位属于必要面板标识，默认保留。修改两份脚本顶部的5×5面板ID、单位和纵轴范围以适应其他系统；各行允许不同单位，但同一行各冲击共用尺度。

浅色/深色分别表示输入的90%/68%后验区间，黑线为中位数。少量指定预测期的点是本模板额外提供的标记：实心表示外层90%后验区间排除零，空心表示包含零。这不等同于频率派显著性检验；原文图本身不使用这层点标记。标记期由脚本中的配置调整。

输入必须包含每一个响应×冲击单元且各单元预测期一致，预测期从0开始；这些IRF不使用事件研究的-1省略期。后验区间和冲击尺度由上游模型生成；脚本不能从此图推断模型识别、估计后验或生成p值。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

525行模拟后验汇总、25面板。Python/Stata中英文均实际执行并视检，数值最大差为0，外层区间排除零的行数均为331。48个月终点的425行变体数值亦一致，Stata刻度0/24/48已视检；多余未知单元按预期返回r(9)。另检查完整矩阵、共同预测期网格、区间嵌套和逐行尺度边界；不重估VAR或后验。

统一图名：`irf_nested_confidence_bands`
