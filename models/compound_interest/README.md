# Compound Interest Effect

> **Area:** Investments / time value of money<br>
> **Status:** Reproducible numerical model with four scenarios, two-way sensitivity, PNG charts, CSV, and Excel output.

## 1. Concept

### Definition

Returns earn subsequent returns, causing wealth to grow exponentially rather than linearly when gains remain invested.

### Financial intuition and why it occurs

Time and return interact multiplicatively; recurring contributions made earlier also receive more compounding periods.

### Why finance professionals care

This mechanism changes financing capacity, valuation, earnings, stakeholder cash flow, or risk. A professional must understand both the directional intuition and the conditions under which it can reverse.

### Key assumptions

- Inputs in `sample_data.csv` are hypothetical and deliberately round; they are **not actual company data**.
- Currency values use the units in the column/chart label, usually $m; rates are decimals.
- The four scenarios change only listed inputs; they are not probabilities or forecasts.
- Calculations are deterministic so every output can be traced and reproduced.

### Limitations

Constant deterministic return, end-of-period contributions, no volatility drag, fees, tax, inflation, withdrawals, sequence risk, or contribution growth.

## 2. Mathematical Model

1. **Principal FV = Principal × (1 + r/m)^(m×years)**
2. **Contribution FV = Payment × ((1 + r/m)^n − 1) ÷ (r/m)**
3. **Effective annual rate = (1 + r/m)^m − 1**

**Variable definitions.** r is nominal annual return, m is compounds per year, n is total periods, and payment is end-of-period contribution.

**Plain English.** The Python function in [`../../src/finance_effects_lab/effects/compound_interest.py`](../../src/finance_effects_lab/effects/compound_interest.py) follows the sequence above, exposes intermediate calculations, and returns tabular results rather than hiding logic inside a chart.

## 3. Base Case

### Initial assumptions / inputs

| Input | Base assumption |
|---|---:|
| `principal` | 10000 |
| `annual_rate` | 0.07 |
| `years` | 20 |
| `compounds_per_year` | 12 |
| `annual_contribution` | 2000 |

### Calculation and output

A $10,000 starting balance receives $2,000 annual contributions for 20 years, allocated monthly, under 0%, 4%, 7%, and 10% return scenarios. Run `python models/compound_interest/model.py` to refresh the complete calculation. Auditable results are saved in [`outputs/scenario_results.csv`](outputs/scenario_results.csv) and [`outputs/compound_interest.xlsx`](outputs/compound_interest.xlsx).

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

Years from 5 to 30 against annual returns from 2% to 10%. The long-form sensitivity export is Power BI-ready; the chart presents the same grid as an annotated heatmap.

## 6. Visualization

- **Scenario/path chart:** communicates direction, magnitude, units, and case labels.
- **Sensitivity heatmap:** identifies combinations that move the output across zero or a threshold.
- **Source note:** every figure labels results as Finance Effects Lab hypothetical assumptions.

See [`charts/`](charts/) for high-resolution PNG files.

## 7. Real-World Application and Evidence Standard

- **Documented context — Berkshire Hathaway:** Shareholder letters discuss long-term compounding; the modeled returns are not Berkshire forecasts. [Primary/public reference](https://www.berkshirehathaway.com/letters/letters.html)
- **Illustrative application — BlackRock:** An investment calculator could use product-specific fees and return ranges. [Primary/public reference](https://ir.blackrock.com/financials/annual-reports-and-proxy)
- **Illustrative application — HDFC Bank:** A savings product illustration could apply contractual rates and cash-flow timing. [Primary/public reference](https://www.hdfcbank.com/personal/about-us/investor-relations/annual-reports)

“Documented” means the linked public source establishes the event, disclosure, or research context. “Illustrative” means the company is only a plausible professional use case. **No public-company performance is simulated, and no claim is made that an organization uses this exact model.** Access date for all links: 20 August 2026.

## 8. Finance Professional Interpretation

- **FP&A analyst:** discount or compound multi-year plan cash flows consistently.
- **Investment analyst:** separate contributions from investment growth.
- **CFO/Treasurer:** compare effective annual funding and investment rates.

## 9. Key Takeaways

### Five key insights

1. The sign and magnitude of the result depend on explicit scenario inputs, not a universal constant.
2. A threshold or denominator can make a seemingly linear driver produce a nonlinear financial outcome.
3. The stress case is most useful when compared with a decision threshold, covenant, risk limit, or required return.
4. Sensitivity analysis is more informative than a single point estimate because major inputs are uncertain.
5. The model output supports judgment; it does not replace accounting policy, legal terms, market data, or due diligence.

### Three formulas to remember

1. **Principal FV = Principal × (1 + r/m)^(m×years)**
2. **Contribution FV = Payment × ((1 + r/m)^n − 1) ÷ (r/m)**
3. **Effective annual rate = (1 + r/m)^m − 1**

### Three practical applications

- Budgeting, valuation, or transaction scenario design.
- Risk-limit and downside-capacity review.
- Investment memo or finance-interview discussion.

### Three common mistakes

- Treating hypothetical scenario outputs as observed company performance.
- Entering percentages as whole numbers rather than decimals.
- Quoting the headline output without checking assumptions, units, thresholds, and omitted risks.

## 10. Interview Questions

### Beginner: What is compounding?

- **Expected thinking:** Contrast interest on principal with interest on accumulated returns.
- **Model answer:** Reinvested gains enlarge the balance that earns the next period's return.
- **Follow-up:** How does simple interest differ?
### Intermediate: Why does frequency matter?

- **Expected thinking:** Convert nominal rate to periodic rate and exponent.
- **Model answer:** More frequent compounding raises effective annual return for a fixed positive nominal rate, though the gain diminishes.
- **Follow-up:** What is continuous compounding?
### Advanced: How does volatility change realized compounding?

- **Expected thinking:** Use geometric versus arithmetic return.
- **Model answer:** For volatile returns, geometric growth is below the arithmetic average; sequence also matters with external cash flows.
- **Follow-up:** How would fees enter?

## Reproduce

```bash
python -m pip install -e .
python models/compound_interest/model.py
jupyter lab models/compound_interest/notebook.ipynb
```

The notebook displays assumptions, scenario results, sensitivity results, and charts. See the repository-level methodology and source catalog for governance and evidence conventions.
