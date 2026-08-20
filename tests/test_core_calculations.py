import math

from finance_effects_lab.effects._bond import bond_price, duration_convexity
from finance_effects_lab.effects.compound_interest import calculate as compound
from finance_effects_lab.effects.dilution_effect import calculate as dilution
from finance_effects_lab.effects.fisher_effect import calculate as fisher, nominal_from_real
from finance_effects_lab.effects.leverage_effect import calculate as leverage
from finance_effects_lab.effects.ma_accretion_dilution import calculate as ma
from finance_effects_lab.effects.tax_shield import calculate as tax_shield


def test_par_bond_prices_at_face_value():
    assert math.isclose(bond_price(1000, .05, .05, 10, 2), 1000, rel_tol=1e-10)


def test_bond_price_moves_inversely_to_yield():
    low = bond_price(1000, .05, .04, 10, 2)
    high = bond_price(1000, .05, .06, 10, 2)
    assert low > 1000 > high


def test_modified_duration_is_positive_and_below_maturity_for_coupon_bond():
    _, macaulay, modified, convexity = duration_convexity(1000, .05, .05, 10, 2)
    assert 0 < modified < macaulay < 10
    assert convexity > 0


def test_unlevered_roe_matches_after_tax_roa():
    result = leverage(100, .10, 0, .06, .25)
    assert math.isclose(result["roe"], .075)
    assert result["interest_expense"] == 0


def test_leverage_magnifies_upside_and_downside():
    upside_unlevered = leverage(100, .15, 0, .06, .25)["roe"]
    upside_levered = leverage(100, .15, .75, .06, .25)["roe"]
    downside_unlevered = leverage(100, -.08, 0, .06, .25)["roe"]
    downside_levered = leverage(100, -.08, .75, .06, .25)["roe"]
    assert upside_levered > upside_unlevered
    assert downside_levered < downside_unlevered


def test_tax_shield_uses_only_available_taxable_income():
    normal = tax_shield(25, 100, .06, .25, 5, 7, 2)
    loss = tax_shield(2, 100, .06, .25, 5, 7, 2)
    assert math.isclose(normal["tax_shield"], 1.5)
    assert math.isclose(loss["tax_shield"], .5)  # no benefit beyond unlevered cash tax


def test_zero_return_issuance_mechanically_dilutes_eps():
    result = dilution(100, 100, 25, 20, 0)
    assert math.isclose(result["old_eps"], 1)
    assert math.isclose(result["new_eps"], .8)
    assert math.isclose(result["eps_dilution_pct"], -.2)


def test_ma_pro_forma_eps_bridge_and_funding_check():
    result = ma(2.5, 100, 1.2, 20, 400, 240, 160, .06, .25, 25, 4)
    expected_ni = 250 + 24 + 18.75 - 10.8
    assert math.isclose(result["pro_forma_net_income"], expected_ni)
    assert math.isclose(result["pro_forma_eps"], expected_ni / 104)
    assert result["funding_check"] == 0


def test_compound_interest_zero_rate_is_well_defined():
    result = compound(10_000, 0, 20, 12, 2_000)
    assert math.isclose(result["future_value"], 50_000)
    assert result["compound_growth"] == 0


def test_fisher_exact_identity_round_trip():
    real = fisher(.06, .03)["real_rate"]
    assert math.isclose(nominal_from_real(real, .03), .06)
    assert real < .03  # exact value is slightly below the subtraction approximation
