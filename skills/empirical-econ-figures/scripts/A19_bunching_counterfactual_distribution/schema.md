# Input contract

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV with `bin_center`, `observed_count`, `counterfactual_count` in any column order. Every field must be finite numeric; counts must be nonnegative. At least ten rows are required. Bin centers must be strictly increasing and equally spaced; their **difference** is the bin width. The configured exclusion lower bound, notch, and exclusion upper bound must be strictly ordered within the plotted x range. The CSV contains counts, not normalized densities or taxpayer shares; changing to densities requires updating axis labels and the supplied input accordingly. A missing counterfactual value is rejected instead of interpolated. The counterfactual is an input, not produced by this code.

Source units are 2010 million Colombian pesos on x and number of tax filers per 10-million-peso bin on y. Generic default labels allow other running variables and bin widths, provided the analyst edits labels to reflect their input. No inference statistic is calculated.
