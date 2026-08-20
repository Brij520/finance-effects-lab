"""Duration-convexity approximation compared with full bond repricing."""
import numpy as np
import pandas as pd
from finance_effects_lab.common import export_results,heatmap_chart,model_root,read_assumptions,scenario_chart
from finance_effects_lab.effects._bond import bond_price,duration_convexity

SLUG="duration_effect"

def calculate(face_value,coupon_rate,yield_rate,maturity_years,yield_shift,frequency=2):
    price,mac,mod,conv=duration_convexity(face_value,coupon_rate,yield_rate,int(maturity_years),int(frequency))
    estimated=-mod*yield_shift+.5*conv*yield_shift**2
    exact_price=bond_price(face_value,coupon_rate,yield_rate+yield_shift,int(maturity_years),int(frequency));exact=exact_price/price-1
    return {"initial_price":price,"macaulay_duration":mac,"modified_duration":mod,"convexity":conv,
            "estimated_change_pct":estimated,"exact_change_pct":exact,"approximation_error_pct":estimated-exact,"shocked_price":exact_price}

def run_scenarios(input_path=None):
    d=read_assumptions(SLUG,input_path);return pd.DataFrame([{"scenario":r["scenario"],**r,**calculate(r["face_value"],r["coupon_rate"],r["yield_rate"],r["maturity_years"],r["yield_shift"],r["frequency"])} for r in d.to_dict("records")])

def sensitivity():
    rows=[]
    for coupon in [.02,.035,.05,.065,.08]:
        for maturity in [2,5,10,20,30]:
            z=calculate(1000,coupon,.05,maturity,.01,2);rows.append({"coupon_rate":coupon,"maturity_years":maturity,**z})
    return pd.DataFrame(rows)

def create_charts(results=None,sensitivity_data=None):
    results=run_scenarios() if results is None else results;sensitivity_data=sensitivity() if sensitivity_data is None else sensitivity_data;d=model_root(SLUG)/"charts"
    scenario_chart(results,"estimated_change_pct","Estimated price change (%)","Duration-Convexity Estimate under Rate Shocks",d/"duration_scenarios.png",percent=True)
    p=sensitivity_data.pivot(index="maturity_years",columns="coupon_rate",values="modified_duration");p.columns=[f"{x:.1%}" for x in p.columns]
    heatmap_chart(p,"Modified Duration Sensitivity","Coupon rate","Maturity (years)","Modified duration (years)",d/"duration_sensitivity.png")

def run_model(input_path=None,export=True):
    r,s=run_scenarios(input_path),sensitivity()
    if export:export_results(SLUG,r,s);create_charts(r,s)
    return r,s
