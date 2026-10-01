# A19 · 门槛附近的扎堆分布与给定反事实

[English](recipe.md) · [中文](recipe.zh-CN.md)

`bunching_distribution_with_counterfactual` · A19

比较税收跳跃门槛附近的观测人数和给定反事实分布，并标明反事实估计的排除区间。

分类依据：观测财富频数加排除扎堆区间后五阶多项式估计的反事实密度。主图所选层并非结构效用模型模拟；论文把额外参数化结构弹性另放附录。

标签：扎堆, 跳跃阈值, 反事实密度, 非结构估计

## 来源与范围

[Behavioural Responses to Wealth Taxation: Evidence from Colombia (2025)](<https://doi.org/10.1093/restud/rdae076>); Figure 3(a); PDF p.11

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在模板目录运行：

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/bunching.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/bunching_stata.png" "en" "0"
```

Stata需预先建立输出父目录。Python `--title` 或Stata最后参数 `1` 开启总标题；`zh` 切换中文。默认无总标题和底部notes。

输入是按横轴递增的等宽分箱中心、非负观测人数与给定反事实人数。脚本顶部同步修改门槛、排除区间上下界及轴标签。示例门槛1000、排除区间[880,1200]、宽度10，数值均为模拟演示；运行变量单位须由使用者明确。

来源只复现 Figure 3(a) 的绘图层。原文横轴为2010年百万哥伦比亚比索，纵轴为每1000万比索分箱的纳税人数，反事实由排除区外五次多项式拟合产生。本代码读取反事实，不估计它；不实现原图其他三个面板。

人数、归一化份额和密度不能混用。原文b是超额质量相对反事实平均高度的统计量，a*是支配区未扎堆比例；模板不计算或显示它们、弹性、边际扎堆者、支配区边界或相关标准误。跳跃门槛notch不同于斜率折点kink，图本身不是RDD估计或密度连续性检验。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

100个等宽分箱，Python与Stata导出数值完全一致；两语言实际拒绝负人数与不等宽分箱。英中默认与可选标题版本实际运行并视检；主agent要求修正notch中文和排除边界图例后再次核对成图。

统一图名：`bunching_counterfactual_distribution`
