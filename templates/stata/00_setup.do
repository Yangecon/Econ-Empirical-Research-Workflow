/*******************************************************************************
00_setup.do

Project setup. Run from project root or from code/.
*******************************************************************************/

clear all
set more off
version 18

capture log close _all

global PROJECT_ROOT ""

if "$PROJECT_ROOT" == "" {
    local current_dir "`c(pwd)'"

    capture confirm file "project.yaml"
    if _rc == 0 {
        global PROJECT_ROOT "`current_dir'"
    }
    else {
        cd ..
        capture confirm file "project.yaml"
        if _rc == 0 {
            global PROJECT_ROOT "`c(pwd)'"
        }
        else {
            di as error "Could not locate project.yaml from current directory or parent."
            exit 601
        }
    }
}

global CODE    "$PROJECT_ROOT/code"
global RAW     "$PROJECT_ROOT/data/raw"
global BUILD   "$PROJECT_ROOT/data/build"
global DATA    "$PROJECT_ROOT/data"
global CODEBLD "$PROJECT_ROOT/code/build"
global OUTPUT  "$PROJECT_ROOT/output"
global FIGURES "$PROJECT_ROOT/output/figures"
global TABLES  "$PROJECT_ROOT/output/tables"
global NOTES   "$PROJECT_ROOT/notes"

cap mkdir "$BUILD"
cap mkdir "$CODEBLD"
cap mkdir "$OUTPUT"
cap mkdir "$OUTPUT/raw"
cap mkdir "$FIGURES"
cap mkdir "$TABLES"
cap mkdir "$NOTES"

log using "$OUTPUT/raw/stata_run.log", replace text

set seed 20260101

di as text "Project root: $PROJECT_ROOT"
di as text "Started: `c(current_date)' `c(current_time)'"
