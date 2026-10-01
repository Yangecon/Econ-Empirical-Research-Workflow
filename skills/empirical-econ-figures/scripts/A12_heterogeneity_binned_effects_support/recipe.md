# A12 · Binned effects with support histograms

[English](recipe.md) · [中文](recipe.zh-CN.md)

`binned_effect_with_support_histogram` · A12

Grouped estimates and intervals above the unconditional sample distribution of the same x variable; effects and sample counts are supplied separately.

Classification: Left columns show mean migration rates and Wilson intervals by network-support group; right columns show heterogeneous fixed-effects regression coefficients and two-way-clustered intervals. The composite is classified by its right-column empirical estimates, with a Summary overlay tag; it is not structural-model output.

Tags: Heterogeneity, Binned effects, Sample support, Summary overlay, Fixed effects

## Sources and scope

[Migration and the Value of Social Networks (2025)](<https://doi.org/10.1093/restud/rdad113>); Figure 6; PDF p.20

The original page image and PDF caption were checked; synthetic data demonstrate only the drawing method.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run inside this template directory:

```shell
python plot.py --effect effect_demo.csv --support support_demo.csv --output YOUR_PROJECT/figures/effect_support.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/effect_demo.csv" "PATH_TO_TEMPLATE/support_demo.csv" "YOUR_PROJECT/figures/effect_support.png" en 0
```

Python `--title` or the final Stata argument `1` enables a title; `zh` switches to Chinese. Both languages’ CONFIG blocks define panel IDs, ranges, ticks and units; update all when replacing data. Intervals are supplied by default; no Wilson intervals, clustered standard errors or new regressions are calculated.

Lower count values come from a specified unconditional population and do not automatically equal regression sample sizes for upper estimates. Both parts must use the same x variable and units. Recheck upper/lower plot-area alignment after changing Stata tick-label lengths or graph composition.

In the reference paper, left panels contain migration rates and Wilson 95% intervals; right panels contain fixed-effects-conditioned model coefficients and two-way-clustered 95% intervals. This describes the source, not an estimation procedure automatically implemented here. Python uses a shorter histogram region; Stata preserves alignment and numeric ticks but uses similarly sized upper/lower regions.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

English/Chinese Python/Stata PNG/PDF outputs were executed and inspected: four panels, 80 estimate points and 80 histogram bins. Stata was repaired to retain numeric y ticks and align upper/lower x axes; nested new-output-directory tests passed. Both languages share supplied estimates, CIs and counts without re-estimation. Layout differs: Stata upper/lower regions have similar heights; Python uses a shorter lower histogram.

Canonical figure name: `heterogeneity_binned_effects_support`
