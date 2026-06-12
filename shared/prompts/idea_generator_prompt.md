# Idea Generator Prompt

Read:
- `idea/intake/human_seed.json`
- `idea/registry/idea_registry.csv`
- previous `contribution_scorecard.json` files
- previous `topic_decision.md` files

Generate candidate ideas for the next round.

Rules:
1. Respect `data_search_policy`.
2. If new data search is not allowed, propose only ideas that can use `existing_data`.
3. If new data search is allowed, include public availability, data fit, unit match, coverage match, key variables, and access-risk checks.
4. React to prior `failure_reasons`.
5. Avoid regenerating dropped ideas unless a concrete data or identification fix exists.
6. Update `idea_registry.csv` and `loop_log.csv`.
