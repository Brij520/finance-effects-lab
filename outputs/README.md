# Consolidated Outputs

Run `python -m finance_effects_lab` to refresh this directory.

| File | Grain | Intended use |
|---|---|---|
| `model_summary.csv` | One row per effect | Dashboard/model inventory |
| `power_bi_all_scenarios.csv` | One row per effect/scenario (four leverage rows per scenario) | Wide analyst review with all assumptions and outputs |
| `power_bi_all_sensitivities.csv` | One row per sensitivity combination | Wide sensitivity review |
| `power_bi_scenario_metrics_long.csv` | One row per scenario case and numeric field | Tidy Power BI fact table |
| `power_bi_sensitivity_metrics_long.csv` | One row per sensitivity case and numeric field | Tidy Power BI sensitivity fact table |
| `finance_effects_lab.xlsx` | Multiple worksheets | Excel-compatible review package |
| `portfolio_dashboard.html` | One self-contained interactive report | Recruiter/portfolio overview |

## Power BI relationships

Use `effect` as the model key. In long scenario data, `scenario_case_id` uniquely identifies an original model row and `scenario` is the case label. In long sensitivity data, `sensitivity_case_id` preserves the original driver combination. `field` contains an assumption or output name and `value` is numeric.

Metrics are intentionally not forced into a common unit. Model READMEs and chart labels define units; do not sum values across fields or effects. For a production semantic layer, add a field dimension with unit, sign convention, and assumption/output classification.

All values originate from hypothetical assumptions and are not actual company performance.
