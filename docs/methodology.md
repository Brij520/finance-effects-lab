# Methodology and Model Governance

## Objective

Demonstrate financial reasoning by turning 18 effects into traceable numerical models. Each module follows the same research sequence: mechanism → formula → assumptions → base case → scenarios → sensitivity → visualization → professional interpretation → limitations.

## Scenario standard

| Case | Use | Probability? |
|---|---|---|
| Optimistic | Tests upside and favorable financing/market conditions | No |
| Base | Central planning anchor | No |
| Pessimistic | Material deterioration | No |
| Stress | Severe educational reverse stress | No |

Scenarios are not forecasts. No probability-weighted expected value is presented unless a future analyst explicitly supplies defensible probabilities.

## Input standard

- Rates use decimals (`0.06 = 6%`).
- Currency uses the unit printed in each table/chart, usually hypothetical USD millions.
- Bond face values use dollars.
- Wealth examples use hypothetical USD thousands where labeled.
- `scenario` labels must be exactly Optimistic, Base, Pessimistic, and Stress.
- Source modules contain sanity checks for critical ranges; tests cover core formulas and invariants.

## Calculation principles

1. Expose intermediate outputs (interest, tax, debt, equity, contributions) instead of returning only a headline metric.
2. Cap cash payments by available cash when priority matters.
3. Do not recognize tax benefits beyond modeled taxable capacity unless explicitly modeling NOLs.
4. Use full bond repricing as the fixed-income benchmark and show duration approximation error.
5. Label reduced-form feedback models as educational mechanisms rather than prediction engines.
6. Preserve signs: negative dilution means EPS dilution; negative price change means loss.

## Sensitivity design

Each model varies two high-impact inputs while other assumptions remain fixed. Grids include thresholds where possible (zero output, margin breach, accretion/dilution crossover). Long-form CSV—not a formatted spreadsheet—is the canonical sensitivity output.

## Visualization standard

Every chart has a title, axis labels, units, legend when needed, and this source note:

> Source: Finance Effects Lab; hypothetical assumptions, not actual company performance.

Color convention: blue = base/neutral, green = favorable, amber = deterioration, red = stress. Heatmaps use diverging colors but must be read with the color bar because “high” is not beneficial for every metric.

## Evidence standard

- **Documented example:** a primary/public source supports the event, disclosure, or research context.
- **Illustrative example:** an institution is a plausible use case only; no claim is made that it uses this exact model.
- Sample data are synthetic. Public data referenced in documentation are listed in `data/source_catalog.csv` with access date, metric, and transformation.

## Validation

Tests cover:

- known identities (par bond price, Fisher relationship, zero-rate compound value);
- directional behavior (bond price/yield, leverage upside/downside, collateral shock/investment);
- constraints (weights sum to 100%, distributions do not exceed cash);
- stress invariants (more capital cannot increase network defaults in the fixed network);
- all 18 scenario and sensitivity functions.

Run `pytest`. A model change should include a formula test or a financial invariant, not merely a line-coverage assertion.

## Review checklist

Before using a result in an interview or memo:

1. State the unit and timing.
2. Name the two assumptions that drive the result.
3. Explain the mechanism without code.
4. Identify a threshold and the stress result.
5. State at least two omissions.
6. Distinguish accounting accretion from value creation and model output from observed fact.
7. Reconcile CSV, Excel, notebook, and chart outputs after any input change.
