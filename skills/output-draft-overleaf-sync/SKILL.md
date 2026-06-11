---
name: output-draft-overleaf-sync
description: Refresh downstream draft assets and Overleaf-ready LaTeX inputs from cleaned empirical output. Use when `output/figures` and `output/tables` need to be propagated into `draft/`, when figure wrappers or table snippets are stale, when `draft/main.tex` needs refreshed inputs, or when a project needs the final output-to-draft-to-Overleaf handoff checked before sync. Triggers: sync output to draft, refresh draft assets, Overleaf sync prep, figure wrappers, table snippets, draft handoff.
---

# Output Draft Overleaf Sync

Treat `output/` as upstream, `draft/` as downstream, and Overleaf as the publishing mirror of `draft/`.

## Trigger phrases

- sync output to draft
- refresh draft assets
- Overleaf sync prep
- figure wrappers
- table snippets
- draft handoff

## Read first

Inspect:

```text
README.md
project.yaml
draft/main.tex
output/figures/
output/tables/
notes/run_log.md
```

If the task includes Overleaf sync, also inspect the project README for:

- Overleaf remote URL
- Overleaf token environment variable
- push and pull policy
- current draft target

## Folder contract

Use only:

```text
draft/main.tex
draft/images/
draft/figures/
draft/tables/
```

Rules:

- copy cleaned image assets from `output/figures/` into `draft/images/`
- place figure wrapper `.tex` files in `draft/figures/`
- place cleaned table snippets in `draft/tables/`
- never treat `draft/` as source of truth for empirical results
- never sync `output/raw/` into `draft/` unless the user explicitly asks

## Required workflow

1. Confirm which figures and tables are the current paper-ready artifacts.
2. Refresh `draft/images/` from cleaned outputs only.
3. Refresh or create figure wrapper files so `draft/main.tex` can `\input{}` them.
4. Refresh or create table snippets so `draft/main.tex` can `\input{}` them.
5. Check path consistency between wrappers/snippets and `draft/main.tex`.
6. If Overleaf is in scope, verify the README records the destination remote and token source before any sync step.

## Figure wrapper rule

Each wrapper should do one job: point to one image under `draft/images/` with a stable caption and label placeholder if the project does not already define them elsewhere.

Prefer wrappers that are easy to diff and easy for a human to edit later.

## Table snippet rule

If the upstream table is already LaTeX-ready, keep it as the snippet.

If the upstream table is not LaTeX-ready, convert it into a minimal snippet that `draft/main.tex` can include without extra manual cleanup.

## Overleaf guardrails

- do not push if the README does not record the target remote
- do not assume the token variable name from memory
- do not rewrite project-specific git policy
- do not create a second draft source outside `draft/`

## Deliverable

Report:

- which draft assets were refreshed
- whether wrappers or snippets were added or updated
- whether `draft/main.tex` is aligned
- whether the project is ready for Overleaf sync
