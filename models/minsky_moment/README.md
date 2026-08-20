# Minsky Moment

> **Area:** Financial stability / credit cycles<br>
> **Status:** Reproducible numerical model with four scenarios, two-way sensitivity, PNG charts, CSV, and Excel output.

## 1. Concept

### Definition

A long expansion in credit and risk-taking can create fragile financing structures that reverse abruptly when debt service becomes unsustainable.

### Financial intuition and why it occurs

Stability can encourage more leverage; after a threshold, tighter credit and selling reinforce declining prices and deleveraging.

### Why finance professionals care

This mechanism changes financing capacity, valuation, earnings, stakeholder cash flow, or risk. A professional must understand both the directional intuition and the conditions under which it can reverse.

### Key assumptions

- Inputs in `sample_data.csv` are hypothetical and deliberately round; they are **not actual company data**.
- Currency values use the units in the column/chart label, usually $m; rates are decimals.
- The four scenarios change only listed inputs; they are not probabilities or forecasts.
- Calculations are deterministic so every output can be traced and reproduced.

### Limitations

Highly simplified deterministic cycle, arbitrary reduced-form coefficients, no expectations, defaults, policy reaction, sector heterogeneity, or empirical forecasting power.

## 2. Mathematical Model

1. **Debt-service ratio = Leverage × Asset price × Interest rate ÷ Income**
2. **Credit growth after trigger = −tightening strength**
3. **Asset-price change = credit beta × credit growth + risk-taking term − tightening term**

**Variable definitions.** Trigger DSR is an assumed fragility threshold; credit beta and tightening strength are educational mechanism parameters, not estimated forecasts.

**Plain English.** The Python function in [`../../src/finance_effects_lab/effects/minsky_moment.py`](../../src/finance_effects_lab/effects/minsky_moment.py) follows the sequence above, exposes intermediate calculations, and returns tabular results rather than hiding logic inside a chart.

## 3. Base Case

### Initial assumptions / inputs

| Input | Base assumption |
|---|---:|
| `initial_asset_price` | 100 |
| `initial_leverage` | 2.5 |
| `credit_growth` | 0.05 |
| `rate` | 0.035 |
| `trigger_debt_service_ratio` | 0.80 |
| `price_credit_beta` | 0.8 |
| `tightening_strength` | 0.05 |
| `periods` | 12 |

### Calculation and output

A 12-period synthetic cycle starts at price index 100 and 2.5× leverage. The 80% debt-service trigger keeps the base case in expansion, while pessimistic and stress cases breach their thresholds and reverse; this makes trigger behavior explicit rather than treating every scenario as a crash. Run `python models/minsky_moment/model.py` to refresh the complete calculation. Auditable results are saved in [`outputs/scenario_results.csv`](outputs/scenario_results.csv) and [`outputs/minsky_moment.xlsx`](outputs/minsky_moment.xlsx).

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

Easy-credit growth from 2% to 16% against interest rates from 2% to 10%. The long-form sensitivity export is Power BI-ready; the chart presents the same grid as an annotated heatmap.

## 6. Visualization

- **Scenario/path chart:** communicates direction, magnitude, units, and case labels.
- **Sensitivity heatmap:** identifies combinations that move the output across zero or a threshold.
- **Source note:** every figure labels results as Finance Effects Lab hypothetical assumptions.

See [`charts/`](charts/) for high-resolution PNG files.

## 7. Real-World Application and Evidence Standard

- **Documented research context — BIS:** BIS research on financial cycles and credit provides empirical context, not calibration for this model. [Primary/public reference](https://www.bis.org/publ/work395.htm)
- **Documented context — IMF:** Global Financial Stability Reports analyze leverage and financial-stability risks. [Primary/public reference](https://www.imf.org/en/Publications/GFSR)
- **Illustrative application — Federal Reserve:** A policymaker could use richer stress models; this notebook is not a Federal Reserve method. [Primary/public reference](https://www.federalreserve.gov/publications/financial-stability-report.htm)

“Documented” means the linked public source establishes the event, disclosure, or research context. “Illustrative” means the company is only a plausible professional use case. **No public-company performance is simulated, and no claim is made that an organization uses this exact model.** Access date for all links: 20 August 2026.

## 8. Finance Professional Interpretation

- **Risk analyst:** track nonlinear combinations of leverage, debt service, and collateral.
- **CFO/Treasurer:** avoid funding long-lived assets with fragile short-term debt.
- **Equity analyst:** distinguish sustainable growth from credit-dependent multiple expansion.

## 9. Key Takeaways

### Five key insights

1. The sign and magnitude of the result depend on explicit scenario inputs, not a universal constant.
2. A threshold or denominator can make a seemingly linear driver produce a nonlinear financial outcome.
3. The stress case is most useful when compared with a decision threshold, covenant, risk limit, or required return.
4. Sensitivity analysis is more informative than a single point estimate because major inputs are uncertain.
5. The model output supports judgment; it does not replace accounting policy, legal terms, market data, or due diligence.

### Three formulas to remember

1. **Debt-service ratio = Leverage × Asset price × Interest rate ÷ Income**
2. **Credit growth after trigger = −tightening strength**
3. **Asset-price change = credit beta × credit growth + risk-taking term − tightening term**

### Three practical applications

- Budgeting, valuation, or transaction scenario design.
- Risk-limit and downside-capacity review.
- Investment memo or finance-interview discussion.

### Three common mistakes

- Treating hypothetical scenario outputs as observed company performance.
- Entering percentages as whole numbers rather than decimals.
- Quoting the headline output without checking assumptions, units, thresholds, and omitted risks.

## 10. Interview Questions

### Beginner: What is a Minsky moment?

- **Expected thinking:** Explain the transition from stability to fragility.
- **Model answer:** Accumulated leverage and speculative financing make a system vulnerable to an abrupt tightening and forced deleveraging.
- **Follow-up:** Is every downturn a Minsky moment?
### Intermediate: Why can calm periods increase risk?

- **Expected thinking:** Discuss endogenous risk-taking.
- **Model answer:** Low observed volatility and easy credit can encourage leverage, weakening resilience to later shocks.
- **Follow-up:** Which indicators would you monitor?
### Advanced: Why is this not a forecast?

- **Expected thinking:** Identify unestimated parameters and omitted behavior.
- **Model answer:** The equations illustrate a mechanism; credible forecasting requires calibrated data, expectations, policy, heterogeneity, and uncertainty.
- **Follow-up:** How would you backtest without overfitting?

## Reproduce

```bash
python -m pip install -e .
python models/minsky_moment/model.py
jupyter lab models/minsky_moment/notebook.ipynb
```

The notebook displays assumptions, scenario results, sensitivity results, and charts. See the repository-level methodology and source catalog for governance and evidence conventions.
