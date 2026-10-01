# A04 · HonestDiD sensitivity figures

[English](README.md) · [中文](README.zh-CN.md)

These two figures are an executed, seeded **synthetic-data demonstration** of [HonestDiD's official Stata examples](https://github.com/mcaceresb/stata-honestdid). They do not reproduce any published paper's data or estimates. The relative-magnitude figure varies the bound \(\bar M\); the smoothness figure varies \(M\). Both show genuine robust confidence intervals computed by `honestdid` 1.3.0 from a Stata event study and its full clustered covariance matrix. The native `honestdid, cached coefplot` renderer produces the figures; no coefficient or interval was entered by hand.

## Outputs

| Figure | PNG | PDF | Numeric intervals |
|---|---|---|---|
| Relative magnitudes, DeltaRM | `honestdid_relative_magnitude.png` | `honestdid_relative_magnitude.pdf` | `rm_intervals.csv` |
| Smoothness, DeltaSD | `honestdid_smoothness.png` | `honestdid_smoothness.pdf` | `sd_intervals.csv` |

The Stata figures have no title or bottom notes by default. Run `do build.do "<this folder>" "A title"` to add a title; an optional third argument, such as `_titled`, appends a suffix to the figure filenames. The two variants remain separate. A conventional interval at `Original` is shown beside each robust sensitivity grid, as implemented by HonestDiD. Its separate x position is categorical, not a numeric M value.

## What was estimated

`build.do` generates 320 units observed in nine periods (2,880 rows). The first 160 units receive treatment from period 5. The outcome contains an individual component, common time trend, individual slope noise, treatment effect `0.18 + 0.055 k` for event time \(k\geq0\), and normally distributed noise. Random generation uses `set seed 29092026`. The fitted `xtreg, fe vce(cluster id)` model includes period effects and treated-by-event indicators for leads -4, -3, -2 and lags 0 through 4. Event time -1 is the sole omitted reference. Every observed treated post period enters the model.

The extracted `b` has eight coefficients in the order -4, -3, -2, 0, 1, 2, 3, 4. `V` is their complete 8-by-8 covariance submatrix from the unit-clustered event study, including off-diagonal entries. `event_study_coefficients.csv` and `event_study_covariance.csv` preserve them. HonestDiD uses `pre(1/3) post(4/8)` and `l_vec(1,0,0,0,0)'`, so the target is the first post-treatment contrast at event time 0. The relative magnitude run uses `delta(rm) method(C-LF)` over \(\bar M=0,0.25,\ldots,2\). The smoothness run uses `delta(sd) method(FLCI)` over \(M=0,0.025,\ldots,0.2\). The intervals are 95% robust intervals from HonestDiD. The native `cionly` plot draws interval bars without presenting a new point estimate.

The RM restriction bounds post-treatment departures from parallel trends relative to the largest pre-treatment departure. RM at \(\bar M=0\) imposes exact post-treatment parallel trends even when preperiod deviations are estimated. The SD restriction bounds changes in the slope of the violation. SD at \(M=0\) allows a linear continuation of the preperiod trend, so it need not match the conventional interval. Increasing either bound weakens the restriction. In this synthetic example the RM interval first includes zero at \(\bar M=0.75\); the SD interval already includes zero at \(M=0\). Those are properties of this generated sample, not empirical policy findings.

## Run and verification

On Windows with Stata 19, change Stata's working directory to this folder and run `do build.do`. A batch example is `StataMP-64.exe -b do build.do`. The default execution log is `build.log`; it contains `EVENT_STUDY_N=2880`, `RM_COMPLETE`, `SD_COMPLETE`, and the final `HONESTDID_BUILD_COMPLETE` marker. The build-only numerical validator checks the CSVs, covariance symmetry and positive definiteness, sensitivity bounds for this fixed demo, PNG/PDF signatures, and output dimensions. Its successful result is preserved in the gallery validation records; the validator and raw logs stay in the source work archive and are not included in the installed skill. The PNGs were inspected visually at native export size for label collision, clipping, and unwanted titles/notes.

The `packages/` folder contains task-local copies of the HonestDiD 1.3.0 Stata ado/help files, Windows OSQP/ECOS plugins, Mata library, and `coefplot` 1.8.8 with its upstream MIT license. `build.do` prepends those paths to Stata's ado search path. No global Stata installation was changed. `dependency_manifest.json` records exact hashes, original installed paths, upstream URLs, and license status. Stata itself must be supplied separately. The bundled plugins are Windows binaries; other systems need the matching binaries and possibly recompilation, per the [official HonestDiD instructions](https://github.com/mcaceresb/stata-honestdid#compiling).

`schema.md` describes every CSV. `source_metadata.json` identifies the method source and states explicitly that no source image or paper figure was reproduced. `portable_files.json` lists the files needed to inspect and rerun this implementation.

Canonical figure name: `event_study_honestdid_sensitivity`
