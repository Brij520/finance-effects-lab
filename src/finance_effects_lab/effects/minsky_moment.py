"""Simplified credit-cycle mechanism inspired by Minsky.

Educational scenario model only. It is explicitly not a prediction engine.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from finance_effects_lab.common import SOURCE_NOTE,export_results,heatmap_chart,model_root,read_assumptions

SLUG="minsky_moment"
def simulate(initial_asset_price,initial_leverage,credit_growth,rate,trigger_debt_service_ratio,price_credit_beta,tightening_strength,periods=12):
    price=float(initial_asset_price);leverage=float(initial_leverage);credit=100.;income=20.;tight=False;rows=[]
    for t in range(int(periods)):
        debt_service=leverage*price*rate;dsr=debt_service/income
        if dsr>trigger_debt_service_ratio:tight=True
        effective_credit_growth=credit_growth if not tight else -tightening_strength
        credit*=1+effective_credit_growth
        leverage=max(.2,leverage*(1+effective_credit_growth*.65))
        risk_taking=max(0,credit_growth*leverage) if not tight else 0
        price_change=price_credit_beta*effective_credit_growth + .015*risk_taking
        if tight:price_change-=tightening_strength*.5
        price=max(1,price*(1+price_change))
        income*=1.02 if not tight else .98
        rows.append({"period":t+1,"asset_price":price,"leverage":leverage,"credit":credit,"debt_service_ratio":dsr,"risk_taking_index":risk_taking,"tightening":tight})
    return pd.DataFrame(rows)
def _calc(r):
    p=simulate(r["initial_asset_price"],r["initial_leverage"],r["credit_growth"],r["rate"],r["trigger_debt_service_ratio"],r["price_credit_beta"],r["tightening_strength"],r["periods"]);z=p.iloc[-1]
    peak=p.asset_price.max();return {"ending_asset_price":z.asset_price,"peak_asset_price":peak,"drawdown_from_peak":z.asset_price/peak-1,"ending_leverage":z.leverage,"tightening_periods":int(p.tightening.sum())}
def run_scenarios(input_path=None):
    d=read_assumptions(SLUG,input_path);return pd.DataFrame([{"scenario":r["scenario"],**r,**_calc(r)} for r in d.to_dict("records")])
def sensitivity():
    rows=[]
    for growth in [.02,.05,.08,.12,.16]:
        for rate in [.02,.04,.06,.08,.10]:
            r={"initial_asset_price":100,"initial_leverage":2.5,"credit_growth":growth,"rate":rate,"trigger_debt_service_ratio":.65,"price_credit_beta":.9,"tightening_strength":.12,"periods":12}
            rows.append({"credit_growth":growth,"rate":rate,**_calc(r)})
    return pd.DataFrame(rows)
def create_charts(results=None,sensitivity_data=None):
    results=run_scenarios() if results is None else results;sensitivity_data=sensitivity() if sensitivity_data is None else sensitivity_data;d=model_root(SLUG)/"charts";d.mkdir(parents=True,exist_ok=True);fig,ax=plt.subplots(figsize=(9,5.3))
    for r in read_assumptions(SLUG).to_dict("records"):
        p=simulate(r["initial_asset_price"],r["initial_leverage"],r["credit_growth"],r["rate"],r["trigger_debt_service_ratio"],r["price_credit_beta"],r["tightening_strength"],r["periods"]);ax.plot(p.period,p.asset_price,marker="o",label=r["scenario"],linewidth=2)
    ax.set(title="Simplified Minsky Cycle: Asset Price Path",xlabel="Period",ylabel="Asset-price index");ax.grid(alpha=.22);ax.legend(frameon=False);fig.text(.01,.01,SOURCE_NOTE+" Educational mechanism; not a forecast.",fontsize=7.5,color="#5D6774");fig.tight_layout(rect=(0,.04,1,1));fig.savefig(d/"minsky_cycle_path.png",dpi=180);plt.close(fig)
    p=sensitivity_data.pivot(index="credit_growth",columns="rate",values="drawdown_from_peak");p.index=[f"{x:.0%}" for x in p.index];p.columns=[f"{x:.0%}" for x in p.columns]
    heatmap_chart(p,"Peak-to-End Drawdown Sensitivity","Interest rate","Easy-credit growth","Drawdown from peak",d/"minsky_sensitivity.png",percent=True)
def run_model(input_path=None,export=True):
    r,s=run_scenarios(input_path),sensitivity()
    if export:export_results(SLUG,r,s);create_charts(r,s)
    return r,s
