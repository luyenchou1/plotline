# The National Debt

Single-file interactive visualizer of U.S. federal debt (Treasury "Debt to the Penny", daily since April 1993) with nominal GDP, debt-to-GDP, and monthly unemployment, CPI inflation and fed funds comparison panels.

- `src/template.html` — page source (markup, CSS, JS) with a `/*__DATA__*/` placeholder
- `src/data.json` — extracted source data (daily debt, monthly indicators, events)
- `src/gdp.csv` — nominal GDP from FRED (`https://fred.stlouisfed.org/graph/fredgraph.csv?id=GDP`)
- `src/us-federal-debt.csv` — the raw daily CSV
- `build.py` — builds `index.html` (the published page) and `artifact.html` (claude.ai artifact build, no download button)

```bash
python3 build.py
```

To refresh: replace the arrays in `src/data.json` (same shapes), re-download `src/gdp.csv`, and rebuild.
