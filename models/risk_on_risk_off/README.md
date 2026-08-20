# Risk-on/Risk-off Effect

> **Area:** Portfolio management<br>
> **Status:** Reproducible numerical model with four scenarios, two-way sensitivity, PNG charts, CSV, and Excel output.

## 1. Concept

### Definition

Broad changes in risk appetite create regimes in which risky assets tend to gain or lose together while defensive assets behave differently.

### Financial intuition and why it occurs

A portfolio's regime result is the sum of each asset return times its allocation, so defensive weights can reduce stress loss at the cost of upside.

### Why finance professionals care

This mechanism changes financing capacity, valuation, earnings, stakeholder cash flow, or risk. A professional must understand both the directional intuition and the conditions under which it can reverse.

### Key assumptions

- Inputs in `sample_data.csv` are hypothetical and deliberately round; they are **not actual company data**.
- Currency values use the units in the column/chart label, usually $m; rates are decimals.
- The four scenarios change only listed inputs; they are not probabilities or forecasts.
- Calculations are deterministic so every output can be traced and reproduced.

### Limitations

Single period, deterministic returns, no covariance, transaction costs, FX, credit spread, path dependence, or estimation uncertainty.

## 2. Mathematical Model

1. **Portfolio return = Σ weightᵢ × returnᵢ**
2. **Asset contribution = weightᵢ × returnᵢ**
3. **Risk-asset weight = Equity weight in this simplified three-asset model**

**Variable definitions.** Weights sum to 100%; modeled assets are equity, bonds, and cash; return assumptions are scenario inputs, not forecasts.

**Plain English.** The Python function in [`../../src/finance_effects_lab/effects/risk_on_risk_off.py`](../../src/finance_effects_lab/effects/risk_on_risk_off.py) follows the sequence above, exposes intermediate calculations, and returns tabular results rather than hiding logic inside a chart.

## 3. Base Case

### Initial assumptions / inputs

| Input | Base assumption |
|---|---:|
| `equity_weight` | 0.60 |
| `bond_weight` | 0.30 |
| `cash_weight` | 0.10 |
| `equity_return` | 0.07 |
| `bond_return` | 0.03 |
| `cash_return` | 0.02 |

### Calculation and output

The base portfolio is 60% equity, 30% bonds, and 10% cash with 7%, 3%, and 2% assumed returns. Stress shifts weights defensively and changes all asset returns. Run `python models/risk_on_risk_off/model.py` to refresh the complete calculation. Auditable results are saved in [`outputs/scenario_results.csv`](outputs/scenario_results.csv) and [`outputs/risk_on_risk_off.xlsx`](outputs/risk_on_risk_off.xlsx).

### Business interpretation

The base case is a decision anchor, not a conclusion. Compare it with the optimistic, pessimistic, and stress cases, identify the driver that crosses a risk or return threshold, and state which omitted factor could change the recommendation.

## 4. Scenario Analysis

| Scenario | Intended interpretation |
|---|---|
| Optimistic | Favorable operating, market, or financing conditions |
| Base | Central planning assumption—not a statistical forecast |
| Pessimistic | Material but manageable deterioration |
| Stress | Severe educational reverse stress; tests mechanism and resilience |

Major assumptions can be changed directly in `sample_data.csv`. Input validation rejects malformed scenario sets and selected nonsensical values.

## 5. Sensitivity Analysis

Equity weight from 20% to 80% against equity return from -25% to +15%, holding 10% cash. The long-form sensitivity export is Power BI-ready; the chart presents the same grid as an annotated heatmap.

## 6. Visualization

- **Scenario/path chart:** communicates direction, magnitude, units, and case labels.
- **Sensitivity heatmap:** identifies combinations that move the output across zero or a threshold.
- **Source note:** every figure labels results as Finance Effects Lab hypothetical assumptions.

See [`charts/`](charts/) for high-resolution PNG files.

## 7. Real-World Application and Evidence Standard

- **Documented context — BlackRock:** Public market outlooks discuss portfolio regimes; no BlackRock allocation is copied here. [Primary/public reference](https://www.blackrock.com/corporate/insights/blackrock-investment-institute/publications/outlook)
- **Documented context — Federal Reserve:** Financial Stability Reports provide risk-appetite indicators for broader analysis. [Primary/public reference](https://www.federalreserve.gov/publications/financial-stability-report.htm)
- **Illustrative application — Berkshire Hathaway:** An analyst could classify public holdings by factor exposure; this model is not Berkshire's portfolio. [Primary/public reference](https://www.berkshirehathaway.com/reports.html)

“Documented” means the linked public source establishes the event, disclosure, or research context. “Illustrative” means the company is only a plausible professional use case. **No public-company performance is simulated, and no claim is made that an organization uses this exact model.** Access date for all links: 20 August 2026.

## 8. Finance Professional Interpretation

- **Portfolio manager:** quantify return contribution by regime and allocation.
- **Equity analyst:** separate beta-driven rerating from company fundamentals.
- **Risk analyst:** challenge assumed defensive correlations during inflation or liquidity shocks.

## 9. Key Takeaways

### Five key insights

1. The sign and magnitude of the result depend on explicit scenario inputs, not a universal constant.
2. A threshold or denominator can make a seemingly linear driver produce a nonlinear financial outcome.
3. The stress case is most useful when compared with a decision threshold, covenant, risk limit, or required return.
4. Sensitivity analysis is more informative than a single point estimate because major inputs are uncertain.
5. The model output supports judgment; it does not replace accounting policy, legal terms, market data, or due diligence.

### Three formulas to remember

1. **Portfolio return = Σ weightᵢ × returnᵢ**
2. **Asset contribution = weightᵢ × returnᵢ**
3. **Risk-asset weight = Equity weight in this simplified three-asset model**

### Three practical applications

- Budgeting, valuation, or transaction scenario design.
- Risk-limit and downside-capacity review.
- Investment memo or finance-interview discussion.

### Three common mistakes

- Treating hypothetical scenario outputs as observed company performance.
- Entering percentages as whole numbers rather than decimals.
- Quoting the headline output without checking assumptions, units, thresholds, and omitted risks.

## 10. Interview Questions

### Beginner: What does risk-on mean?

- **Expected thinking:** Define behavior, not a permanent asset label.
- **Model answer:** Risk tolerance rises, often supporting equities and credit relative to defensive assets.
- **Follow-up:** Can bonds fall in risk-off?
### Intermediate: How do contributions differ from returns?

- **Expected thinking:** Multiply each asset return by its weight.
- **Model answer:** A high-return small position can contribute less than a moderate-return large position.
- **Follow-up:** How should cash be treated?
### Advanced: How would you identify regimes?

- **Expected thinking:** Use transparent indicators and avoid look-ahead bias.
- **Model answer:** Combine volatility, spreads, correlations, and flows, estimate regimes on available data, and test stability out of sample.
- **Follow-up:** How would transaction costs alter switching?

## Reproduce

```bash
python -m pip install -e .
python models/risk_on_risk_off/model.py
jupyter lab models/risk_on_risk_off/notebook.ipynb
```

The notebook displays assumptions, scenario results, sensitivity results, and charts. See the repository-level methodology and source catalog for governance and evidence conventions.
