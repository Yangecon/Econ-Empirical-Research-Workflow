"""Synthetic monthly policy-phase timetable; not historical rollout dates."""
from pathlib import Path
import csv

out = Path(__file__).with_name("demo.csv")
rows = [
    ["cohort_a", 1, "Cohort A", "队列A", 18, "policy", "2020-04-01", "2020-08-01", "2020-08-01", "2021-03-01", "2021-03-01"],
    ["cohort_b", 2, "Cohort B", "队列B", 24, "policy", "2020-07-01", "2020-11-01", "2020-11-01", "2021-03-01", "2021-03-01"],
    ["cohort_c", 3, "Cohort C", "队列C", 75, "policy", "2020-09-01", "2021-03-01", "", "", "2021-03-01"],
    ["nonpolicy", 4, "Nonpolicy cohorts", "非政策队列", 100, "nonpolicy", "", "", "", "", "2021-03-01"],
]
with out.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["cohort", "cohort_order", "cohort_label_en", "cohort_label_zh", "n",
                     "status", "transition_start", "transition_end", "enforcement_start",
                     "enforcement_end", "termination_month"])
    writer.writerows(rows)
print(f"DEMO_COMPLETE cohorts={len(rows)} output={out}")
