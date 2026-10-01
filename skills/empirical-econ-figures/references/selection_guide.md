# Choosing and adapting a figure

[English](selection_guide.md) · [中文](selection_guide.zh-CN.md)

Choose by the object being displayed, then by composition. Similar marks do not imply identical estimands.

| Input / purpose | Suitable family | Preserve when adapting |
|---|---|---|
| Coefficients indexed by event time | Event study | Numeric event time, omitted reference, estimator-specific intervals, filled/hollow significance rule |
| Multiple groups of dynamic coefficients | Grouped event study | Group identity, small numeric offsets, common comparison scale |
| Dynamic effects and window averages | Event study with pre/post averages | Full covariance, fixed normalized weights, windows, distinct scalar-mean intervals |
| Several outcomes/specifications | Coefficient/forest plot | Outcome units, model labels, CI meaning; use facets when scales differ |
| Raw or residualized paired observations | Scatter / binned scatter | Point unit, residualization sample, actual fit and bin definitions |
| Outcomes around a level discontinuity | Binned RD display | Separate left/right bins and fits, cutoff assignment, bandwidth, outcome range, upstream controls |
| Outcomes around a slope change | Continuous kink panels | Common fitted level at threshold, left/right slopes, original running-variable units, separate outcome scales |
| Observed distributions | Histogram / ECDF / boxplot | Denominator, weights, bin or quantile rules, common scales |
| Ordered descriptive series | Time trend | Real dates/gaps, units, intervention timing; avoid incidental row ordering |
| Two outcomes evolving together | Time-encoded phase path | Connect by time rather than x or y, distinguish pre-logged inputs from log axes, label phase and key dates |
| Model counterfactual CDF points | Scenario distribution panels | Scenario assumptions, outcome units, CDF denominator and monotonicity; CDF is not an attention/take-up probability |
| Policy rollout stages by cohort | Phase timeline | Parsed dates, endpoint convention, phase exceptions, population counts and termination |
| Null draws and an observed statistic | Randomization diagnostic | Assignment mechanism, tail rule, Monte Carlo correction; plotting draws does not validate randomization |
| Responses by horizon and shock | Impulse-response matrix | Posterior vs frequentist intervals, each interval level, numeric horizons and response units |
| Weighted observations and distribution thresholds | Distribution overlay | Bin probability mass versus density, full-sample denominator, weights, threshold ties and visible truncation |
| Cumulative population and resource shares | Concentration / Lorenz curves | Common external rank versus each resource's own rank, treatment of ties and weighted totals |
| Effect estimates and supporting sample counts | Aligned effect / histogram panels | Independent input tables, genuinely shared x coordinates, labeled y units on both panels |
| Policies varying an explicit parameter | Efficiency–equity frontier | Parameter order, benchmarks, numerator/denominator of disparity, distinct point and path roles |
| Additive signed estimates | Component decomposition | Positive and negative stacking, algebraic total, common units and supplied accounting identity |
| Coefficients at numerical outcome quantiles | Quantile coefficient profile | Outcome-quantile positions, unconditional versus conditional estimator, supplied interval coverage; do not assume QTE |
| Prior, posterior and frequentist estimates of the same parameter | Prior/posterior interval comparison | Pair the same prior source with its posterior, separate ITT points, retain interval type and outcome units |
| Re-estimated coefficients across bandwidths | Bandwidth sensitivity profile | Numeric bandwidth and units, fixed estimand, changing samples, named uncertainty methods |
| Results under many explicit choices | Specification curve with choice matrix | Stable specification IDs, same ordering in curve and matrix, the actual displayed statistic and optional supplied intervals |
| Paired binary observations | Four-state transition stacks | Matched IDs, four exhaustive joint states, common paired denominator, distinct conditional-rate denominators |
| Actual values and perceived means by category | Reference/perception dumbbells | Shared units, unchanged input order, confidence intervals belonging only to the estimated mean, zero and negative differences |
| Two variables evolving through time | Time-encoded phase path | Chronological connection, preserved horizontal reversals, already transformed coordinates, stated phase boundaries and selected year labels |
| Predicted belief versus a reference probability | Probability calibration display | Correct x/y roles, 45-degree benchmark, explicit bin rules, conditional spread versus uncertainty of the mean |
| Distribution around a tax notch | Bunching distribution with counterfactual | Observed and counterfactual series in the same units, fixed bins, notch and excluded-region bounds, externally estimated bunching statistics |
| Two jointly estimated quantities | Joint bootstrap region | Joint coverage, saved region construction, reference inequality and point estimate; marginal intervals cannot recover the region |
| Costs of dispatched units across scenarios | Merit-order cost curves | Sort by unit cost, use dispatched quantity as step width, preserve common demand and cost units, keep dispatch optimization upstream |
| Two policy parameters and two outcome surfaces | Policy counterfactual contours | Complete numeric grid, parameter units, outcome-specific level values, observed baseline and actual contour geometry |
| Reallocation between two sets of categories | Bilateral flow Sankey | Quantitative edge amounts, conserved node totals, one common width scale and explicit stock-versus-flow meaning |
| Choices followed by randomized assignment | Randomization decision tree | Which nodes are choices versus random draws, chronological order, conditional denominators and the reason any paths are omitted |

The catalog lists which of these families are currently implemented; this guide is not a promise that every row already has code.

## Deduplication

Keep one representative when two source figures differ only in topic, labels or colors. Keep a documented variant when panel structure, uncertainty, grouping or the statistical object changes the required input or reading. For example, a descriptive ECDF and a quantile treatment-effect plot are different; repeating the same event-study design for another outcome usually does not require another template.

