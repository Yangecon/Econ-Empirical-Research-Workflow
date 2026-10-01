# C17 · 地理分区着色图

[English](recipe.md) · [中文](recipe.zh-CN.md)

`geographic_choropleth` · C17

真实现代行政区 GeoJSON 与显式区域ID数值匹配，使用共同分箱并区分无数据；演示值为模拟。

分类依据：原图呈现地理分区的医疗巡诊记录等观测信息。通用地图接口已用真实2016年喀麦隆行政区及模拟值验证；演示行政区不是论文历史族群边界，原文边界和数值仍未取得。

标签：地理, 分级设色图, 空间覆盖

## 来源与范围

[The Legacy of Colonial Medicine in Central Africa (2021)](<https://doi.org/10.1257/aer.20180284>); Figure 2; PDF p.12

补充参考: [Eric Yongchen Zou, Unwatched Pollution: The Effect of Intermittent Monitoring on Air Quality (2021)](<https://doi.org/10.1257/aer.20181346>); Figure 7; PDF p.20

论文图注与页图已核对；通用画法演示使用另一套真实现代行政区和模拟值，不复现论文历史边界或数值。边界来源与许可随模板保存。

全部示例数值为模拟数据；替换输入时保留文档说明的统计解释。

## 输入

[输入规范](<schema.zh-CN.md>)

## 运行

仅生成英文图，不再同时绘制中文版；说明文档保留中英文。

在模板目录运行，下列输出目录应属于研究项目：

```shell
python plot.py demo_region_values.csv YOUR_PROJECT/figures/map.png --bins 0 2 4 6 8 10 --legend-title "Synthetic index"
```

`--title "标题"` 显式开启标题，默认无标题/底部notes。字段、统计对象及显示限制见schema.md。地图请保留ATTRIBUTION.md中的边界来源和许可；不要把地理演示数据当作论文数据。

将 YOUR_PROJECT 替换为研究项目路径；含空格的路径加引号。默认输出无整体标题和底部注释。

## 验证

已核10个真实区域、唯一ID匹配、未知/重复ID拒绝、缺失值斜线及多边形孔洞像素测试。喀麦隆2016行政区与论文历史族群边界不同；模拟值不复现论文结果。本地等距圆柱近似仅供显示，不用于距离/面积推断，范围限制见schema。 Python已实跑，主agent已视检；绘图示例不等于原论文数值复现。

统一图名：`map_geographic_choropleth`
