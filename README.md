# Plotline

Current events, drawn from the data. A collection of small, self-contained interactive visualizers ("plots"), one folder per plot, published with GitHub Pages.

## Plots

| Plot | Path | Status |
|---|---|---|
| The National Debt | `national-debt/` | live |

## How a plot is built

Each plot is one folder with a static `index.html` that works offline and needs no backend. Where a plot is generated from data, the folder also holds `src/` (template + data) and a `build.py` that writes `index.html`. Nothing is built on the server: commit the built page.

```bash
cd national-debt && python3 build.py
```

The landing page at the repo root lists the plots by hand; add a card when a plot goes live.

## Deploying

Push to `main`. GitHub Pages serves the repo root. A custom domain is a `CNAME` file at the root plus DNS.
