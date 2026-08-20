# Data Governance

## What is in this repository

Every `models/<effect>/sample_data.csv` is a **synthetic assumption set** created for this portfolio. The values are round, explicitly hypothetical, and must not be interpreted as actual company, institution, security, or market performance. This design makes every calculation deterministic and reviewable without licensing restrictions.

`source_catalog.csv` records public sources used for research context and possible future calibration. The catalog states the URL, access date, relevant metric, transformation, and whether the source is used in a calculation. The current release does **not** silently mix public observations into hypothetical models.

## Optional public data

`download_public_data.py` reproducibly downloads selected Federal Reserve Economic Data (FRED) CSV series from official St. Louis Fed endpoints:

- `DGS10`: 10-Year Treasury constant-maturity rate;
- `DFII10`: 10-Year Treasury inflation-indexed constant-maturity rate;
- `CPIAUCSL`: Consumer Price Index for All Urban Consumers.

These optional files are inputs for future empirical extensions, **not** inputs to the committed model outputs. Downloaded values remain observations with their native dates; no interpolation is applied. Rates are converted from percentage points to decimals in separate `_decimal` columns; CPI year-over-year inflation is calculated as 12-month percentage change.

```bash
python data/download_public_data.py
```

## Controls

1. Keep raw public observations unchanged.
2. Put transformations in code, never manual spreadsheet edits.
3. Preserve units and observation dates.
4. Record source and access date.
5. Never label model assumptions as reported company values.
6. Review source terms before redistribution or commercial use.
