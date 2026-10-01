* Portable runner. Supply the input CSV explicitly; no workspace-specific path.
version 19.0
args root input outputdir lang
if `"`root'"'=="" local root "`c(pwd)'"
if `"`input'"'=="" exit 198
if `"`outputdir'"'=="" local outputdir "`root'"
if `"`lang'"'=="" local lang "en"
if !inlist(`"`lang'"', "en", "zh") exit 198
capture mkdir "`outputdir'"
do "`root'/plot_coefplot.do" "`input'" "`outputdir'/robustness_coefplot_`lang'.png" `lang' robustness horizontal 0 "`root'/packages/c"
do "`root'/plot_coefplot.do" "`input'" "`outputdir'/subgroup_coefplot_`lang'.png" `lang' subgroup vertical 0 "`root'/packages/c"
do "`root'/plot_coefplot.do" "`input'" "`outputdir'/subgroup_coefplot_`lang'_title.png" `lang' subgroup vertical 1 "`root'/packages/c"
display "COEFPLOT_DEMO_COMPLETE"
