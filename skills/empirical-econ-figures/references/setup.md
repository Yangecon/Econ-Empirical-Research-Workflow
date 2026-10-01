# Environment and workflow integration

[English](setup.md) · [中文](setup.zh-CN.md)

The portable skill contains its own `requirements.txt` and a tested full `requirements_lock.txt`. Tested environment: Python 3.12.14 and Stata 19 on Windows. The plotting programs independently draw from the documented common input. A synthetic CSV is supplied to demonstrate the interface. The six-estimator staggered DID demonstration first estimates in Stata and exports a shared CSV; its Python renderer does not independently estimate those six models (including jwdid). Check each recipe's estimation dependencies before promising an end-to-end Python-only run.

Create one virtual environment for the host research project, then install the skill's requirements into it. Do not create a new environment for each figure. The lock file records the complete tested package versions; the smaller requirements file names direct plotting dependencies. PDF extraction and library-build tools are not needed to use the plotting templates.

The accepted line family uses one `scripts/_shared/line_geometry.py` module. Keep that sibling directory when copying a member template into another project; the catalog records it under `shared_resources`. Imports resolve relative to the script location, not the current working directory. The gallery carries corresponding code and the shared dependency next to each code directory. Series/phase JSON configuration is currently supported by C10/C11 in Python; other source-specific configuration limits remain documented in their recipes.

For third-party Stata commands, consult [STATA_DEPENDENCIES.md](../STATA_DEPENDENCIES.md) and [stata_packages.json](../stata_packages.json). Use one project-local ado directory and preserve the tested package versions or hashes. The figure programs do not automatically update global packages.

Windows example:

```shell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r PATH_TO_SKILL/requirements.txt
```

Use `.venv/bin/python` for the second command on macOS/Linux. Activate the new environment or continue using its full Python executable for plotting. The recipe commands written simply as `python` assume that environment is active. Use English labels for generated figures.

## Integration boundary

1. The empirical workflow constructs the analysis sample, runs the chosen estimator and exports data, coefficients, intervals or covariance matrices.
2. This skill selects a catalogued drawing template, validates its input and generates figures in the research project's output directory.
3. The writing or output-sync stage supplies the title, caption, source attribution and statistical notes in the draft.

Do not rename an estimator based on how its graph looks. Regression discontinuity, regression kink, threshold-conditioned associations and event studies can share some graphical marks but need different upstream designs and labels. A supplied confidence interval is an input, not a clustering procedure.

Use the host workflow's established paths. Typical roles are an immutable source-data directory, intermediate saved estimates, an `output/figures` destination, and the draft's downstream assets. Replace `YOUR_PROJECT` in recipes with an absolute project path and quote paths containing spaces. Keep Stata's working directory in the host project so its run logs and diagnostic CSVs stay there. The skill itself is kept free of generated PNGs. The separate gallery is a reference and inspection aid; it is not a numerical-data source.

## Reproducibility record

Retain the template ID, copied script version or hash, exact input, invocation, output paths and successful run log. Record the sample, weighting, estimand, confidence level and interval method alongside the exported figure. When both languages are used, compare the numerical objects they plot before judging image similarity; pixel-perfect agreement between different graphics engines is not required.


Generate English figures only by default; do not generate a second Chinese copy. The English and Chinese documentation pages are independent of the figure language. Older validation records may describe historical Chinese test renders.
