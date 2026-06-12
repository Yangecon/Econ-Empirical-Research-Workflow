/*******************************************************************************
99_master.do

Master script for the default applied econ pipeline.
*******************************************************************************/

do "code/build/00_build_sample.do"
capture log close

do "code/01_estimation.do"
capture log close

do "code/02_robustness.do"
capture log close

do "code/03_figures.do"
capture log close

do "code/04_tables.do"
capture log close
