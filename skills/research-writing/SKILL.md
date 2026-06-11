---
name: research-writing
description: Write and revise English empirical economics papers, refresh draft TeX assets from output, manage Data/Empirical Strategy/Results body sections, build multi-table narratives, enforce main-text vs appendix boundaries, and use concise top-journal economics writing conventions. Use when the user asks to draft or revise sections, interpret tables in paper prose, refresh draft LaTeX assets, or tighten results narratives for applied econ papers. Triggers: write results section, draft empirical strategy, revise paper prose, interpret table, LaTeX draft assembly, top-journal econ writing.
---

# Research Writing

## Purpose

Use this skill when the task concerns empirical paper writing or draft assembly.

It combines two responsibilities:

1. Draft-folder workflow: moving cleaned outputs into `draft/images/`, `draft/figures/`, and `draft/tables/`.
2. Prose workflow: drafting and revising English empirical economics sections in a generic top-journal style.

This skill is generic. It should not encode project-specific variable names, data sources, table numbers, or preferred examples. Project-specific examples belong in the project README, project notes, or `templates/custom/`.

## Trigger phrases

- write results section
- draft empirical strategy
- interpret this table
- revise paper prose
- LaTeX draft assembly
- top-journal econ writing

## Required project inputs

Before writing or refreshing the draft, inspect:

```text
README.md
project.yaml
notes/identification.md
notes/estimand_registry.csv
notes/robustness_plan.csv
notes/run_log.md
output/tables/
output/figures/
references/reference_merged/
draft/main.tex
```

If rewriting an existing section, also inspect the target section and neighboring sections.

## Draft folder structure

Use only:

```text
draft/main.tex
draft/images/
draft/figures/
draft/tables/
```

Rules:

- `draft/images/` stores image assets.
- `draft/figures/` stores TeX figure wrappers that point to `draft/images/`.
- `draft/tables/` stores TeX table snippets.
- `draft/main.tex` directly includes `figures/*.tex` and `tables/*.tex`.
- Do not create extra draft subfolders by default.

## Output-to-draft rule

`output/` is upstream. `draft/` is downstream.

- cleaned image files go from `output/figures/` to `draft/images/`
- figure TeX wrappers go to `draft/figures/`
- table TeX snippets go to `draft/tables/`
- do not sync `output/raw/` into `draft/` unless explicitly requested
- do not copy from `draft/` back into `output/` as source of truth

## Generic empirical paper body structure

Default sequence:

```text
Data
Empirical Strategy / Research Design
Results
Mechanisms / Heterogeneity / Additional Outcomes
Robustness and Validity
Conclusion
```

Inside Results, use this logic:

```text
Baseline Specification
Baseline Results
Heterogeneity or Mechanisms
Additional Outcomes
Robustness Summary
```

Exact titles can vary by project, but the logic should remain stable.

## Data section rule

The Data section explains data and measurement. It does not report results.

Allowed in Data:

- data source
- coverage
- sample construction
- unit of observation
- variable definitions
- measurement assumptions
- sample restrictions
- descriptive statistics needed to understand scale or construction
- data limitations that matter for interpretation

Avoid in Data:

- regression results
- treatment-effect claims
- mechanism claims
- robustness findings
- extended previews of result tables
- language such as `we find that` unless it describes a data fact rather than a result

Use conceptual subsection names rather than long source-based headings.

## Empirical Strategy and Baseline Specification

The first time a model is used, define it cleanly.

A baseline specification should include:

- outcome
- treatment, shock, or exposure
- timing
- fixed effects
- controls
- standard errors or clustering
- sample
- coefficient of interest
- unit of interpretation

For a main empirical design, write the equation once and interpret the terms needed for the reader.

Do not restate the same full specification in every later outcome section. Later sections can state that they keep the same sample, timing, fixed effects, and controls while changing the outcome or subgroup.

## Results section rule

The Results section should begin with the baseline specification or point back to where it is defined.

Default opening logic:

1. State what the table or figure tests.
2. Define the baseline equation or remind the reader where it is defined.
3. Report the main estimate.
4. Translate the estimate into economic magnitude.
5. Interpret the estimate against a meaningful benchmark.
6. State what subsequent columns, rows, figures, or tables add.

Do not open Results with a long literature reminder or data description.

## Heterogeneity rule

When presenting heterogeneity with interactions, write the interaction specification explicitly once.

Define:

- moderator
- treatment, shock, or exposure
- interaction term
- reference group
- coefficient of interest
- how to interpret the main effect and interaction coefficient
- whether estimates are levels, logs, percentages, standardized units, or elasticities

Do not leave interaction estimates to speak for themselves. Explain what the interaction means economically.

## Additional outcome sections

After the baseline and heterogeneity specifications are defined, additional outcome sections should not repeat the full equation unless the design changes.

Use compact transitions:

```text
We next examine whether the same shock affects [outcome family].
```

```text
Using the same specification, Table X replaces the dependent variable with [outcome].
```

```text
These outcomes capture [economic channel] rather than the primary outcome studied above.
```

## Result interpretation rule

Avoid mechanical coefficient dumps.

Preferred logic:

1. direction
2. outcome
3. magnitude
4. benchmark
5. inference
6. interpretation

## Abbreviation rule

Write out every abbreviation on first use. Do not introduce an abbreviation unless it will be used multiple times.

## Multi-table narrative stitching

Do not interpret each table as an isolated object. Build one narrative across related tables.

For each thematic block:

1. State the economic theme.
2. Explain why the tables or figures belong together.
3. Use each table or figure for a distinct step in the argument.
4. Avoid repeating the same coefficient interpretation table by table.
5. End with the combined conclusion.

## Main text vs appendix discipline

The main text should contain the primary identification argument and main conclusions.

Main text should include:

- main data objects at a high level
- main sample and outcome definitions
- baseline specification
- main estimate
- most important heterogeneity or mechanism
- short robustness summary only if necessary for credibility

Appendix should include:

- alternative fixed effects
- alternative clustering choices
- sample restrictions
- bandwidth or tuning-parameter grids
- alternative variable definitions
- extended data construction details
- additional descriptive tables
- secondary robustness tables
- long prompts, API details, or classification diagnostics
- detailed provenance for auxiliary datasets

## Journal overlay rule

This skill is generic. For a specific journal, keep project-specific journal notes inside `notes/journal_target_profile.md` in the project itself. If a dedicated journal skill is available, use it as an overlay for journal-specific constraints, submission style, and replication requirements.

## Output expectations

When asked to draft or revise a section, return:

1. revised English text
2. a short list of what changed
3. unresolved TODOs if required evidence is missing
4. optional LaTeX-ready version if the user asks

Do not fabricate table numbers, sample means, coefficients, appendix labels, or data details.
