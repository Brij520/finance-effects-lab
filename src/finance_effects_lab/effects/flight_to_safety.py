"""Asset-allocation flows from risky assets toward safe assets after a shock."""
import numpy as np
import pandas as pd
from finance_effects_lab.common import export_results,heatmap_chart,model_root,read_assumptions,scenario_chart

SLUG="flight_to_safety"
def calculate(portfolio_value,initial_safe_weight,risk_aversion_shock,reallocation_sensitivity,safe_market_depth,risky_market_depth):
    flow=min(portfolio_value*(1-initial_safe_weight),max(0,portfolio_value*risk_aversion_shock*reallocation_sensitivity))
    safe_return=flow/safe_market_depth;risky_return=-flow/risky_market_depth;new_safe_value=portfolio_value*initial_safe_weight+flow
    return {"flow_to_safe":flow,"safe_asset_return":safe_return,"risky_asset_return":risky_return,"new_safe_weight":new_safe_value/portfolio_value,"spread_move":safe_return-risky_return}
def run_scenarios(input_path=None):
    d=read_assumptions(SLUG,input_path);return pd.DataFrame([{"scenario":r["scenario"],**r,**calculate(r["portfolio_value"],r["initial_safe_weight"],r["risk_aversion_shock"],r["reallocation_sensitivity"],r["safe_market_depth"],r["risky_market_depth"])} for r in d.to_dict("records")])
def sensitivity():
    rows=[]
    for shock in [0,.05,.10,.15,.20,.25]:
        for depth in [500,750,1000,1500,2000]: rows.append({"risk_aversion_shock":shock,"safe_market_depth":depth,**calculate(100,0.30,shock,.8,depth,750)})
    return pd.DataFrame(rows)
def create_charts(results=None,sensitivity_data=None):
    results=run_scenarios() if results is None else results;sensitivity_data=sensitivity() if sensitivity_data is None else sensitivity_data;d=model_root(SLUG)/"charts"
    scenario_chart(results,"flow_to_safe","Flow ($m)","Modeled Reallocation toward Safe Assets",d/"flight_to_safety_scenarios.png")
    p=sensitivity_data.pivot(index="risk_aversion_shock",columns="safe_market_depth",values="safe_asset_return");p.index=[f"{x:.0%}" for x in p.index]
    heatmap_chart(p,"Safe-Asset Return Sensitivity","Safe-market depth ($m)","Risk-aversion shock","Modeled safe return",d/"flight_to_safety_sensitivity.png",percent=True)
def run_model(input_path=None,export=True):
    r,s=run_scenarios(input_path),sensitivity()
    if export:export_results(SLUG,r,s);create_charts(r,s)
    return r,s
