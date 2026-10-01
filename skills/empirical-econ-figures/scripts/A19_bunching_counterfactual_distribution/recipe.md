# A19 · Bunching distribution with a supplied counterfactual

[English](recipe.md) · [中文](recipe.zh-CN.md)

`bunching_distribution_with_counterfactual` · A19

Compare observed counts and a supplied counterfactual near a tax notch, marking the exclusion interval used in counterfactual estimation.

Classification: Observed wealth frequencies and a fifth-order-polynomial counterfactual density estimated outside the bunching exclusion region. The chosen main-figure layer is not a structural utility-model simulation; additional parametric structural elasticities appear separately in the paper appendix.

Tags: Bunching, Notch, Counterfactual density, Nonstructural estimation

## Sources and scope

[Behavioural Responses to Wealth Taxation: Evidence from Colombia (2025)](<https://doi.org/10.1093/restud/rdae076>); Figure 3(a); PDF p.11

The original page image and PDF caption were checked; synthetic data demonstrate only the drawing method.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run inside the template directory:

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/bunching.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/bunching_stata.png" "en" "0"
```

Create the Stata output parent directory first. Python `--title` or the last Stata argument `1` enables an overall title; `zh` switches to Chinese. Defaults omit overall titles and bottom notes.

Input equal-width bin centers in increasing x order, with nonnegative observed counts and supplied counterfactual counts. Update the threshold, exclusion lower/upper bounds and axis labels at the top of both scripts. The synthetic example uses threshold 1000, exclusion [880,1200] and width 10. Users must specify running-variable units.

Only the drawing layer of source Figure 3(a) is reproduced. Its x axis is 2010 million Colombian pesos and its y axis is the number of taxpayers in each 10-million-peso bin. The counterfactual comes from a fifth-order polynomial fit outside the excluded region. This code reads the counterfactual rather than estimating it and does not implement the other three original panels.

Counts, normalized shares and densities are not interchangeable. The source b is excess mass relative to the average counterfactual height, and a* is the nonbunching share in the dominated region. The template neither calculates nor displays these, elasticities, marginal bunchers, dominated-region bounds or associated standard errors. A notch differs from a kink; the figure itself is not an RDD estimate or density-continuity test.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

One hundred equal-width bins have exactly matching Python/Stata exported values. Both reject negative counts and unequal bin widths. English/Chinese defaults and optional titles were executed and inspected; figures were rechecked after the lead agent requested corrected Chinese notch wording and exclusion-boundary legend.

Canonical figure name: `bunching_counterfactual_distribution`
