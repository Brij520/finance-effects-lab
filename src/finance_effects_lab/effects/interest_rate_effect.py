"""Full-repricing bond model for parallel interest-rate shocks."""
import numpy as np
import pandas as pd
from finance_effects_lab.common import export_results,heatmap_chart,model_root,read_assumptions,scenario_chart
from finance_effects_lab.effects._bond import bond_price

SLUG="interest_rate_effect"

def calculate(face_value,coupon_rate,base_yield,maturity_years,yield_shift,frequency=2):
    initial=bond_price(face_value,coupon_rate,base_yield,int(maturity_years),int(frequency));new_yield=base_yield+yield_shift
    shocked=bond_price(face_value,coupon_rate,new_yield,int(maturity_years),int(frequency))
    return {"initial_price":initial,"new_yield":new_yield,"shocked_price":shocked,"price_change":shocked-initial,"price_change_pct":shocked/initial-1}

def run_scenarios(input_path=None):
    d=read_assumptions(SLUG,input_path)
    return pd.DataFrame([{"scenario":r["scenario"],**r,**calculate(r["face_value"],r["coupon_rate"],r["base_yield"],r["maturity_years"],r["yield_shift"],r["frequency"])} for r in d.to_dict("records")])

def sensitivity():
    rows=[]
    for maturity in [2,5,10,20,30]:
        for shift in [-.02,-.01,0,.01,.02]:
            rows.append({"maturity_years":maturity,"yield_shift":shift,**calculate(1000,.05,.05,maturity,shift,2)})
    return pd.DataFrame(rows)

def create_charts(results=None,sensitivity_data=None):
    results=run_scenarios() if results is None else results;sensitivity_data=sensitivity() if sensitivity_data is None else sensitivity_data;d=model_root(SLUG)/"charts"
    scenario_chart(results,"price_change_pct","Price change (%)","Bond Price Response to Parallel Yield Shifts",d/"interest_rate_scenarios.png",percent=True)
    p=sensitivity_data.pivot(index="maturity_years",columns="yield_shift",values="price_change_pct");p.columns=[f"{x:+.0%}" for x in p.columns]
    heatmap_chart(p,"Bond Price Sensitivity by Maturity","Yield shift","Maturity (years)","Price change",d/"interest_rate_sensitivity.png",percent=True)

def run_model(input_path=None,export=True):
    r,s=run_scenarios(input_path),sensitivity()
    if export:export_results(SLUG,r,s);create_charts(r,s)
    return r,s
