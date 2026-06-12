/*******************************************************************************
_write_version_log.do

Append a per-script Stata version/package log to output/raw/stata_version_log.csv.

Usage:
    local required_packages "reghdfe estout coefplot"
    do "code/_write_version_log.do" "01_estimation.do" "`required_packages'"

This is intentionally not a global environment snapshot. Each .do file should pass
only the packages it uses.
*******************************************************************************/

args script_name package_list

capture confirm global OUTPUT
if _rc != 0 {
    di as error "Global OUTPUT is not defined. Run code/00_setup.do first."
    exit 198
}

cap mkdir "$OUTPUT"
cap mkdir "$OUTPUT/raw"

local log_file "$OUTPUT/raw/stata_version_log.csv"

capture confirm file "`log_file'"
if _rc != 0 {
    file open version_log using "`log_file'", write replace text
    file write version_log "script_name,run_date,run_time,stata_version,stata_flavor,os,working_directory,package_name,package_status,package_path" _n
    file close version_log
}

local run_date = c(current_date)
local run_time = c(current_time)
local stata_version = c(version)
local stata_flavor = c(flavor)
local os = c(os)
local pwd = c(pwd)

if "`package_list'" == "" {
    file open version_log using "`log_file'", write append text
    file write version_log `""`script_name'","`run_date'","`run_time'","`stata_version'","`stata_flavor'","`os'","`pwd'","<none>","not_checked","""' _n
    file close version_log
}
else {
    foreach package_name of local package_list {
        capture which `package_name'
        if _rc == 0 {
            local package_status "installed"
            local package_path "`r(fn)'"
        }
        else {
            local package_status "missing"
            local package_path ""
        }

        file open version_log using "`log_file'", write append text
        file write version_log `""`script_name'","`run_date'","`run_time'","`stata_version'","`stata_flavor'","`os'","`pwd'","`package_name'","`package_status'","`package_path'""' _n
        file close version_log
    }
}
