# Project Architecture

Finance Effects Lab uses a deliberately small architecture: one Python package, one folder per effect, and shared export/chart helpers. The goal is auditable financial logic—not a web platform.

```text
finance-effects-lab/
├── README.md                      # recruiter-facing portfolio overview
├── LICENSE
├── requirements.txt / environment.yml / pyproject.toml
├── data/
│   ├── README.md                  # governance and units
│   ├── source_catalog.csv         # URL, access date, metric, transformation
│   └── download_public_data.py    # optional reproducible FRED download
├── notebooks/                     # discoverable copies of all 18 notebooks
├── src/finance_effects_lab/
│   ├── common.py                  # validation, chart, CSV, XLSX helpers
│   ├── registry.py                # model metadata
│   ├── runner.py                  # all-model CLI and consolidation
│   ├── dashboard.py               # interactive and static dashboard
│   └── effects/                   # 18 independent numerical modules
├── models/<effect>/
│   ├── README.md                  # concept through interview questions
│   ├── model.py                   # directly runnable wrapper
│   ├── notebook.ipynb             # scenario/sensitivity walkthrough
│   ├── sample_data.csv            # four editable hypothetical scenarios
│   ├── outputs/                   # scenario CSV, sensitivity CSV, XLSX
│   └── charts/                    # scenario/path and sensitivity PNG
├── outputs/                       # consolidated Excel and Power BI CSV
├── charts/                        # portfolio relationship map
├── docs/                          # methodology and career materials
├── scripts/                       # reproducible documentation/notebook tooling
└── tests/                         # formulas, invariants, and all-model smoke tests
```

## Dependency direction

`model.py` and notebooks import `src/finance_effects_lab/effects/<effect>.py`. Effect modules call a small number of functions in `common.py` for I/O and presentation. Financial equations remain in each effect module, making formula review and testing straightforward.

## Data flow

```text
sample_data.csv
    → run_scenarios()
        → auditable pandas DataFrame
            → model CSV (Power BI-ready)
            → model XLSX (Excel-compatible)
            → charts
            → consolidated portfolio outputs
```

Sensitivity functions create long-form tables with one row per assumption combination. Heatmaps pivot only for presentation; the underlying export remains BI-friendly.

## Design decisions

- **No database:** the portfolio is small and file-based reproducibility is clearer.
- **No API/web framework:** the project demonstrates finance, not backend engineering.
- **No hidden spreadsheet formulas:** formulas are versioned Python and covered by tests.
- **No live company-data dependency:** committed runs always reproduce; optional public data are separately governed.
- **One source of financial truth:** notebooks call package functions rather than reimplementing equations.
