"""Leverage effect: debt changes the distribution of return on equity."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from finance_effects_lab.common import SOURCE_NOTE, export_results, model_root, ordered, read_assumptions, heatmap_chart, validate_rates

SLUG = "leverage_effect"
DEBT_RATIOS = (0.00, 0.25, 0.50, 0.75)


def calculate(assets: float, return_on_assets: float, debt_ratio: float, interest_rate: float, tax_rate: float) -> dict:
    if assets <= 0 or not 0 <= debt_ratio < 1:
        raise ValueError("Assets must be positive and debt ratio in [0, 1)")
    debt = assets * debt_ratio
    equity = assets - debt
    ebit = assets * return_on_assets
    interest_expense = debt * interest_rate
    pre_tax_income = ebit - interest_expense
    taxes = max(pre_tax_income, 0) * tax_rate  # no NOL benefit is recognized in loss cases
    net_income = pre_tax_income - taxes
    return {"assets": assets, "debt_ratio": debt_ratio, "debt": debt, "equity": equity,
            "ebit": ebit, "interest_expense": interest_expense, "pre_tax_income": pre_tax_income,
            "taxes": taxes, "net_income": net_income, "roe": net_income / equity}


def run_scenarios(input_path=None) -> pd.DataFrame:
    assumptions = read_assumptions(SLUG, input_path)
    validate_rates(assumptions, ["return_on_assets", "interest_rate", "tax_rate"])
    rows = []
    for row in assumptions.to_dict("records"):
        for debt_ratio in DEBT_RATIOS:
            rows.append({"scenario": row["scenario"], **calculate(row["assets"], row["return_on_assets"], debt_ratio, row["interest_rate"], row["tax_rate"])})
    return ordered(pd.DataFrame(rows))


def sensitivity() -> pd.DataFrame:
    records = []
    for roa in np.array([-0.08, -0.04, 0.00, 0.04, 0.08, 0.12, 0.16]):
        for debt_ratio in DEBT_RATIOS:
            records.append({"return_on_assets": roa, "debt_ratio": debt_ratio,
                            "roe": calculate(100, roa, debt_ratio, 0.06, 0.25)["roe"]})
    return pd.DataFrame(records)


def create_charts(results=None, sensitivity_data=None):
    results = run_scenarios() if results is None else results
    sensitivity_data = sensitivity() if sensitivity_data is None else sensitivity_data
    chart_dir = model_root(SLUG) / "charts"; chart_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 5.4))
    for scenario, group in results.groupby("scenario", observed=True):
        ax.plot(group["debt_ratio"] * 100, group["roe"] * 100, marker="o", linewidth=2, label=str(scenario))
    ax.axhline(0, color="#273444", linewidth=.8)
    ax.set(title="Leverage Magnifies ROE Outcomes", xlabel="Debt / Assets (%)", ylabel="Return on Equity (%)")
    ax.grid(alpha=.22); ax.legend(frameon=False)
    fig.text(.01, .01, SOURCE_NOTE, fontsize=7.5, color="#5D6774")
    fig.tight_layout(rect=(0, .04, 1, 1)); fig.savefig(chart_dir / "leverage_scenarios.png", dpi=180); plt.close(fig)
    pivot = sensitivity_data.pivot(index="return_on_assets", columns="debt_ratio", values="roe")
    pivot.index = [f"{x:.0%}" for x in pivot.index]; pivot.columns = [f"{x:.0%}" for x in pivot.columns]
    heatmap_chart(pivot, "ROE Sensitivity to Operating Return and Leverage", "Debt / Assets", "Return on Assets", "ROE", chart_dir / "leverage_sensitivity.png", percent=True)


def run_model(input_path=None, export=True):
    results, sens = run_scenarios(input_path), sensitivity()
    if export: export_results(SLUG, results, sens); create_charts(results, sens)
    return results, sens
