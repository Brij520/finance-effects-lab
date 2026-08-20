import math

from finance_effects_lab.effects.cash_flow_waterfall import calculate as waterfall
from finance_effects_lab.effects.contagion_effect import simulate as contagion
from finance_effects_lab.effects.financial_accelerator import calculate as accelerator
from finance_effects_lab.effects.leverage_cycle import simulate as leverage_cycle
from finance_effects_lab.effects.liquidity_spiral import simulate as liquidity_spiral
from finance_effects_lab.effects.margin_spiral import simulate as margin_spiral
from finance_effects_lab.effects.risk_on_risk_off import calculate as regime


def test_liquidity_spiral_stops_when_margin_is_satisfied():
    path = liquidity_spiral(100, 2, .02, .20, 1.5)
    assert path.iloc[-1]["forced_sale_units"] == 0
    assert len(path) <= 13


def test_higher_liquidity_reduces_price_damage():
    deep = liquidity_spiral(100, 4, .10, .25, 2.0).iloc[-1].price
    thin = liquidity_spiral(100, 4, .10, .25, .5).iloc[-1].price
    assert deep >= thin


def test_margin_spiral_reduces_debt_when_sale_occurs():
    path = margin_spiral(100, 80, .20, .20, .55, .40)
    assert path.iloc[-1].debt <= path.iloc[0].debt
    assert path.forced_sale.sum() >= 0


def test_waterfall_distributions_do_not_exceed_post_debt_cash():
    result = waterfall(120, 72, .25, 180, .07, 20, 40, .11, 5, 100, .08, .20)
    available = result["ebitda"] - result["taxes"] - result["senior_interest"] - result["senior_principal"] - result["mezzanine_interest"] - result["mezzanine_principal"]
    assert math.isclose(result["total_equity_distribution"], max(available, 0), abs_tol=1e-9)
    assert result["lp_distribution"] >= result["sponsor_distribution"]


def test_accelerator_investment_falls_with_collateral_shock():
    good = accelerator(50, .10, 2.5, 20, .35, 50)["investment"]
    bad = accelerator(50, -.40, 2.5, 20, .35, 50)["investment"]
    assert good > bad


def test_more_capital_does_not_increase_network_defaults():
    weak, _ = contagion(5, 8, .3, .6, .5)
    strong, _ = contagion(5, 8, .3, 1.5, .5)
    assert strong.defaulted.sum() <= weak.defaulted.sum()


def test_leverage_cycle_has_positive_balance_sheet_values():
    path = leverage_cycle(100, 70, -.12, .25, .8, 8)
    assert (path[["collateral", "equity", "leverage"]] > 0).all().all()


def test_portfolio_weights_must_sum_to_one():
    try:
        regime(.5, .3, .1, .1, .03, .02)
    except ValueError as error:
        assert "sum to 1" in str(error)
    else:
        raise AssertionError("Expected invalid weight error")
