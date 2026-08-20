# Contagion Effect

> **Area:** Systemic risk / network finance<br>
> **Status:** Reproducible numerical model with four scenarios, two-way sensitivity, PNG charts, CSV, and Excel output.

## 1. Concept

### Definition

Losses propagate across connected institutions when a default impairs creditors and newly weakened creditors then fail.

### Financial intuition and why it occurs

The same initial loss can remain contained in a well-capitalized sparse network or cascade through concentrated, low-recovery exposures.

### Why finance professionals care

This mechanism changes financing capacity, valuation, earnings, stakeholder cash flow, or risk. A professional must understand both the directional intuition and the conditions under which it can reverse.

### Key assumptions

- Inputs in `sample_data.csv` are hypothetical and deliberately round; they are **not actual company data**.
- Currency values use the units in the column/chart label, usually $m; rates are decimals.
- The four scenarios change only listed inputs; they are not probabilities or forecasts.
- Calculations are deterministic so every output can be traced and reproduced.

### Limitations

Static known bilateral exposures; no netting, collateral, maturity, liquidity hoarding, central counterparty, endogenous recovery, or behavioral response. Not a prediction engine.

## 2. Mathematical Model

1. **Creditor lossᵢⱼ = Exposureᵢⱼ × (1 − recovery rate)**
2. **Institution i defaults if cumulative lossᵢ ≥ capitalᵢ**
3. **System loss = Σ institution losses**

**Variable definitions.** Exposure i,j is lender i's claim on borrower j; capital is loss-absorbing capacity; recovery is value retained after default.

**Plain English.** The Python function in [`../../src/finance_effects_lab/effects/contagion_effect.py`](../../src/finance_effects_lab/effects/contagion_effect.py) follows the sequence above, exposes intermediate calculations, and returns tabular results rather than hiding logic inside a chart.

## 3. Base Case

### Initial assumptions / inputs

| Input | Base assumption |
|---|---:|
| `shock_node` | 5 |
| `initial_shock_loss` | 6 |
| `recovery_rate` | 0.50 |
| `capital_multiplier` | 1.00 |
| `liquidity_loss_rate` | 0.20 |

### Calculation and output

Six synthetic nodes—two banks, a fund, insurer, company, and market SPV—have explicitly hypothetical exposures. A Market-SPV shock propagates until no new node breaches capital. Run `python models/contagion_effect/model.py` to refresh the complete calculation. Auditable results are saved in [`outputs/scenario_results.csv`](outputs/scenario_results.csv) and [`outputs/contagion_effect.xlsx`](outputs/contagion_effect.xlsx).

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

Recovery rates from 0% to 80% against capital multipliers from 0.5× to 1.5×. The long-form sensitivity export is Power BI-ready; the chart presents the same grid as an annotated heatmap.

## 6. Visualization

- **Scenario/path chart:** communicates direction, magnitude, units, and case labels.
- **Sensitivity heatmap:** identifies combinations that move the output across zero or a threshold.
- **Source note:** every figure labels results as Finance Effects Lab hypothetical assumptions.

See [`charts/`](charts/) for high-resolution PNG files.

## 7. Real-World Application and Evidence Standard

- **Documented case — Lehman Brothers:** The Financial Crisis Inquiry Commission report documents interconnected distress during the financial crisis. [Primary/public reference](https://www.govinfo.gov/app/details/GPO-FCIC)
- **Documented case — AIG:** The same public inquiry provides evidence on counterparty and derivatives linkages. [Primary/public reference](https://www.govinfo.gov/app/details/GPO-FCIC)
- **Illustrative application — JPMorgan Chase:** A bank would use confidential counterparty and collateral data; no JPMorgan exposures are represented. [Primary/public reference](https://www.jpmorganchase.com/ir/annual-report)

“Documented” means the linked public source establishes the event, disclosure, or research context. “Illustrative” means the company is only a plausible professional use case. **No public-company performance is simulated, and no claim is made that an organization uses this exact model.** Access date for all links: 20 August 2026.

## 8. Finance Professional Interpretation

- **Risk analyst:** identify concentrated counterparties and second-round loss paths.
- **Treasurer:** prepare liquidity for indirect network shocks.
- **Regulator/systemic-risk analyst:** stress common exposures and capital jointly.

## 9. Key Takeaways

### Five key insights

1. The sign and magnitude of the result depend on explicit scenario inputs, not a universal constant.
2. A threshold or denominator can make a seemingly linear driver produce a nonlinear financial outcome.
3. The stress case is most useful when compared with a decision threshold, covenant, risk limit, or required return.
4. Sensitivity analysis is more informative than a single point estimate because major inputs are uncertain.
5. The model output supports judgment; it does not replace accounting policy, legal terms, market data, or due diligence.

### Three formulas to remember

1. **Creditor lossᵢⱼ = Exposureᵢⱼ × (1 − recovery rate)**
2. **Institution i defaults if cumulative lossᵢ ≥ capitalᵢ**
3. **System loss = Σ institution losses**

### Three practical applications

- Budgeting, valuation, or transaction scenario design.
- Risk-limit and downside-capacity review.
- Investment memo or finance-interview discussion.

### Three common mistakes

- Treating hypothetical scenario outputs as observed company performance.
- Entering percentages as whole numbers rather than decimals.
- Quoting the headline output without checking assumptions, units, thresholds, and omitted risks.

## 10. Interview Questions

### Beginner: What is financial contagion?

- **Expected thinking:** Describe transmission rather than simultaneous correlation.
- **Model answer:** A loss at one node causes losses at connected nodes, potentially creating further defaults.
- **Follow-up:** How is a common shock different?
### Intermediate: What makes a network fragile?

- **Expected thinking:** Mention concentration, low capital, low recovery, and common holdings.
- **Model answer:** Large exposures to central nodes and thin buffers can turn a local default into a cascade.
- **Follow-up:** Can more connections ever stabilize it?
### Advanced: How would you model real exposures?

- **Expected thinking:** Address netting, collateral, uncertainty, and privacy.
- **Model answer:** Aggregate by legal netting set, model collateral and recovery, infer missing links with ranges, and run reverse stress tests.
- **Follow-up:** How would fire sales enter?

## Reproduce

```bash
python -m pip install -e .
python models/contagion_effect/model.py
jupyter lab models/contagion_effect/notebook.ipynb
```

The notebook displays assumptions, scenario results, sensitivity results, and charts. See the repository-level methodology and source catalog for governance and evidence conventions.
