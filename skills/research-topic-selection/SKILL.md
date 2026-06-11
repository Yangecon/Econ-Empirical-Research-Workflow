---
name: research-topic-selection
description: Evaluate empirical economics research questions using human anchors, Elicit literature discovery, prior-literature mapping, gap assessment, identification plausibility, data feasibility, contribution scoring, and alternative-question generation. Use when the user asks to evaluate a topic, screen research ideas, assess novelty, compare candidate questions, decide go/refine/park/drop, or do topic-stage Elicit work. Triggers: topic selection, research idea evaluation, contribution score, novelty check, feasible question, applied econ topic, Elicit topic scan.
---

# Research Topic Selection

## Purpose

Use this skill in the `idea/` stage.

The goal is to turn raw research ideas into a structured topic decision:

```text
go / refine / park / drop
```

## Trigger phrases

- topic selection
- evaluate this research idea
- is this question publishable
- novelty check
- contribution score
- feasible applied econ topic
- Elicit topic scan
- go refine park drop

## Folder

Use:

```text
idea/
```

Do not put topic-stage evaluation under `references/`. The `references/` folder is the longer-term literature library.

## Elicit role

Elicit API is used in the topic stage to collect and structure prior literature.

Preferred order:

1. Systematic Review API for structured search, screening, fulltext, extraction, and report outputs.
2. Search API as supplementary fallback when broader candidate discovery is needed.

Elicit is evidence collection, not final judgment.

## Required tasks

1. Normalize the research question.
2. Record human anchor references.
3. Generate an Elicit config.
4. Save Elicit outputs under `idea/`.
5. Write prior-literature summary.
6. Build gap map.
7. Evaluate identification plausibility.
8. Evaluate data feasibility.
9. Score expected contribution.
10. Generate alternative research questions.
11. Write topic decision memo.

## Required outputs

```text
idea/question_intake.json
idea/anchor_references.md
idea/elicit_systematic_review_config.json
idea/elicit_search.csv
idea/elicit_screen.csv
idea/elicit_fulltext.csv
idea/elicit_extract.csv
idea/prior_literature.md
idea/gap_map.csv
idea/contribution_scorecard.json
idea/alternative_questions.json
idea/topic_decision.md
```

## Scoring rubric

Total: 100

- question clarity: 10
- literature gap and novelty: 20
- identification plausibility: 25
- data feasibility: 20
- importance and audience: 15
- execution cost: 10

Decision rule:

- 85-100: `go`
- 70-84: `refine`
- 55-69: `park`
- below 55: `drop`

Hard kill-switch:

- no credible identification path
- no credible data path
- closest literature already answers the same question with the same design

## Alternative-question rule

Always produce:

1. `sharper_identification`
2. `lighter_data`
3. `bigger_contribution`
