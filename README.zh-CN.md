# Econ Empirical Research Workflow

一个面向实证经济学项目的 Codex-ready skill bundle。它把选题、文献证据、识别设计、Stata 实证执行、结果整理、论文写作和投稿打包成可复用的工作流。

## 核心定位

这个 repo 不是所有项目的 home directory，而是一个可安装、可复制的 workflow/skill bundle。真实项目建议和本 repo 平行放置：

```text
Project-A/
Project-B/
econ-empirical-research-workflow/
```

## 主流程

主流程只保留真正的阶段和 hard gates：

```text
Idea
  -> Topic Gate
      -> Identification Gate
          -> Empirical Analysis
              -> Output
                  -> Draft
                      -> Submission
```

`references/` 和 `notes/` 是持续资源层，贯穿多个阶段，但不是主流程中间的独立步骤。

## 显式 workflow state

每个项目的 `project.yaml` 仍保留兼容旧版的 `active_stage` / `active_rq_id`，但 router 应以明确的 `workflow_state` 为准：

```yaml
workflow_state:
  active_stage: idea
  active_idea_id: null
  active_rq_id: null
  topic_gate_status: null          # go / refine / park / drop
  identification_gate_status: null # freeze / redesign / park
  output_status: null              # not_started / running / ready / stale
  draft_status: null               # not_started / drafting / ready / stale
  submission_status: null          # not_started / packaging / ready
  last_empirical_run_id: null
  current_reproduction_target: null
```

router 按这个状态判断是否允许进入下一阶段：

1. topic 没有 `go`，不进入 identification；
2. identification 没有 `freeze`，不进入 empirical analysis；
3. output 没有 `ready`，不进入 draft；
4. draft 没有 `ready`，不进入 submission。

## Idea 阶段：bounded two-agent loop

idea 阶段拆成两个 agent：

```text
Idea Generator Agent
  负责提出新 idea、改写 idea、根据失败原因继续发散

Literature + Judge Agent
  负责查文献、整理 evidence、打分、判断 go/refine/park/drop
```

循环最多 10 轮，并通过文件交接，不靠自由聊天状态：

```text
Idea Generator -> candidate ideas / idea queue
Literature + Judge -> scorecard + topic_decision + failure_reasons
Idea Generator -> 读取 failure_reasons 后继续下一轮
```

停止条件：

1. 找到至少一个 `go`；
2. 达到 10 轮；
3. 连续几轮最高分无改善；
4. human 手动停止；
5. 所有候选都因为数据不可得被 `park`/`drop`。

Elicit 只负责 evidence collection，不是最终判断。

## human seed + data policy

项目初始化时需要填写：

```text
idea/intake/human_seed.md
idea/intake/human_seed.json
```

核心字段包括：

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

如果 `allow_new_data_search = false`，Idea Generator 只能基于已有数据发散。如果允许找新数据，必须检查 public availability、data fit、unit match、coverage match、key variables availability 和 access risk。

## Stata version log

不做全局 Stata 环境快照。每个 `.do` 文件根据自己的依赖包调用：

```text
code/_write_version_log.do
```

并把脚本级 version/package check 输出到：

```text
output/raw/stata_version_log.csv
```

## 使用

```bash
python scripts/scaffold_project.py --dest /path/to/Project-A --slug project-a --title "Project A"
python scripts/validate_project.py --project-root /path/to/Project-A
```

## Skill List

```text
skills/
  econ-empirical-research-workflow/
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

- `econ-empirical-research-workflow`：整个仓库的统一入口 skill，负责把一个项目从 idea 路由到 submission。
- `research-workflow`：读取 `project.yaml` 和 `workflow_state`，判断当前阶段与下一步动作。
- `research-topic-selection`：负责 bounded two-agent idea loop。
- `research-identification`：冻结 estimand、识别设计、核心假设、数据要求与 robustness plan。
- `research-empirics`：负责通用 empirical production workflow。
- `empirical-analysis-stata`：Stata-first 的 applied econ 实证执行 skill。
- `research-writing`：负责经验论文写作、改写与 draft folder 组织。
- `output-draft-overleaf-sync`：把 output 刷新到 draft，并检查 Overleaf handoff readiness。
- `research-submission`：准备 submission-ready `paper/` folder 和 replication package。
- `reference-elicit-agent`：管理 `references/` 下以 Elicit 为中心的持续文献工作流。
