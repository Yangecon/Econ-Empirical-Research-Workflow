# Input and output schema

[English](schema.md) · [中文](schema.zh-CN.md)

Wide CSV: `pair_id,black_contacts,white_contacts`; one row per genuine twin pair. Pair IDs must be unique and nonblank. Outcomes are finite nonnegative integer contact counts. At least three complete pairs are required; the code rejects missing or duplicate IDs and never silently drops one twin. The jittered x positions depend only on sorted pair ID and are exported, while y values stay as supplied.

Checked pair CSV: original values, `difference_white_minus_black`, `x_black`, `x_white`. Summary CSV: group means and normal-approximation 95% intervals, plus the paired difference mean and standard error. Density smoothing is illustrative and does not change any contacts, pair links, means, or intervals.
