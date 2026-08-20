# Interest Rate Effect

> **Area:** Fixed income / treasury<br>
> **Status:** Reproducible numerical model with four scenarios, two-way sensitivity, PNG charts, CSV, and Excel output.

## 1. Concept

### Definition

A bond's present value changes inversely with its discount yield because fixed cash flows are discounted at the new market rate.

### Financial intuition and why it occurs

When required yield rises, the same coupons and principal are worth less today; longer-dated cash flows usually move more.

### Why finance professionals care

This mechanism changes financing capacity, valuation, earnings, stakeholder cash flow, or risk. A professional must understand both the directional intuition and the conditions under which it can reverse.

### Key assumptions

- Inputs in `sample_data.csv` are hypothetical and deliberately round; they are **not actual company data**.
- Currency values use the units in the column/chart label, usually $m; rates are decimals.
- The four scenarios change only listed inputs; they are not probabilities or forecasts.
- Calculations are deterministic so every output can be traced and reproduced.

### Limitations

Parallel deterministic shifts; no spread movement, optionality, default, tax, liquidity premium, reinvestment risk, or curve-key-rate exposure.

## 2. Mathematical Model

1. **Bond price = Σ CFₜ ÷ (1 + y/m)^(m×t)**
2. **Coupon per period = Face value × coupon rate ÷ m**
3. **Price change % = Shocked price ÷ Initial price − 1**

**Variable definitions.** CF is coupon or principal cash flow; y is yield to maturity; m is payments per year; t is time in years.

**Plain English.** The Python function in [`../../src/finance_effects_lab/effects/interest_rate_effect.py`](../../src/finance_effects_lab/effects/interest_rate_effect.py) follows the sequence above, exposes intermediate calculations, and returns tabular results rather than hiding logic inside a chart.

## 3. Base Case

### Initial assumptions / inputs

| Input | Base assumption |
|---|---:|
| `face_value` | 1000 |
| `coupon_rate` | 0.05 |
| `base_yield` | 0.05 |
| `maturity_years` | 10 |
| `yield_shift` | 0.00 |
| `frequency` | 2 |

### Calculation and output

A $1,000 face, 5% coupon, 10-year semiannual bond is priced at a 5% yield and fully repriced at -2%, 0%, +1%, and +2% parallel shifts. Run `python models/interest_rate_effect/model.py` to refresh the complete calculation. Auditable results are saved in [`outputs/scenario_results.csv`](outputs/scenario_results.csv) and [`outputs/interest_rate_effect.xlsx`](outputs/interest_rate_effect.xlsx).

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

Maturity from 2 to 30 years against yield shifts from -2% to +2%. The long-form sensitivity export is Power BI-ready; the chart presents the same grid as an annotated heatmap.

## 6. Visualization

- **Scenario/path chart:** communicates direction, magnitude, units, and case labels.
- **Sensitivity heatmap:** identifies combinations that move the output across zero or a threshold.
- **Source note:** every figure labels results as Finance Effects Lab hypothetical assumptions.

See [`charts/`](charts/) for high-resolution PNG files.

## 7. Real-World Application and Evidence Standard

- **Documented context — JPMorgan Chase:** Annual reports disclose interest-rate risk and earnings/value sensitivity; this model is an independent bond example. [Primary/public reference](https://www.jpmorganchase.com/ir/annual-report)
- **Documented context — BlackRock:** Public reports discuss investment portfolios and market risk without providing inputs to this simulation. [Primary/public reference](https://ir.blackrock.com/financials/annual-reports-and-proxy)
- **Illustrative application — HDFC Bank:** A treasury analyst could reprice an actual securities book using instrument-level cash flows. [Primary/public reference](https://www.hdfcbank.com/personal/about-us/investor-relations/annual-reports)

“Documented” means the linked public source establishes the event, disclosure, or research context. “Illustrative” means the company is only a plausible professional use case. **No public-company performance is simulated, and no claim is made that an organization uses this exact model.** Access date for all links: 20 August 2026.

## 8. Finance Professional Interpretation

- **CFO/Treasurer:** measure debt and investment exposure to rate scenarios.
- **Equity analyst:** translate rate moves into funding cost and securities valuation.
- **Risk analyst:** supplement parallel shocks with curve, spread, and optionality stress.

## 9. Key Takeaways

### Five key insights

1. The sign and magnitude of the result depend on explicit scenario inputs, not a universal constant.
2. A threshold or denominator can make a seemingly linear driver produce a nonlinear financial outcome.
3. The stress case is most useful when compared with a decision threshold, covenant, risk limit, or required return.
4. Sensitivity analysis is more informative than a single point estimate because major inputs are uncertain.
5. The model output supports judgment; it does not replace accounting policy, legal terms, market data, or due diligence.

### Three formulas to remember

1. **Bond price = Σ CFₜ ÷ (1 + y/m)^(m×t)**
2. **Coupon per period = Face value × coupon rate ÷ m**
3. **Price change % = Shocked price ÷ Initial price − 1**

### Three practical applications

- Budgeting, valuation, or transaction scenario design.
- Risk-limit and downside-capacity review.
- Investment memo or finance-interview discussion.

### Three common mistakes

- Treating hypothetical scenario outputs as observed company performance.
- Entering percentages as whole numbers rather than decimals.
- Quoting the headline output without checking assumptions, units, thresholds, and omitted risks.

## 10. Interview Questions

### Beginner: Why do bond prices fall when yields rise?

- **Expected thinking:** Use discounted cash flow.
- **Model answer:** A higher required return increases discount factors, reducing the present value of fixed contractual cash flows.
- **Follow-up:** Which cash flow is most sensitive?
### Intermediate: Why is the response nonlinear?

- **Expected thinking:** Discuss convexity.
- **Model answer:** The price-yield curve is curved, so equal up/down yield moves produce asymmetric price changes.
- **Follow-up:** When can convexity be negative?
### Advanced: How would you hedge a portfolio?

- **Expected thinking:** Move from full repricing to duration and key-rate exposures.
- **Model answer:** Match DV01 or key-rate durations with swaps/futures, then test basis, convexity, and nonparallel shifts.
- **Follow-up:** What risk remains after a DV01 hedge?

## Reproduce

```bash
python -m pip install -e .
python models/interest_rate_effect/model.py
jupyter lab models/interest_rate_effect/notebook.ipynb
```

The notebook displays assumptions, scenario results, sensitivity results, and charts. See the repository-level methodology and source catalog for governance and evidence conventions.
