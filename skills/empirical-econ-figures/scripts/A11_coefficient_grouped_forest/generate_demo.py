"""Deterministic synthetic data for two coefficient-interval drawing variants."""
from pathlib import Path
import csv
import numpy as np

rng = np.random.default_rng(20260928)
out = Path(__file__).with_name("demo.csv")
rows = []

specs = [
    ("preferred", "Preferred", "首选规格"),
    ("extra_fe", "Extra fixed effects", "加入固定效应"),
    ("unweighted", "Unweighted", "不加权"),
    ("drop_region", "Drop one region", "剔除一个地区"),
    ("controls", "More controls", "增加控制变量"),
    ("movers", "Movers only", "仅流动者"),
    ("stayers", "Stayers only", "仅未流动者"),
    ("placebo", "Placebo cohort", "安慰剂队列"),
]
panels = [
    ("mortality", -12.0, 1.6),
    ("difficulty", -3.5, .55),
    ("transfer", -5.0, .85),
    ("employment", 4.0, .65),
]
for pi, (panel, center, scale) in enumerate(panels, 1):
    for ti, (term, en, zh) in enumerate(specs, 1):
        estimate = center + rng.normal(0, scale * (.55 if ti < 8 else 1.3))
        if term == "placebo":
            estimate = rng.normal(0, scale * .6)
        half = scale * (1.55 + .35 * rng.random())
        se = half / 1.96
        # One row tests the explicit SE fallback in both implementations.
        low, high = ("", "") if panel == "transfer" and term == "movers" else (estimate-half, estimate+half)
        rows.append(["robustness", panel, pi, term, ti, en, zh, "main", 1,
                     estimate, low, high, se])

outcomes = [
    ("gpa", "Cumulative GPA", "累计平均绩点", -.030, -.001),
    ("graduation", "High-school graduation", "高中毕业", -.013, -.001),
    ("college", "College enrollment", "大学入学", -.007, .001),
]
for ti, (term, en, zh, a, b) in enumerate(outcomes, 1):
    for gi, (group, estimate) in enumerate((("group_a", a), ("group_b", b)), 1):
        half = (.003 if gi == 1 else .013) * (1 + .1 * (ti - 1))
        rows.append(["subgroup", "education", 1, term, ti, en, zh, group, gi,
                     estimate, estimate-half, estimate+half, half/1.96])

with out.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["variant", "panel", "panel_order", "term", "term_order",
                     "term_label_en", "term_label_zh", "group", "group_order",
                     "estimate", "ci_low", "ci_high", "se"])
    for row in rows:
        writer.writerow([v if isinstance(v, str) else f"{v:.6f}" if isinstance(v, float) else v for v in row])
print(f"DEMO_COMPLETE rows={len(rows)} output={out}")
