# Input contract

[English](schema.md) · [中文](schema.zh-CN.md)

UTF-8 CSV with `bin_low,bin_high,relative_price,relative_productivity,relative_sales_per_worker`. Each row is one labor-share bin. Bin **widths** must be strictly positive, equal, contiguous and contained in `[0,1]`; `bin_low=0` is valid and at least three bins are required. Components and total must be finite signed numeric quantities in the same relative log units. Each row must satisfy `relative_sales_per_worker = relative_price + relative_productivity` within `2e-6` to allow six-decimal CSV rounding.

The two component bars stack **separately above and below zero**. A positive component starts at the current positive stack height; a negative component starts at the current negative depth. The total is an algebraic sum, so it can lie between the positive and negative extents when component signs differ. `_checked.csv` gives `price_low/price_high`, `prod_low/prod_high`, and the original total for numerical audit. Neither component is a percentage of 100, and the chart is not a 100% stack. The source defines relative physical labor productivity as relative sales per worker minus relative prices; this template reads all three saved values and verifies the identity, without estimating them.
