---
name: research-workflow
description: Route an empirical economics project to the correct skill by inspecting project.yaml, workflow_state, current gates, paths, settings, and missing artifacts. Use when the user asks what to do next, which stage the project is in, whether a gate blocks progress, whether output/draft/submission is ready, or which specialized skill should handle the next task. Triggers: workflow router, next step, project stage, workflow state, missing artifacts, gate status, route this project, what should I do next, empirical workflow.
---

# Research Workflow

## Purpose

Use this skill as the router for an empirical economics project. It should not do all substantive work itself. It decides which specialized skill should run next and which artifacts are missing.

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

- `references/` is a persistent literature resource layer, not a main workflow stage.
- `notes/` is a persistent project-note layer, not a main workflow stage.
- Use `paper/` for submission-stage TeX and replication package.
- Do not create top-level `docs/`, `design/`, or `papers/` by default.
- Use `notes/run_log.md` for lightweight run logs.
- Use `notes/decision_log.md` for major decisions.

## Pre-flight

Before changing project files, read:

```text
README.md
project.yaml
```

Check:

1. `workflow_state.active_stage`.
2. `workflow_state.active_idea_id`.
3. `workflow_state.active_rq_id`.
4. `workflow_state.topic_gate_status`.
5. `workflow_state.identification_gate_status`.
6. `workflow_state.output_status`.
7. `workflow_state.draft_status`.
8. `workflow_state.submission_status`.
9. `workflow_state.last_empirical_run_id`.
10. `workflow_state.current_reproduction_target`.
11. Whether the task touches Elicit, Zotero, Overleaf, raw data, restricted data, or submission.
12. Whether `work/` or the main pipeline should be used.

## Hard routing logic

1. If `workflow_state.topic_gate_status != go`, route to `research-topic-selection` and do not enter identification.
2. If `workflow_state.identification_gate_status != freeze`, route to `research-identification` and do not enter empirical analysis.
3. If the design is frozen but no empirical run exists, route to `research-empirics` or `empirical-analysis-stata`.
4. If outputs are missing or stale, route to `research-empirics` or `empirical-analysis-stata`.
5. If `workflow_state.output_status != ready`, do not refresh draft.
6. If output is ready but draft snippets are stale or missing, route to `research-writing` or `output-draft-overleaf-sync`.
7. If `workflow_state.draft_status != ready`, do not package submission.
8. If the user asks for submission version or replication package and draft is ready, route to `research-submission`.
9. If the user asks for literature discovery, BibTeX, or PDFs outside topic gate, route to `reference-elicit-agent`.

## Report format

Report:

- current workflow state
- missing artifacts
- blocked gates
- next skill
- rationale
- exact files to inspect or create next
