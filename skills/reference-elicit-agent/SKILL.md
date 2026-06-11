---
name: reference-elicit-agent
description: Run Elicit-assisted reference workflows, preserving systematic-review outputs, ranked AI candidates, human references, merged references, and Zotero follow-up queues. Use when the user asks for literature discovery, structured paper screening, extraction tables, BibTeX refresh, PDF follow-up, or a merged writing-ready reference library. Triggers: literature review, Elicit search, paper screening, extract references, BibTeX merge, Zotero follow-up, reference library.
---

# Reference Elicit Agent

## Purpose

Use this skill for literature workflows.

## Trigger phrases

- literature review
- Elicit search
- screen papers
- extract papers
- BibTeX merge
- reference library
- Zotero follow-up

## Folder

Use:

```text
references/
```

Do not use a top-level `papers/` folder for references.

## Reference lanes

```text
references/reference_by_human/
references/reference_by_ai/
references/reference_merged/
```

## Rules

- Human references are trusted anchors.
- AI references are candidate papers from Elicit.
- Merged references are the writing-ready pool.
- Keep metadata, PDFs, BibTeX, screening notes, and writing evidence separate.
- Use Elicit Systematic Review API first when available.
- Use Search API only as fallback or supplementary expansion.
- Use Zotero for unresolved PDFs and citation verification.
- Never hard-code API keys.

## Required environment variable

Read the Elicit API key from the environment variable named in the project README or `project.yaml`.

## Required outputs

```text
references/reference_by_ai/systematic_review/search.csv
references/reference_by_ai/systematic_review/screen.csv
references/reference_by_ai/systematic_review/fulltext.csv
references/reference_by_ai/systematic_review/extract.csv
references/reference_by_ai/paper_registry.jsonl
references/reference_by_ai/reference_overview.csv
references/reference_by_ai/ref.bib
references/reference_merged/approved_papers.jsonl
references/reference_merged/ref.bib
references/reference_merged/literature_review.md
```
