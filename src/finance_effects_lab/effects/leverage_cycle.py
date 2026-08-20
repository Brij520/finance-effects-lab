"""Procyclical leverage capacity under changing collateral values and haircuts."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from finance_effects_lab.common import SOURCE_NOTE,export_results,heatmap_chart,model_root,read_assumptions

SLUG="leverage_cycle"
def simulate(initial_collateral,initial_debt,asset_return,haircut,procyclicality,periods=8):
    collateral=float(initial_collateral);debt=float(initial_debt);rows=[]
    for t in range(int(periods)):
        collateral*=1+asset_return
        dynamic_haircut=float(np.clip(haircut-procyclicality*asset_return,0.05,.90))
        debt_capacity=collateral*(1-dynamic_haircut)
        debt += .65*(debt_capacity-debt)  # balance-sheet adjustment is gradual, not instantaneous
        equity=max(collateral-debt,1e-9);leverage=collateral/equity
        rows.append({"period":t+1,"collateral":collateral,"haircut":dynamic_haircut,"debt_capacity":debt_capacity,"debt":debt,"equity":equity,"leverage":leverage})
    return pd.DataFrame(rows)
def _calc(r):
    p=simulate(r["initial_collateral"],r["initial_debt"],r["asset_return"],r["haircut"],r["procyclicality"],r["periods"]);z=p.iloc[-1]
    return {"ending_collateral":z.collateral,"ending_debt":z.debt,"ending_leverage":z.leverage,"ending_haircut":z.haircut,"debt_capacity_change":z.debt_capacity-r["initial_debt"]}
def run_scenarios(input_path=None):
    d=read_assumptions(SLUG,input_path);return pd.DataFrame([{"scenario":r["scenario"],**r,**_calc(r)} for r in d.to_dict("records")])
def sensitivity():
    rows=[]
    for ret in [-.15,-.10,-.05,0,.05,.10,.15]:
        for pro in [.2,.4,.6,.8,1.0]:
            r={"initial_collateral":100,"initial_debt":70,"asset_return":ret,"haircut":.25,"procyclicality":pro,"periods":8};rows.append({"asset_return":ret,"procyclicality":pro,**_calc(r)})
    return pd.DataFrame(rows)
def create_charts(results=None,sensitivity_data=None):
    results=run_scenarios() if results is None else results;sensitivity_data=sensitivity() if sensitivity_data is None else sensitivity_data;d=model_root(SLUG)/"charts";d.mkdir(parents=True,exist_ok=True);fig,ax=plt.subplots(figsize=(9,5.3))
    for r in read_assumptions(SLUG).to_dict("records"):
        p=simulate(r["initial_collateral"],r["initial_debt"],r["asset_return"],r["haircut"],r["procyclicality"],r["periods"]);ax.plot(p.period,p.leverage,marker="o",linewidth=2,label=r["scenario"])
    ax.set(title="Procyclical Leverage Path",xlabel="Period",ylabel="Assets / equity (x)");ax.grid(alpha=.22);ax.legend(frameon=False);fig.text(.01,.01,SOURCE_NOTE,fontsize=7.5,color="#5D6774");fig.tight_layout(rect=(0,.04,1,1));fig.savefig(d/"leverage_cycle_path.png",dpi=180);plt.close(fig)
    p=sensitivity_data.pivot(index="asset_return",columns="procyclicality",values="ending_leverage");p.index=[f"{x:.0%}" for x in p.index]
    heatmap_chart(p,"Ending Leverage Sensitivity","Procyclicality coefficient","Periodic asset return","Ending leverage (x)",d/"leverage_cycle_sensitivity.png")
def run_model(input_path=None,export=True):
    r,s=run_scenarios(input_path),sensitivity()
    if export:export_results(SLUG,r,s);create_charts(r,s)
    return r,s
