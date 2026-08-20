"""Margin spiral: volatility-sensitive haircuts produce procyclical sales."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from finance_effects_lab.common import SOURCE_NOTE, export_results, heatmap_chart, model_root, read_assumptions

SLUG="margin_spiral"


def simulate(initial_assets:float,debt:float,initial_haircut:float,volatility_shock:float,haircut_sensitivity:float,
             price_impact:float,rounds:int=8):
    asset_value=initial_assets*(1-volatility_shock); current_debt=debt; volatility=volatility_shock; out=[]
    for i in range(rounds+1):
        equity=asset_value-current_debt
        haircut=min(.95,initial_haircut+haircut_sensitivity*volatility)
        max_debt=asset_value*(1-haircut)
        debt_gap=max(0.0,current_debt-max_debt)
        # Selling one dollar also removes that collateral dollar. Divide the debt gap by
        # the haircut to solve D-x <= (A-x)*(1-h), before secondary market impact.
        sale=min(asset_value, debt_gap/haircut if haircut>0 else asset_value)
        out.append({"round":i,"asset_value":asset_value,"debt":current_debt,"equity":equity,"haircut":haircut,"forced_sale":sale})
        if sale<1e-7: break
        current_debt=max(0.0,current_debt-sale)
        market_loss=price_impact*sale
        asset_value=max(0.0,asset_value-sale-market_loss)
        # Market loss raises measured risk and therefore the next margin requirement.
        volatility+=market_loss/initial_assets
    return pd.DataFrame(out)


def _calc(r):
    p=simulate(r["initial_assets"],r["debt"],r["initial_haircut"],r["volatility_shock"],r["haircut_sensitivity"],r["price_impact"])
    z=p.iloc[-1]
    return {"ending_asset_value":z.asset_value,"ending_equity":z.equity,"ending_haircut":z.haircut,"forced_sales":p.forced_sale.sum(),"rounds":int(z["round"])}


def run_scenarios(input_path=None):
    d=read_assumptions(SLUG,input_path)
    return pd.DataFrame([{"scenario":r["scenario"],**r,**_calc(r)} for r in d.to_dict("records")])


def sensitivity():
    rows=[]
    for vol in [.02,.05,.10,.15,.20]:
        for impact in [.05,.10,.20,.35,.50]:
            r={"initial_assets":100,"debt":75,"initial_haircut":.20,"volatility_shock":vol,"haircut_sensitivity":.35,"price_impact":impact}
            rows.append({"volatility_shock":vol,"price_impact":impact,**_calc(r)})
    return pd.DataFrame(rows)


def create_charts(results=None,sensitivity_data=None):
    results=run_scenarios() if results is None else results;sensitivity_data=sensitivity() if sensitivity_data is None else sensitivity_data
    d=model_root(SLUG)/"charts";d.mkdir(parents=True,exist_ok=True); fig,ax=plt.subplots(figsize=(9,5.3))
    for r in read_assumptions(SLUG).to_dict("records"):
        p=simulate(r["initial_assets"],r["debt"],r["initial_haircut"],r["volatility_shock"],r["haircut_sensitivity"],r["price_impact"])
        ax.plot(p["round"],p["haircut"]*100,marker="o",linewidth=2,label=r["scenario"])
    ax.set(title="Haircuts Rise as the Margin Spiral Progresses",xlabel="Margin round",ylabel="Required haircut (%)");ax.grid(alpha=.22);ax.legend(frameon=False)
    fig.text(.01,.01,SOURCE_NOTE,fontsize=7.5,color="#5D6774");fig.tight_layout(rect=(0,.04,1,1));fig.savefig(d/"margin_spiral_path.png",dpi=180);plt.close(fig)
    p=sensitivity_data.pivot(index="volatility_shock",columns="price_impact",values="forced_sales");p.index=[f"{x:.0%}" for x in p.index];p.columns=[f"{x:.0%}" for x in p.columns]
    heatmap_chart(p,"Forced-Sale Sensitivity","Price impact per $ sold","Volatility shock","Cumulative forced sales ($m)",d/"margin_spiral_sensitivity.png")


def run_model(input_path=None,export=True):
    r,s=run_scenarios(input_path),sensitivity()
    if export:export_results(SLUG,r,s);create_charts(r,s)
    return r,s
