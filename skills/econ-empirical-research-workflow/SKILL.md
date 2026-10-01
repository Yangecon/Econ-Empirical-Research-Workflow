---
name: econ-empirical-research-workflow
description: "End-to-end workflow router for Default applied economics research in Codex. Use when the user wants to run the whole empirical research workflow as one umbrella skill, asks for the next stage from idea to submission, wants one entrypoint for topic selection, identification, Stata execution, writing, draft sync, and submission packaging, or wants Codex to decide which specialized skill should handle the task. Triggers: full empirical workflow, end-to-end applied econ workflow, whole research pipeline, umbrella workflow skill, one skill for idea to submission, route this empirical project."
---

# Econ Empirical Research Workflow

Use this as the umbrella entrypoint for the full repository.

This skill does not replace the specialized skills. It reads the project state, decides which stage is active, and routes to the right underlying skill.

## Trigger phrases

- full empirical workflow
- end-to-end applied econ workflow
- whole research pipeline
- umbrella workflow skill
- one skill for idea to submission
- route this empirical project

## Scope

This umbrella skill covers the repository's full Default applied econ pipeline:

```text
Idea -> Topic Gate -> Identification Gate -> Empirical Analysis -> Output -> Draft -> Submission
```

Persistent resource layers:

```text
references/
notes/
work/
```

## Required project inputs

For project-wide routing, inspect:

- `README.md`
- `project.yaml`

Prefer `workflow_state` in `project.yaml` as the source of truth.

## Routing map

Route to:

- `research-topic-selection` for idea generation, topic scoring, topic gate decisions, and the bounded two-agent loop
- `research-identification` for estimand definition, identification design, assumptions, data requirements, and robustness planning
- `research-empirics` for generic empirical production workflow
- `empirical-analysis-stata` for the full Stata-first applied econ execution stack
- `empirical-econ-figures` for supported descriptive, design and estimated-result figures
- `research-writing` for prose drafting and draft-folder writing logic
- `output-draft-overleaf-sync` for output-to-draft refresh and Overleaf handoff checks
- `research-submission` for submission packaging and replication bundle work
- `reference-elicit-agent` for persistent literature and BibTeX workflows

For descriptive and regression tables, route to `empirical-analysis-stata` and apply its `references/08-tables-plots.md` contract. Default to one consolidated XLSX workbook with one table per sheet. Export CSV, Word, or TeX only when requested.

## Figure requests

For an explicit drawing request with existing observations or saved estimates, route to `empirical-econ-figures`. Read the project README/state when available; a standalone figure request does not require scaffolding a new empirical project. Do not mark identification, output or draft gates ready merely because a graph was rendered. If requested estimates or covariance are missing/stale, return to `empirical-analysis-stata` or `research-empirics` first.

Use the catalog to choose among A reduced-form estimates, B structural-form estimates, C summary, D research design and E prediction/algorithm evaluation. Heterogeneity and robustness are tags within the numerical-origin category. Descriptive diagnostics and design diagrams may support early work without claiming a frozen causal design. Formal causal figures must preserve the project's frozen estimand, sample, estimator and inference.

Keep estimation upstream, figure inputs under the project's existing `output/raw/` convention, accepted figures under `output/figures/`, and provenance in `notes/figure_log.csv` and the run log. Exploratory figures stay under `work/<slug>/`. Captions, sources and notes are supplied by writing/draft-sync. See [figure integration](../empirical-econ-figures/references/workflow_integration.md).

## Hard gate logic

These gates govern progression of the main empirical pipeline. Standalone drawing follows the Figure requests section above.

1. If `workflow_state.topic_gate_status != go`, stay in the idea stage and route to `research-topic-selection`.
2. If `workflow_state.identification_gate_status != freeze`, route to `research-identification`.
3. If the user wants a full Stata run or design-specific Stata estimator workflow, route to `empirical-analysis-stata`.
4. If output is missing or stale, route to `research-empirics` or `empirical-analysis-stata`.
5. If `workflow_state.output_status != ready`, do not refresh draft assets yet.
6. If output is ready but draft is stale, route to `research-writing` or `output-draft-overleaf-sync`.
7. If `workflow_state.draft_status != ready`, do not package submission yet.
8. If the user asks for replication-package or submission work and draft is ready, route to `research-submission`.

## Output expectations

When invoked, report:

- current workflow stage
- blocked gates
- missing artifacts
- next specialized skill
- why that skill is the best next step
