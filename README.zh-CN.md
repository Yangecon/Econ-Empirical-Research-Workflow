# Econ Empirical Research Workflow

[English Version](./README.md)

一个可复用、可直接安装到 Codex 的实证经济学工作流 skill bundle。

这个仓库把 applied economics 项目里常见的环节打包成可复用组件：idea 筛选、文献证据收集、识别设计、Stata-first 实证执行、结果整理、论文写作、Overleaf 同步与投稿打包。整体默认面向 AER / QJE / AEJ 风格的 applied econ 项目。

## 这个仓库是什么

这是一个公开的 skill bundle 仓库，不是所有实证项目的 home directory。

你可以把其中的 skills 安装到 Codex，也可以按需使用其中的 templates、scripts 和 shared schemas。

## 适用范围

这个仓库是有明确取舍的：

1. 只聚焦 default applied economics。
2. 以 Stata 作为默认实证执行栈。
3. 以 `output/ -> draft/ -> paper/` 作为默认下游写作与投稿流程。
4. 把 `references/` 和 `notes/` 视为 persistent resource layers，而不是主流程阶段。

它不试图覆盖 epidemiology workflow、ML-causal workflow，或 Python-first 的实证执行栈。

## 标准主流程

```text
Idea
  -> Topic Gate
      -> Identification Gate
          -> Empirical Analysis
              -> Output
                  -> Draft
                      -> Submission
```

持续资源层包括：

```text
references/
notes/
work/
```

这些目录贯穿全项目使用，但不属于 hard gate 阶段。

## Idea 阶段：Bounded Two-Agent Loop

idea 阶段是一个有上限、基于文件交接的 loop，而不是自由聊天。

```text
Human seed + data policy
  -> Idea Generator Agent
      -> candidate ideas / idea queue
          -> Literature + Judge Agent
              -> evidence / scorecard / topic decision / failure reasons
                  -> Idea Generator Agent reads failure reasons and generates next round
```

loop 限制：

- `max_idea_search_rounds = 10`
- 至少有一个 idea 获得 `go` 时停止
- 连续多轮最高分不再提高时停止
- human 手动停止时停止
- 所有候选都因数据路径不可得而被 `park` / `drop` 时停止

Elicit 负责 evidence collection，不负责最终判断。

## Project Structure

scaffold 后的项目结构如下：

```text
<Project>/
  README.md
  project.yaml
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
  references/
  notes/
  data/
    raw/
    build/
    codebook/
    final_sample.dta
  code/
    build/
      00_build_sample.do
    _write_version_log.do
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

## Skill List

```text
skills/
  econ-empirical-research-workflow/
  research-workflow/
  research-idea-selection/
  research-identification/
  research-empirics/
  empirical-analysis-stata/
  research-writing/
  output-draft-overleaf-sync/
  research-submission/
  reference-elicit-agent/
```

各个 skill 的作用：

- `econ-empirical-research-workflow`：整个仓库的统一入口 skill，负责把项目从 idea 路由到 submission。
- `research-workflow`：读取 `project.yaml`、`workflow_state` 和关键产物，判断当前阶段与下一步。
- `research-idea-selection`：管理 bounded two-agent idea loop。
- `research-identification`：冻结 estimand、识别设计、核心假设、数据要求与 robustness plan。
- `research-empirics`：运行通用 empirical production workflow，并刷新 output artifacts。
- `empirical-analysis-stata`：Stata-first 的 applied econ 实证执行 skill。
- `research-writing`：负责论文正文写作、改写与 draft folder 逻辑。
- `output-draft-overleaf-sync`：刷新下游 draft assets，并检查 Overleaf handoff readiness。
- `research-submission`：准备 submission-ready `paper/` folder 和 replication package。
- `reference-elicit-agent`：管理 `references/` 下以 Elicit 为中心的持续文献工作流。

## Repo Contents

精简目录清单见 [docs/repo-contents.md](./docs/repo-contents.md)。
