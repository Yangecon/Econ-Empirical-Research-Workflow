# Input and calculations

[English](schema.md) · [中文](schema.zh-CN.md)

`plot.py --input path.csv` accepts long CSV rows with `race_id` (nonempty race key), `horizon_ms` (exactly 1, 10, 100, 1000, or 10000), `metric` (`price_impact` or `profits`), and `value_bps` (numeric per-share basis points, signed, blank allowed). One race–horizon–metric row is permitted; duplicate keys fail. Each metric and horizon must appear. Rows can be absent; `sample_counts.csv` reports the denominator within each supplied horizon. This template does not infer unobserved race–horizon records.

The default `--zero-policy exclude` follows the Figure V caption: exactly zero values are omitted from the KDE, but counted in `n_zero`. `n_rows` includes missing values, `n_finite` excludes them, `zero_share_of_finite = n_zero/n_finite`, and `n_density` is the KDE denominator after the zero policy. If no finite observations or no remaining observations, rendering fails rather than reporting a zero density. `--zero-policy include` is an explicit alternative. Missing `value_bps` never contributes to KDE or zero share.

`density_grid.csv` contains one Gaussian KDE per metric–horizon. Formula: `f(x)=sum_i phi((x-v_i)/h)/(n_density*h)` with `h=--bandwidth` (default 0.55 basis points). All ten curves use this *same* bandwidth. The five horizons in each panel use the same 401-point x grid: price impact −20 to 20 bps, profits −10 to 10 bps. The visible grid truncates tails; density is normalized over the real line by the KDE formula, not renormalized to the visible x range. One absolute density-to-ridge-height scale is shared across both panels. Vertical position is a categorical horizon slot, not elapsed time on a linear axis. The figure has no title or bottom notes by default; `--title` enables a heading.

The packaged demo has deterministic synthetic values and some exact zeros. It demonstrates layout and semantics only, not the paper's sample size, zero mass, or numerical estimates.
