# Fisher Effect

> **Area:** Financial economics / macro rates<br>
> **Status:** Reproducible numerical model with four scenarios, two-way sensitivity, PNG charts, CSV, and Excel output.

## 1. Concept

### Definition

Nominal interest rates reflect real required returns and expected inflation, with an interaction term in the exact relationship.

### Financial intuition and why it occurs

A lender cares about purchasing power: higher expected inflation generally requires a higher nominal rate to preserve a given real return.

### Why finance professionals care

This mechanism changes financing capacity, valuation, earnings, stakeholder cash flow, or risk. A professional must understand both the directional intuition and the conditions under which it can reverse.

### Key assumptions

- Inputs in `sample_data.csv` are hypothetical and deliberately round; they are **not actual company data**.
- Currency values use the units in the column/chart label, usually $m; rates are decimals.
- The four scenarios change only listed inputs; they are not probabilities or forecasts.
- Calculations are deterministic so every output can be traced and reproduced.

### Limitations

Static ex-ante identity, no risk premium, tax, term premium, liquidity premium, inflation uncertainty, or distinction between expected and realized holding-period returns.

## 2. Mathematical Model

1. **1 + nominal rate = (1 + real rate) × (1 + expected inflation)**
2. **Exact real rate = (1 + nominal) ÷ (1 + expected inflation) − 1**
3. **Approximate real rate ≈ nominal rate − expected inflation**

**Variable definitions.** Expected—not realized—inflation belongs in the ex-ante relationship; approximation error is the omitted interaction term.

**Plain English.** The Python function in [`../../src/finance_effects_lab/effects/fisher_effect.py`](../../src/finance_effects_lab/effects/fisher_effect.py) follows the sequence above, exposes intermediate calculations, and returns tabular results rather than hiding logic inside a chart.

## 3. Base Case

### Initial assumptions / inputs

| Input | Base assumption |
|---|---:|
| `nominal_rate` | 0.06 |
| `expected_inflation` | 0.03 |

### Calculation and output

At a 6% nominal rate and 3% expected inflation, the model calculates exact and approximate real rates, then stresses inflation to 9%. Run `python models/fisher_effect/model.py` to refresh the complete calculation. Auditable results are saved in [`outputs/scenario_results.csv`](outputs/scenario_results.csv) and [`outputs/fisher_effect.xlsx`](outputs/fisher_effect.xlsx).

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

Nominal rates from 2% to 12% against expected inflation from 0% to 10%. The long-form sensitivity export is Power BI-ready; the chart presents the same grid as an annotated heatmap.

## 6. Visualization

- **Scenario/path chart:** communicates direction, magnitude, units, and case labels.
- **Sensitivity heatmap:** identifies combinations that move the output across zero or a threshold.
- **Source note:** every figure labels results as Finance Effects Lab hypothetical assumptions.

See [`charts/`](charts/) for high-resolution PNG files.

## 7. Real-World Application and Evidence Standard

- **Documented data — Federal Reserve / FRED:** Nominal Treasury and inflation-indexed yields support market-based real-rate analysis; no live data are embedded in the base case. [Primary/public reference](https://fred.stlouisfed.org/series/DFII10)
- **Documented context — Reserve Bank of India:** Policy publications discuss inflation and interest-rate conditions. [Primary/public reference](https://www.rbi.org.in/Scripts/AnnualReportPublications.aspx)
- **Illustrative application — HDFC Bank:** A treasury analyst could use scenario inflation and instrument-specific rates; no bank forecast is implied. [Primary/public reference](https://www.hdfcbank.com/personal/about-us/investor-relations/annual-reports)

“Documented” means the linked public source establishes the event, disclosure, or research context. “Illustrative” means the company is only a plausible professional use case. **No public-company performance is simulated, and no claim is made that an organization uses this exact model.** Access date for all links: 20 August 2026.

## 8. Finance Professional Interpretation

- **CFO/Treasurer:** compare nominal borrowing cost with expected real burden.
- **Equity analyst:** separate inflation compensation from changes in real discount rates.
- **Risk analyst:** stress expected inflation, real rates, and risk premia separately.

## 9. Key Takeaways

### Five key insights

1. The sign and magnitude of the result depend on explicit scenario inputs, not a universal constant.
2. A threshold or denominator can make a seemingly linear driver produce a nonlinear financial outcome.
3. The stress case is most useful when compared with a decision threshold, covenant, risk limit, or required return.
4. Sensitivity analysis is more informative than a single point estimate because major inputs are uncertain.
5. The model output supports judgment; it does not replace accounting policy, legal terms, market data, or due diligence.

### Three formulas to remember

1. **1 + nominal rate = (1 + real rate) × (1 + expected inflation)**
2. **Exact real rate = (1 + nominal) ÷ (1 + expected inflation) − 1**
3. **Approximate real rate ≈ nominal rate − expected inflation**

### Three practical applications

- Budgeting, valuation, or transaction scenario design.
- Risk-limit and downside-capacity review.
- Investment memo or finance-interview discussion.

### Three common mistakes

- Treating hypothetical scenario outputs as observed company performance.
- Entering percentages as whole numbers rather than decimals.
- Quoting the headline output without checking assumptions, units, thresholds, and omitted risks.

## 10. Interview Questions

### Beginner: State the Fisher relationship.

- **Expected thinking:** Use gross rates for the exact identity.
- **Model answer:** One plus nominal equals one plus real times one plus expected inflation.
- **Follow-up:** When is subtraction adequate?
### Intermediate: Can the real rate be negative?

- **Expected thinking:** Compare nominal with inflation using the exact formula.
- **Model answer:** Yes; if expected inflation exceeds nominal yield, the ex-ante real rate is negative.
- **Follow-up:** What about realized real return?
### Advanced: Why can nominal yields move more than inflation expectations?

- **Expected thinking:** Decompose term and risk premia.
- **Model answer:** Yields also contain real-rate, term-premium, liquidity, tax, and credit components, so Fisher is not a complete pricing model.
- **Follow-up:** How would you infer expected inflation?

## Reproduce

```bash
python -m pip install -e .
python models/fisher_effect/model.py
jupyter lab models/fisher_effect/notebook.ipynb
```

The notebook displays assumptions, scenario results, sensitivity results, and charts. See the repository-level methodology and source catalog for governance and evidence conventions.
