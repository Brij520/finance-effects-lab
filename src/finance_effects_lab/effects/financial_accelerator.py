"""Financial accelerator: net-worth shocks alter external finance capacity."""
import numpy as np
import pandas as pd

from finance_effects_lab.common import export_results, heatmap_chart, model_root, read_assumptions, scenario_chart, validate_rates

SLUG = "financial_accelerator"


def calculate(initial_net_worth: float, asset_price_shock: float, collateral_multiplier: float,
              baseline_investment: float, investment_credit_sensitivity: float, existing_debt: float) -> dict:
    shocked_net_worth = max(0.0, initial_net_worth * (1 + asset_price_shock))
    borrowing_capacity = max(0.0, shocked_net_worth * collateral_multiplier - existing_debt)
    investment = max(0.0, baseline_investment + investment_credit_sensitivity * borrowing_capacity)
    return {"shocked_net_worth": shocked_net_worth, "borrowing_capacity": borrowing_capacity,
            "external_finance_premium": 0.04 + 0.08 * max(0, 1 - shocked_net_worth / initial_net_worth),
            "investment": investment, "investment_change": investment - baseline_investment}


def run_scenarios(input_path=None):
    data = read_assumptions(SLUG, input_path); validate_rates(data, ["asset_price_shock"])
    rows = []
    for r in data.to_dict("records"):
        rows.append({"scenario": r["scenario"], **r, **calculate(r["initial_net_worth"], r["asset_price_shock"], r["collateral_multiplier"], r["baseline_investment"], r["investment_credit_sensitivity"], r["existing_debt"])})
    return pd.DataFrame(rows)


def sensitivity():
    rows=[]
    for shock in np.linspace(-.40, .20, 7):
        for multiplier in [1.5, 2.0, 2.5, 3.0]:
            out=calculate(50, shock, multiplier, 20, .35, 50)
            rows.append({"asset_price_shock": shock, "collateral_multiplier": multiplier, **out})
    return pd.DataFrame(rows)


def create_charts(results=None, sensitivity_data=None):
    results=run_scenarios() if results is None else results; sensitivity_data=sensitivity() if sensitivity_data is None else sensitivity_data
    d=model_root(SLUG)/"charts"
    scenario_chart(results,"investment","Investment ($m)","Collateral Shocks Amplify Investment Outcomes",d/"financial_accelerator_scenarios.png")
    p=sensitivity_data.pivot(index="asset_price_shock",columns="collateral_multiplier",values="investment")
    p.index=[f"{x:.0%}" for x in p.index]
    heatmap_chart(p,"Investment Sensitivity to Collateral Shock","Collateral multiplier (x)","Asset-price shock","Investment ($m)",d/"financial_accelerator_sensitivity.png")


def run_model(input_path=None,export=True):
    r,s=run_scenarios(input_path),sensitivity()
    if export: export_results(SLUG,r,s); create_charts(r,s)
    return r,s
