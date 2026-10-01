# C06 · 跨面板统一面积尺度的联合频数气泡图

[English](recipe.md) · [中文](recipe.zh-CN.md)

`joint_frequency_bubble_panels` · C06

以二维取值对的频数控制气泡面积，跨轮次共用同一尺度，另外标出给定理论基准点。

分类依据：个体实验回答的两个信念维度组成联合频数，气泡面积表示人数；图中的理论基准点不把观测频数变成结构估计。

标签：联合频数, 气泡面积, 共同尺度

## 来源与范围

[Mental Models and Learning: The Case of Base-Rate Neglect (2024)](<https://doi.org/10.1257/aer.20201004>); Figure 3: Density Plots for Primitives; PDF p.13

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在模板目录运行：

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/joint_frequency.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/joint_frequency_stata.png" "en" "0"
```

Stata输出父目录需预先存在。Python `--title` 或Stata末尾参数 `1` 开启总标题；`zh` 使用中文。默认无总标题和底部notes，保留轮次面板名称。

输入bubble行的count为二维坐标对的非负整数频数；benchmark行是给定理论基准坐标且count留空。两个轮次使用全体气泡共同的最大频数，直径为 `27*sqrt(count/max_count)` 打印点数，面积因此与频数成正比。Stata直径保留8位小数，存在极小舍入；checked CSV核对的是目标面积比，不是像素面积测量。零频数不画，缺失频数报错，不做面板内独立归一化。

原图x为负信号下的条件信念，y为正信号下的条件信念，单位百分比；个体信念按3的倍数取整并计数属于上游处理。只参考Figure 3，原页同时含Figure 4但未据此增加第二套代码。理论基准坐标需研究者给定，模板不重新估计或推导信念模型。全部例子为模拟值。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

29行模拟输入，跨面板最大频数60，两种实现面积比最大数值差5.56e-17，2条零频数保留而不绘制；缺失频数在两语言实际被拒绝。中英文及标题版实际运行，默认成图经视检；源Figure 3及图注核对通过。

统一图名：`bubble_joint_frequencies`