Every selected representative retains paper, year, DOI, Figure/panel, PDF page and local source where known. Unknown metadata stays unknown. A supplementary screenshot may later be linked to a paper only after visual and caption verification.

An annotated historical trend can reuse a time-trend family, but its event-label layer must actually be implemented before being promised. A day-by-day monitoring calendar is a different input structure. Similarly, a concentration curve is not an ECDF, and a waterfall accounting sequence is not an ordinary grouped bar chart.

The source paper's analytical role determines the required languages. A boxplot of model-estimated probabilities is treated as a result figure even though boxplots are often descriptive. A later adaptation that turns a Python-only summary template into an estimated-effect display needs a checked Stata counterpart before claiming the library's two-language result contract.

## Real-data transfer

Copy the template to the working project or direct its output there. Replace synthetic CSVs with validated data or saved estimates. Read the recipe before renaming columns: different templates may accept precomputed CIs, standard errors, or a full covariance matrix. Do not manufacture covariance from marginal SEs, and do not change confidence levels merely to tighten intervals.

Axis labels and units belong in the figure. Citation, sample construction, estimator, controls, clustering, weights and caveats belong in the adjacent draft/caption; defaults suppress the in-image title and bottom notes. Panel labels and legends are allowed. Synthetic gallery values illustrate the drawing grammar and cannot support empirical claims.

Dynamic-effect markers follow the user convention: filled when the displayed interval excludes zero, hollow otherwise. For nested intervals, document which level controls this encoding. A posterior credible region excluding zero is not automatically a frequentist significance test; retain its posterior interpretation in the figure's accompanying text. IRF horizons start at the shock and need not have the omitted pre-period used in an event study.

## Interval and envelope meanings

| Supplied object | What the drawing can communicate | What it must not add |
|---|---|---|
| Frequentist confidence interval | Saved point estimate and uncertainty under the stated method | A new clustering rule or simultaneous coverage claim |
| Prior interval | Quantiles of the stated prior distribution | A sampling-confidence or empirical-significance interpretation |
| Posterior interval | Credible region under the stated model, prior and data | A frequentist p-value inferred from zero exclusion |
| Set-identified response envelope | Minimum/maximum admissible response at each horizon | An inferred confidence level or significance test |
| Scenario envelope | Range produced by explicit alternative assumptions or policy parameters | A sampling-confidence level or an identified-set interpretation without additional justification |
| Conditional interquartile range | Middle half of individual outcomes or beliefs within a defined bin | A confidence interval for the conditional mean |
| Pointwise median across admissible paths | A separate median at each horizon | A claim that the whole median curve is one jointly admissible structural path |

Keep these definitions beside the figure in the recipe and draft. The absence of in-image notes does not remove the need to record them.

Ribbon diagrams can show either quantitative flows or qualitative relationships. Use the quantitative Sankey template only when edge amounts and node totals are defined; a source with broad connecting bands does not by itself establish that width measures frequency or money. Likewise, a stock of investment reassigned from registration location to ultimate ownership is not automatically a period cash flow.

A decision tree may omit later choices because nobody in the observed sample changed their mind. Such an empirical omission is different from a design rule forbidding that choice. Keep participant decisions separate from randomized assignment; branch proportions do not make every split random.

Two displayed bands can also reflect **different inference methods at the same confidence level**, such as cluster-robust versus Conley intervals. Do not relabel them as 68% versus 95% bands or require one to nest inside the other. A bandwidth-sensitivity x coordinate is the sample-selection radius used for each regression, not an individual observation's distance from a cutoff.

A specification curve may display coefficients, fit statistics, or an average of t statistics across experiments. Preserve that object and its label. An average t statistic does not acquire a conventional ±1.96 rejection threshold merely because its name contains “t”. Sort the result rows and the choices matrix through the same specification identifier; an unrecorded choice is not evidence that the option was excluded.

## Distributions and transitions

Keep the object on a histogram's horizontal axis explicit: observed outcomes, estimated individual effects, posterior draws, and randomization draws are different inputs. A histogram of estimated individual effects does not reveal their individual standard errors or isolate the distribution of true effects from estimation noise. Reusing a histogram's drawing code does not remove that distinction.

For paired binary states, the four joint categories sum to the number of complete pairs. Their percentages use that common denominator. A conditional transition probability such as P(after=1 | before=0) instead divides by the complete pairs starting at zero. If no pair starts at zero, that conditional rate is undefined, not zero. Two unpaired cross-sectional marginals cannot identify these four transitions. Any paired-comparison hypothesis test belongs to a separately specified analysis and is not automatically inherited from the source figure.

A probability-calibration scatter can have true or reference probabilities on x and predicted beliefs on y. Preserve this orientation when interpreting overprediction relative to the 45-degree line. A conditional IQR band summarizes individual dispersion; it is not a confidence band around a fitted relation. Large probability masses at zero or one can require explicitly defined separate bins rather than ordinary quantile splitting.

A bunching figure compares an observed distribution with a constructed counterfactual near a policy notch or kink. It is not an RD outcome fit, a density-continuity test, or an estimate of a behavioural elasticity by itself. Keep counts, bin shares and density units distinct; counterfactual construction, the excluded region, excess-mass normalization and uncertainty belong to the upstream analysis. Do not infer a marginal buncher or a dominated-region boundary from the point where two displayed curves appear to meet.

A policy-contour axis can describe a relative percentage change in a probability, rather than a percentage-point change. A 10% relative increase transforms d into 1.1d; adding 0.10 is a different policy. Contours of an acceptance-probability change and a per-visit payment change have different output units even when they share the same policy axes. Preserve the labels for the actual contour levels.
