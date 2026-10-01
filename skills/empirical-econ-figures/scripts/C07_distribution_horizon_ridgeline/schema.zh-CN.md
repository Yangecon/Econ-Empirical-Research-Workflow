# 输入与计算

[English](schema.md) · [中文](schema.zh-CN.md)

`plot.py --input path.csv` 接受长格式 CSV，包含 `race_id`（非空竞速事件键）、`horizon_ms`（仅为1、10、100、1000或10000）、`metric`（`price_impact` 或 `profits`）与 `value_bps`（每股基点数，可带符号、可为空）。每个竞速事件—期限—指标仅允许一行；重复键报错。每个指标与期限均须出现。允许记录缺席；`sample_counts.csv` 报告每个已提供期限内的分母。模板不推断未观测竞速事件—期限记录。

默认 `--zero-policy exclude` 遵循 Figure V 图注：严格为零的值不进入 KDE，但计入 `n_zero`。`n_rows` 包括缺失值，`n_finite` 排除缺失值，`zero_share_of_finite = n_zero/n_finite`，`n_density` 是零值规则处理后的 KDE 分母。若没有有限观测或处理后没有观测，则绘图失败，而非报告零密度。`--zero-policy include` 是显式替代选项。缺失的 `value_bps` 不计入 KDE 或零值份额。

`density_grid.csv` 为每个指标—期限保存一条 Gaussian KDE。公式为 `f(x)=sum_i phi((x-v_i)/h)/(n_density*h)`，其中 `h=--bandwidth`（默认0.55基点）。全部十条曲线使用*相同*带宽。每个面板的五个期限使用相同的401点横轴网格：价格影响为−20至20基点，利润为−10至10基点。可见网格截去尾部；KDE 公式在实数域归一化，不在可见横轴范围重新归一化。两个面板共用同一个绝对密度到脊线高度的比例。纵向位置是期限类别槽位，不是线性时间轴上的经过时间。默认无标题和底部说明；`--title` 开启标题。

随附示例为确定性的模拟值，含部分严格零值。仅演示布局与含义，不代表论文的样本量、零点质量或数值估计。
