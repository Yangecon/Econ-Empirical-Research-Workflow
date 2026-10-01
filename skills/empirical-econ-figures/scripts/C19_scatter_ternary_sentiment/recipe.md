# C19 · Time-faceted ternary sentiment scatter

[English](recipe.md) · [中文](recipe.zh-CN.md)

`time_faceted_ternary_sentiment_scatter` · C19

Represent each book by three-share ternary coordinates, faceting by time and using common sentiment-percentile colors across panels.

Classification: Each point is a book; topic shares and sentiment percentiles are text measures, faceted by year. A measurement model is not an economic structural model.

Tags: Text measures, Ternary composition, Time facets, Composition, Ternary scatter, Facets

## Sources and scope

[Enlightenment Ideals and Belief in Progress in the Run-up to the Industrial Revolution: A Textual Analysis (2026)](<https://doi.org/10.1093/qje/qjaf054>); Figure VI; PDF p.30

The original page image and PDF caption have been checked; synthetic data demonstrate the drawing only.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run in the template directory; the output directory below should belong to the research project:

```shell
python plot.py demo_books.csv YOUR_PROJECT/figures/ternary.png --centers 1550 1600 1650 1700 1750 1800 1850 --half-window 10
```

`--title "标题"` explicitly enables a title; no title or bottom notes appear by default. See schema.md for fields, statistical objects, and display restrictions.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Verified vertex coordinates, nonnegative shares summing to one, book IDs, percentile ranges, and inclusive time windows. Colors use upstream percentiles, without within-panel reranking; maxima are visible light gray rather than white points on white backgrounds. Python was executed and visually checked by the main agent; the drawing demonstration is not a numerical reproduction of the paper.

Canonical figure name: `scatter_ternary_sentiment`
