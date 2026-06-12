# Workflow Map

## Main stage sequence

```text
Idea
  -> Topic Gate
      -> Identification Gate
          -> Empirical Analysis
              -> Output
                  -> Draft
                      -> Submission
```

## Persistent resource layers

```text
references/
notes/
work/
```

These are not workflow stages. They support multiple stages.

## Router state

The router should read `project.yaml`, especially:

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

## Hard gates

| From | To | Required state |
|---|---|---|
| Idea | Identification Gate | `topic_gate_status: go` |
| Identification Gate | Empirical Analysis | `identification_gate_status: freeze` |
| Empirical Analysis | Output | `last_empirical_run_id` recorded and outputs refreshed |
| Output | Draft | `output_status: ready` |
| Draft | Submission | `draft_status: ready` |

## Idea-stage loop

```text
Human seed + data policy
  -> Idea Generator Agent
      -> candidate ideas
          -> Literature + Judge Agent
              -> scorecard + decision + failure reasons
                  -> next round or stop
```

Maximum search rounds: 10.

Elicit is evidence collection, not final judgment.
