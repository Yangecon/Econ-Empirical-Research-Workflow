# Stata dependencies and command variants

[English](STATA_DEPENDENCIES.md) · [中文](STATA_DEPENDENCIES.zh-CN.md)

Tested with Stata 19. Native `twoway`, `graph`, data-management and estimation commands ship with Stata. Third-party dependencies below are recorded only after the corresponding template or command variant is accepted. Exact headers, sources, hashes and local modifications are preserved in `stata_packages.json`. An installed version number alone is not evidence that a particular script ran.

Use one ado directory for the host research project. Set `sysdir set PLUS "YOUR_PROJECT/stata_packages"` in that Stata session before installing required SSC packages, and keep that setting local to the run. Package installation is separate from drawing and is never triggered automatically by the gallery. Follow the chosen recipe for its dependencies; most templates need only native Stata.

The staggered-estimator demonstration includes a documented local `event_plot` patch. Do not silently replace it with an upstream release and assume identical behavior; keep the original source and patch record, or rerun the extraction and numerical checks. Python plotting dependencies remain in the shared requirements files.

| Template / variant | Dependency evidence |
|---|---|
| staggered_event_study_estimator_comparison | reghdfe, ftools, csdid, avar, drdid, did_imputation, did_multiplegt_old, eventstudyinteract, event_plot_patched, jwdid, jwdid_estat, jwdid_plot, hdfe; exact record in `stata_packages.json` |
| honestdid_sensitivity | honestdid 1.3.0, coefplot 1.8.8, Windows OSQP/ECOS plugins, Mata library; exact record in `stata_packages.json` |
| regression_discontinuity_binned_outcomes / rdplot | rdplot; exact record in `stata_packages.json` |
| grouped_coefficient_forest / coefplot | coefplot; exact record in `stata_packages.json` |

Copied skill/gallery packages retain this consolidated manifest for portability. Manifest paths are repository-relative where bundled. STATA_PLUS denotes an external Stata installation; original-build-record denotes provenance kept outside this repository. Gallery items retain sanitized JSON/CSV validation evidence. New package versions require a new execution record, not an unrecorded global update.
