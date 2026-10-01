# Input schema and checks

[English](schema.md) · [中文](schema.zh-CN.md)

Nodes CSV: required `id,label,region,exam_group,label_show`; optional paired `x,y`. `id` must be unique and all text fields nonblank; `label_show` is 0 or 1. At most two region labels are supported by the black/white fill. Coordinates, when supplied, must be finite and complete for all nodes. Otherwise the renderer computes stable schematic exam-group positions.

Edges CSV: `source,target,type,directed`. Endpoints must be listed node IDs. Supported type values are `blood` (dash-dot), `provincial_exam` (dotted), and `national_exam` (solid). `directed` is 0/1. Self-loops and duplicate same-type ties are rejected; a reversed undirected tie counts as duplicate, whereas direction is respected for directed ties. Different types may connect the same pair when separately listed. No missing pair is added, including people in the same exam group.
