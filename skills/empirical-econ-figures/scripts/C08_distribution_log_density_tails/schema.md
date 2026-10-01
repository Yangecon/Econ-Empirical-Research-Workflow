# Input schema

[English](schema.md) · [中文](schema.zh-CN.md)

One row per distinct finite x grid point. Required `x` is numeric; choose either a strictly positive numeric `density` column (name configurable) or a finite numeric `log_density` column (name configurable). Missing or duplicate x and nonfinite values are invalid. At least seven grid points and three points in each nonoverlapping, explicitly supplied inclusive tail interval are required. The normal benchmark mean must be finite and standard deviation positive. The plotter does not estimate a density from microdata or choose fit intervals.
