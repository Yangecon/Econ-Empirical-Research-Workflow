"""Synthetic mean-t specification results and binary choices."""
from pathlib import Path
import numpy as np
import pandas as pd

here=Path(__file__).resolve().parent
rng=np.random.default_rng(20260928)
options=("baseline","regional","first_round","exclude_municipalities","pool_one_site",
         "logarithm","gdp","gdp_per_capita","population","fiscal_income","fiscal_expenditure")
n=48
choices=rng.binomial(1,.4,size=(n,len(options)))
weights=np.array([.13,.14,-.08,.17,.12,.11,.16,.15,.12,.11,.18])
result=1.05+choices@weights+np.linspace(.05,2.35,n)+rng.normal(0,.08,n)
frame=pd.DataFrame({"spec_id":[f"S{i:03d}" for i in range(1,n+1)],"result":result})
for j,name in enumerate(options): frame[f"opt_{name}"]=choices[:,j]
frame.to_csv(here/"demo.csv",index=False,float_format="%.12g")
frame.sample(frac=1,random_state=47).to_csv(here/"qa_shuffled.csv",index=False,float_format="%.12g")
with_ci=frame.copy()
with_ci["ci_low"]=with_ci.result-.28
with_ci["ci_high"]=with_ci.result+.32
with_ci.to_csv(here/"qa_with_ci.csv",index=False,float_format="%.12g")
one_sided=with_ci.copy();one_sided.loc[0,"ci_high"]=np.nan
one_sided.to_csv(here/"qa_one_sided_ci.csv",index=False,float_format="%.12g")
bad_ci=with_ci.copy();bad_ci[["ci_low","ci_high"]]=bad_ci[["ci_low","ci_high"]].astype(object)
bad_ci.loc[0,["ci_low","ci_high"]]=["bad","bad"]
bad_ci.to_csv(here/"qa_bad_ci.csv",index=False,float_format="%.12g")
extra_option=frame.copy();extra_option["opt_unconfigured"]=0
extra_option.to_csv(here/"qa_extra_option.csv",index=False,float_format="%.12g")
print("DEMO_COMPLETE specs=48 options=11 synthetic_mean_t; optional_CI_fixture=true")
