---
name: research-submission
description: Prepare the submission-stage paper folder, including final TeX copy and replication package. Use when the user asks to freeze a submission draft, assemble a replication package, check that paper tables and figures match cleaned output, or prepare a journal-ready archival copy under `paper/`. Triggers: submission package, replication package, final TeX, archive submission draft, submission-ready paper, replication README.
---

# Research Submission

## Purpose

Use this skill when the project is moving from active drafting to submission or replication-package preparation.

## Trigger phrases

- submission package
- replication package
- final TeX
- freeze the paper
- archive submission draft
- replication README

## Folder

Use:

```text
paper/
```

This is not the reference folder. References live under:

```text
references/
```

## Expected structure

```text
paper/
  tex/
  replication_package/
```

## Required tasks

1. Copy or freeze the submission TeX draft into `paper/tex/`.
2. Assemble replication code and data into `paper/replication_package/`.
3. Write a replication README.
4. Confirm that code paths are relative.
5. Confirm that raw restricted data are not accidentally included.
6. Confirm that tables and figures in the submission draft match cleaned outputs.
7. Use a journal-specific overlay when available.

## Required outputs

```text
paper/tex/
paper/replication_package/README.md
paper/replication_package/code/
paper/replication_package/data/
paper/replication_package/output/
```
