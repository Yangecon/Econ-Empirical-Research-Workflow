# C16 · Community network with typed edges

[English](recipe.md) · [中文](recipe.zh-CN.md)

`typed_edge_community_network` · C16

Use exam-group schematic layouts, node fills for regions, and line styles for explicitly supplied relationship types; draw only listed edges.

Classification: An elite relationship network arranged by examination groups: line styles distinguish relationship types and node fills distinguish regions. Read nodes, typed edges, and explicit groups/coordinates. Layout distances are neither geographical nor causal, and circular node placement does not create nonexistent edges.

Tags: Network, Edge types, Communities

## Sources and scope

[Web of Power: How Elite Networks Shaped War and Politics in China (2023)](<https://doi.org/10.1093/qje/qjac041>); Figure I; PDF p.14

The original page image and PDF caption have been checked; synthetic data demonstrate the drawing only.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run in this template directory:

```shell
python plot.py --nodes demo_nodes.csv --edges demo_edges.csv --output-prefix YOUR_PROJECT/figures/typed_edge_community_network
```

`--title "标题"` explicitly adds a title; no title or bottom notes appear by default. See schema.md for fields, exclusions, and display meaning. Outputs include PNG, PDF, and accounting CSV.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Verified nodes and endpoints, types, directions, duplicate undirected edges, explicit coordinates, and drawing only the six supplied edges. Python was executed and visually checked. Layout distances are neither geographical nor causal. All example values and relationships are synthetic, not reproductions of the paper.

Canonical figure name: `network_typed_communities`
