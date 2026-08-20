# Wealth Effect

> **Area:** Financial economics / consumer demand<br>
> **Status:** Reproducible numerical model with four scenarios, two-way sensitivity, PNG charts, CSV, and Excel output.

## 1. Concept

### Definition

A change in household net worth can alter consumption because households spend a fraction of gains or cut spending after losses.

### Financial intuition and why it occurs

Asset appreciation relaxes lifetime budget constraints, though the response depends on liquidity, permanence, distribution, and household type.

### Why finance professionals care

This mechanism changes financing capacity, valuation, earnings, stakeholder cash flow, or risk. A professional must understand both the directional intuition and the conditions under which it can reverse.

### Key assumptions

- Inputs in `sample_data.csv` are hypothetical and deliberately round; they are **not actual company data**.
- Currency values use the units in the column/chart label, usually $m; rates are decimals.
- The four scenarios change only listed inputs; they are not probabilities or forecasts.
- Calculations are deterministic so every output can be traced and reproduced.

### Limitations

Representative household, symmetric linear MPC, no income shock, debt, age, asset liquidity, distributional heterogeneity, or confidence channel.

## 2. Mathematical Model

1. **Wealth change = Initial wealth × asset return**
2. **Consumption change = MPC out of wealth × Wealth change**
3. **Consumption change % = Consumption change ÷ Baseline consumption**

**Variable definitions.** MPC is marginal propensity to consume from a dollar of wealth change; it is an assumption, not a universal constant.

**Plain English.** The Python function in [`../../src/finance_effects_lab/effects/wealth_effect.py`](../../src/finance_effects_lab/effects/wealth_effect.py) follows the sequence above, exposes intermediate calculations, and returns tabular results rather than hiding logic inside a chart.

## 3. Base Case

### Initial assumptions / inputs

| Input | Base assumption |
|---|---:|
| `initial_wealth` | 500 |
| `wealth_return` | 0.05 |
| `marginal_propensity_to_consume` | 0.04 |
| `baseline_consumption` | 80 |

### Calculation and output

A household segment has $500k wealth, $80k annual consumption, and 4% MPC. The model applies returns from +20% to -30% and converts wealth changes to spending. Run `python models/wealth_effect/model.py` to refresh the complete calculation. Auditable results are saved in [`outputs/scenario_results.csv`](outputs/scenario_results.csv) and [`outputs/wealth_effect.xlsx`](outputs/wealth_effect.xlsx).

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

Wealth returns from -30% to +30% against MPC estimates from 2% to 6%. The long-form sensitivity export is Power BI-ready; the chart presents the same grid as an annotated heatmap.

## 6. Visualization

- **Scenario/path chart:** communicates direction, magnitude, units, and case labels.
- **Sensitivity heatmap:** identifies combinations that move the output across zero or a threshold.
- **Source note:** every figure labels results as Finance Effects Lab hypothetical assumptions.

See [`charts/`](charts/) for high-resolution PNG files.

## 7. Real-World Application and Evidence Standard

- **Documented data — Federal Reserve:** Distributional Financial Accounts provide household wealth context; no series is embedded in the hypothetical base case. [Primary/public reference](https://www.federalreserve.gov/releases/z1/dataviz/dfa/)
- **Illustrative application — Visa:** An analyst could compare modeled spending sensitivity with disclosed payment-volume trends; this is not a Visa forecast. [Primary/public reference](https://annualreport.visa.com/)
- **Illustrative application — Mastercard:** The framework could support consumer-spending scenarios using separately sourced data. [Primary/public reference](https://investor.mastercard.com/financials-and-sec-filings/annual-reports-and-proxy/default.aspx)

“Documented” means the linked public source establishes the event, disclosure, or research context. “Illustrative” means the company is only a plausible professional use case. **No public-company performance is simulated, and no claim is made that an organization uses this exact model.** Access date for all links: 20 August 2026.

## 8. Finance Professional Interpretation

- **FP&A analyst:** link macro wealth scenarios to category demand with explicit elasticity.
- **Equity analyst:** test consumer-exposed revenue against asset-price shocks.
- **Risk analyst:** avoid applying one MPC to every household or spending category.

## 9. Key Takeaways

### Five key insights

1. The sign and magnitude of the result depend on explicit scenario inputs, not a universal constant.
2. A threshold or denominator can make a seemingly linear driver produce a nonlinear financial outcome.
3. The stress case is most useful when compared with a decision threshold, covenant, risk limit, or required return.
4. Sensitivity analysis is more informative than a single point estimate because major inputs are uncertain.
5. The model output supports judgment; it does not replace accounting policy, legal terms, market data, or due diligence.

### Three formulas to remember

1. **Wealth change = Initial wealth × asset return**
2. **Consumption change = MPC out of wealth × Wealth change**
3. **Consumption change % = Consumption change ÷ Baseline consumption**

### Three practical applications

- Budgeting, valuation, or transaction scenario design.
- Risk-limit and downside-capacity review.
- Investment memo or finance-interview discussion.

### Three common mistakes

- Treating hypothetical scenario outputs as observed company performance.
- Entering percentages as whole numbers rather than decimals.
- Quoting the headline output without checking assumptions, units, thresholds, and omitted risks.

## 10. Interview Questions

### Beginner: What is the wealth effect?

- **Expected thinking:** Separate wealth from current income.
- **Model answer:** Households may adjust consumption when asset values change because perceived lifetime resources change.
- **Follow-up:** Which assets generate the largest response?
### Intermediate: Why might losses matter more than gains?

- **Expected thinking:** Discuss constraints and precautionary saving.
- **Model answer:** Liquidity constraints, debt, and confidence can make consumption responses asymmetric.
- **Follow-up:** How would you model asymmetry?
### Advanced: How would you estimate MPC?

- **Expected thinking:** Use household panels or quasi-experimental shocks.
- **Model answer:** Segment by wealth composition and liquidity, control for income, and test lagged and nonlinear responses.
- **Follow-up:** What identification problem remains?

## Reproduce

```bash
python -m pip install -e .
python models/wealth_effect/model.py
jupyter lab models/wealth_effect/notebook.ipynb
```

The notebook displays assumptions, scenario results, sensitivity results, and charts. See the repository-level methodology and source catalog for governance and evidence conventions.
