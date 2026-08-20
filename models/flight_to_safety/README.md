# Flight-to-Safety Effect

> **Area:** Asset allocation / market stress<br>
> **Status:** Reproducible numerical model with four scenarios, two-way sensitivity, PNG charts, CSV, and Excel output.

## 1. Concept

### Definition

Investors reallocate from risky or illiquid assets toward instruments perceived as safer or more liquid during stress.

### Financial intuition and why it occurs

Risk tolerance falls and balance-sheet constraints tighten, producing safe-asset inflows, risky-asset outflows, and wider relative returns or spreads.

### Why finance professionals care

This mechanism changes financing capacity, valuation, earnings, stakeholder cash flow, or risk. A professional must understand both the directional intuition and the conditions under which it can reverse.

### Key assumptions

- Inputs in `sample_data.csv` are hypothetical and deliberately round; they are **not actual company data**.
- Currency values use the units in the column/chart label, usually $m; rates are decimals.
- The four scenarios change only listed inputs; they are not probabilities or forecasts.
- Calculations are deterministic so every output can be traced and reproduced.

### Limitations

Two asset buckets, linear and immediate impact, no yield/price conversion, FX, central-bank action, collateral convenience yield, or reversal dynamics.

## 2. Mathematical Model

1. **Flow to safe = Portfolio value × risk-aversion shock × reallocation sensitivity**
2. **Safe return impact = Flow ÷ Safe-market depth**
3. **Risky return impact = −Flow ÷ Risky-market depth**

**Variable definitions.** Market depth is a reduced-form dollar scale translating flow into price return; it is not trading volume.

**Plain English.** The Python function in [`../../src/finance_effects_lab/effects/flight_to_safety.py`](../../src/finance_effects_lab/effects/flight_to_safety.py) follows the sequence above, exposes intermediate calculations, and returns tabular results rather than hiding logic inside a chart.

## 3. Base Case

### Initial assumptions / inputs

| Input | Base assumption |
|---|---:|
| `portfolio_value` | 100 |
| `initial_safe_weight` | 0.30 |
| `risk_aversion_shock` | 0.05 |
| `reallocation_sensitivity` | 0.80 |
| `safe_market_depth` | 1200 |
| `risky_market_depth` | 900 |

### Calculation and output

A $100m allocation starts 30% safe. A 5% risk-aversion shock reallocates assets according to 0.8 sensitivity, bounded by risky holdings. Run `python models/flight_to_safety/model.py` to refresh the complete calculation. Auditable results are saved in [`outputs/scenario_results.csv`](outputs/scenario_results.csv) and [`outputs/flight_to_safety.xlsx`](outputs/flight_to_safety.xlsx).

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

Risk-aversion shock from 0% to 25% against safe-market depth from $500m to $2,000m. The long-form sensitivity export is Power BI-ready; the chart presents the same grid as an annotated heatmap.

## 6. Visualization

- **Scenario/path chart:** communicates direction, magnitude, units, and case labels.
- **Sensitivity heatmap:** identifies combinations that move the output across zero or a threshold.
- **Source note:** every figure labels results as Finance Effects Lab hypothetical assumptions.

See [`charts/`](charts/) for high-resolution PNG files.

## 7. Real-World Application and Evidence Standard

- **Documented context — Federal Reserve:** Financial Stability Reports discuss safe-asset demand and market liquidity in stress. [Primary/public reference](https://www.federalreserve.gov/publications/financial-stability-report.htm)
- **Documented context — BIS:** BIS publications analyze safe-haven flows and dollar funding conditions. [Primary/public reference](https://www.bis.org/publ/qtrpdf/r_qt2009.htm)
- **Illustrative application — BlackRock:** A portfolio team could replace depth assumptions with asset-specific execution estimates. [Primary/public reference](https://ir.blackrock.com/financials/annual-reports-and-proxy)

“Documented” means the linked public source establishes the event, disclosure, or research context. “Illustrative” means the company is only a plausible professional use case. **No public-company performance is simulated, and no claim is made that an organization uses this exact model.** Access date for all links: 20 August 2026.

## 8. Finance Professional Interpretation

- **Portfolio manager:** pre-plan liquidity and safe-asset capacity before stress.
- **Risk analyst:** stress correlations, depth, and crowding simultaneously.
- **CFO/Treasurer:** understand how flight-to-safety changes funding spreads and investment values.

## 9. Key Takeaways

### Five key insights

1. The sign and magnitude of the result depend on explicit scenario inputs, not a universal constant.
2. A threshold or denominator can make a seemingly linear driver produce a nonlinear financial outcome.
3. The stress case is most useful when compared with a decision threshold, covenant, risk limit, or required return.
4. Sensitivity analysis is more informative than a single point estimate because major inputs are uncertain.
5. The model output supports judgment; it does not replace accounting policy, legal terms, market data, or due diligence.

### Three formulas to remember

1. **Flow to safe = Portfolio value × risk-aversion shock × reallocation sensitivity**
2. **Safe return impact = Flow ÷ Safe-market depth**
3. **Risky return impact = −Flow ÷ Risky-market depth**

### Three practical applications

- Budgeting, valuation, or transaction scenario design.
- Risk-limit and downside-capacity review.
- Investment memo or finance-interview discussion.

### Three common mistakes

- Treating hypothetical scenario outputs as observed company performance.
- Entering percentages as whole numbers rather than decimals.
- Quoting the headline output without checking assumptions, units, thresholds, and omitted risks.

## 10. Interview Questions

### Beginner: What is flight to safety?

- **Expected thinking:** Describe allocation and relative pricing.
- **Model answer:** Investors shift toward perceived safety/liquidity, often supporting safe assets while pressuring risky ones.
- **Follow-up:** Is cash always safe?
### Intermediate: Why does market depth matter?

- **Expected thinking:** Connect a fixed flow to impact.
- **Model answer:** The same dollar flow moves prices more in a shallow market than a deep one.
- **Follow-up:** Can the safest market become illiquid?
### Advanced: How would you distinguish safety from liquidity?

- **Expected thinking:** Use multiple instruments and event data.
- **Model answer:** Compare credit-risk-free but less liquid assets with liquid but risky assets and decompose spread changes.
- **Follow-up:** What role does collateral demand play?

## Reproduce

```bash
python -m pip install -e .
python models/flight_to_safety/model.py
jupyter lab models/flight_to_safety/notebook.ipynb
```

The notebook displays assumptions, scenario results, sensitivity results, and charts. See the repository-level methodology and source catalog for governance and evidence conventions.
