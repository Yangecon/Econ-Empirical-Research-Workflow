# C17 · Geographic choropleth map

[English](recipe.md) · [中文](recipe.zh-CN.md)

`geographic_choropleth` · C17

Match real modern administrative GeoJSON regions to values by explicit region IDs, using common bins and a distinct no-data encoding; demonstration values are synthetic.

Classification: The original map displays observed information such as medical-campaign records by geographic area. The general map interface was validated with real 2016 Cameroon administrative regions and synthetic values. These regions are not the paper's historical ethnic boundaries; original boundaries and values remain unavailable.

Tags: Geography, Choropleth, Spatial coverage

## Sources and scope

[The Legacy of Colonial Medicine in Central Africa (2021)](<https://doi.org/10.1257/aer.20180284>); Figure 2; PDF p.12

Additional reference: [Eric Yongchen Zou, Unwatched Pollution: The Effect of Intermittent Monitoring on Air Quality (2021)](<https://doi.org/10.1257/aer.20181346>); Figure 7; PDF p.20

The paper caption and page image have been checked. The general drawing demonstration uses a different set of real modern administrative boundaries and synthetic values; it does not reproduce the paper's historical boundaries or numbers. Boundary sources and licenses are retained with the template.

All example values are synthetic; preserve the documented statistical interpretation when replacing inputs.

## Inputs

[Input specification](<schema.md>)

## Run

Generate English figures only; do not also render a Chinese copy. Documentation is bilingual.

Run in the template directory; the output directory below should belong to the research project:

```shell
python plot.py demo_region_values.csv YOUR_PROJECT/figures/map.png --bins 0 2 4 6 8 10 --legend-title "Synthetic index"
```

`--title "标题"` explicitly enables a title; titles and bottom notes are absent by default. See schema.md for fields, statistical objects, and display restrictions. Preserve the boundary source and license in ATTRIBUTION.md. Do not treat geographical demonstration inputs as the paper's data.

Replace YOUR_PROJECT with your research project path and quote paths containing spaces. Default output has no overall title or bottom notes.

## Validation

Verified ten real regions, unique ID matching, rejection of unknown/duplicate IDs, hatching for missing values, and a polygon-hole pixel test. Cameroon 2016 administrative regions differ from the paper's historical ethnic boundaries; synthetic values do not reproduce results. The local equirectangular approximation is for display only, not distance/area inference; see schema restrictions. Python was executed and visually checked by the main agent; the drawing example is not a numerical reproduction.

Canonical figure name: `map_geographic_choropleth`
