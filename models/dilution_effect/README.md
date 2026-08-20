# Dilution Effect

> **Area:** Equity capital markets<br>
> **Status:** Reproducible numerical model with four scenarios, two-way sensitivity, PNG charts, CSV, and Excel output.

## 1. Concept

### Definition

Issuing new shares reduces existing owners' percentage ownership and can reduce EPS unless proceeds generate enough incremental income.

### Financial intuition and why it occurs

The earnings pie may grow after an issuance, but it is divided among more shares; accretion requires the return on proceeds to clear the earnings yield implied by the issue economics.

### Why finance professionals care

This mechanism changes financing capacity, valuation, earnings, stakeholder cash flow, or risk. A professional must understand both the directional intuition and the conditions under which it can reverse.

### Key assumptions

- Inputs in `sample_data.csv` are hypothetical and deliberately round; they are **not actual company data**.
- Currency values use the units in the column/chart label, usually $m; rates are decimals.
- The four scenarios change only listed inputs; they are not probabilities or forecasts.
- Calculations are deterministic so every output can be traced and reproduced.

### Limitations

No fees, taxes, issue discount dynamics, option dilution, buybacks, time-weighted shares, signaling, debt reduction, or multi-year deployment.

## 2. Mathematical Model

1. **Pro forma shares = Existing shares + New shares**
2. **Pro forma EPS = (Net income + Proceeds × return on proceeds) ÷ Pro forma shares**
3. **EPS dilution % = Pro forma EPS ÷ Existing EPS − 1**

**Variable definitions.** Issue price times new shares equals gross proceeds; return on proceeds is first-year after-tax income yield in this simplified model.

**Plain English.** The Python function in [`../../src/finance_effects_lab/effects/dilution_effect.py`](../../src/finance_effects_lab/effects/dilution_effect.py) follows the sequence above, exposes intermediate calculations, and returns tabular results rather than hiding logic inside a chart.

## 3. Base Case

### Initial assumptions / inputs

| Input | Base assumption |
|---|---:|
| `net_income` | 100 |
| `existing_shares` | 100 |
| `new_shares` | 20 |
| `issue_price` | 20 |
| `return_on_proceeds` | 0.04 |

### Calculation and output

A company earns $100m on 100m shares and issues 20m shares at $20. At a 4% first-year return on proceeds, the model compares old/new EPS and ownership. Run `python models/dilution_effect/model.py` to refresh the complete calculation. Auditable results are saved in [`outputs/scenario_results.csv`](outputs/scenario_results.csv) and [`outputs/dilution_effect.xlsx`](outputs/dilution_effect.xlsx).

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

New shares from 0m to 50m against return on proceeds from 0% to 8%. The long-form sensitivity export is Power BI-ready; the chart presents the same grid as an annotated heatmap.

## 6. Visualization

- **Scenario/path chart:** communicates direction, magnitude, units, and case labels.
- **Sensitivity heatmap:** identifies combinations that move the output across zero or a threshold.
- **Source note:** every figure labels results as Finance Effects Lab hypothetical assumptions.

See [`charts/`](charts/) for high-resolution PNG files.

## 7. Real-World Application and Evidence Standard

- **Documented context — Tesla:** SEC filings document historical equity offerings; this model does not reproduce any specific offering. [Primary/public reference](https://www.sec.gov/edgar/browse/?CIK=1318605&owner=exclude)
- **Documented context — AMC Entertainment:** SEC filings provide issuance and share-count disclosures for independent analysis. [Primary/public reference](https://www.sec.gov/edgar/browse/?CIK=1411579&owner=exclude)
- **Illustrative application — Amazon:** An ECM analyst could model a hypothetical issuance; no announced Amazon transaction is implied. [Primary/public reference](https://www.sec.gov/edgar/browse/?CIK=1018724&owner=exclude)

“Documented” means the linked public source establishes the event, disclosure, or research context. “Illustrative” means the company is only a plausible professional use case. **No public-company performance is simulated, and no claim is made that an organization uses this exact model.** Access date for all links: 20 August 2026.

## 8. Finance Professional Interpretation

- **CFO:** weigh dilution against liquidity, leverage reduction, and growth returns.
- **Investment banker:** size issuance and communicate EPS/ownership effects.
- **Equity analyst:** separate mechanical dilution from value created with proceeds.

## 9. Key Takeaways

### Five key insights

1. The sign and magnitude of the result depend on explicit scenario inputs, not a universal constant.
2. A threshold or denominator can make a seemingly linear driver produce a nonlinear financial outcome.
3. The stress case is most useful when compared with a decision threshold, covenant, risk limit, or required return.
4. Sensitivity analysis is more informative than a single point estimate because major inputs are uncertain.
5. The model output supports judgment; it does not replace accounting policy, legal terms, market data, or due diligence.

### Three formulas to remember

1. **Pro forma shares = Existing shares + New shares**
2. **Pro forma EPS = (Net income + Proceeds × return on proceeds) ÷ Pro forma shares**
3. **EPS dilution % = Pro forma EPS ÷ Existing EPS − 1**

### Three practical applications

- Budgeting, valuation, or transaction scenario design.
- Risk-limit and downside-capacity review.
- Investment memo or finance-interview discussion.

### Three common mistakes

- Treating hypothetical scenario outputs as observed company performance.
- Entering percentages as whole numbers rather than decimals.
- Quoting the headline output without checking assumptions, units, thresholds, and omitted risks.

## 10. Interview Questions

### Beginner: What is share dilution?

- **Expected thinking:** Distinguish ownership and EPS dilution.
- **Model answer:** New shares lower an existing holder's percentage; EPS also falls unless incremental earnings offset the larger denominator.
- **Follow-up:** Can ownership dilute while EPS rises?
### Intermediate: What is the EPS break-even return?

- **Expected thinking:** Set new EPS equal to old EPS.
- **Model answer:** Incremental net income must equal existing EPS times new shares; divide by proceeds to get the required yield.
- **Follow-up:** How does issue price affect it?
### Advanced: How would you model options and convertibles?

- **Expected thinking:** Use treasury-stock and if-converted methods plus timing.
- **Model answer:** Build basic and diluted weighted-average shares, apply anti-dilution rules, and scenario conversion economics.
- **Follow-up:** How do buybacks interact?

## Reproduce

```bash
python -m pip install -e .
python models/dilution_effect/model.py
jupyter lab models/dilution_effect/notebook.ipynb
```

The notebook displays assumptions, scenario results, sensitivity results, and charts. See the repository-level methodology and source catalog for governance and evidence conventions.
