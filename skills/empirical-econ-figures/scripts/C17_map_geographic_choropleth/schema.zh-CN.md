# 输入结构

[English](schema.md) · [中文](schema.zh-CN.md)

数值 CSV：`shapeID`（唯一非空字符串，匹配 GeoJSON 中的ID）、`value`（有限数值，或空值表示无数据）。允许缺失区域行，其显示为无数据；未知或重复ID报错。所有已观测值须位于显式提供的 `--bins` 边界内；边界须为有限、一维、严格递增的序列，至少三个。

几何：GeoJSON FeatureCollection，要求 `crs.properties.name = urn:ogc:def:crs:OGC:1.3:CRS84`。每个要素须有唯一非空的 `properties.shapeID`，几何类型为 Polygon 或 MultiPolygon。坐标须为有限经纬度，分别在±180°/±90°内。局部显示近似拒绝纬度超出±75°的坐标，以及经度跨度超过180°的要素；不支持跨反经线。支持闭合外环与孔洞环。提供的几何含10个现代喀麦隆 ADM1 区域（2016），其单位与历史时期均不同于 AER Figure 2 来源。
