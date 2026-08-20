"""Iterative liquidity spiral with margin-driven sales and linear price impact.

This is an educational mechanism model, not a market prediction engine.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from finance_effects_lab.common import SOURCE_NOTE, export_results, heatmap_chart, model_root, read_assumptions, validate_rates

SLUG="liquidity_spiral"


def simulate(initial_assets: float, leverage: float, initial_shock: float, margin_requirement: float,
             market_liquidity: float, max_rounds: int=12) -> pd.DataFrame:
    if initial_assets <= 0 or leverage < 1 or market_liquidity <= 0 or not 0 <= margin_requirement < 1:
        raise ValueError("Require positive assets/liquidity, leverage >= 1, and margin in [0,1)")
    units=initial_assets; price=1.0; debt=initial_assets-initial_assets/leverage
    rows=[]
    price *= (1-initial_shock)
    for round_no in range(max_rounds+1):
        assets=units*price; equity=assets-debt; margin_ratio=equity/assets if assets>0 else -np.inf
        required_sale=0.0
        if equity <= 0:
            required_sale=units
        elif margin_ratio < margin_requirement:
            # Sale proceeds repay debt; solve E/(A-sale) >= required margin.
            required_sale_value=max(0.0, assets-equity/margin_requirement)
            required_sale=min(units, required_sale_value/price)
        rows.append({"round":round_no,"price":price,"units":units,"asset_value":assets,"debt":debt,
                     "equity":equity,"margin_ratio":margin_ratio,"forced_sale_units":required_sale})
        if required_sale <= 1e-8: break
        sale_value=required_sale*price; units-=required_sale; debt=max(0.0,debt-sale_value)
        incremental_impact=min(.95, required_sale/initial_assets/market_liquidity)
        price *= (1-incremental_impact)
    return pd.DataFrame(rows)


def _summary(r):
    path=simulate(r["initial_assets"],r["leverage"],r["initial_shock"],r["margin_requirement"],r["market_liquidity"])
    last=path.iloc[-1]
    return {"final_price":last.price,"price_decline":1-last.price,"final_equity":last.equity,
            "forced_sales":path.forced_sale_units.sum(),"rounds":int(last["round"]),"default_flag":int(last.equity<=0)}


def run_scenarios(input_path=None):
    data=read_assumptions(SLUG,input_path); validate_rates(data,["initial_shock","margin_requirement"])
    return pd.DataFrame([{"scenario":r["scenario"],**r,**_summary(r)} for r in data.to_dict("records")])


def sensitivity():
    rows=[]
    for shock in [.02,.05,.08,.12,.16,.20]:
        for leverage in [2,3,4,5,6]:
            r={"initial_assets":100,"leverage":leverage,"initial_shock":shock,"margin_requirement":.25,"market_liquidity":.75}
            rows.append({"initial_shock":shock,"leverage":leverage,**_summary(r)})
    return pd.DataFrame(rows)


def create_charts(results=None,sensitivity_data=None):
    results=run_scenarios() if results is None else results; sensitivity_data=sensitivity() if sensitivity_data is None else sensitivity_data
    d=model_root(SLUG)/"charts"; d.mkdir(parents=True,exist_ok=True)
    assumptions=read_assumptions(SLUG); fig,ax=plt.subplots(figsize=(9,5.3))
    for r in assumptions.to_dict("records"):
        path=simulate(r["initial_assets"],r["leverage"],r["initial_shock"],r["margin_requirement"],r["market_liquidity"])
        ax.plot(path["round"],path["price"]*100,marker="o",label=r["scenario"],linewidth=2)
    ax.set(title="Liquidity Feedback Loop: Price by Forced-Sale Round",xlabel="Feedback round",ylabel="Asset price (initial = 100)");ax.grid(alpha=.22);ax.legend(frameon=False)
    fig.text(.01,.01,SOURCE_NOTE,fontsize=7.5,color="#5D6774");fig.tight_layout(rect=(0,.04,1,1));fig.savefig(d/"liquidity_spiral_path.png",dpi=180);plt.close(fig)
    p=sensitivity_data.pivot(index="initial_shock",columns="leverage",values="final_price");p.index=[f"{x:.0%}" for x in p.index];p.columns=[f"{x:.0f}x" for x in p.columns]
    heatmap_chart(p,"Ending Price after Liquidity Feedback","Initial leverage","Initial price shock","Ending price (initial = 1.00)",d/"liquidity_spiral_sensitivity.png")


def run_model(input_path=None,export=True):
    r,s=run_scenarios(input_path),sensitivity()
    if export: export_results(SLUG,r,s); create_charts(r,s)
    return r,s
