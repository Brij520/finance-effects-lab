"""M&A EPS accretion/dilution model with debt, equity, tax, and synergies."""
import numpy as np
import pandas as pd
from finance_effects_lab.common import export_results,heatmap_chart,model_root,read_assumptions,scenario_chart

SLUG="ma_accretion_dilution"
def calculate(acquirer_eps,acquirer_shares,target_eps,target_shares,purchase_price,debt_financing,equity_financing,
              interest_rate,tax_rate,pre_tax_synergies,new_shares_issued):
    acquirer_net_income=acquirer_eps*acquirer_shares;target_net_income=target_eps*target_shares
    after_tax_synergies=pre_tax_synergies*(1-tax_rate);after_tax_interest=debt_financing*interest_rate*(1-tax_rate)
    pro_forma_net_income=acquirer_net_income+target_net_income+after_tax_synergies-after_tax_interest
    pro_forma_shares=acquirer_shares+new_shares_issued;pro_forma_eps=pro_forma_net_income/pro_forma_shares
    return {"acquirer_net_income":acquirer_net_income,"target_net_income":target_net_income,"after_tax_synergies":after_tax_synergies,
            "after_tax_interest":after_tax_interest,"pro_forma_net_income":pro_forma_net_income,"pro_forma_shares":pro_forma_shares,
            "pro_forma_eps":pro_forma_eps,"accretion_dilution_pct":pro_forma_eps/acquirer_eps-1,
            "funding_check":debt_financing+equity_financing-purchase_price}
def run_scenarios(input_path=None):
    d=read_assumptions(SLUG,input_path);return pd.DataFrame([{"scenario":r["scenario"],**r,**calculate(r["acquirer_eps"],r["acquirer_shares"],r["target_eps"],r["target_shares"],r["purchase_price"],r["debt_financing"],r["equity_financing"],r["interest_rate"],r["tax_rate"],r["pre_tax_synergies"],r["new_shares_issued"])} for r in d.to_dict("records")])
def sensitivity():
    rows=[];share_price=40
    for price in [300,350,400,450,500,550]:
        for synergy in [0,10,20,30,40,50]:
            debt=price*.60;equity=price-debt;new=equity/share_price
            z=calculate(2.5,100,1.2,20,price,debt,equity,.06,.25,synergy,new);rows.append({"purchase_price":price,"pre_tax_synergies":synergy,**z})
    return pd.DataFrame(rows)
def create_charts(results=None,sensitivity_data=None):
    results=run_scenarios() if results is None else results;sensitivity_data=sensitivity() if sensitivity_data is None else sensitivity_data;d=model_root(SLUG)/"charts"
    scenario_chart(results,"accretion_dilution_pct","EPS accretion / (dilution)","Pro Forma M&A EPS Impact",d/"ma_scenarios.png",percent=True)
    p=sensitivity_data.pivot(index="purchase_price",columns="pre_tax_synergies",values="accretion_dilution_pct")
    heatmap_chart(p,"M&A Accretion / Dilution Sensitivity","Pre-tax synergies ($m)","Purchase price ($m)","EPS accretion / (dilution)",d/"ma_sensitivity.png",percent=True)
def run_model(input_path=None,export=True):
    r,s=run_scenarios(input_path),sensitivity()
    if export:export_results(SLUG,r,s);create_charts(r,s)
    return r,s
