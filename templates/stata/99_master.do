/*******************************************************************************
99_master.do

Master script for the default applied econ pipeline.
*******************************************************************************/

do "code/build/00_build_sample.do"
log close

do "code/00_setup.do"
log close

do "code/01_estimation.do"
do "code/02_robustness.do"
do "code/03_figures.do"
do "code/04_tables.do"
