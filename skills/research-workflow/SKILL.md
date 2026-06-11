---
name: research-workflow
description: Route an empirical economics project to the correct skill by inspecting project structure, current stage, settings, and missing artifacts. Use when the user asks what to do next, which stage the project is in, which files are missing, whether the design is frozen, or which specialized skill should handle the next task. Triggers: workflow router, next step, project stage, missing artifacts, route this project, what should I do next, empirical workflow.
---

# Research Workflow

## Purpose

Use this skill as the router for an empirical economics project.

It should not do all substantive work itself. It should decide which specialized skill should run next and which artifacts are missing.

## Trigger phrases

- what should I do next
- which stage is this project in
- route this project
- workflow router
- missing artifacts
- next empirical step

## Expected project folders

```text
idea/
references/
notes/
data/
code/
output/
draft/
work/
paper/
```

## Folder rules

- Use `references/`, not `papers/`, for literature and citation materials.
- Use `paper/` for submission-stage TeX and replication package.
- Use `notes/` as a flat folder by default.
- Do not create top-level `docs/`, `design/`, or `papers/` by default.
- Do not create `output/manifests/` by default.
- Use `notes/run_log.md` for lightweight run logs.
- Use `notes/decision_log.md` for major decisions.

## Pre-flight

Before changing project files, read:

```text
README.md
project.yaml
```

Check:

1. Active stage.
2. Active research question.
3. Current reproduction target.
4. Whether the task touches Elicit, Zotero, Overleaf, raw data, restricted data, or submission.
5. Environment variable names for Elicit and Overleaf.
6. Overleaf draft workspace, remote URL, username, and token source.
7. Whether a journal overlay is expected.
8. Whether the task belongs in `work/` or the main pipeline.
9. Whether `notes/run_log.md` or `notes/decision_log.md` needs an update.

## Routing logic

1. If `idea/topic_decision.md` is missing, call `research-topic-selection`.
2. If topic decision is not `go`, stop and report the topic status.
3. If `notes/identification_status.json` is missing or not `freeze`, call `research-identification`.
4. If the user asks for a full Stata-first applied econ workflow, call `empirical-analysis-stata`.
5. If the design is frozen but no cleaned tables or figures exist under `output/`, call `research-empirics`.
6. If outputs exist but draft TeX wrappers are stale or missing, call `research-writing` or `output-draft-overleaf-sync`.
7. If the user asks for literature discovery, BibTeX, or PDFs, call `reference-elicit-agent`.
8. If the user asks for submission version or replication package, call `research-submission`.
9. If the user asks to write or revise empirical paper prose, call `research-writing`.

## Report format

Report:

- current stage
- missing artifacts
- next skill
- rationale
- whether the task is blocked by a hard gate
