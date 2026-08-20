# Liquidity Spiral

> **Area:** Market risk / funding liquidity<br>
> **Status:** Reproducible numerical model with four scenarios, two-way sensitivity, PNG charts, CSV, and Excel output.

## 1. Concept

### Definition

A price decline tightens funding constraints, forces asset sales, and causes further market-price declines through price impact.

### Financial intuition and why it occurs

A levered holder must sell into a thin market to restore margin; the sale itself lowers prices and can create another margin breach.

### Why finance professionals care

This mechanism changes financing capacity, valuation, earnings, stakeholder cash flow, or risk. A professional must understand both the directional intuition and the conditions under which it can reverse.

### Key assumptions

- Inputs in `sample_data.csv` are hypothetical and deliberately round; they are **not actual company data**.
- Currency values use the units in the column/chart label, usually $m; rates are decimals.
- The four scenarios change only listed inputs; they are not probabilities or forecasts.
- Calculations are deterministic so every output can be traced and reproduced.

### Limitations

Linear impact, one representative holder, no order-book recovery, hedges, new capital, cross-asset liquidation, or strategic counterparties. It is not a prediction engine.

## 2. Mathematical Model

1. **Equity = Marked asset value − Debt**
2. **Margin ratio = Equity ÷ Marked asset value**
3. **Price impact = Forced units ÷ (Initial units × market-liquidity parameter)**

**Variable definitions.** Leverage fixes initial equity; required margin is minimum equity/assets; market liquidity scales the price response to forced sales.

**Plain English.** The Python function in [`../../src/finance_effects_lab/effects/liquidity_spiral.py`](../../src/finance_effects_lab/effects/liquidity_spiral.py) follows the sequence above, exposes intermediate calculations, and returns tabular results rather than hiding logic inside a chart.

## 3. Base Case

### Initial assumptions / inputs

| Input | Base assumption |
|---|---:|
| `initial_assets` | 100 |
| `leverage` | 3 |
| `initial_shock` | 0.05 |
| `margin_requirement` | 0.25 |
| `market_liquidity` | 1.00 |

### Calculation and output

A $100m position financed at 3× leverage absorbs a 5% shock. The model solves required sales, applies linear price impact, repays debt with proceeds, and repeats until compliant or exhausted. Run `python models/liquidity_spiral/model.py` to refresh the complete calculation. Auditable results are saved in [`outputs/scenario_results.csv`](outputs/scenario_results.csv) and [`outputs/liquidity_spiral.xlsx`](outputs/liquidity_spiral.xlsx).

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

Initial shocks from 2% to 20% against leverage from 2× to 6×. The long-form sensitivity export is Power BI-ready; the chart presents the same grid as an annotated heatmap.

## 6. Visualization

- **Scenario/path chart:** communicates direction, magnitude, units, and case labels.
- **Sensitivity heatmap:** identifies combinations that move the output across zero or a threshold.
- **Source note:** every figure labels results as Finance Effects Lab hypothetical assumptions.

See [`charts/`](charts/) for high-resolution PNG files.

## 7. Real-World Application and Evidence Standard

- **Documented context — Federal Reserve:** The Financial Stability Report discusses interactions among leverage, funding risk, and market liquidity. [Primary/public reference](https://www.federalreserve.gov/publications/financial-stability-report.htm)
- **Documented context — BIS:** BIS research documents margining practices and liquidity demand during stress. [Primary/public reference](https://www.bis.org/bcbs/publ/d537.htm)
- **Illustrative application — BlackRock:** An asset manager could use position-level liquidity and financing terms; no BlackRock positions are modeled. [Primary/public reference](https://ir.blackrock.com/financials/annual-reports-and-proxy)

“Documented” means the linked public source establishes the event, disclosure, or research context. “Illustrative” means the company is only a plausible professional use case. **No public-company performance is simulated, and no claim is made that an organization uses this exact model.** Access date for all links: 20 August 2026.

## 8. Finance Professional Interpretation

- **Treasurer:** hold enough liquidity to avoid selling into impaired markets.
- **Risk analyst:** combine funding and market-liquidity stresses instead of shocking them independently.
- **Portfolio manager:** size leverage using liquidation cost, not only ex-ante volatility.

## 9. Key Takeaways

### Five key insights

1. The sign and magnitude of the result depend on explicit scenario inputs, not a universal constant.
2. A threshold or denominator can make a seemingly linear driver produce a nonlinear financial outcome.
3. The stress case is most useful when compared with a decision threshold, covenant, risk limit, or required return.
4. Sensitivity analysis is more informative than a single point estimate because major inputs are uncertain.
5. The model output supports judgment; it does not replace accounting policy, legal terms, market data, or due diligence.

### Three formulas to remember

1. **Equity = Marked asset value − Debt**
2. **Margin ratio = Equity ÷ Marked asset value**
3. **Price impact = Forced units ÷ (Initial units × market-liquidity parameter)**

### Three practical applications

- Budgeting, valuation, or transaction scenario design.
- Risk-limit and downside-capacity review.
- Investment memo or finance-interview discussion.

### Three common mistakes

- Treating hypothetical scenario outputs as observed company performance.
- Entering percentages as whole numbers rather than decimals.
- Quoting the headline output without checking assumptions, units, thresholds, and omitted risks.

## 10. Interview Questions

### Beginner: What creates the feedback loop?

- **Expected thinking:** Trace price, margin, sale, and price impact in order.
- **Model answer:** Losses reduce margin equity, the holder sells to comply, and market impact causes another loss.
- **Follow-up:** When does the loop stop?
### Intermediate: Why can a small shock become nonlinear?

- **Expected thinking:** Identify the constraint threshold and thin-market impact.
- **Model answer:** Nothing is sold before the threshold; once breached, forced volume and impact can jump discontinuously.
- **Follow-up:** How would central clearing affect it?
### Advanced: How would you calibrate liquidity?

- **Expected thinking:** Use observed depth, bid-ask spreads, and stressed liquidation data.
- **Model answer:** Estimate impact by asset and horizon, then validate against historical stress windows without treating history as a hard bound.
- **Follow-up:** How would you model multiple funds?

## Reproduce

```bash
python -m pip install -e .
python models/liquidity_spiral/model.py
jupyter lab models/liquidity_spiral/notebook.ipynb
```

The notebook displays assumptions, scenario results, sensitivity results, and charts. See the repository-level methodology and source catalog for governance and evidence conventions.
