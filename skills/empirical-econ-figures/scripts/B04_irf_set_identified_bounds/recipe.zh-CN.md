# B04 · 集合识别的动态响应边界与代表路径

[English](recipe.md) · [中文](recipe.zh-CN.md)

`set_identified_impulse_response_bounds` · B04

分别画出各期限的可容许响应上下界、逐期中位数和给定的maxG代表路径。

分类依据：事件限制 panel VAR 从约化式协方差中筛选结构冲击响应矩阵，画 admissible set 边界；不是置信带。

标签：脉冲响应, 部分识别, 识别边界, SVAR, 折线图

## 来源与范围

[Using Disasters to Estimate the Impact of Uncertainty (2024)](<https://doi.org/10.1093/restud/rdad036>); Figure 3; PDF p.20

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在模板目录运行：

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/set_bounds.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/set_bounds_stata.png" "en" "0"
```

Stata需预先建立输出父目录。Python `--title` 或Stata最后参数 `1` 开启总标题；`zh` 切换中文。默认无总标题和底部notes。

蓝线是逐期可容许响应集合的最小值和最大值；绿叉是逐期中位数，红色空心圆是给定maxG路径。这里没有置信区间或后验区间，标记形状用于区分路径，不作显著性编码。

输入期限唯一且严格递增，两个代表序列逐期位于上下界内。逐期中位数组成的连线未必对应同一个共同可行结构解；maxG的可行性和限制条件必须在上游验证，绘图不重新求解VAR、事件限制或最大化问题。

来源的第1期是冲击当期；示例包含第1至15期，轴上明确标出冲击时点。换为从0开始或不同单位的期限时，同步修改两脚本标签。GDP同比增速响应以百分点表示。全部示例值为模拟数据，边界排除零不能当作抽样置信区间排除零来解释。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

15个期限，中英文两版本的Python与Stata输出数值完全一致。两语言实际拒绝超出可容许边界的中位数及乱序期限。默认中英文和标题版本运行通过，默认图经视检；修正横轴以明确第1期为冲击当期。

统一图名：`irf_set_identified_bounds`
