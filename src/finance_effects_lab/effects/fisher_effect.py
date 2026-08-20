"""Exact and approximate Fisher relationship between nominal, real rates, and inflation."""
import numpy as np
import pandas as pd
from finance_effects_lab.common import export_results,heatmap_chart,model_root,read_assumptions,scenario_chart

SLUG="fisher_effect"
def calculate(nominal_rate,expected_inflation):
    if expected_inflation<=-1:raise ValueError("Expected inflation must exceed -100%")
    real=(1+nominal_rate)/(1+expected_inflation)-1;approx=nominal_rate-expected_inflation
    return {"real_rate":real,"approximate_real_rate":approx,"approximation_error":approx-real,"gross_real_growth":1+real}
def nominal_from_real(real_rate,expected_inflation):return (1+real_rate)*(1+expected_inflation)-1
def run_scenarios(input_path=None):
    d=read_assumptions(SLUG,input_path);return pd.DataFrame([{"scenario":r["scenario"],**r,**calculate(r["nominal_rate"],r["expected_inflation"])} for r in d.to_dict("records")])
def sensitivity():
    rows=[]
    for nominal in [.02,.04,.06,.08,.10,.12]:
        for inflation in [0,.02,.04,.06,.08,.10]:rows.append({"nominal_rate":nominal,"expected_inflation":inflation,**calculate(nominal,inflation)})
    return pd.DataFrame(rows)
def create_charts(results=None,sensitivity_data=None):
    results=run_scenarios() if results is None else results;sensitivity_data=sensitivity() if sensitivity_data is None else sensitivity_data;d=model_root(SLUG)/"charts"
    scenario_chart(results,"real_rate","Ex-ante real rate (%)","Fisher Effect: Real Rate by Inflation Scenario",d/"fisher_scenarios.png",percent=True)
    p=sensitivity_data.pivot(index="expected_inflation",columns="nominal_rate",values="real_rate");p.index=[f"{x:.0%}" for x in p.index];p.columns=[f"{x:.0%}" for x in p.columns]
    heatmap_chart(p,"Exact Real-Rate Sensitivity","Nominal interest rate","Expected inflation","Exact real rate",d/"fisher_sensitivity.png",percent=True)
def run_model(input_path=None,export=True):
    r,s=run_scenarios(input_path),sensitivity()
    if export:export_results(SLUG,r,s);create_charts(r,s)
    return r,s
