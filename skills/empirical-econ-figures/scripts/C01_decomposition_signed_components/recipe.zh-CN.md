# C01 · 有符号分量堆叠与代数分解

[English](recipe.md) · [中文](recipe.zh-CN.md)

`signed_component_decomposition` · C01

沿分箱横轴显示正负分量；正值与负值分别堆叠，并核对分量之和等于总量。

分类依据：产品价格和销售份额构造相对价格，劳动生产率部分由相对销售/劳动减价格部分得到；展示数据中的横截面核算关系，不用结构估计参数生成该图。

标签：分解, 有符号组成项, 会计恒等式, 会计分解, 堆叠柱状图

## 来源与范围

[The Micro-Level Anatomy of the Labor Share Decline (2021)](<https://doi.org/10.1093/qje/qjab002>); Figure VIII; PDF p.37

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在模板目录运行：

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/decomposition.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/decomposition_stata.png" "en" "0"
```

Stata需预先建立输出父目录。Python `--title` 或Stata最后参数 `1` 开启总标题；`zh` 切换中文。默认无总标题和底部notes。

每行是一个劳动份额分箱；分箱等宽、连续且位于[0,1]。相对价格、相对实物劳动生产率和相对人均销售额使用同一相对对数单位，并满足价格加生产率等于销售额。示例使用模拟值，只读取并核对这三个预计算变量，不复现上游估计。

正负分量分别从零轴向上、向下堆叠。代数总量可能处于两个堆叠端点之间；不能把它当作100%构成图，也不能用最上端柱高代替总量。导出的 `_checked.csv` 保留各分量上下端点和原始总量。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

20个连续等宽分箱；Python与Stata中英文及标题版本实际运行并视检，数值最大差1.11e-16。另检查价格负而生产率正的反向混合符号，Stata拒绝不满足加总恒等式的输入；Python拒绝分箱间隙、不等宽及超出[0,1]。

统一图名：`decomposition_signed_components`
