# Bilateral flow input and accounting

[English](schema.md) · [中文](schema.zh-CN.md)

Pass **both** `--flows` and `--nodes`, or neither for the synthetic demo. `flows.csv` has `source`, `destination`, and `amount_usd_billion`; every ordered source-destination pair appears at most once. Amounts are finite and nonnegative in **USD billions**. Zero edges are valid input rows and draw no band. Every positive band has the same vertical scale at its source and destination: one diagram unit represents one USD billion. Color encodes the destination, and the node order comes from `nodes.csv`; sorting affects placement only, never thickness.

`nodes.csv` has `side` (`source` or `destination`), `node`, optional complete `label_zh`, and `total_usd_billion`. Rows define top-to-bottom order independently for each side. Every edge endpoint must be declared. A node may have a zero total; it is labeled but has no positive-height box. For **every** node, the sum of incident edge amounts must equal its declared total within numerical rounding tolerance. Sum of all source totals must equal sum of all destination totals. Any unmatched balance raises an error rather than disappearing from the picture. To depict a real unmatched category, supply it as an explicit source or destination node and edge, with an honest label.

The diagram is a descriptive reclassification map from tax-haven affiliate location to ultimate company country. Its paths encode amounts already supplied to the script; the script does not infer ownership, construct firm links, or estimate reallocation. Demo flow and node values are invented and should not be read as the original 2017 amounts.
