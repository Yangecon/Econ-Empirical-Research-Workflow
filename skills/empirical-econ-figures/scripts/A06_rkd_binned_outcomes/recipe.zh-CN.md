# A06 · 回归折点：多结果分箱与连续拟合

[English](recipe.md) · [中文](recipe.zh-CN.md)

`threshold_binned_regression_panels` · A06

在同一政策阈值两侧展示多种结果的分箱均值，用连续分段线性拟合显示斜率变化。

分类依据：已核对Landais Figure7图注：日工资850瑞典克朗处的回归折点，包含替代率规则与参保选择、风险面板。保留斜率改变和水平跳跃的区别；上游残差化与识别不由绘图代替。

标签：RKD, 阈值, 分箱散点图

## 来源与范围

[Risk-Based Selection in Unemployment Insurance: Evidence and Implications (2021)](<https://doi.org/10.1257/aer.20180820>); Figure 7; PDF p.30

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在本模板目录中运行：

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/kink.png --lang en
```

Stata 使用：

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/kink_stata.png" "en" "0"
```

Python `--title` 或 Stata 最后参数 `1` 开启总标题，`zh` 切换中文。同步修改两脚本的阈值、窗口、面板ID、单位、箱数、显示范围和坐标刻度。默认阈值850、窗口[500,1200]、每侧12箱；四种结果使用独立纵轴，不能直接比较线段的视觉陡峭程度。

拟合在所有窗口内观测上独立于分箱进行，模型为 `y = a + b*(x-c) + d*max(x-c,0)`，左斜率为b，右斜率为b+d，阈值处共同水平为a。因此这是连续折点图，不是允许水平跳跃的断点图。分箱仅用于显示均值；空心点属于该图的散点样式，不编码显著性，因为没有显示区间。

原文来源仅为AER2021的Figure 7。其投保结果做过协变量调整，并有350SEK带宽下的模型估计和标准误；本模板不执行原文残差化或推断，也不复现其数值。可提供明确记录过上游调整的结果，但必须同时调整单位、显示范围和样本说明。输出CSV保存分箱、拟合系数及样本计数；图中斜率变化本身不证明因果识别。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

17,600行模拟数据、96个分箱和4个连续折点拟合，Python/Stata中英文均实际执行并视检，CSV数值最大差4.60e-9以内。两语言一致接受各面板左侧24行/右侧48行的非对称样本，少一行按预期拒绝；另检查端点、阈值右侧归属、满秩和显示范围。

统一图名：`rkd_binned_outcomes`
