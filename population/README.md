# The Population Ledger

Every country's population ledger, births, deaths and net migration, from 1950 to the UN's 2100 projection, drawn on a world map with a year slider.

## How it builds

```
src/fetch.sh      downloads WPP2024 (medium variant, demographic indicators) + world-atlas countries-110m into src/raw/ (git-ignored), then runs assemble.py
src/assemble.py   -> src/data.json (world / regions / subregions / countries; pop, births, deaths, net migration, TFR, median age, life expectancy per year)
                  -> src/geo.json  (TopoJSON decoded to GeoJSON, ids = UN M49 numeric = WPP LocID)
build.py          -> index.html, meta.json, card.json; copies data.json + geo.json beside index.html (the page fetches them at load)
```

Units inside `data.json`: population, births, deaths and migration in thousands; fertility ×100; median age and life expectancy ×10. Nulls where the UN has no value.

Runs weekly from `.github/workflows/refresh.yml`. The UN revises WPP every two years; the page shows the last estimate year (`lastEstimate`) and marks later years as projections.

## Sources

- United Nations, World Population Prospects 2024, medium variant. https://population.un.org/wpp/ (CC BY 3.0 IGO)
- world-atlas 2.0.2 (Natural Earth 110m boundaries). https://github.com/topojson/world-atlas (ISC)

Unmatched geometries (no UN row): Antarctica, French Southern Lands, Northern Cyprus, Somaliland, Kosovo (the UN carries Kosovo as a row but Natural Earth's id for it is not an M49 code).
