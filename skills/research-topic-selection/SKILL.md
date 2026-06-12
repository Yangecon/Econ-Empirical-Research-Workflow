---
name: research-topic-selection
description: Manage the idea-stage bounded two-agent loop for empirical economics research. Use when the user asks to evaluate or generate research ideas, run topic selection, process human seed data, check novelty, use Elicit for topic-stage evidence, score contribution, decide go/refine/park/drop, record failure reasons, or update idea registries. Triggers: topic selection, idea generator, literature judge, human seed, data policy, contribution score, failure reasons, novelty check, feasible question, Elicit topic scan, go refine park drop.
---

# Research Topic Selection

## Purpose

Use this skill in the `idea/` stage.

The goal is to turn human seed input and candidate research questions into a structured topic gate decision:

```text
go / refine / park / drop
```

## Architecture

The idea stage is a bounded two-agent loop:

```text
Human seed + data policy
  -> Idea Generator Agent
      -> candidate ideas
          -> Literature + Judge Agent
              -> evidence + scorecard + decision + failure reasons
                  -> next round or stop
```

Elicit is evidence collection, not final judgment.

## Required folders

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

## Human seed and data policy

The first required input is:

```text
idea/intake/human_seed.json
```

Minimum fields:

```json
{
  "initial_research_question": "",
  "existing_data": [],
  "data_search_policy": {
    "allow_new_data_search": false,
    "allow_public_data_only": true,
    "allow_restricted_data": false,
    "must_use_existing_data": true
  }
}
```

If `allow_new_data_search = false`, the Idea Generator may only propose ideas using human-provided existing data.

If `allow_new_data_search = true`, new-data ideas must check:

- public availability
- data fit
- unit match
- coverage match
- key variables availability
- access risk

## Loop limits

Read from `project.yaml`:

```yaml
idea_loop:
  max_idea_search_rounds: 10
  stop_if_any_go: true
  no_improvement_rounds_limit: 3
  human_manual_stop: false
  stop_if_all_candidates_data_blocked: true
```

Stop when:

1. at least one candidate receives `go`;
2. 10 rounds are reached;
3. the best score fails to improve for the configured number of rounds;
4. the human manually stops;
5. all candidates are blocked by unavailable data.

## Idea Generator Agent

Responsibilities:

1. Generate new ideas from human seed and data policy.
2. Rewrite weak ideas based on failure reasons.
3. Produce variants with sharper identification, lighter data, and bigger contribution.
4. Avoid repeating dropped ideas unless a concrete fix exists.
5. Write candidate files under `idea/ideas/<idea_id>/`.
6. Update `idea/registry/idea_registry.csv` and `idea/registry/loop_log.csv`.

## Literature + Judge Agent

Responsibilities:

1. Collect and organize prior literature evidence.
2. Use Elicit outputs under `idea/ideas/<idea_id>/elicit/`.
3. Build a gap map.
4. Evaluate identification plausibility.
5. Evaluate data feasibility.
6. Score expected contribution.
7. Write `contribution_scorecard.json`.
8. Write `topic_decision.md`.
9. Record structured failure reasons.
10. Update the idea registry and loop log.

## Required output per idea

```text
idea/ideas/<idea_id>/question_intake.json
idea/ideas/<idea_id>/data_fit.json
idea/ideas/<idea_id>/idea_brief.md
idea/ideas/<idea_id>/elicit/
idea/ideas/<idea_id>/prior_literature.md
idea/ideas/<idea_id>/gap_map.csv
idea/ideas/<idea_id>/contribution_scorecard.json
idea/ideas/<idea_id>/topic_decision.md
```

## Idea registry

Maintain:

```text
idea/registry/idea_registry.csv
```

Required columns:

```text
idea_id,round,source,normalized_question,uses_existing_data,requires_new_data,new_data_allowed,public_data_available,data_fit_status,total_score,decision,failure_reasons,next_action
```

Parked or dropped ideas should remain in the registry so they can be revived when data or identification improves.

## Scoring rubric

Total: 100.

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
- new data required but not allowed by data policy

Structured failure reasons:

```text
weak_identification
weak_data_path
unclear_data_access
low_novelty
closest_literature_too_close
too_expensive
audience_too_narrow
unclear_mechanism
measurement_problem
scope_too_broad
new_data_not_allowed
public_data_not_available
```

## Topic gate update

When an idea receives `go`, update `project.yaml`:

```yaml
workflow_state:
  active_stage: identification_gate
  active_idea_id: <idea_id>
  active_rq_id: <rq_id>
  topic_gate_status: go
```

For `refine`, `park`, or `drop`, keep `active_stage: idea` unless the human overrides.
