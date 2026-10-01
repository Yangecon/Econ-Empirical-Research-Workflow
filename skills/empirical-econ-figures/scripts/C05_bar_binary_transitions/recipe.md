# C05 · Paired binary-transition stacks

[English](recipe.md) · [中文](recipe.zh-CN.md)

`paired_binary_transition_stacks` · C05

Calculate four state transitions from paired individual observations and draw percentage stacks using a common complete-pair denominator.

Classification: The four joint states of paired binary outcomes are 1 at both times, 1 to 0, 0 to 1, and 0 at both times, drawn as 100% stacks by task. Only the descriptive bars are selected; the source's lower p-value and hypothesis-test table is excluded, so the full results figure is not reproduced. Matched individuals supply the common denominator; conditional transition rates instead use starting-state counts. Independent cross-sectional marginals cannot recover transitions. Missing pairs must be handled and reported explicitly; retain zero components and avoid crowding narrow-segment labels.

Tags: Paired states, Transition shares, Stacked bars

## Sources and scope

[Contingent Thinking and the Sure-Thing Principle: Revisiting Classic Anomalies in the Laboratory (2024)](<https://doi.org/10.1093/restud/rdad102>); Figure 7, upper descriptive bars only; PDF p.16

The original page image and PDF caption have been checked; synthetic data demonstrate the drawing only.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run in the template directory:

```shell
python plot.py --input figures/demo_pairs.csv --output YOUR_PROJECT/figures/paired_states
```

Generates English PNG/PDF outputs and numerical summaries. `--title-en "Title"` enables the corresponding titles; no title or bottom notes appear by default.

The four components are 00, 01, 10, and 11, using each task's complete-pair count as their common denominator. Do not substitute starting-state group counts as bar denominators. The summary separately provides conditional transition rates using initial 0 or 1 counts; empty groups are missing, not zero. Individual-task keys must be unique; missing pairs are reported by task. Adapt the meanings of 0/1, task abbreviations, and order to the research.

Only the descriptive stacks in the upper part of original Figure 7 are implemented. The lower hypothesis tests and p-values are not reproduced. All demonstration data are synthetic.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

200 synthetic rows across five tasks, with 194 complete pairs and six excluded incomplete pairs; each bar sums to 100%. Zero components are retained, and conditional transition rates remain undefined when the starting-state group is empty. English and Chinese outputs were executed and visually checked; the source image and caption were verified. Main acceptance corrected optional-title clipping, reran both titled language versions, and visually checked a representative figure.

Canonical figure name: `bar_binary_transitions`
