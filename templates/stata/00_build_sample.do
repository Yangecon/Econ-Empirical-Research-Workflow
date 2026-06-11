/*******************************************************************************
00_build_sample.do

Build the cleaned analysis sample from raw inputs.
*******************************************************************************/

do "code/00_setup.do"

* Replace these placeholders with the actual raw input files for the project.
* Keep raw data read-only and write derived files to data/build/ or data/.

capture confirm file "$RAW/source_data.dta"
if _rc != 0 {
    di as error "Expected raw input $RAW/source_data.dta was not found."
    di as error "Update 00_build_sample.do to point to the project's real raw files."
    exit 601
}

use "$RAW/source_data.dta", clear

* Basic hygiene block. Expand to the project's actual cleaning logic.
compress
duplicates drop

* Example variable construction placeholders.
capture confirm variable outcome
if _rc != 0 gen outcome = .

capture confirm variable treatment
if _rc != 0 gen treatment = .

capture confirm variable unit_id
if _rc != 0 gen unit_id = _n

capture confirm variable year
if _rc != 0 gen year = .

order unit_id year treatment outcome
sort unit_id year

save "$BUILD/final_sample_intermediate.dta", replace
save "$DATA/final_sample.dta", replace

log close
