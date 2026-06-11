# <Project Title>

This repository is the cleaned working copy of the project. It should be runnable through relative paths and should record all project-specific settings needed before agents edit results, run the Stata pipeline, refresh draft files, touch Overleaf, work on references, or prepare replication materials.

## Current status

- Active stage:
- Active research question ID:
- Topic gate status:
- Identification gate status:
- Last empirical run:
- Current draft target:
- Current submission target:
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
- `code/build/...`
- `code/01_estimation.do`
- `code/02_robustness.do`
- `code/03_figures.do`
- `code/04_tables.do`
- `code/99_master.do`

## Folder map

- `idea/`: research-question evaluation and Elicit topic-stage evidence
- `references/`: human, AI, and merged literature/reference lanes
- `notes/`: flat project notes, identification memo, PAP, robustness plan, decision log, run log
- `data/`: raw data, build data, and final analysis samples
- `code/`: Stata build scripts plus estimation, robustness, figure, and table scripts
- `output/`: raw outputs plus cleaned figures/tables
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

Main final sample:

```text
data/<final_sample>.dta
```

Scripts should still resolve the project root when launched from `code/`.

## Project settings

### Elicit

- Elicit API key environment variable: `ELICIT_API_KEY`
- Topic-stage Elicit folder: `idea/`
- Reference-stage Elicit folder: `references/reference_by_ai/`
- Default Elicit role: literature discovery, screening, extraction, and topic/reference evaluation

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

1. Active stage and task target.
2. Whether Elicit, Zotero, Overleaf, or a journal overlay is involved.
3. Whether required environment variables are named and available.
4. Whether raw or restricted data are involved.
5. Whether the task should touch `work/` only or main `code/`, `output/`, and `draft/`.
6. Whether Overleaf remote URL and token source are recorded before any git sync.
7. Whether current outputs are newer than draft snippets before refreshing the draft.

## Agent workflow

- For topic evaluation, work in `idea/` and write `idea/topic_decision.md`.
- For identification, write flat files under `notes/`, especially `notes/identification.md` and `notes/identification_status.json`.
- For empirical work, use `code/build/` for sample construction and root `code/` scripts for estimation and outputs.
- For exploratory branches, use `work/<exploration_slug>/`.
- For draft updates, treat `output/` as upstream and `draft/` as downstream.
- For Overleaf sync, read this README first and verify remote URL and token source.
- For submission, use `paper/tex/` and `paper/replication_package/`.

## Notes

- `notes/run_log.md` records major empirical runs.
- `notes/decision_log.md` records major research decisions.
- `notes/` should remain flat by default.
