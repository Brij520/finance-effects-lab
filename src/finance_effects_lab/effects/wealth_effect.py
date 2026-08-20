"""Consumption response to household wealth changes."""
import numpy as np
import pandas as pd
from finance_effects_lab.common import export_results,heatmap_chart,model_root,read_assumptions,scenario_chart

SLUG="wealth_effect"
def calculate(initial_wealth,wealth_return,marginal_propensity_to_consume,baseline_consumption):
    wealth_change=initial_wealth*wealth_return;consumption_change=marginal_propensity_to_consume*wealth_change
    return {"ending_wealth":initial_wealth+wealth_change,"wealth_change":wealth_change,"consumption_change":consumption_change,
            "ending_consumption":baseline_consumption+consumption_change,"consumption_change_pct":consumption_change/baseline_consumption}
def run_scenarios(input_path=None):
    d=read_assumptions(SLUG,input_path);return pd.DataFrame([{"scenario":r["scenario"],**r,**calculate(r["initial_wealth"],r["wealth_return"],r["marginal_propensity_to_consume"],r["baseline_consumption"])} for r in d.to_dict("records")])
def sensitivity():
    rows=[]
    for ret in [-.30,-.20,-.10,0,.10,.20,.30]:
        for mpc in [.02,.03,.04,.05,.06]: rows.append({"wealth_return":ret,"mpc":mpc,**calculate(500,ret,mpc,80)})
    return pd.DataFrame(rows)
def create_charts(results=None,sensitivity_data=None):
    results=run_scenarios() if results is None else results;sensitivity_data=sensitivity() if sensitivity_data is None else sensitivity_data;d=model_root(SLUG)/"charts"
    scenario_chart(results,"consumption_change","Consumption change ($k)","Modeled Consumption Response to Wealth Shocks",d/"wealth_scenarios.png")
    p=sensitivity_data.pivot(index="wealth_return",columns="mpc",values="consumption_change");p.index=[f"{x:.0%}" for x in p.index];p.columns=[f"{x:.0%}" for x in p.columns]
    heatmap_chart(p,"Consumption Sensitivity","Marginal propensity to consume","Wealth return","Consumption change ($k)",d/"wealth_sensitivity.png")
def run_model(input_path=None,export=True):
    r,s=run_scenarios(input_path),sensitivity()
    if export:export_results(SLUG,r,s);create_charts(r,s)
    return r,s
