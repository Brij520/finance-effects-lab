# M&A Accretion/Dilution

> **Area:** Investment banking / M&A<br>
> **Status:** Reproducible numerical model with four scenarios, two-way sensitivity, PNG charts, CSV, and Excel output.

## 1. Concept

### Definition

The model compares an acquirer's standalone EPS with pro forma EPS after adding target earnings, synergies, financing cost, and new shares.

### Financial intuition and why it occurs

A deal can be strategically attractive yet EPS dilutive; accretion is an accounting output driven by price, funding mix, rates, target earnings, and synergies—not proof of value creation.

### Why finance professionals care

This mechanism changes financing capacity, valuation, earnings, stakeholder cash flow, or risk. A professional must understand both the directional intuition and the conditions under which it can reverse.

### Key assumptions

- Inputs in `sample_data.csv` are hypothetical and deliberately round; they are **not actual company data**.
- Currency values use the units in the column/chart label, usually $m; rates are decimals.
- The four scenarios change only listed inputs; they are not probabilities or forecasts.
- Calculations are deterministic so every output can be traced and reproduced.

### Limitations

One-year EPS, no purchase accounting, amortization, step-ups, fees, lost interest, refinancing, integration cost, synergy timing, tax attributes, or deal close timing.

## 2. Mathematical Model

1. **Pro forma net income = Acquirer NI + Target NI + after-tax synergies − after-tax interest**
2. **Pro forma EPS = Pro forma net income ÷ (Acquirer shares + New shares)**
3. **Accretion/(dilution) = Pro forma EPS ÷ Acquirer EPS − 1**

**Variable definitions.** Target NI equals target EPS times target shares; funding check confirms debt plus equity equals purchase price; all amounts are hypothetical $m except per-share data.

**Plain English.** The Python function in [`../../src/finance_effects_lab/effects/ma_accretion_dilution.py`](../../src/finance_effects_lab/effects/ma_accretion_dilution.py) follows the sequence above, exposes intermediate calculations, and returns tabular results rather than hiding logic inside a chart.

## 3. Base Case

### Initial assumptions / inputs

| Input | Base assumption |
|---|---:|
| `acquirer_eps` | 2.5 |
| `acquirer_shares` | 100 |
| `target_eps` | 1.2 |
| `target_shares` | 20 |
| `purchase_price` | 400 |
| `debt_financing` | 240 |
| `equity_financing` | 160 |
| `interest_rate` | 0.06 |
| `tax_rate` | 0.25 |
| `pre_tax_synergies` | 25 |
| `new_shares_issued` | 4 |

### Calculation and output

The acquirer has $2.50 EPS and 100m shares; the target has $1.20 EPS and 20m shares. A $400m purchase uses $240m debt and $160m equity, with 6% debt cost and $25m pre-tax synergies. Run `python models/ma_accretion_dilution/model.py` to refresh the complete calculation. Auditable results are saved in [`outputs/scenario_results.csv`](outputs/scenario_results.csv) and [`outputs/ma_accretion_dilution.xlsx`](outputs/ma_accretion_dilution.xlsx).

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

Purchase price from $300m to $550m against pre-tax synergies from $0m to $50m at 60/40 debt/equity funding. The long-form sensitivity export is Power BI-ready; the chart presents the same grid as an annotated heatmap.

## 6. Visualization

- **Scenario/path chart:** communicates direction, magnitude, units, and case labels.
- **Sensitivity heatmap:** identifies combinations that move the output across zero or a threshold.
- **Source note:** every figure labels results as Finance Effects Lab hypothetical assumptions.

See [`charts/`](charts/) for high-resolution PNG files.

## 7. Real-World Application and Evidence Standard

- **Documented transaction — ExxonMobil / Pioneer:** SEC filings document transaction terms; this model is not a reconstruction. [Primary/public reference](https://www.sec.gov/edgar/browse/?CIK=34088&owner=exclude)
- **Documented transaction — Microsoft / Activision Blizzard:** SEC filings document the transaction; no figures are imported here. [Primary/public reference](https://www.sec.gov/edgar/browse/?CIK=789019&owner=exclude)
- **Illustrative application — Goldman Sachs:** An advisory team would use detailed purchase accounting and financing assumptions. [Primary/public reference](https://www.goldmansachs.com/investor-relations/financials/current/annual-reports)

“Documented” means the linked public source establishes the event, disclosure, or research context. “Illustrative” means the company is only a plausible professional use case. **No public-company performance is simulated, and no claim is made that an organization uses this exact model.** Access date for all links: 20 August 2026.

## 8. Finance Professional Interpretation

- **CFO:** judge financing, integration, and strategic returns beyond headline EPS.
- **Investment banker:** build transparent pro forma EPS and sensitivity cases.
- **Equity analyst:** challenge synergy timing and distinguish accretion from economic value.

## 9. Key Takeaways

### Five key insights

1. The sign and magnitude of the result depend on explicit scenario inputs, not a universal constant.
2. A threshold or denominator can make a seemingly linear driver produce a nonlinear financial outcome.
3. The stress case is most useful when compared with a decision threshold, covenant, risk limit, or required return.
4. Sensitivity analysis is more informative than a single point estimate because major inputs are uncertain.
5. The model output supports judgment; it does not replace accounting policy, legal terms, market data, or due diligence.

### Three formulas to remember

1. **Pro forma net income = Acquirer NI + Target NI + after-tax synergies − after-tax interest**
2. **Pro forma EPS = Pro forma net income ÷ (Acquirer shares + New shares)**
3. **Accretion/(dilution) = Pro forma EPS ÷ Acquirer EPS − 1**

### Three practical applications

- Budgeting, valuation, or transaction scenario design.
- Risk-limit and downside-capacity review.
- Investment memo or finance-interview discussion.

### Three common mistakes

- Treating hypothetical scenario outputs as observed company performance.
- Entering percentages as whole numbers rather than decimals.
- Quoting the headline output without checking assumptions, units, thresholds, and omitted risks.

## 10. Interview Questions

### Beginner: What drives M&A accretion?

- **Expected thinking:** List target earnings, price, financing cost, new shares, tax, and synergies.
- **Model answer:** Pro forma earnings per share rises when incremental after-tax earnings exceed financing and dilution burden.
- **Follow-up:** Can an all-stock deal be accretive?
### Intermediate: Why is accretion not value creation?

- **Expected thinking:** Compare accounting EPS with NPV and return on invested capital.
- **Model answer:** Cheap financing or P/E differences can create EPS accretion even if the premium exceeds synergy value.
- **Follow-up:** What metric would you add?
### Advanced: What does a full model need?

- **Expected thinking:** Cover purchase accounting and timing.
- **Model answer:** Add sources/uses, debt schedule, new shares, target adjustments, amortization, fees, integration costs, synergy ramp, and closing-date weighting.
- **Follow-up:** How would you model circular interest?

## Reproduce

```bash
python -m pip install -e .
python models/ma_accretion_dilution/model.py
jupyter lab models/ma_accretion_dilution/notebook.ipynb
```

The notebook displays assumptions, scenario results, sensitivity results, and charts. See the repository-level methodology and source catalog for governance and evidence conventions.
