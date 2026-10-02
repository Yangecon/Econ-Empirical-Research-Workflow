# Repository Contents

This document summarizes the public contents of `econ-empirical-research-workflow`.

## Root

```text
README.md
README.zh-CN.md
LICENSE
.gitignore
```

## Docs

```text
docs/workflow-map.md
docs/repo-contents.md
```

## Skills

```text
skills/econ-empirical-research-workflow/SKILL.md
skills/econ-empirical-research-workflow/agents/openai.yaml
skills/research-workflow/SKILL.md
skills/research-workflow/agents/openai.yaml
skills/research-topic-selection/SKILL.md
skills/research-topic-selection/agents/openai.yaml
skills/research-identification/SKILL.md
skills/research-identification/agents/openai.yaml
skills/research-empirics/SKILL.md
skills/research-empirics/agents/openai.yaml
skills/empirical-analysis-stata/SKILL.md
skills/empirical-analysis-stata/agents/openai.yaml
skills/empirical-analysis-stata/references/
skills/empirical-analysis-stata/references/09-table-examples.md
skills/research-writing/SKILL.md
skills/research-writing/agents/openai.yaml
skills/output-draft-overleaf-sync/SKILL.md
skills/output-draft-overleaf-sync/agents/openai.yaml
skills/research-submission/SKILL.md
skills/research-submission/agents/openai.yaml
skills/reference-elicit-agent/SKILL.md
skills/reference-elicit-agent/agents/openai.yaml
```

## Templates

```text
templates/project/README.md
templates/project/project.yaml
templates/idea/intake/
templates/idea/registry/
templates/idea/agents/
templates/idea/ideas/idea_001/
templates/stata/
templates/writing/
templates/submission/
templates/references/
templates/custom/
```

## Scripts

```text
scripts/scaffold_project.py
scripts/validate_project.py
```

## Shared

```text
shared/schemas/human_seed.schema.json
shared/schemas/question_intake.schema.json
shared/schemas/contribution_scorecard.schema.json
shared/schemas/workflow_state.schema.json
shared/rubrics/topic_contribution_score.md
shared/prompts/idea_generator_prompt.md
shared/prompts/literature_judge_prompt.md
shared/prompts/topic_evaluation_prompt.md
```

## Curated figure resources

- `skills/empirical-econ-figures/`: portable skill, 50 templates, inputs, paired documentation and shared dependencies.
- `gallery/empirical-econ-figures/`: 97 English example PNGs, 56 paper/original reference PNGs and paired 50-row overview; shared plotting code stays in the skill.
- `scripts/figure_catalog.py`: category/tag/language/ID discovery.
- `scripts/validate_figures.py`: catalog, integrity, gallery and runtime checks.
- `docs/figure-integration.md` / `.zh-CN.md`: workflow handoff and examples.
- `requirements-figures.txt`: shared figure runtime.
- `.github/workflows/figures.yml`: Python integration checks.
