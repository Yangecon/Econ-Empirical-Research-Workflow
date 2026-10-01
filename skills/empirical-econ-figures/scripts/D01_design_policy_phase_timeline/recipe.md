# D01 · Staggered policy-phase timeline

[English](recipe.md) · [中文](recipe.zh-CN.md)

`staggered_policy_phase_timeline` · D01

Display monthly policy phases, sample counts, and a common termination date by cohort, retaining a nonpolicy comparison group.

Classification: Staggered-policy voluntary transition, mandatory enforcement, and termination require phase-interval inputs; a purely institutional illustration may use Python alone.

Tags: Policy rollout, Staggered timing, DID design context

## Sources and scope

[Prabhat Barnwal, Curbing Leakage in Public Programs: Evidence from India's Direct Benefit Transfer Policy (2024)](<https://doi.org/10.1257/aer.20161864>); Figure 3; PDF p.10

The original page image and PDF caption have been checked; synthetic data demonstrate the drawing only.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run in this template directory:

```shell
python plot.py --input demo.csv --lang en --output YOUR_PROJECT/figures/policy_timeline.png
```

`--title` enables a title; `--lang zh` switches to Chinese. A PDF with the same stem is exported automatically. Inputs use actual parseable month-start dates and explicit cohort order; coordinates are calculated in months.

Phases are left-closed, right-open intervals. For example `[2020-04-01, 2020-08-01)` covers April through July, with enforcement able to begin immediately in August. The termination line is optional; all nonblank termination_month values must agree. Displayed n is a user-defined population count whose meaning belongs outside the figure.

Dates and counts in the 2020–2021 example are fictional, not the Indian policy's historical timing in the source paper. The paper reports implementation exceptions within phases; cohort bands cannot establish individual eligibility or actual compliance.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

English and Chinese PNGs were executed in Python 3.12 and visually checked; PDFs were also exported. The example contains three policy cohorts and one nonpolicy group. Five invalid timing inputs were rejected: overlaps, inverted intervals, intervals beyond termination, non-month-start dates, and nonpolicy rows with phase intervals.

Canonical figure name: `design_policy_phase_timeline`
