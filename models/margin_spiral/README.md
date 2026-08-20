# Margin Spiral

> **Area:** Counterparty and market risk<br>
> **Status:** Reproducible numerical model with four scenarios, two-way sensitivity, PNG charts, CSV, and Excel output.

## 1. Concept

### Definition

Rising volatility or haircuts reduces debt capacity, forcing deleveraging that can lower asset values and trigger still higher margin needs.

### Financial intuition and why it occurs

Risk-sensitive financing terms are procyclical: secured funding is abundant in calm markets but contracts when measured risk rises.

### Why finance professionals care

This mechanism changes financing capacity, valuation, earnings, stakeholder cash flow, or risk. A professional must understand both the directional intuition and the conditions under which it can reverse.

### Key assumptions

- Inputs in `sample_data.csv` are hypothetical and deliberately round; they are **not actual company data**.
- Currency values use the units in the column/chart label, usually $m; rates are decimals.
- The four scenarios change only listed inputs; they are not probabilities or forecasts.
- Calculations are deterministic so every output can be traced and reproduced.

### Limitations

Haircut rule is illustrative; real agreements use asset-specific schedules, variation margin, netting, collateral substitution, and intraday calls.

## 2. Mathematical Model

1. **Haircut = base haircut + sensitivity × volatility shock × round**
2. **Maximum debt = Asset value × (1 − haircut)**
3. **Forced sale = max(0, Debt − Maximum debt)**

**Variable definitions.** Haircut is borrower equity required against collateral; price impact is the incremental loss per dollar sold.

**Plain English.** The Python function in [`../../src/finance_effects_lab/effects/margin_spiral.py`](../../src/finance_effects_lab/effects/margin_spiral.py) follows the sequence above, exposes intermediate calculations, and returns tabular results rather than hiding logic inside a chart.

## 3. Base Case

### Initial assumptions / inputs

| Input | Base assumption |
|---|---:|
| `initial_assets` | 100 |
| `debt` | 75 |
| `initial_haircut` | 0.20 |
| `volatility_shock` | 0.06 |
| `haircut_sensitivity` | 0.30 |
| `price_impact` | 0.10 |

### Calculation and output

A $100m portfolio with $75m debt, a 20% initial haircut, and a 6% volatility shock recalculates debt capacity over sequential margin rounds. Run `python models/margin_spiral/model.py` to refresh the complete calculation. Auditable results are saved in [`outputs/scenario_results.csv`](outputs/scenario_results.csv) and [`outputs/margin_spiral.xlsx`](outputs/margin_spiral.xlsx).

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

Volatility shocks from 2% to 20% against sale-price impact from 5% to 50%. The long-form sensitivity export is Power BI-ready; the chart presents the same grid as an annotated heatmap.

## 6. Visualization

- **Scenario/path chart:** communicates direction, magnitude, units, and case labels.
- **Sensitivity heatmap:** identifies combinations that move the output across zero or a threshold.
- **Source note:** every figure labels results as Finance Effects Lab hypothetical assumptions.

See [`charts/`](charts/) for high-resolution PNG files.

## 7. Real-World Application and Evidence Standard

- **Documented case — Credit Suisse / Archegos:** The Federal Reserve enforcement release describes counterparty risk-management deficiencies related to Archegos. [Primary/public reference](https://www.federalreserve.gov/newsevents/pressreleases/enforcement20230724a.htm)
- **Documented context — BIS:** BIS work on margining during stress provides institutional context. [Primary/public reference](https://www.bis.org/bcbs/publ/d537.htm)
- **Illustrative application — Goldman Sachs:** A prime broker could apply client-level financing terms; this model uses no Goldman Sachs data. [Primary/public reference](https://www.goldmansachs.com/investor-relations/financials/current/annual-reports)

“Documented” means the linked public source establishes the event, disclosure, or research context. “Illustrative” means the company is only a plausible professional use case. **No public-company performance is simulated, and no claim is made that an organization uses this exact model.** Access date for all links: 20 August 2026.

## 8. Finance Professional Interpretation

- **CFO/Treasurer:** monitor collateral calls and unencumbered assets.
- **Risk analyst:** stress haircut migration together with gap risk and concentration.
- **Investment banker:** assess financing resilience where transaction funding relies on pledged securities.

## 9. Key Takeaways

### Five key insights

1. The sign and magnitude of the result depend on explicit scenario inputs, not a universal constant.
2. A threshold or denominator can make a seemingly linear driver produce a nonlinear financial outcome.
3. The stress case is most useful when compared with a decision threshold, covenant, risk limit, or required return.
4. Sensitivity analysis is more informative than a single point estimate because major inputs are uncertain.
5. The model output supports judgment; it does not replace accounting policy, legal terms, market data, or due diligence.

### Three formulas to remember

1. **Haircut = base haircut + sensitivity × volatility shock × round**
2. **Maximum debt = Asset value × (1 − haircut)**
3. **Forced sale = max(0, Debt − Maximum debt)**

### Three practical applications

- Budgeting, valuation, or transaction scenario design.
- Risk-limit and downside-capacity review.
- Investment memo or finance-interview discussion.

### Three common mistakes

- Treating hypothetical scenario outputs as observed company performance.
- Entering percentages as whole numbers rather than decimals.
- Quoting the headline output without checking assumptions, units, thresholds, and omitted risks.

## 10. Interview Questions

### Beginner: How is a margin spiral different from an ordinary loss?

- **Expected thinking:** Emphasize endogenous financing terms.
- **Model answer:** The initial loss raises required collateral or haircut, forcing balance-sheet action that creates additional losses.
- **Follow-up:** How is variation margin different from initial margin?
### Intermediate: Why are haircuts procyclical?

- **Expected thinking:** Connect measured volatility and lender risk limits.
- **Model answer:** Volatility and correlation rise in stress, so lenders demand more protection just as borrower equity falls.
- **Follow-up:** What policy can reduce procyclicality?
### Advanced: What would a prime-broker model add?

- **Expected thinking:** Mention netting sets, wrong-way risk, liquidity horizon, and concentration.
- **Model answer:** Model legal-netting sets, collateral eligibility, intraday variation margin, liquidation horizon, and correlated client defaults.
- **Follow-up:** How would you test gap risk?

## Reproduce

```bash
python -m pip install -e .
python models/margin_spiral/model.py
jupyter lab models/margin_spiral/notebook.ipynb
```

The notebook displays assumptions, scenario results, sensitivity results, and charts. See the repository-level methodology and source catalog for governance and evidence conventions.
