#!/usr/bin/env python3
"""Design-only timing tree for initial choice and independent contract randomization."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Circle, Rectangle
import numpy as np
import pandas as pd

DEMO = {
    "data_status": "synthetic illustrative parameters, not source-paper values",
    "p_initial_accept": 0.62,
    "p_contract_maintained_given_initial_accept": 0.50,
    "p_contract_maintained_given_initial_reject": 0.50,
    "p_ultimate_accept_given_initial_reject_and_lifted": 0.35,
    "paths": ["A1_F1_U1", "A1_F0_U1", "A0_F1_U0", "A0_F0_U1", "A0_F0_U0"],
}
EXPECTED_PATHS = DEMO["paths"]


def calculate(spec: dict) -> pd.DataFrame:
    if spec.get("paths") != EXPECTED_PATHS:
        raise ValueError("paths must contain the five source-design leaves in order")
    names = ["p_initial_accept", "p_contract_maintained_given_initial_accept",
             "p_contract_maintained_given_initial_reject",
             "p_ultimate_accept_given_initial_reject_and_lifted"]
    values = {}
    for name in names:
        value = spec.get(name)
        if not isinstance(value, (int, float)) or not np.isfinite(value) or not 0 <= value <= 1:
            raise ValueError(f"{name} must be a finite probability in [0,1]")
        values[name] = float(value)
    p_a = values[names[0]]
    p_f_a1, p_f_a0 = values[names[1]], values[names[2]]
    p_u = values[names[3]]
    if not np.isclose(p_f_a1, p_f_a0, atol=1e-12, rtol=0):
        raise ValueError("Contract randomization must be independent of initial choice: both conditional probabilities must match")
    rows = [
        ("A1_F1_U1", 1, 1, 1, p_a * p_f_a1, "P(A=1)", p_f_a1),
        ("A1_F0_U1", 1, 0, 1, p_a * (1-p_f_a1), "P(A=1)", 1-p_f_a1),
        ("A0_F1_U0", 0, 1, 0, (1-p_a) * p_f_a0, "P(A=0)", p_f_a0),
        ("A0_F0_U1", 0, 0, 1, (1-p_a) * (1-p_f_a0) * p_u,
         "P(A=0,F=0)", p_u),
        ("A0_F0_U0", 0, 0, 0, (1-p_a) * (1-p_f_a0) * (1-p_u),
         "P(A=0,F=0)", 1-p_u),
    ]
    out = pd.DataFrame(rows, columns=["path", "initial_accept", "contract_maintained",
                                      "ultimate_accept", "joint_probability",
                                      "final_branch_denominator", "conditional_final_probability"])
    out["payment_branch"] = np.where(out.ultimate_accept.eq(1), "E_or_C", "R")
    assert np.isclose(out.joint_probability.sum(), 1)
    return out


def chinese_font() -> str:
    names = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in ("Microsoft YaHei", "SimHei", "Noto Sans CJK SC",
                      "Source Han Sans SC", "Arial Unicode MS"):
        if candidate in names:
            return candidate
    raise RuntimeError("No installed Chinese font found")


def render(outdir: Path, lang: str, title: str | None) -> None:
    if lang == "zh":
        plt.rcParams["font.family"] = chinese_font()
        plt.rcParams["axes.unicode_minus"] = False
        text = {"a1": "A=1\n初始接受", "a0": "A=0\n初始拒绝",
                "f1": "F=1\n要求保留", "f0": "F=0\n要求取消",
                "accept": "最终接受", "reject": "最终拒绝",
                "stage1": "初始选择", "stage2": "合同要求随机化",
                "stage3": "最终选择", "stage4": "三天后\n付款",
                "pay_yes": "E 或 C", "pay_no": "R"}
    else:
        plt.rcParams["font.family"] = "DejaVu Sans"
        text = {"a1": "A=1\nInitially accept", "a0": "A=0\nInitially reject",
                "f1": "F=1\nRequirement maintained", "f0": "F=0\nRequirement lifted",
                "accept": "Ultimately accept", "reject": "Ultimately reject",
                "stage1": "Initial choice", "stage2": "Contract randomized",
                "stage3": "Ultimate choice", "stage4": "Payment\n3 days later",
                "pay_yes": "E or C", "pay_no": "R"}
    fig, ax = plt.subplots(figsize=(10, 5.9))
    ax.axhspan(2.55, 5.15, facecolor="#DFE7F8", zorder=0)
    ax.plot([0.5, 0.5], [0.15, 2.5], color="#555555", linestyle=(0, (4, 4)), linewidth=0.8)
    ax.plot([0.5, 3.0], [2.5, 4.15], color="#252525", linewidth=1.35)
    ax.plot([0.5, 3.0], [2.5, 1.45], color="#252525", linewidth=1.35)
    branches = [
        ((3.0, 4.15), (5.7, 4.87), "#252525"),
        ((3.0, 4.15), (5.7, 3.36), "#AAAAAA"),
        ((3.0, 1.45), (5.7, 2.18), "#252525"),
        ((3.0, 1.45), (5.7, 0.83), "#AAAAAA"),
        ((5.7, 0.83), (7.5, 1.12), "#AAAAAA"),
        ((5.7, 0.83), (7.5, 0.48), "#AAAAAA"),
    ]
    for (x0, y0), (x1, y1), color in branches:
        ax.plot([x0, x1], [y0, y1], color=color, linewidth=1.25, zorder=1)
    ax.add_patch(Rectangle((0.38, 2.38), 0.24, 0.24,
                           facecolor="white", edgecolor="#222222", linewidth=1.2, zorder=4))
    for x, y in ((3.0, 4.15), (3.0, 1.45)):
        ax.add_patch(Circle((x, y), 0.17, facecolor="white",
                            edgecolor="#222222", linewidth=1.2, zorder=4))
    ax.add_patch(Rectangle((5.58, 0.71), 0.24, 0.24,
                           facecolor="white", edgecolor="#222222", linewidth=1.2, zorder=4))
    def label(x: float, y: float, value: str, size: float = 9.5,
              ha: str = "center", background: str | None = None) -> None:
        bbox = (dict(facecolor=background, edgecolor="none", pad=2.0)
                if background else None)
        ax.text(x, y, value, ha=ha, va="center", fontsize=size,
                color="#242424", bbox=bbox, zorder=5)
    label(1.5, 4.43, text["a1"])
    label(1.5, 1.35, text["a0"])
    label(4.35, 4.88, text["f1"], background="#DFE7F8")
    label(4.35, 3.41, text["f0"], background="#DFE7F8")
    label(4.35, 2.14, text["f1"], background="white")
    label(4.35, 0.72, text["f0"], background="white")
    for x, y, outcome, payment in (
        (6.13, 4.87, "accept", "pay_yes"),
        (6.13, 3.36, "accept", "pay_yes"),
        (6.13, 2.18, "reject", "pay_no"),
        (7.8, 1.12, "accept", "pay_yes"),
        (7.8, 0.48, "reject", "pay_no"),
    ):
        label(x, y, text[outcome], size=8.6, ha="left")
        label(9.38, y, text[payment], size=8.8)
    ax.axvline(9.08, color="#666666", linestyle=(0, (2, 3)), linewidth=0.8)
    for x, key in ((0.5, "stage1"), (3.0, "stage2"),
                   (5.7, "stage3"), (9.80, "stage4")):
        label(x, -0.12, text[key], size=8.6)
    ax.set_xlim(0.1, 10.7)
    ax.set_ylim(-0.32, 5.25)
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=12, pad=10)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.90 if title else 0.96, bottom=0.08)
    for extension in ("png", "pdf"):
        fig.savefig(outdir / f"randomization_decision_tree_{lang}.{extension}",
                    dpi=300, facecolor="white")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, help="Explicit five-path design and illustrative probabilities JSON")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "figures")
    parser.add_argument("--title-en", help="Optional English title")
    parser.add_argument("--title-zh", help="Optional Chinese title")
    parser.add_argument("--lang", choices=("en", "zh"), default="en")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    if args.spec:
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
    else:
        spec = DEMO
        (args.output / "demo_design.json").write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
    leaves = calculate(spec)
    leaves.to_csv(args.output / "illustrative_leaf_probabilities.csv", index=False)
    render(args.output, args.lang, args.title_en if args.lang == "en" else args.title_zh)
    print(leaves[["path", "joint_probability", "final_branch_denominator"]].to_string(index=False))
    print("Illustrative probabilities only; Figure 1 itself supplies no branch probabilities.")
    print("RANDOMIZATION_DECISION_TREE_COMPLETE")


if __name__ == "__main__":
    main()
