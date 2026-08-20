"""Shared fixed-income calculations used by rate and duration modules."""
from __future__ import annotations

import numpy as np


def bond_cash_flows(face_value: float, coupon_rate: float, maturity_years: int, frequency: int = 2):
    periods = int(round(maturity_years * frequency))
    coupon = face_value * coupon_rate / frequency
    cash_flows = np.full(periods, coupon, dtype=float)
    cash_flows[-1] += face_value
    times = np.arange(1, periods + 1) / frequency
    return times, cash_flows


def bond_price(face_value: float, coupon_rate: float, yield_rate: float, maturity_years: int, frequency: int = 2) -> float:
    if maturity_years <= 0 or frequency <= 0 or face_value <= 0:
        raise ValueError("Face value, maturity, and frequency must be positive")
    times, cash_flows = bond_cash_flows(face_value, coupon_rate, maturity_years, frequency)
    periods = np.arange(1, len(times) + 1)
    return float(np.sum(cash_flows / (1 + yield_rate / frequency) ** periods))


def duration_convexity(face_value: float, coupon_rate: float, yield_rate: float, maturity_years: int, frequency: int = 2):
    times, cash_flows = bond_cash_flows(face_value, coupon_rate, maturity_years, frequency)
    periods = np.arange(1, len(times) + 1)
    pv = cash_flows / (1 + yield_rate / frequency) ** periods
    price = float(pv.sum())
    macaulay = float(np.sum(times * pv) / price)
    modified = macaulay / (1 + yield_rate / frequency)
    # Annualized convexity under periodic compounding.
    convexity = float(np.sum(periods * (periods + 1) * pv) / (price * frequency**2 * (1 + yield_rate / frequency) ** 2))
    return price, macaulay, modified, convexity
