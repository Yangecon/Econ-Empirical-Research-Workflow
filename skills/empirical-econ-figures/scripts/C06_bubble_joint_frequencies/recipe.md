# C06 · Joint-frequency bubble panels

[English](recipe.md) · [中文](recipe.zh-CN.md)

`joint_frequency_bubble_panels` · C06

Use the frequency of two-dimensional value pairs to control bubble area, sharing one scale across rounds and separately marking supplied theoretical benchmarks.

Classification: Joint frequencies combine two belief dimensions in individual experimental responses. Bubble area represents people; theoretical benchmark points do not turn observed frequencies into structural estimates.

Tags: Joint frequencies, Bubble area, Common scale

## Sources and scope

[Mental Models and Learning: The Case of Base-Rate Neglect (2024)](<https://doi.org/10.1257/aer.20201004>); Figure 3: Density Plots for Primitives; PDF p.13

The original page image and PDF caption have been checked; synthetic data demonstrate the drawing only.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run in the template directory:

```shell
python plot.py --input demo.csv --output YOUR_PROJECT/figures/joint_frequency.png --lang en
```

```stata
do "PATH_TO_TEMPLATE/plot.do" "PATH_TO_TEMPLATE/demo.csv" "YOUR_PROJECT/figures/joint_frequency_stata.png" "en" "0"
```

The Stata output parent directory must already exist. Python `--title` or final Stata argument `1` enables the overall title; `zh` selects Chinese. By default, overall titles and bottom notes are absent, but round-panel names remain.

For bubble rows, count is the nonnegative integer frequency of an x–y pair. Benchmark rows supply theoretical benchmark coordinates and leave count blank. Both rounds use the same maximum count across all bubbles; diameter is `27*sqrt(count/max_count)` printer points, making area proportional to frequency. Stata rounds diameters to eight decimals, introducing negligible rounding. Checked CSV files audit target area ratios, not measured pixel areas. Zero frequencies are not drawn, missing frequencies raise errors, and panels are not normalized independently.

In the source, x is belief conditional on a negative signal and y conditional on a positive signal, both in percent. Rounding individual beliefs to multiples of three and counting them are upstream steps. Only Figure 3 is referenced; although Figure 4 is on the same page, no second implementation was added from it. Researchers must supply benchmark coordinates; the template does not re-estimate or derive the belief model. All examples are synthetic.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

29 synthetic input rows and a maximum frequency of 60 across panels. Maximum numerical difference in area ratios across implementations was 5.56e-17. Two zero-frequency rows were retained but not drawn; both languages rejected missing frequencies. English, Chinese, and titled versions were executed; default figures were visually checked, and source Figure 3 and its caption were verified.

Canonical figure name: `bubble_joint_frequencies`
