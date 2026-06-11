# Econ Empirical Research Workflow

[中文说明 / Chinese Version](./README.zh-CN.md)

A reusable Codex skill bundle for empirical economics research.

This repository packages a complete Default applied-economics workflow for Codex: idea triage, identification design, Stata execution, draft assembly, and submission packaging. It is designed for AER, QJE, and AEJ-style empirical projects and ships with reusable skills, project scaffolds, Stata templates, writing templates, and validation helpers.

## What This Repo Is

This is a public skill bundle repository, not the home directory for all of your projects.

Recommended layout:

```text
Project-A/
Project-B/
econ-empirical-research-workflow/
```

Keep your real empirical projects outside this repository and install or copy the skills into Codex separately.

## Scope

This repository is intentionally opinionated:

1. It focuses on Default applied econ only.
2. It treats Stata as the canonical empirical execution stack.
3. It treats `output/ -> draft/ -> Overleaf` as the default downstream writing pipeline.

It does not try to cover epidemiology workflows, ML-causal workflows, or a Python-first empirical stack.

## Canonical Workflow

```text
idea
  -> topic gate
      -> references + notes
          -> identification gate
              -> data + code
                  -> output
                      -> draft
                          -> Overleaf / paper
```

Hard gates:

1. Topic gate: `go`, `refine`, `park`, or `drop`
2. Identification gate: `freeze`, `redesign`, or `park`

Once the design is frozen, the default empirical pipeline is:

```text
import / cleaning
-> variable construction
-> Table 1
-> diagnostic tests
-> baseline modeling
-> robustness gauntlet
-> mechanism + heterogeneity
-> publication-ready tables / figures
```

## Skill List

```text
skills/
  research-workflow/
  research-topic-selection/
  research-identification/
  research-empirics/
  empirical-analysis-stata/
  research-writing/
  output-draft-overleaf-sync/
  research-submission/
  reference-elicit-agent/
```

What each skill does:

- `research-workflow`: routes a project to the correct next skill by inspecting stage, structure, and missing artifacts.
- `research-topic-selection`: evaluates candidate research questions, novelty, feasibility, and contribution.
- `research-identification`: freezes the estimand, design, assumptions, data requirements, and robustness plan.
- `research-empirics`: runs the generic empirical production workflow and refreshes output artifacts.
- `empirical-analysis-stata`: the main Stata-first applied econ skill, including deep references under `skills/empirical-analysis-stata/references/`.
- `research-writing`: drafts and revises empirical paper prose and manages draft-folder logic.
- `output-draft-overleaf-sync`: refreshes downstream draft assets and checks Overleaf handoff readiness.
- `research-submission`: prepares a submission-ready `paper/` folder and replication package.
- `reference-elicit-agent`: manages the Elicit-centered literature workflow under `references/`.

## Main Stata Skill

`empirical-analysis-stata` is the core execution skill in this repository.

It is adapted from a stronger general Stata empirical-analysis skill and narrowed to one branch only:

```text
Default applied econ only
```

It includes:

- an 8-step applied-econ Stata workflow
- trigger-rich skill metadata for Codex
- step-by-step deep references for cleaning, transformation, descriptives, diagnostics, modeling, robustness, further analysis, and tables/plots

Key estimator families:

- `reghdfe`
- `ivreg2` and `ivreghdfe`
- `csdid`, `eventstudyinteract`, `did_imputation`, `sdid`
- `rdrobust`
- `synth` and `synth_runner`
- `teffects`, `psmatch2`, `ebalance`

Key robustness tools:

- `bacondecomp`
- `honestdid`
- `boottest`
- `ritest`
- `rwolf`
- `psacalc`

## Project Structure

The scaffolded project structure is:

```text
<Project>/
  README.md
  project.yaml
  idea/
  references/
  notes/
  data/
    raw/
    build/
    final_sample.dta
  code/
    build/
    00_setup.do
    01_estimation.do
    02_robustness.do
    03_figures.do
    04_tables.do
    99_master.do
  output/
    raw/
    figures/
    tables/
  draft/
    main.tex
    images/
    figures/
    tables/
  work/
  paper/
    tex/
    replication_package/
```

## Install in Codex

Codex discovers skills when each skill folder is placed under the user's skill directory.

Typical install flow:

1. Clone or download this repository.
2. Copy or symlink the needed folders from `skills/` into `~/.codex/skills/` or `$CODEX_HOME/skills/`.
3. Keep the folder names unchanged.
4. Open a separate empirical project and invoke the installed skills there.

This repository already includes `agents/openai.yaml` metadata for the bundled skills, which improves the Codex skill-list and chip-style UI experience.

## How Skills Trigger

Each skill in this repository includes:

- a `SKILL.md` file with valid frontmatter
- a `description` that explicitly states when to use the skill
- trigger phrases inside the skill body

That is enough for core skill discovery.

For richer skill-list and chip-style UI behavior in Codex, this repository already includes `agents/openai.yaml` metadata for all bundled skills.

## Templates and Scripts

Included template groups:

```text
templates/project/
templates/stata/
templates/writing/
templates/submission/
templates/references/
templates/custom/
```

Scaffold a project:

```bash
python scripts/scaffold_project.py --dest /path/to/Project-A --slug project-a --title "Project A"
```

Validate a scaffolded project:

```bash
python scripts/validate_project.py --project-root /path/to/Project-A
```

## Repo Contents

For a compact inventory of the repository, see [docs/repo-contents.md](./docs/repo-contents.md).

## License

See [LICENSE](./LICENSE).
