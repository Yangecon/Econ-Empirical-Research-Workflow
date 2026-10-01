* Portable runner. Supply the input CSV explicitly; no workspace-specific path.
version 19
args root input outputdir packages lang
if `"`root'"'=="" local root "`c(pwd)'"
if `"`input'"'=="" exit 198
if `"`outputdir'"'=="" local outputdir "`root'"
if `"`lang'"'=="" local lang "en"
if !inlist(`"`lang'"', "en", "zh") exit 198
capture mkdir "`outputdir'"
if `"`packages'"'!="" adopath ++ "`packages'"
do "`root'/plot_rdplot.do" "`input'" "`outputdir'/rdplot_`lang'.png" `lang' 0
do "`root'/plot_rdplot.do" "`input'" "`outputdir'/rdplot_`lang'_title.png" `lang' 1
display "RDPLOT_DEMO_COMPLETE"
