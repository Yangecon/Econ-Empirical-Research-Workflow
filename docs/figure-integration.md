# Figure integration

[English](figure-integration.md) · [中文](figure-integration.zh-CN.md)

The workflow now includes [empirical-econ-figures](../skills/empirical-econ-figures/README.md): 50 accepted variants and 40 drawing targets. Browse the [PNG gallery](../gallery/empirical-econ-figures/README.md), then choose a recipe by the numbers being plotted, method and available inputs. A is reduced form, B structural, C summary, D research design and E prediction/algorithm evaluation. Geometry, heterogeneity and robustness are tags.

## Estimation to drawing to draft

| Task | Responsible skill | Project artifacts |
|---|---|---|
| Construct sample, estimate and export results | research-empirics / empirical-analysis-stata | data, code, output/raw |
| Choose supported template and preserve inference | empirical-econ-figures | code/03_figures.do or project plotting entrypoint, output/figures, notes/figure_log.csv |
| Caption, source, statistical notes and asset synchronization | research-writing / output-draft-overleaf-sync | draft/images, draft/figures, draft/main.tex |

Standalone drawing requests with observations or saved estimates can use the figure skill directly. A graph does not freeze an identification design or make the whole output ready. Missing estimates/covariance go back to estimation. Exploratory sample diagnostics remain under `work/<slug>/` until promoted under the host workflow.

Keep one Python environment for the research project. From this repository, run `python -m pip install -r requirements-figures.txt`. From an installed skill, install its own `requirements.txt` in that same project environment. Read Stata package versions in the skill's dependency page; plotting does not automatically install or update global ado packages.

From the repository root:

```shell
python scripts/figure_catalog.py --category reduced_form --tag "Event study"
python scripts/figure_catalog.py --id A01 --json
python scripts/figure_catalog.py --category summary --code-language python
```

The selector only lists supported interfaces. There is no universal plotting CLI. Read the recipe's inputs/arguments. When using an installed skill without this repository helper, read `references/catalog.json` and `figure_naming.json` directly. Copy the selected script and needed helpers to your project or call the installed script with explicit paths. Preserve the sibling `scripts/_shared` directory for shared line renderers.

## A01 runnable demonstration

```shell
python skills/empirical-econ-figures/scripts/A01_event_study_pre_post_averages/event_study_with_pre_post_averages.py --output YOUR_PROJECT/work/figure_demo
```

Replace and quote YOUR_PROJECT. This actually estimates the bundled 980-row synthetic panel in Python. Stata independently estimates the same panel through its demo mode. Keep -1 as a hollow normalized zero and include it in the six-period pre denominator; eight-period post minus pre equals static DID for this balanced common-timing design. The contrast interval uses full covariance. This identity is not assumed for other specifications, and the demonstration values are not project results.

A03 runs six Stata staggered-DID estimators including jwdid, exports their actual estimates and lets Python redraw them. A04 uses Stata HonestDiD for relative-magnitude and smoothness intervals. Follow these recipes; do not fabricate coefficients or infer robust point estimates from sensitivity-interval midpoints.

## Publication conventions and validation

Figures default to English labels, no overall title and no bottom notes. Titles are optional. Preserve axes, units, panel labels and legends. Record the estimator, estimand, sample, weights, reference, clustering, covariance and interval meaning outside the image. Put paper attribution and notes in the draft; reference papers are drawing inspirations, not numerical-data provenance.

The gallery contains 97 generated English PNGs, 56 paper/original reference PNGs and clickable bilingual overview tables with separate example/reference columns. Code remains in the skill; full paper PDFs remain in the local materials archive. Bundled components retain their notices; see the figure skill's licensing page. Its attribution/third-party boundaries are not replaced by the root workflow license.

Run `python scripts/validate_figures.py --smoke --output-dir YOUR_PROJECT/work/figure_validation`. It checks catalog paths, paired skill documentation, PNG packaging and the integrity manifest, and runs A01 plus a shared-line and saved-estimator rendering example. It also tests selector matches and unavailable-language handling. CI does not claim a fresh Stata execution; retained source validation distinguishes actual Stata runs from static-only package-runner checks.
