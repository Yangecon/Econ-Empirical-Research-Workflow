# C11 · 按时间连接的分阶段双变量轨迹

[English](recipe.md) · [中文](recipe.zh-CN.md)

`time_encoded_phase_path` · C11

以两个已给定变量为坐标，按年份连接并以阶段灰阶和年份标注编码历史路径。

分类依据：横轴历史人口、纵轴实际工资，按年份连接；虽然后文据此估计劳动需求模型，这张 Figure II 本身展示数据关系。

标签：时间路径, 阶段轨迹, 趋势, 阶段路径, 测量, 折线图

## 来源与范围

[When Did Growth Begin? New Estimates of Productivity Growth in England from 1250 to 1870 (2025)](<https://doi.org/10.1093/qje/qjae046>); Figure II: Real Wages and Population; PDF p.5

原始页图与 PDF 图注已核对；仅以模拟数据演示画法

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在模板目录运行：

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/phase_path.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/phase_path_stata.png" "en" "0"
```

Stata需预先创建输出目录。Python `--title` 或Stata最后参数 `1` 开启标题；`zh` 使用中文，默认无标题和底部notes。

严格按递增年份连接，不能按横轴排序；跨阶段线段归入新阶段。输入x/y已经是显示尺度，原例为人口对数与实际工资对数，脚本不会再取log。原文人口来自模型估计，绘图使用上游给定坐标，不重新估计历史人口或拟合关系。阶段配置为early/middle/late，每阶段至少两个连续点。全部示例数值为模拟值。

共享绘图依赖：保持本目录与相邻 `_shared/line_geometry.py` 的关系；复制到研究项目时同时复制共享模块。导入按脚本位置解析，可从不同工作目录运行。共享模块只画给定折线或右连续阶梯，归一化、累计份额、拟合区间、风险集与 Greenwood 区间仍由各适配器处理。

自定义系列／阶段及轴单位时使用随附 JSON；默认不传 `--config` 则兼容原示例：

```shell
python plot.py --input custom_demo.csv --config custom_config.json --output YOUR_PROJECT/figures/custom.png --lang en
```

`--lang zh` 使用中文标签，`--title` 显示配置中的标题。此配置扩展仅限 Python；若本项保留 Stata，其入口仍按原 schema 运行。C10 的有限非负值、日期和明确基期规则保留；C11 按年份顺序连线，不能按横坐标重新排序。


将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

20个模拟年份，双语言中英文输出数值完全一致，保留横轴逆行。两语言拒绝年份乱序及非连续重复阶段。默认图和标题版本实际运行，默认图经视检；主验收补充了标注年份的整数检查和额外CSV列兼容。 续作共享折线／阶梯几何后，从不同工作目录重跑，默认导出坐标与原验收结果在1e-10容差内一致；统计适配保留，F38条形不变。 已执行外部系列/阶段ID、中文标签及可选标题示例，非法值或阶段/年份顺序输入会拒绝。

统一图名：`line_time_encoded_phase_path`
