"""Future value under discrete compounding and recurring contributions."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from finance_effects_lab.common import SOURCE_NOTE,export_results,heatmap_chart,model_root,read_assumptions

SLUG="compound_interest"
def calculate(principal,annual_rate,years,compounds_per_year,annual_contribution=0):
    if compounds_per_year<=0 or years<0:raise ValueError("Compounding frequency must be positive and years non-negative")
    n=int(round(years*compounds_per_year));period_rate=annual_rate/compounds_per_year
    principal_fv=principal*(1+period_rate)**n
    contribution_per_period=annual_contribution/compounds_per_year
    contribution_fv=contribution_per_period*((1+period_rate)**n-1)/period_rate if period_rate!=0 else contribution_per_period*n
    fv=principal_fv+contribution_fv;total_contributed=principal+annual_contribution*years
    return {"future_value":fv,"principal_future_value":principal_fv,"contribution_future_value":contribution_fv,"total_contributed":total_contributed,"compound_growth":fv-total_contributed,"effective_annual_rate":(1+period_rate)**compounds_per_year-1}
def run_scenarios(input_path=None):
    d=read_assumptions(SLUG,input_path);return pd.DataFrame([{"scenario":r["scenario"],**r,**calculate(r["principal"],r["annual_rate"],r["years"],r["compounds_per_year"],r["annual_contribution"])} for r in d.to_dict("records")])
def sensitivity():
    rows=[]
    for years in [5,10,15,20,25,30]:
        for rate in [.02,.04,.06,.08,.10]:rows.append({"years":years,"annual_rate":rate,**calculate(10000,rate,years,12,2000)})
    return pd.DataFrame(rows)
def create_charts(results=None,sensitivity_data=None):
    results=run_scenarios() if results is None else results;sensitivity_data=sensitivity() if sensitivity_data is None else sensitivity_data;d=model_root(SLUG)/"charts";d.mkdir(parents=True,exist_ok=True);fig,ax=plt.subplots(figsize=(9,5.3))
    for rate in [.02,.04,.06,.08,.10]:
        subset=sensitivity_data[sensitivity_data.annual_rate==rate];ax.plot(subset.years,subset.future_value/1000,marker="o",label=f"{rate:.0%}")
    ax.set(title="Compound Growth by Horizon and Annual Return",xlabel="Investment horizon (years)",ylabel="Future value ($000s)");ax.grid(alpha=.22);ax.legend(title="Return",frameon=False);fig.text(.01,.01,SOURCE_NOTE,fontsize=7.5,color="#5D6774");fig.tight_layout(rect=(0,.04,1,1));fig.savefig(d/"compound_growth.png",dpi=180);plt.close(fig)
    p=sensitivity_data.pivot(index="years",columns="annual_rate",values="future_value");p.columns=[f"{x:.0%}" for x in p.columns]
    heatmap_chart(p,"Future Value Sensitivity","Annual return","Years","Future value ($)",d/"compound_sensitivity.png")
def run_model(input_path=None,export=True):
    r,s=run_scenarios(input_path),sensitivity()
    if export:export_results(SLUG,r,s);create_charts(r,s)
    return r,s
