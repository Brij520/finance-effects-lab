# Public Data and Evidence Sources

The authoritative machine-readable catalog is [`../data/source_catalog.csv`](../data/source_catalog.csv). It includes source, URL, access date, relevant metric, transformation, portfolio use, and whether a source enters committed calculations.

## Current release

All committed model inputs are hypothetical. This avoids fabricating company performance and keeps the portfolio reproducible. Public sources are used for:

1. conceptual grounding (Federal Reserve, BIS, IMF);
2. documented case context (Federal Reserve reviews, FCIC, SEC EDGAR);
3. optional future calibration (FRED Treasury yields, real yields, and CPI).

No model claims to reconstruct a company or institution. Annual-report and SEC links identify where an analyst would obtain audited/reported inputs; they do not imply endorsement or use of this repository.

## Reproducing optional FRED downloads

```bash
python data/download_public_data.py
```

The script downloads official CSV endpoints and performs transparent transformations. It does not overwrite model sample inputs. Source files should be retained unchanged if used in future research.

## Recommended extensions

- **Rates:** add Treasury curve tenors and calculate key-rate durations.
- **Banking:** add RBI/Federal Reserve aggregate capital and liquidity series, never confidential exposures.
- **Corporate finance:** use SEC XBRL APIs with issuer, accession number, filing date, and taxonomy mapping documented.
- **Markets:** preserve market-data license restrictions; do not commit data that cannot be redistributed.

## Citation rule

For a chart based on public observations, cite institution, dataset/series, URL, observation window, access date, units, missing-value treatment, and every transformation. A screenshot or finance website without provenance is not an acceptable source.
