# <Project Title>

This folder is the cleaned working copy of the project. It should be runnable through relative paths and should record all project-specific settings needed before agents edit results, run the Stata pipeline, refresh draft files, touch Overleaf, work on references, or prepare replication materials.

## Current workflow state

The source of truth is `project.yaml`, especially:

```yaml
workflow_state:
  active_stage: idea
  active_idea_id: null
  active_rq_id: null
  topic_gate_status: null
  identification_gate_status: null
  output_status: null
  draft_status: null
  submission_status: null
  last_empirical_run_id: null
  current_reproduction_target: null
```

Current status:

- Active stage:
- Active idea ID:
- Active research question ID:
- Topic gate status:
- Identification gate status:
- Output status:
- Draft status:
- Submission status:
- Last empirical run:
- Current reproduction target:

## What this version reproduces

Describe the source-of-truth target for this version.

Examples:

- `notes/result_summary_YYYYMMDD.xlsx`
- `output/tables/table_main_results.tex`
- `draft/main.tex`
- `paper/tex/main.tex`

Main scripts aligned to this target:

- `code/build/00_build_sample.do`
- `code/01_estimation.do`
- `code/02_robustness.do`
- `code/03_figures.do`
- `code/04_tables.do`
- `code/99_master.do`

## Main workflow

```text
Idea
  -> Topic Gate
      -> Identification Gate
          -> Empirical Analysis
              -> Output
                  -> Draft
                      -> Submission
```

`references/` and `notes/` are persistent resource layers, not main workflow stages.

## Idea stage

The idea stage is a bounded two-agent loop.

Folder map:

```text
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
```

The Idea Generator Agent proposes candidate ideas. The Literature + Judge Agent collects evidence, scores the topic, records failure reasons, and writes a gate decision. Elicit is evidence collection, not final judgment.

## Human seed and data policy

Before generating ideas, complete:

```text
idea/intake/human_seed.md
idea/intake/human_seed.json
```

If `allow_new_data_search` is false, candidate ideas must use existing data. If it is true, new-data ideas must pass checks for public availability, data fit, unit match, coverage match, key variables, and access risk.

## Folder map

- `idea/`: bounded topic-search loop and topic-gate artifacts
- `references/`: persistent human, AI, and merged literature/reference lanes
- `notes/`: flat project notes, identification memo, PAP, robustness plan, decision log, run log
- `data/`: raw data, build data, codebook, and final analysis samples
- `code/`: Stata build scripts plus estimation, robustness, figure, and table scripts
- `output/`: raw outputs plus cleaned paper-ready figures and tables
- `draft/`: `main.tex`, images, figure TeX wrappers, table TeX snippets
- `work/`: exploratory side branches
- `paper/`: submission TeX copy and replication package

## Running the project

Run scripts from the project root unless otherwise stated.

Recommended order:

```text
code/build/00_build_sample.do
code/01_estimation.do
code/02_robustness.do
code/03_figures.do
code/04_tables.do
code/99_master.do
```

Each `.do` file should append to:

```text
output/raw/stata_version_log.csv
```

## Project settings

### Elicit

- Elicit API key environment variable: `ELICIT_API_KEY`
- Topic-stage Elicit folder: `idea/ideas/<idea_id>/elicit/`
- Reference-stage Elicit folder: `references/reference_by_ai/`
- Default Elicit role: literature discovery, screening, extraction, and evidence collection

### Zotero

- Zotero use:
- Default browser:
- Zotero Connector installed:
- PDF archive target:
- BibTeX source of truth:

### Overleaf

- Draft workspace: `draft/`
- Overleaf remote URL:
- Overleaf username: `git`
- Overleaf token source: environment variable `<OVERLEAF_TOKEN_ENV_NAME>`
- Push policy:
- Pull policy:

The Overleaf remote URL determines the destination project. The token only authenticates the account.

### Journal overlay

- Target journal:
- Journal-specific rules source:
- Writing overlay policy:
- Replication or submission overlay policy:

### Raw data and restricted data

- Raw data location:
- Restricted data:
- Data that must not be committed:
- Data that can enter replication package:
- Data access notes:

## Required pre-flight before agent work

Before changing files, the agent should confirm from this README and `project.yaml`:

1. Current `workflow_state`.
2. Whether the task is blocked by topic, identification, output, draft, or submission gate.
3. Whether Elicit, Zotero, Overleaf, or a journal overlay is involved.
4. Whether required environment variables are named and available.
5. Whether raw or restricted data are involved.
6. Whether the task should touch `work/` only or main `code/`, `output/`, and `draft/`.
7. Whether Overleaf remote URL and token source are recorded before any git sync.
8. Whether current outputs are newer than draft snippets before refreshing the draft.

## Notes

- `notes/run_log.md` records major empirical runs.
- `notes/decision_log.md` records major research decisions.
- `notes/` should remain flat by default.
