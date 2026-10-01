# A03 · Staggered DID event study across estimators

[English](recipe.md) · [中文](recipe.zh-CN.md)

`staggered_event_study_estimator_comparison` · A03

Six actual Stata estimation routes, including jwdid, share a synthetic panel. Common exported results are drawn in Python, native twoway, and an event_plot extraction plus twoway overlay.

Classification: Extract results from six actual Stata estimation commands, including jwdid, and align event times and support. Stata and Python read the same actual estimation results. The paper supplies the drawing reference; no claim is made to have obtained the authors' Analysis do-files or reproduced original numbers.

Tags: DID, Staggered adoption, Event study, Estimator comparison, Robustness, Point-interval, event_plot, jwdid, ETWFE, Simulated data

## Sources and scope

[Braghieri, Luca, Ro'ee Levy, and Alexey Makarin, Social Media and Mental Health (2022)](<https://doi.org/10.1257/aer.20211218>); Figure 2; PDF p.19

Original Figure 2, PDF p19, and the user screenshot were checked. The author archive was located, but the original analysis do-file was not retrieved. Method-author examples were checked separately.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Read schema.md and methods.md and create the research project's output directory first. No title or bottom notes appear by default. Python does not independently estimate the six methods, including jwdid.

Use Python to plot the saved estimate table:

```shell
python plot_python.py --input audited_estimates.csv --output-stem YOUR_PROJECT/figures/staggered_python
```

Native Stata (`PATH_TO_TEMPLATE` is this template directory):

```stata
do "PATH_TO_TEMPLATE/run_plot_twoway.do" "PATH_TO_TEMPLATE" "YOUR_PROJECT/estimates.csv" "YOUR_PROJECT/figures/staggered_twoway"
```

Combined package/native-command version:

```stata
do "PATH_TO_TEMPLATE/plot_event_plot.do" "PATH_TO_TEMPLATE" "YOUR_PROJECT/estimates.csv" "YOUR_PROJECT/figures/staggered_event_plot" "" "YOUR_PROJECT/figures/event_plot_extracted.csv"
```

Python `--title "标题"` or the Stata title argument following the output path enables a title. The hybrid's empty string specifies no title. `event_plot` handles matrix parsing, coordinates, and intervals; `twoway` handles filled/hollow points within an estimator. This must not be called an unmodified pure event_plot rendering.

To rerun estimation, first copy the entire template into the research project's work directory, configure project Stata dependencies according to dependency_manifest.json, and run estimate_all.do from that copy. Do not generate synthetic data or figures inside an installed skill. When reading real results, retain estimation support, clustering, different pretrend definitions, and the two normalized references; unsupported periods must not be filled with zeros.

The normalized reference at event time −1 is displayed as a hollow circle with no confidence interval. It is not an estimated effect and is excluded from pre/post averages.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Six Stata commands were executed on a synthetic panel of 300 units×15 periods; dCDH used 199 unit-cluster bootstrap repetitions. The common table has 61 rows (59 estimates/tests and two normalized references). jwdid actually exports k=0..5 and the full 6×6 covariance matrix, without inventing pre-treatment coefficients. All three renderers share inputs; maximum event_plot interval difference was below 1.35e-7. Main-agent visual checks passed. Python only redraws the Stata-exported table. Preperiod interpretations and estimands differ across methods. A fresh Stata installation was not rebuilt; dependencies and the tested environment are documented.

Canonical figure name: `event_study_staggered_estimator_comparison`
