"""Primary share issuance and EPS/ownership dilution model."""
import numpy as np
import pandas as pd
from finance_effects_lab.common import export_results,heatmap_chart,model_root,read_assumptions,scenario_chart

SLUG="dilution_effect"
def calculate(net_income,existing_shares,new_shares,issue_price,return_on_proceeds=0.0):
    if existing_shares<=0 or new_shares<0:raise ValueError("Existing shares must be positive and new shares non-negative")
    proceeds=new_shares*issue_price;incremental_income=proceeds*return_on_proceeds
    old_eps=net_income/existing_shares;pro_forma_shares=existing_shares+new_shares;new_eps=(net_income+incremental_income)/pro_forma_shares
    return {"gross_proceeds":proceeds,"incremental_income":incremental_income,"pro_forma_shares":pro_forma_shares,
            "existing_holder_ownership_pct":existing_shares/pro_forma_shares,"old_eps":old_eps,"new_eps":new_eps,
            "eps_dilution_pct":new_eps/old_eps-1,"ownership_dilution_pct":existing_shares/pro_forma_shares-1}
def run_scenarios(input_path=None):
    d=read_assumptions(SLUG,input_path);return pd.DataFrame([{"scenario":r["scenario"],**r,**calculate(r["net_income"],r["existing_shares"],r["new_shares"],r["issue_price"],r["return_on_proceeds"])} for r in d.to_dict("records")])
def sensitivity():
    rows=[]
    for new in [0,10,20,30,40,50]:
        for roi in [0,.02,.04,.06,.08]:rows.append({"new_shares":new,"return_on_proceeds":roi,**calculate(100,100,new,20,roi)})
    return pd.DataFrame(rows)
def create_charts(results=None,sensitivity_data=None):
    results=run_scenarios() if results is None else results;sensitivity_data=sensitivity() if sensitivity_data is None else sensitivity_data;d=model_root(SLUG)/"charts"
    scenario_chart(results,"eps_dilution_pct","EPS accretion / (dilution)","EPS Impact of New Share Issuance",d/"dilution_scenarios.png",percent=True)
    p=sensitivity_data.pivot(index="new_shares",columns="return_on_proceeds",values="eps_dilution_pct");p.columns=[f"{x:.0%}" for x in p.columns]
    heatmap_chart(p,"EPS Sensitivity to Issuance and Reinvestment","Return on proceeds","New shares (m)","EPS accretion / (dilution)",d/"dilution_sensitivity.png",percent=True)
def run_model(input_path=None,export=True):
    r,s=run_scenarios(input_path),sensitivity()
    if export:export_results(SLUG,r,s);create_charts(r,s)
    return r,s
