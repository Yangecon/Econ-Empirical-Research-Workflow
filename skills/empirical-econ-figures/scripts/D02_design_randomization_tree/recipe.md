# D02 · Randomization and sequential-choice tree

[English](recipe.md) · [中文](recipe.zh-CN.md)

`randomization_decision_tree` · D02

Distinguish behavioral choices from randomized assignment using different nodes, tracing five observed experimental paths over time.

Classification: Experimental-design decision tree: distinguish randomized assignment, participant choices, and later outcome timing; self-selected branches must not be labeled randomization.

Tags: RCT, Random assignment, Sequential choice

## Sources and scope

[Whither Formal Contracts? (2021)](<https://doi.org/10.3982/ECTA16083>); Figure 1; PDF p.10

The original page image and PDF caption have been checked; synthetic data demonstrate the drawing only.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run in the template directory:

```shell
python plot.py --spec figures/demo_design.json --output YOUR_PROJECT/figures/design_tree
```

Generates English PNG/PDF outputs and a synthetic path-probability table. `--title-en "Title"` enables overall titles; no overall title or bottom notes appear by default. Stage names are structural labels within the figure.

Initial acceptance/rejection is the buyer's choice; only subsequent maintenance/removal of the contract requirement is independently randomized. Initial choice must not be labeled a randomized treatment. The source omits later choice nodes in branches where sample buyers did not change their initial choice; this does not mean the experiment logically prohibits changing choices.

This is a temporal tree with a fixed five-leaf structure. JSON can adjust illustrative probabilities. Changing experimental structure, node names, or stages requires changes to the drawing function and path checks, not probabilities alone. Only the 'initially rejected and contract requirement removed' branch displays a further acceptance/rejection choice, whose conditional denominator is P(A=0,F=0). E, C, and R retain the source's ultimate-behavior codes. Joint path probabilities use fictional parameters only to illustrate denominators and are not shown in the figure; source Figure 1 supplies no such probabilities. The chart does not estimate treatment effects.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

English and Chinese default/titled versions were executed and visually checked. Synthetic probabilities across the five paths sum to one; independent-assignment restrictions and conditional denominators passed checks. Main acceptance corrected lines crossing English branch labels and clarified that omitted decision nodes reflect sample behavior rather than logical design restrictions.

Canonical figure name: `design_randomization_tree`
