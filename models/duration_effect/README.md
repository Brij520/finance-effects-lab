# Duration Effect

> **Area:** Fixed income risk<br>
> **Status:** Reproducible numerical model with four scenarios, two-way sensitivity, PNG charts, CSV, and Excel output.

## 1. Concept

### Definition

Modified duration approximates a bond's percentage price sensitivity to a small yield change; convexity improves the estimate for larger moves.

### Financial intuition and why it occurs

Duration is a PV-weighted timing measure: lower coupons and longer maturities defer value and generally increase rate sensitivity.

### Why finance professionals care

This mechanism changes financing capacity, valuation, earnings, stakeholder cash flow, or risk. A professional must understand both the directional intuition and the conditions under which it can reverse.

### Key assumptions

- Inputs in `sample_data.csv` are hypothetical and deliberately round; they are **not actual company data**.
- Currency values use the units in the column/chart label, usually $m; rates are decimals.
- The four scenarios change only listed inputs; they are not probabilities or forecasts.
- Calculations are deterministic so every output can be traced and reproduced.

### Limitations

Yield-to-maturity framework assumes fixed cash flows; it is insufficient for callable securities, mortgage prepayments, credit spread changes, and curve twists.

## 2. Mathematical Model

1. **Macaulay duration = Σ(t × PV(CFₜ)) ÷ Price**
2. **Modified duration = Macaulay duration ÷ (1 + y/m)**
3. **ΔP/P ≈ −Modified duration × Δy + ½ × Convexity × (Δy)²**

**Variable definitions.** t is payment time; y is yield; m is coupon frequency; convexity captures curvature of the price-yield function.

**Plain English.** The Python function in [`../../src/finance_effects_lab/effects/duration_effect.py`](../../src/finance_effects_lab/effects/duration_effect.py) follows the sequence above, exposes intermediate calculations, and returns tabular results rather than hiding logic inside a chart.

## 3. Base Case

### Initial assumptions / inputs

| Input | Base assumption |
|---|---:|
| `face_value` | 1000 |
| `coupon_rate` | 0.04 |
| `yield_rate` | 0.05 |
| `maturity_years` | 10 |
| `yield_shift` | 0.00 |
| `frequency` | 2 |

### Calculation and output

The model computes exact price, Macaulay duration, modified duration, and convexity for a 10-year 4% bond yielding 5%, then compares approximation with full repricing. Run `python models/duration_effect/model.py` to refresh the complete calculation. Auditable results are saved in [`outputs/scenario_results.csv`](outputs/scenario_results.csv) and [`outputs/duration_effect.xlsx`](outputs/duration_effect.xlsx).

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

Coupons from 2% to 8% against maturities from 2 to 30 years; all cells show modified duration. The long-form sensitivity export is Power BI-ready; the chart presents the same grid as an annotated heatmap.

## 6. Visualization

- **Scenario/path chart:** communicates direction, magnitude, units, and case labels.
- **Sensitivity heatmap:** identifies combinations that move the output across zero or a threshold.
- **Source note:** every figure labels results as Finance Effects Lab hypothetical assumptions.

See [`charts/`](charts/) for high-resolution PNG files.

## 7. Real-World Application and Evidence Standard

- **Documented case — Silicon Valley Bank:** The Federal Reserve review discusses interest-rate and liquidity risk-management weaknesses; this is not a reconstruction of SVB's portfolio. [Primary/public reference](https://www.federalreserve.gov/publications/review-of-the-federal-reserves-supervision-and-regulation-of-silicon-valley-bank.htm)
- **Documented context — BlackRock:** Fixed-income portfolios disclose rate risk in public reporting. [Primary/public reference](https://ir.blackrock.com/financials/annual-reports-and-proxy)
- **Illustrative application — SBI:** A bank treasury could map actual holdings into duration buckets. [Primary/public reference](https://sbi.co.in/web/investor-relations/annual-report)

“Documented” means the linked public source establishes the event, disclosure, or research context. “Illustrative” means the company is only a plausible professional use case. **No public-company performance is simulated, and no claim is made that an organization uses this exact model.** Access date for all links: 20 August 2026.

## 8. Finance Professional Interpretation

- **Treasurer:** align asset and liability duration within risk appetite.
- **Portfolio manager:** size rate hedges and express curve views.
- **Risk analyst:** monitor DV01, key-rate duration, convexity, and stress loss.

## 9. Key Takeaways

### Five key insights

1. The sign and magnitude of the result depend on explicit scenario inputs, not a universal constant.
2. A threshold or denominator can make a seemingly linear driver produce a nonlinear financial outcome.
3. The stress case is most useful when compared with a decision threshold, covenant, risk limit, or required return.
4. Sensitivity analysis is more informative than a single point estimate because major inputs are uncertain.
5. The model output supports judgment; it does not replace accounting policy, legal terms, market data, or due diligence.

### Three formulas to remember

1. **Macaulay duration = Σ(t × PV(CFₜ)) ÷ Price**
2. **Modified duration = Macaulay duration ÷ (1 + y/m)**
3. **ΔP/P ≈ −Modified duration × Δy + ½ × Convexity × (Δy)²**

### Three practical applications

- Budgeting, valuation, or transaction scenario design.
- Risk-limit and downside-capacity review.
- Investment memo or finance-interview discussion.

### Three common mistakes

- Treating hypothetical scenario outputs as observed company performance.
- Entering percentages as whole numbers rather than decimals.
- Quoting the headline output without checking assumptions, units, thresholds, and omitted risks.

## 10. Interview Questions

### Beginner: What does modified duration mean?

- **Expected thinking:** Give a percentage-price interpretation with sign.
- **Model answer:** A modified duration of 7 implies roughly a 7% price decline for a 100 bp yield rise, before convexity.
- **Follow-up:** When is that approximation poor?
### Intermediate: Why do low-coupon bonds have longer duration?

- **Expected thinking:** Locate more PV in principal.
- **Model answer:** Less value arrives through early coupons, so the PV-weighted average payment time is later.
- **Follow-up:** Can duration exceed maturity?
### Advanced: Duration matched—are you hedged?

- **Expected thinking:** Discuss curve and convexity mismatch.
- **Model answer:** Not necessarily: equal aggregate duration can hide key-rate, spread, basis, optionality, and convexity differences.
- **Follow-up:** How would you test a twist?

## Reproduce

```bash
python -m pip install -e .
python models/duration_effect/model.py
jupyter lab models/duration_effect/notebook.ipynb
```

The notebook displays assumptions, scenario results, sensitivity results, and charts. See the repository-level methodology and source catalog for governance and evidence conventions.
