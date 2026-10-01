# Input schema

[English](schema.md) · [中文](schema.zh-CN.md)

CSV with one row per book. Required fields: unique nonblank `book_id`; integer `year`; numeric `religion`, `political_economy`, and `science` shares each in [0,1] and summing to one within 1e-7; and **precomputed** numeric `sentiment_percentile` in [0,1]. No required field may be missing or nonfinite. Every requested center year must have at least one book within its inclusive window. The coordinate transformation is `x = science + 0.5 × religion`, `y = (sqrt(3)/2) × religion`.
