# B01 · 情景与分组累计分布比较

[English](recipe.md) · [中文](recipe.zh-CN.md)

`scenario_cdf_panels` · B01

按情景分面，以不同线型比较组别的累计分布；明确区分横轴结果变量、CDF 与模型情景假设。

分类依据：两阶段注意/离散计划选择模型 V，改变注意概率和 switching costs，模拟 overspending 改变的 CDF。

标签：反事实, 累积分布函数, 情景比较, 折线图

## 来源与范围

[Heiss et al., Inattention and Switching Costs as Sources of Inertia in Medicare Part D (2021)](<https://doi.org/10.1257/aer.20170471>); Figure 10; PDF p.40

页图与 PDF 图注已核对；原图为 Model V 反事实减少超额支出的经验累计分布，非注意力概率

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在本模板目录中运行：

```shell
python plot.py --input demo.csv --lang en --output YOUR_PROJECT/figures/scenario_cdf.png
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/scenario_cdf.png" en 0
```

Python `--title` 或 Stata 最后一个参数 `1` 开启整体标题；`zh` 切换中文。自动导出同名 PDF。修改代码顶部面板/组别 IDs 和中英文标签，适配两个情景、每情景三条曲线。横轴排序由数值决定，不能把 CDF 当成普通无序折线。

输入为已计算的累计分布点；代码不估计结构模型或自行构造政策反事实。原论文比较低、中、高 acuity 三组，在强制注意与取消切换成本两种情景下减少的超额支出；本示例曲线仅说明画法。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

Python 3.12 与 Stata 19 的中英文四张 PNG 均实际执行并视检，另导出 PDF。共同 CSV 有 966 行，即 2 面板×3 组×161 个横轴点；每条曲线检查唯一横轴、CDF 范围及单调性。

统一图名：`counterfactual_cdf_panels`
