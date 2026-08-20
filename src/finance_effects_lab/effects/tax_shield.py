"""Levered versus unlevered income and cash-flow tax shield comparison."""
import numpy as np
import pandas as pd
from finance_effects_lab.common import export_results,heatmap_chart,model_root,read_assumptions,scenario_chart

SLUG="tax_shield"
def calculate(ebit,debt,interest_rate,tax_rate,depreciation,capex,change_nwc):
    interest=debt*interest_rate;taxable=max(0,ebit-interest);levered_tax=taxable*tax_rate;unlevered_tax=max(0,ebit)*tax_rate
    net_income=ebit-interest-levered_tax;tax_shield=unlevered_tax-levered_tax
    levered_fcf=net_income+depreciation-capex-change_nwc;unlevered_fcf=ebit-unlevered_tax+depreciation-capex-change_nwc
    return {"interest":interest,"taxable_income":taxable,"tax":levered_tax,"net_income":net_income,"tax_shield":tax_shield,
            "levered_fcf_after_interest":levered_fcf,"unlevered_fcf":unlevered_fcf,"pv_perpetual_tax_shield":debt*tax_rate}
def run_scenarios(input_path=None):
    d=read_assumptions(SLUG,input_path);return pd.DataFrame([{"scenario":r["scenario"],**r,**calculate(r["ebit"],r["debt"],r["interest_rate"],r["tax_rate"],r["depreciation"],r["capex"],r["change_nwc"])} for r in d.to_dict("records")])
def sensitivity():
    rows=[]
    for debt in [0,25,50,75,100,125]:
        for tax in [.10,.20,.25,.30,.35]: rows.append({"debt":debt,"tax_rate":tax,**calculate(25,debt,.06,tax,5,7,2)})
    return pd.DataFrame(rows)
def create_charts(results=None,sensitivity_data=None):
    results=run_scenarios() if results is None else results;sensitivity_data=sensitivity() if sensitivity_data is None else sensitivity_data;d=model_root(SLUG)/"charts"
    scenario_chart(results,"tax_shield","Tax saving ($m)","Interest Tax Shield by Scenario",d/"tax_shield_scenarios.png")
    p=sensitivity_data.pivot(index="debt",columns="tax_rate",values="tax_shield");p.columns=[f"{x:.0%}" for x in p.columns]
    heatmap_chart(p,"Annual Tax Shield Sensitivity","Statutory tax rate","Debt ($m)","Tax shield ($m)",d/"tax_shield_sensitivity.png")
def run_model(input_path=None,export=True):
    r,s=run_scenarios(input_path),sensitivity()
    if export:export_results(SLUG,r,s);create_charts(r,s)
    return r,s
