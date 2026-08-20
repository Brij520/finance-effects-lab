# Cash Flow Waterfall

> **Area:** Private equity / project finance<br>
> **Status:** Reproducible numerical model with four scenarios, two-way sensitivity, PNG charts, CSV, and Excel output.

## 1. Concept

### Definition

A contractual sequence allocates operating cash first to taxes and senior claims, then subordinated debt, preferred return, catch-up, carry, and residual equity.

### Financial intuition and why it occurs

Priority, not just total project cash, determines which stakeholder receives value in each scenario.

### Why finance professionals care

This mechanism changes financing capacity, valuation, earnings, stakeholder cash flow, or risk. A professional must understand both the directional intuition and the conditions under which it can reverse.

### Key assumptions

- Inputs in `sample_data.csv` are hypothetical and deliberately round; they are **not actual company data**.
- Currency values use the units in the column/chart label, usually $m; rates are decimals.
- The four scenarios change only listed inputs; they are not probabilities or forecasts.
- Calculations are deterministic so every output can be traced and reproduced.

### Limitations

Single-period distributable cash; no opening arrears, reserve account, PIK toggle, IRR hurdle, European/American waterfall distinction, or clawback.

## 2. Mathematical Model

1. **CFADS = EBITDA − cash taxes**
2. **Debt service = interest paid + scheduled principal paid, subject to available cash**
3. **GP catch-up = LP preferred return × carry ÷ (1 − carry), capped by cash**

**Variable definitions.** CFADS is cash flow available for debt service; LP is limited partner; GP/sponsor receives catch-up and carry after senior tiers.

**Plain English.** The Python function in [`../../src/finance_effects_lab/effects/cash_flow_waterfall.py`](../../src/finance_effects_lab/effects/cash_flow_waterfall.py) follows the sequence above, exposes intermediate calculations, and returns tabular results rather than hiding logic inside a chart.

## 3. Base Case

### Initial assumptions / inputs

| Input | Base assumption |
|---|---:|
| `revenue` | 155 |
| `operating_expenses` | 72 |
| `tax_rate` | 0.25 |
| `senior_debt` | 180 |
| `senior_rate` | 0.07 |
| `scheduled_senior_principal` | 20 |
| `mezzanine_debt` | 40 |
| `mezzanine_rate` | 0.11 |
| `scheduled_mezz_principal` | 5 |
| `lp_contribution` | 100 |
| `preferred_return_rate` | 0.08 |
| `carry_rate` | 0.20 |

### Calculation and output

Base revenue is $155m and opex $72m. Cash pays tax, senior interest/principal, mezzanine interest/principal, an 8% LP preference, sponsor catch-up, then an 80/20 residual split. Run `python models/cash_flow_waterfall/model.py` to refresh the complete calculation. Auditable results are saved in [`outputs/scenario_results.csv`](outputs/scenario_results.csv) and [`outputs/cash_flow_waterfall.xlsx`](outputs/cash_flow_waterfall.xlsx).

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

Revenue from $90m to $150m against carried-interest rates from 10% to 30%. The long-form sensitivity export is Power BI-ready; the chart presents the same grid as an annotated heatmap.

## 6. Visualization

- **Scenario/path chart:** communicates direction, magnitude, units, and case labels.
- **Sensitivity heatmap:** identifies combinations that move the output across zero or a threshold.
- **Source note:** every figure labels results as Finance Effects Lab hypothetical assumptions.

See [`charts/`](charts/) for high-resolution PNG files.

## 7. Real-World Application and Evidence Standard

- **Documented context — Blackstone:** Annual reports disclose incentive-fee and carried-interest economics; this hypothetical waterfall is not a Blackstone fund model. [Primary/public reference](https://ir.blackstone.com/financial-information/annual-reports-and-proxy-statements/default.aspx)
- **Documented context — KKR:** Public reports describe carried interest and fund economics at a high level. [Primary/public reference](https://ir.kkr.com/financial-information/annual-reports)
- **Illustrative application — Apollo:** A deal team could substitute governing-document tiers and asset-level debt terms. [Primary/public reference](https://ir.apollo.com/financials/annual-reports-and-proxies/default.aspx)

“Documented” means the linked public source establishes the event, disclosure, or research context. “Illustrative” means the company is only a plausible professional use case. **No public-company performance is simulated, and no claim is made that an organization uses this exact model.** Access date for all links: 20 August 2026.

## 8. Finance Professional Interpretation

- **CFO:** forecast covenant headroom and distributable cash after debt service.
- **FP&A analyst:** trace operating variance into stakeholder distributions.
- **Investment banker:** structure debt sizing and sponsor returns around payment priority.

## 9. Key Takeaways

### Five key insights

1. The sign and magnitude of the result depend on explicit scenario inputs, not a universal constant.
2. A threshold or denominator can make a seemingly linear driver produce a nonlinear financial outcome.
3. The stress case is most useful when compared with a decision threshold, covenant, risk limit, or required return.
4. Sensitivity analysis is more informative than a single point estimate because major inputs are uncertain.
5. The model output supports judgment; it does not replace accounting policy, legal terms, market data, or due diligence.

### Three formulas to remember

1. **CFADS = EBITDA − cash taxes**
2. **Debt service = interest paid + scheduled principal paid, subject to available cash**
3. **GP catch-up = LP preferred return × carry ÷ (1 − carry), capped by cash**

### Three practical applications

- Budgeting, valuation, or transaction scenario design.
- Risk-limit and downside-capacity review.
- Investment memo or finance-interview discussion.

### Three common mistakes

- Treating hypothetical scenario outputs as observed company performance.
- Entering percentages as whole numbers rather than decimals.
- Quoting the headline output without checking assumptions, units, thresholds, and omitted risks.

## 10. Interview Questions

### Beginner: Why does payment priority matter?

- **Expected thinking:** Separate enterprise cash generation from claimant allocation.
- **Model answer:** Senior claims can be fully paid while junior equity receives nothing; upside reaches junior tiers only after hurdles.
- **Follow-up:** What is cash flow available for debt service?
### Intermediate: What is a GP catch-up?

- **Expected thinking:** Explain how distributions move the GP toward the agreed profit share after LP preference.
- **Model answer:** After the LP preferred tier, a defined share may flow to the GP until cumulative sharing reaches the carry split.
- **Follow-up:** How does a European waterfall differ?
### Advanced: How would you model an IRR hurdle?

- **Expected thinking:** Use dated cash flows and solve tier-by-tier distributions.
- **Model answer:** Accrue the preferred balance by actual dates, allocate cash iteratively, and include clawback/escrow provisions.
- **Follow-up:** How would PIK interest affect the exit waterfall?

## Reproduce

```bash
python -m pip install -e .
python models/cash_flow_waterfall/model.py
jupyter lab models/cash_flow_waterfall/notebook.ipynb
```

The notebook displays assumptions, scenario results, sensitivity results, and charts. See the repository-level methodology and source catalog for governance and evidence conventions.
