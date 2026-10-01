# A10 · 残差分箱均值与观测层拟合

[English](recipe.md) · [中文](recipe.zh-CN.md)

`residualized_binned_scatter` · A10

以等量分箱均值展示残差关系；拟合线使用全部原始观测，明确分箱排序和并列值规则。

分类依据：分箱均值与拟合关系需要明确输入和聚合规则，与逐观测散点分别整理。

标签：工具变量第一阶段, 残差化, 分箱散点图

## 来源与范围

[Thorsten Rogall, Mobilizing the Masses for Genocide (2021)](<https://doi.org/10.1257/aer.20160999>); Figure 1; PDF p.16

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在本模板目录中运行，指定项目输出路径：

```shell
python plot.py --input demo.csv --bins 50 --lang en --output YOUR_PROJECT/figures/binned_scatter.png
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/binned_scatter.png" en 50 0
```

Python `--title` 或 Stata 最后一个参数 `1` 打开标题；`zh` 切换中文。轴标签在代码顶部配置。两语言均独立生成 bin-summary CSV 和 PNG/PDF。Stata 输出父文件夹应预先存在，日志及箱汇总写入当前工作目录。

本模板接收已经按同一分析样本和控制变量处理的 rx、ry，不自行残差化，不把拟合线称为 IV 估计。分箱规则为按 rx、唯一文本 id 排序后，用 `floor((r-1)*B/N)+1` 分配；并列值可以跨箱。它是明确、可复核的演示规则，不冒称论文作者原代码的并列值算法。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

Python/Stata 中英文四张 PNG 实际执行与视检通过，PDF 已导出。503 行观测分成 50 个箱，每箱 10–11 行；两语言箱计数一致，均值最大差小于 5e-11，观测层 OLS 截距/斜率一致到八位小数。输入包含大量并列 rx，已验证确定性规则。 续作修复首次输出到不存在目录时的失败：EN 默认和 ZH 标题两次 fresh-folder 运行成功，50 个 bin 的导出表与原验收数据逐值一致，503 个观测的 OLS 系数一致。Stata 与统计计算未改。

统一图名：`binscatter_residualized_fit`
