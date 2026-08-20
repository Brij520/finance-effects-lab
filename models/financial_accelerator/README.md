# Financial Accelerator Effect

> **Area:** Financial economics / credit<br>
> **Status:** Reproducible numerical model with four scenarios, two-way sensitivity, PNG charts, CSV, and Excel output.

## 1. Concept

### Definition

Changes in borrower net worth alter collateral capacity and the external-finance premium, amplifying an initial economic or asset-price shock.

### Financial intuition and why it occurs

A lower collateral value reduces borrowing capacity precisely when firms may need financing, causing investment to fall by more than the original wealth shock.

### Why finance professionals care

This mechanism changes financing capacity, valuation, earnings, stakeholder cash flow, or risk. A professional must understand both the directional intuition and the conditions under which it can reverse.

### Key assumptions

- Inputs in `sample_data.csv` are hypothetical and deliberately round; they are **not actual company data**.
- Currency values use the units in the column/chart label, usually $m; rates are decimals.
- The four scenarios change only listed inputs; they are not probabilities or forecasts.
- Calculations are deterministic so every output can be traced and reproduced.

### Limitations

Reduced-form one-period relationship; no lender optimization, maturity wall, covenant cure, default option, or general-equilibrium feedback.

## 2. Mathematical Model

1. **Shocked net worth = Initial net worth × (1 + asset-price shock)**
2. **Borrowing capacity = max(0, collateral multiplier × net worth − existing debt)**
3. **Investment = baseline investment + credit sensitivity × borrowing capacity**

**Variable definitions.** The collateral multiplier converts net worth into gross secured capacity; existing debt consumes capacity; credit sensitivity maps available finance to investment.

**Plain English.** The Python function in [`../../src/finance_effects_lab/effects/financial_accelerator.py`](../../src/finance_effects_lab/effects/financial_accelerator.py) follows the sequence above, exposes intermediate calculations, and returns tabular results rather than hiding logic inside a chart.

## 3. Base Case

### Initial assumptions / inputs

| Input | Base assumption |
|---|---:|
| `initial_net_worth` | 50 |
| `asset_price_shock` | 0.00 |
| `collateral_multiplier` | 2.5 |
| `baseline_investment` | 20 |
| `investment_credit_sensitivity` | 0.35 |
| `existing_debt` | 50 |

### Calculation and output

A hypothetical borrower starts with $50m net worth and $50m debt. With 2.5× collateral capacity, available borrowing supports investment; a 20%–40% collateral loss sharply reduces that support. Run `python models/financial_accelerator/model.py` to refresh the complete calculation. Auditable results are saved in [`outputs/scenario_results.csv`](outputs/scenario_results.csv) and [`outputs/financial_accelerator.xlsx`](outputs/financial_accelerator.xlsx).

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

Asset-price shocks from -40% to +20% against collateral multipliers from 1.5× to 3.0×. The long-form sensitivity export is Power BI-ready; the chart presents the same grid as an annotated heatmap.

## 6. Visualization

- **Scenario/path chart:** communicates direction, magnitude, units, and case labels.
- **Sensitivity heatmap:** identifies combinations that move the output across zero or a threshold.
- **Source note:** every figure labels results as Finance Effects Lab hypothetical assumptions.

See [`charts/`](charts/) for high-resolution PNG files.

## 7. Real-World Application and Evidence Standard

- **Documented research — NBER:** Bernanke, Gertler, and Gilchrist formalized balance-sheet amplification; this implementation is deliberately simpler. [Primary/public reference](https://www.nber.org/papers/w6455)
- **Documented context — JPMorgan Chase:** Public credit-risk and allowance disclosures show why borrower quality and collateral matter; no bank data enter the simulation. [Primary/public reference](https://www.jpmorganchase.com/ir/annual-report)
- **Illustrative application — ICICI Bank:** A credit analyst could replace hypothetical inputs with sanctioned exposure and collateral data. [Primary/public reference](https://www.icicibank.com/about-us/annual)

“Documented” means the linked public source establishes the event, disclosure, or research context. “Illustrative” means the company is only a plausible professional use case. **No public-company performance is simulated, and no claim is made that an organization uses this exact model.** Access date for all links: 20 August 2026.

## 8. Finance Professional Interpretation

- **CFO:** protect liquidity before collateral values weaken.
- **FP&A analyst:** link financing availability to capex scenarios.
- **Risk analyst:** stress collateral, borrower net worth, and credit availability jointly.

## 9. Key Takeaways

### Five key insights

1. The sign and magnitude of the result depend on explicit scenario inputs, not a universal constant.
2. A threshold or denominator can make a seemingly linear driver produce a nonlinear financial outcome.
3. The stress case is most useful when compared with a decision threshold, covenant, risk limit, or required return.
4. Sensitivity analysis is more informative than a single point estimate because major inputs are uncertain.
5. The model output supports judgment; it does not replace accounting policy, legal terms, market data, or due diligence.

### Three formulas to remember

1. **Shocked net worth = Initial net worth × (1 + asset-price shock)**
2. **Borrowing capacity = max(0, collateral multiplier × net worth − existing debt)**
3. **Investment = baseline investment + credit sensitivity × borrowing capacity**

### Three practical applications

- Budgeting, valuation, or transaction scenario design.
- Risk-limit and downside-capacity review.
- Investment memo or finance-interview discussion.

### Three common mistakes

- Treating hypothetical scenario outputs as observed company performance.
- Entering percentages as whole numbers rather than decimals.
- Quoting the headline output without checking assumptions, units, thresholds, and omitted risks.

## 10. Interview Questions

### Beginner: What is the accelerator?

- **Expected thinking:** Describe amplification rather than the initial shock.
- **Model answer:** A net-worth loss worsens financing terms and lowers credit-funded activity, making the ultimate output effect larger than the original shock.
- **Follow-up:** What could dampen it?
### Intermediate: Why does collateral matter?

- **Expected thinking:** Connect pledgeable assets to agency costs and loss given default.
- **Model answer:** More collateral lowers lender downside and can increase capacity or reduce the external-finance premium.
- **Follow-up:** How would unsecured borrowers differ?
### Advanced: How would you validate the coefficient?

- **Expected thinking:** Seek panel data and identify exogenous collateral shocks.
- **Model answer:** Estimate investment sensitivity using borrower-level credit and collateral data, control for demand, and test out of sample.
- **Follow-up:** What endogeneity remains?

## Reproduce

```bash
python -m pip install -e .
python models/financial_accelerator/model.py
jupyter lab models/financial_accelerator/notebook.ipynb
```

The notebook displays assumptions, scenario results, sensitivity results, and charts. See the repository-level methodology and source catalog for governance and evidence conventions.
