# C15 · Bilateral attribution Sankey diagram

[English](recipe.md) · [中文](recipe.zh-CN.md)

`bilateral_flow_sankey` · C15

Connect categories on two sides using one quantity scale, allocating band thickness by amount and checking each node total against its incident flows.

Classification: A conserved bilateral funding-flow diagram: band widths share a common unit, with node totals checked against all edge amounts. The figure reclassifies residence to ultimate nationality; unmatched balances must not be hidden.

Tags: Bilateral attribution, Sankey, Financial stocks

## Sources and scope

[Redrawing the Map of Global Capital Flows: The Role of Cross-Border Financing and Tax Havens (2021)](<https://doi.org/10.1093/qje/qjab014>); Figure II; PDF p.21

The original page image and PDF caption have been checked; synthetic data demonstrate the drawing only.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run in the template directory:

```shell
python plot.py --flows figures/demo_flows.csv --nodes figures/demo_nodes.csv --output YOUR_PROJECT/figures/flows
```

Outputs English PNG/PDF files and node-level checks. `--title-en "Title"` enables titles. Overall titles and bottom notes are absent by default; the two column headings are category labels.

Amounts are USD billions. Left and right endpoints share one vertical quantity scale and are not separately normalized to 100%; each band's two ends have thickness equal to the same amount. Gaps between nodes serve layout purposes and are not unallocated balances. Zero flows are not drawn but remain in input and audit records. An absent edge means no flow; unknown amounts must be handled upstream and cannot automatically be zeroed. Color identifies the right-side destination and node order comes from input.

The source reassigns US corporate-bond investments in 2017 from tax-haven-incorporated affiliates to ultimate company countries. It shows attribution of holdings, not necessarily within-period cash flows. Original ownership identification and investment-data processing occur outside the plotter. The template omits some source within-band amount labels, displaying quantities through node totals instead. All examples are synthetic.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

30 synthetic bilateral records, including 13 zero flows; all 11 nodes conserve amounts and both sides total USD 90 billion. Negative amounts, duplicate edges, unknown endpoints, and node-total mismatches are rejected. Zero-total nodes are allowed. English/Chinese PNG/PDF outputs were executed and visually checked; the source image and caption were verified. Main acceptance fixed optional-title clipping, reran both titled language versions, and visually checked a representative figure.

Canonical figure name: `flow_bilateral_sankey`
