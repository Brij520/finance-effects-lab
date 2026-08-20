"""Transparent two-regime multi-asset portfolio model."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from finance_effects_lab.common import SOURCE_NOTE,export_results,heatmap_chart,model_root,read_assumptions

SLUG="risk_on_risk_off"
def calculate(equity_weight,bond_weight,cash_weight,equity_return,bond_return,cash_return):
    total=equity_weight+bond_weight+cash_weight
    if not np.isclose(total,1):raise ValueError("Portfolio weights must sum to 1")
    contributions={"equity_contribution":equity_weight*equity_return,"bond_contribution":bond_weight*bond_return,"cash_contribution":cash_weight*cash_return}
    return {**contributions,"portfolio_return":sum(contributions.values()),"risk_asset_weight":equity_weight}
def run_scenarios(input_path=None):
    d=read_assumptions(SLUG,input_path);return pd.DataFrame([{"scenario":r["scenario"],**r,**calculate(r["equity_weight"],r["bond_weight"],r["cash_weight"],r["equity_return"],r["bond_return"],r["cash_return"])} for r in d.to_dict("records")])
def sensitivity():
    rows=[]
    for ew in [.2,.35,.5,.65,.8]:
        for er in [-.25,-.15,-.05,.05,.15]:
            bw=.9-ew;rows.append({"equity_weight":ew,"equity_return":er,**calculate(ew,bw,.1,er,.04,.02)})
    return pd.DataFrame(rows)
def create_charts(results=None,sensitivity_data=None):
    results=run_scenarios() if results is None else results;sensitivity_data=sensitivity() if sensitivity_data is None else sensitivity_data;d=model_root(SLUG)/"charts";d.mkdir(parents=True,exist_ok=True)
    x=np.arange(len(results));fig,ax=plt.subplots(figsize=(9,5.3));bottom=np.zeros(len(results))
    for c,label,color in [("equity_contribution","Equity","#2364AA"),("bond_contribution","Bond","#16856C"),("cash_contribution","Cash","#E59F23")]:
        v=results[c].to_numpy()*100;ax.bar(x,v,bottom=bottom,label=label,color=color);bottom+=v
    ax.set_xticks(x,results.scenario);ax.set(title="Risk-on / Risk-off Portfolio Return Contributions",xlabel="Regime scenario",ylabel="Return contribution (%)");ax.axhline(0,color="#273444",lw=.8);ax.legend(frameon=False);fig.text(.01,.01,SOURCE_NOTE,fontsize=7.5,color="#5D6774");fig.tight_layout(rect=(0,.04,1,1));fig.savefig(d/"risk_regime_contributions.png",dpi=180);plt.close(fig)
    p=sensitivity_data.pivot(index="equity_return",columns="equity_weight",values="portfolio_return");p.index=[f"{x:.0%}" for x in p.index];p.columns=[f"{x:.0%}" for x in p.columns]
    heatmap_chart(p,"Portfolio Sensitivity to Equity Regime","Equity weight","Equity return","Portfolio return",d/"risk_regime_sensitivity.png",percent=True)
def run_model(input_path=None,export=True):
    r,s=run_scenarios(input_path),sensitivity()
    if export:export_results(SLUG,r,s);create_charts(r,s)
    return r,s
