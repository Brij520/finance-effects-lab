# Leverage Effect

> **Area:** Corporate finance / capital structure<br>
> **Status:** Reproducible numerical model with four scenarios, two-way sensitivity, PNG charts, CSV, and Excel output.

## 1. Concept

### Definition

Debt financing concentrates operating gains and losses into a smaller equity base after contractual interest expense.

### Financial intuition and why it occurs

When return on assets exceeds the after-tax cost of debt, leverage lifts ROE; when operating return falls below financing cost, the same fixed claim accelerates equity losses.

### Why finance professionals care

This mechanism changes financing capacity, valuation, earnings, stakeholder cash flow, or risk. A professional must understand both the directional intuition and the conditions under which it can reverse.

### Key assumptions

- Inputs in `sample_data.csv` are hypothetical and deliberately round; they are **not actual company data**.
- Currency values use the units in the column/chart label, usually $m; rates are decimals.
- The four scenarios change only listed inputs; they are not probabilities or forecasts.
- Calculations are deterministic so every output can be traced and reproduced.

### Limitations

One-period book-value model; no distress costs, covenants, refinancing, tax-loss carryforwards, or endogenous interest spread.

## 2. Mathematical Model

1. **Interest = Debt × interest rate**
2. **Net income = (EBIT − Interest) × (1 − tax rate), when pre-tax income is positive**
3. **ROE = Net income ÷ (Assets − Debt)**

**Variable definitions.** EBIT is operating profit; Debt is interest-bearing borrowing; tax rate is the modeled cash tax rate; ROE is return on book equity.

**Plain English.** The Python function in [`../../src/finance_effects_lab/effects/leverage_effect.py`](../../src/finance_effects_lab/effects/leverage_effect.py) follows the sequence above, exposes intermediate calculations, and returns tabular results rather than hiding logic inside a chart.

## 3. Base Case

### Initial assumptions / inputs

| Input | Base assumption |
|---|---:|
| `assets` | 100 |
| `return_on_assets` | 0.10 |
| `interest_rate` | 0.06 |
| `tax_rate` | 0.25 |

### Calculation and output

At $100m of assets, 10% ROA, 6% debt cost, and 25% tax, compare 0%, 25%, 50%, and 75% debt/assets. The smaller equity denominator raises base-case ROE, but the stress loss becomes progressively worse. Run `python models/leverage_effect/model.py` to refresh the complete calculation. Auditable results are saved in [`outputs/scenario_results.csv`](outputs/scenario_results.csv) and [`outputs/leverage_effect.xlsx`](outputs/leverage_effect.xlsx).

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

ROA from -8% to 16% against debt/assets of 0%, 25%, 50%, and 75%. The long-form sensitivity export is Power BI-ready; the chart presents the same grid as an annotated heatmap.

## 6. Visualization

- **Scenario/path chart:** communicates direction, magnitude, units, and case labels.
- **Sensitivity heatmap:** identifies combinations that move the output across zero or a threshold.
- **Source note:** every figure labels results as Finance Effects Lab hypothetical assumptions.

See [`charts/`](charts/) for high-resolution PNG files.

## 7. Real-World Application and Evidence Standard

- **Documented context — Berkshire Hathaway:** Annual reports disclose operating earnings, debt, and capital allocation; the model does not substitute those values. [Primary/public reference](https://www.berkshirehathaway.com/reports.html)
- **Documented context — Amazon:** SEC filings provide debt and interest disclosures useful for an analyst-built leverage bridge. [Primary/public reference](https://www.sec.gov/edgar/browse/?CIK=1018724&owner=exclude)
- **Illustrative application — KKR:** A buyout underwriting team could use this framework with deal-specific debt schedules; no KKR data are used. [Primary/public reference](https://ir.kkr.com/financial-information/annual-reports)

“Documented” means the linked public source establishes the event, disclosure, or research context. “Illustrative” means the company is only a plausible professional use case. **No public-company performance is simulated, and no claim is made that an organization uses this exact model.** Access date for all links: 20 August 2026.

## 8. Finance Professional Interpretation

- **CFO:** compare financing capacity with downside interest coverage and ROE volatility.
- **FP&A analyst:** bridge operating plan changes through interest, tax, net income, and ROE.
- **Equity analyst:** separate operating improvement from financial leverage in peer ROE.

## 9. Key Takeaways

### Five key insights

1. The sign and magnitude of the result depend on explicit scenario inputs, not a universal constant.
2. A threshold or denominator can make a seemingly linear driver produce a nonlinear financial outcome.
3. The stress case is most useful when compared with a decision threshold, covenant, risk limit, or required return.
4. Sensitivity analysis is more informative than a single point estimate because major inputs are uncertain.
5. The model output supports judgment; it does not replace accounting policy, legal terms, market data, or due diligence.

### Three formulas to remember

1. **Interest = Debt × interest rate**
2. **Net income = (EBIT − Interest) × (1 − tax rate), when pre-tax income is positive**
3. **ROE = Net income ÷ (Assets − Debt)**

### Three practical applications

- Budgeting, valuation, or transaction scenario design.
- Risk-limit and downside-capacity review.
- Investment memo or finance-interview discussion.

### Three common mistakes

- Treating hypothetical scenario outputs as observed company performance.
- Entering percentages as whole numbers rather than decimals.
- Quoting the headline output without checking assumptions, units, thresholds, and omitted risks.

## 10. Interview Questions

### Beginner: Why can leverage increase ROE?

- **Expected thinking:** Compare ROA with debt cost and focus on the equity denominator.
- **Model answer:** Debt is accretive to ROE when the incremental after-tax operating return exceeds the financing burden; it also makes negative outcomes larger.
- **Follow-up:** Would your answer change when EBIT is negative?
### Intermediate: At what operating return does leverage stop helping?

- **Expected thinking:** Set levered ROE equal to unlevered ROE and solve for the break-even return.
- **Model answer:** In the simplified pre-tax model, the crossover is near the cost of debt; taxes, loss treatment, and changing spreads alter it.
- **Follow-up:** How would a floating-rate loan change the sensitivity?
### Advanced: How would you extend this for an LBO?

- **Expected thinking:** Add time, mandatory amortization, cash sweeps, changing rates, exit value, and IRR/MOIC.
- **Model answer:** Build a multi-period debt schedule linked to cash flow and covenant tests, then solve sponsor returns across exit scenarios.
- **Follow-up:** Which covenant would bind first in the stress case?

## Reproduce

```bash
python -m pip install -e .
python models/leverage_effect/model.py
jupyter lab models/leverage_effect/notebook.ipynb
```

The notebook displays assumptions, scenario results, sensitivity results, and charts. See the repository-level methodology and source catalog for governance and evidence conventions.
