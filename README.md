# Econ Empirical Research Workflow

[中文说明 / Chinese Version](./README.zh-CN.md)

A reusable Codex-ready skill bundle for empirical economics research.

This repository packages an opinionated applied-economics workflow for idea triage, literature evidence collection, identification design, Stata-first empirical execution, output cleaning, draft assembly, and submission packaging. It is designed for AER/QJE/AEJ-style empirical projects and ships with reusable skills, project scaffolds, Stata templates, writing templates, validation helpers, and explicit workflow-state files.

## What This Repo Is

This is a public skill bundle repository, not the home directory for all empirical projects.

Keep real empirical projects outside this repository and install or copy the skills into Codex separately.

## Scope

This repository is intentionally opinionated:

1. It focuses on default applied economics only.
2. It treats Stata as the canonical empirical execution stack.
3. It treats `output/ -> draft/ -> paper/` as the default downstream writing and submission pipeline.
4. It treats `references/` and `notes/` as persistent resource layers, not as main workflow stages.

It does not try to cover epidemiology workflows, ML-causal workflows, or a Python-first empirical stack.

## Canonical Workflow

```text
Idea
  -> Topic Gate
      -> Identification Gate
          -> Empirical Analysis
              -> Output
                  -> Draft
                      -> Submission
```

Persistent resource layers:

```text
references/
notes/
work/
```

These folders are used throughout the project but are not gate stages.

## Idea Stage: Bounded Two-Agent Loop

The idea stage is a bounded file-mediated loop, not free-form chat.

```text
Human seed + data policy
  -> Idea Generator Agent
      -> candidate ideas / idea queue
          -> Literature + Judge Agent
              -> evidence / scorecard / topic decision / failure reasons
                  -> Idea Generator Agent reads failure reasons and generates next round
```

Loop limits:

- `max_idea_search_rounds = 10`
- stop when at least one idea receives `go`
- stop when the maximum score fails to improve for several rounds
- stop when the human manually stops
- stop when all candidates are parked/dropped because the data path is unavailable

Elicit is an evidence-collection tool. It is not the final judge.

## Project Structure

The scaffolded project structure is:

```text
<Project>/
  README.md
  project.yaml
  idea/
    intake/
      human_seed.md
      human_seed.json
    registry/
      idea_registry.csv
      loop_log.csv
    agents/
      idea_generator/
        prompts/
        outputs/
        state.json
      literature_judge/
        prompts/
        outputs/
        state.json
    ideas/
      idea_001/
        question_intake.json
        data_fit.json
        idea_brief.md
        elicit/
        prior_literature.md
        gap_map.csv
        contribution_scorecard.json
        topic_decision.md
  references/
  notes/
  data/
    raw/
    build/
    codebook/
    final_sample.dta
  code/
    build/
      00_build_sample.do
    _write_version_log.do
    00_setup.do
    01_estimation.do
    02_robustness.do
    03_figures.do
    04_tables.do
    99_master.do
  output/
    raw/
    figures/
    tables/
  draft/
    main.tex
    images/
    figures/
    tables/
  work/
  paper/
    tex/
    replication_package/
```

## Skill List

```text
skills/
  econ-empirical-research-workflow/
  research-workflow/
  research-idea-selection/
  research-identification/
  research-empirics/
  empirical-analysis-stata/
  research-writing/
  output-draft-overleaf-sync/
  research-submission/
  reference-elicit-agent/
```

What each skill does:

- `econ-empirical-research-workflow`: umbrella entrypoint that routes one project through the whole repository workflow from idea to submission.
- `research-workflow`: routes a project by reading `project.yaml`, `workflow_state`, and required artifacts.
- `research-idea-selection`: manages the bounded two-agent idea loop.
- `research-identification`: freezes the estimand, design, assumptions, data requirements, and robustness plan.
- `research-empirics`: runs the generic empirical production workflow and refreshes output artifacts.
- `empirical-analysis-stata`: the Stata-first applied-econ execution skill.
- `research-writing`: drafts and revises empirical paper prose and manages draft-folder logic.
- `output-draft-overleaf-sync`: refreshes downstream draft assets and checks Overleaf handoff readiness.
- `research-submission`: prepares a submission-ready `paper/` folder and replication package.
- `reference-elicit-agent`: manages the persistent Elicit-centered literature workflow under `references/`.

## Repo Contents

For a compact inventory, see [docs/repo-contents.md](./docs/repo-contents.md).
