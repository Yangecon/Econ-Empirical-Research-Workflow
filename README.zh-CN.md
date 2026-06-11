# Econ Empirical Research Workflow

[English Version](./README.md)

这是一个面向 Codex 的经验经济学研究 skill bundle 仓库。

这个仓库把一整套 Default applied econ 工作流打包好了：从选题筛选、识别策略冻结、Stata 实证执行、draft 组装，到 submission package 整理。它面向 AER、QJE、AEJ 风格的经验研究项目，内置了可复用的 skills、项目脚手架、Stata 模板、写作模板和结构校验脚本。

## 这个仓库是什么

这是一个公开的 skill bundle 仓库，不是你所有研究项目的总目录。

推荐目录结构：

```text
Project-A/
Project-B/
econ-empirical-research-workflow/
```

真实项目建议放在仓库外部，再把这里的 skills 安装到 Codex 中使用。

## 仓库范围

这个仓库是有意收敛过的：

1. 只聚焦 Default applied econ
2. 把 Stata 作为默认实证执行栈
3. 把 `output/ -> draft/ -> Overleaf` 作为默认下游写作流水线

它不打算覆盖：

- epidemiology workflow
- ML-causal workflow
- Python-first empirical workflow

## 标准工作流

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

两个硬门槛：

1. Topic gate: `go`、`refine`、`park`、`drop`
2. Identification gate: `freeze`、`redesign`、`park`

一旦设计被冻结，默认实证流水线是：

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

## Skill 列表

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

各个 skill 的作用：

- `research-workflow`：读取项目状态、阶段和缺失产物，决定下一步该调用哪个 skill
- `research-topic-selection`：评估研究问题、创新性、可行性和贡献度
- `research-identification`：冻结 estimand、设计、假设、数据需求和 robustness plan
- `research-empirics`：执行通用实证生产流程并刷新 output 产物
- `empirical-analysis-stata`：仓库里的核心 Stata 主 skill，并带有分步骤深度 references
- `research-writing`：负责经验论文英文写作和 draft 目录逻辑
- `output-draft-overleaf-sync`：把清洗后的 output 刷到 draft，并检查 Overleaf handoff 是否就绪
- `research-submission`：准备 submission-ready 的 `paper/` 文件夹和 replication package
- `reference-elicit-agent`：管理 `references/` 下的 Elicit 文献工作流

## 核心 Stata Skill

`empirical-analysis-stata` 是这个仓库最核心的执行型 skill。

它参考了一个更强、更泛化的 Stata empirical-analysis skill，但在这里被有意收窄为：

```text
只保留 Default applied econ
```

它包含：

- 一套 8-step applied-econ Stata workflow
- 适合 Codex 触发的 trigger-rich skill metadata
- 按步骤拆开的深度参考文档：cleaning、transformation、descriptives、diagnostics、modeling、robustness、further analysis、tables/plots

主要估计器家族：

- `reghdfe`
- `ivreg2` 和 `ivreghdfe`
- `csdid`、`eventstudyinteract`、`did_imputation`、`sdid`
- `rdrobust`
- `synth` 和 `synth_runner`
- `teffects`、`psmatch2`、`ebalance`

主要 robustness 工具：

- `bacondecomp`
- `honestdid`
- `boottest`
- `ritest`
- `rwolf`
- `psacalc`

## 项目目录结构

脚手架生成的标准项目结构如下：

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

## 如何安装到 Codex

当每个 skill 文件夹被放进用户的 skill 目录后，Codex 就可以发现这些 skills。

典型安装方式：

1. clone 或下载这个仓库
2. 把 `skills/` 下面需要的 skill 文件夹复制或 symlink 到 `~/.codex/skills/` 或 `$CODEX_HOME/skills/`
3. 保持 skill 文件夹名字不变
4. 在一个单独的经验研究项目中调用这些已安装的 skills

为了在 Codex 中获得更好的 UI 体验，这个仓库已经为每个 bundled skill 补上了 `agents/openai.yaml`。

## Skill 是如何触发的

这个仓库中的每个 skill 都包含：

- 合法的 `SKILL.md`
- 在 `description` 中明确写清 “什么时候该用”
- skill 正文里的 trigger phrases

这已经足够用于基础 skill discovery。

如果你想要更完整的 Codex skill 列表、chips 或更好的 UI 展示体验，这个仓库已经把这层 `agents/openai.yaml` 元数据包含进来了。

## 模板和脚本

仓库包含以下模板组：

```text
templates/project/
templates/stata/
templates/writing/
templates/submission/
templates/references/
templates/custom/
```

生成一个新项目：

```bash
python scripts/scaffold_project.py --dest /path/to/Project-A --slug project-a --title "Project A"
```

校验项目结构：

```bash
python scripts/validate_project.py --project-root /path/to/Project-A
```

## 仓库内容清单

如果想快速看仓库内容，可以看 [docs/repo-contents.md](./docs/repo-contents.md)。

## License

见 [LICENSE](./LICENSE)。
