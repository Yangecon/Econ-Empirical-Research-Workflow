# A08 · Paired outcomes and difference distributions

[English](recipe.md) · [中文](recipe.zh-CN.md)

`paired_difference_distribution` · A08

Genuine pair IDs link individual outcomes to show marginal densities, group means and paired differences; pairs are never guessed by sorting outcomes.

Classification: Contact counts come from twin profiles with randomized racial signals. Paired individuals and group means/intervals display experimental treatment differences, so the figure is classified as an RCT result display rather than by scatterplot appearance alone.

Tags: RCT, Paired outcomes, Difference distribution

## Sources and scope

[LinkedOut? A Field Experiment on Discrimination in Job Network Formation (2025)](<https://doi.org/10.1093/qje/qjae035>); Figure III; PDF p.22

The original page image and PDF caption were checked; synthetic data demonstrate only the drawing method.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run Python in the selected template directory, writing to the research project:

```shell
python plot.py --input demo_pairs.csv --output-prefix YOUR_PROJECT/figures/paired_difference_distribution
```

Run Stata from this template directory with explicit arguments:

```stata
do plot.do "demo_pairs.csv" "YOUR_PROJECT/figures/paired.png" 0
```

Python may add `--title "标题"`; change Stata’s last argument from 0 to 1 to enable the example title. Defaults omit the title and bottom notes. See schema.md for input fields and statistical boundaries.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Hand-calculated paired examples, shared paired coordinates, group means and the paired-difference standard error were checked across Python/Stata. Density smoothing differs between implementations; no numerical equality of density curves is claimed. Mean 95% intervals use a 1.96 normal approximation. Both implementations were executed and the lead agent visually inspected the figures. The example is not a numerical replication of the original paper.

Canonical figure name: `distribution_paired_differences`
