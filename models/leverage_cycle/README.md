# Leverage Cycle

> **Area:** Financial economics / collateral<br>
> **Status:** Reproducible numerical model with four scenarios, two-way sensitivity, PNG charts, CSV, and Excel output.

## 1. Concept

### Definition

Leverage expands in rising markets as collateral values increase and haircuts fall, then contracts in falling markets as both mechanisms reverse.

### Financial intuition and why it occurs

Collateral-based debt capacity moves with prices, so lender terms and borrower balance-sheet adjustment reinforce asset cycles.

### Why finance professionals care

This mechanism changes financing capacity, valuation, earnings, stakeholder cash flow, or risk. A professional must understand both the directional intuition and the conditions under which it can reverse.

### Key assumptions

- Inputs in `sample_data.csv` are hypothetical and deliberately round; they are **not actual company data**.
- Currency values use the units in the column/chart label, usually $m; rates are decimals.
- The four scenarios change only listed inputs; they are not probabilities or forecasts.
- Calculations are deterministic so every output can be traced and reproduced.

### Limitations

Constant repeated return, mechanical haircut, no defaults, new equity, lender capital, interest, maturity, fire-sale feedback, or equilibrium price formation.

## 2. Mathematical Model

1. **Dynamic haircut = Base haircut − procyclicality × asset return**
2. **Debt capacity = Collateral value × (1 − haircut)**
3. **Leverage = Collateral value ÷ (Collateral value − Debt)**

**Variable definitions.** Procyclicality translates asset return into haircut movement; debt closes 65% of the gap to capacity each modeled period.

**Plain English.** The Python function in [`../../src/finance_effects_lab/effects/leverage_cycle.py`](../../src/finance_effects_lab/effects/leverage_cycle.py) follows the sequence above, exposes intermediate calculations, and returns tabular results rather than hiding logic inside a chart.

## 3. Base Case

### Initial assumptions / inputs

| Input | Base assumption |
|---|---:|
| `initial_collateral` | 100 |
| `initial_debt` | 70 |
| `asset_return` | 0.02 |
| `haircut` | 0.25 |
| `procyclicality` | 0.60 |
| `periods` | 8 |

### Calculation and output

$100m collateral and $70m debt evolve for eight periods. A 2% return changes collateral, haircut, debt capacity, debt, equity, and leverage sequentially. Run `python models/leverage_cycle/model.py` to refresh the complete calculation. Auditable results are saved in [`outputs/scenario_results.csv`](outputs/scenario_results.csv) and [`outputs/leverage_cycle.xlsx`](outputs/leverage_cycle.xlsx).

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

Periodic asset return from -15% to +15% against procyclicality from 0.2 to 1.0. The long-form sensitivity export is Power BI-ready; the chart presents the same grid as an annotated heatmap.

## 6. Visualization

- **Scenario/path chart:** communicates direction, magnitude, units, and case labels.
- **Sensitivity heatmap:** identifies combinations that move the output across zero or a threshold.
- **Source note:** every figure labels results as Finance Effects Lab hypothetical assumptions.

See [`charts/`](charts/) for high-resolution PNG files.

## 7. Real-World Application and Evidence Standard

- **Documented research — Federal Reserve:** FEDS research on collateralized lending discusses leverage-cycle mechanisms; coefficients here are not taken from the paper. [Primary/public reference](https://www.federalreserve.gov/econres/feds/files/2022052pap.pdf)
- **Documented context — BIS:** BIS credit-cycle research links financing conditions and asset prices. [Primary/public reference](https://www.bis.org/publ/work395.htm)
- **Illustrative application — Goldman Sachs:** A secured-financing desk could calibrate actual collateral haircuts; no firm data are used. [Primary/public reference](https://www.goldmansachs.com/investor-relations/financials/current/annual-reports)

“Documented” means the linked public source establishes the event, disclosure, or research context. “Illustrative” means the company is only a plausible professional use case. **No public-company performance is simulated, and no claim is made that an organization uses this exact model.** Access date for all links: 20 August 2026.

## 8. Finance Professional Interpretation

- **Risk analyst:** stress collateral and haircut jointly.
- **CFO/Treasurer:** preserve borrowing headroom through the cycle.
- **Equity analyst:** recognize when asset growth is financed by procyclical debt capacity.

## 9. Key Takeaways

### Five key insights

1. The sign and magnitude of the result depend on explicit scenario inputs, not a universal constant.
2. A threshold or denominator can make a seemingly linear driver produce a nonlinear financial outcome.
3. The stress case is most useful when compared with a decision threshold, covenant, risk limit, or required return.
4. Sensitivity analysis is more informative than a single point estimate because major inputs are uncertain.
5. The model output supports judgment; it does not replace accounting policy, legal terms, market data, or due diligence.

### Three formulas to remember

1. **Dynamic haircut = Base haircut − procyclicality × asset return**
2. **Debt capacity = Collateral value × (1 − haircut)**
3. **Leverage = Collateral value ÷ (Collateral value − Debt)**

### Three practical applications

- Budgeting, valuation, or transaction scenario design.
- Risk-limit and downside-capacity review.
- Investment memo or finance-interview discussion.

### Three common mistakes

- Treating hypothetical scenario outputs as observed company performance.
- Entering percentages as whole numbers rather than decimals.
- Quoting the headline output without checking assumptions, units, thresholds, and omitted risks.

## 10. Interview Questions

### Beginner: What drives the leverage cycle?

- **Expected thinking:** Trace price, haircut, capacity, and debt.
- **Model answer:** Rising collateral and lower haircuts expand debt capacity; the reverse forces deleveraging in downturns.
- **Follow-up:** How is this different from operating leverage?
### Intermediate: Why include gradual adjustment?

- **Expected thinking:** Real balance sheets cannot instantly move to maximum capacity.
- **Model answer:** The close-rate represents execution, governance, and funding frictions and avoids assuming immediate optimization.
- **Follow-up:** How would a covenant change it?
### Advanced: How would you add equilibrium?

- **Expected thinking:** Introduce borrowers, lenders, and endogenous prices.
- **Model answer:** Let lender capital set haircuts, borrower demand set leverage, and forced sales clear through a price-impact function.
- **Follow-up:** What data identify procyclicality?

## Reproduce

```bash
python -m pip install -e .
python models/leverage_cycle/model.py
jupyter lab models/leverage_cycle/notebook.ipynb
```

The notebook displays assumptions, scenario results, sensitivity results, and charts. See the repository-level methodology and source catalog for governance and evidence conventions.
