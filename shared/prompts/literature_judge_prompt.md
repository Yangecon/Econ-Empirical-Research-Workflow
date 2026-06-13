# Literature + Judge Prompt

Read the candidate idea folder under `idea/ideas/<idea_id>/`.

Use Elicit and human references only as evidence. Do not outsource final judgment to Elicit.

Produce:
- `prior_literature.md`
- `gap_map.csv`
- `contribution_scorecard.json`
- `topic_decision.md`

Scoring:
- question clarity: 10
- literature gap and novelty: 20
- identification plausibility: 25
- data feasibility: 20
- importance and audience (general interest / cross-subfield interest): 15
- execution cost: 10

For `importance and audience`, judge this in the editor sense, not the mass-public sense.

- Ask whether the paper has general-interest value for a top-field editor.
- Ask whether economists outside the home field would cite it.
- Use a cross-subfield-interest test.
- If you cannot name at least three economics subfields that would plausibly cite the paper, treat the audience as too narrow for a top general-interest outlet.

Decision:
- 85-100: go
- 70-84: refine
- 55-69: park
- below 55: drop

Always record structured `failure_reasons`.
