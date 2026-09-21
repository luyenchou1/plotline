# Plotline roadmap

Living list. Ordered roughly by what's next; dated when added. Done items move to the bottom.

## Next

- **Population drill-down for five to seven countries.** Rather than a deep page for every country, pick the handful that carry the distinct dynamics and give each a full ledger over time: China (peak 2022, one-child overhang), India (the new largest, dividend window), Nigeria (fastest-growing large country), Japan (the frontier of decline), South Korea (lowest fertility on record), the United States (growth on the migration line alone) and Germany or Italy (migration covering, or not covering, the gap). Each gets births / deaths / migration bars per year 1950 to 2100, a fertility line, and an age pyramid that plays through time (needs the WPP population-by-age file, kept only for the chosen countries). Version 2 adds causes of death (WHO Global Health Estimates) and gross in/out migration (OECD) for the same set. Clicking those countries on the map opens the deep page; every other country keeps the hover ledger. *(2026-09-21)*
- **Auto-refresh for The National Debt.** Write `national-debt/src/fetch.py` (Treasury Debt to the Penny API, FRED CSVs for GDP, unemployment, CPI, fed funds) so the weekly workflow covers all three plots. *(added 2026-09-20)*
- **The Mamdani Scorecard** (Politics). No prior copy exists on this machine; rebuild from city sources or locate the earlier work. *(2026-09-20)*
- **Custom domain.** `CNAME` at the repo root plus DNS once a domain is chosen; the Plotline name has no clean .com, .io or .news. *(2026-09-20)*

## Later

- **Report Card, next layer.** State-level NAEP (the API takes a jurisdiction code), spending by state, and the long-term-trend NAEP back to 1971 for the longer view. *(2026-09-21)*
- **Report Card, school-lunch series after 2022.** NCES dropped the lunch-eligibility flag in 2024; watch for whatever income proxy replaces it in the data service. *(2026-09-21)*
- **Views and likes, and ordering by them.** An indicator of how often each plot is viewed (and possibly liked), so the landing page can surface the most-viewed plots and offer sorting and filtering by theme, views and publication date. Constraint: the site promises no accounts and no tracking, so counting has to be aggregate and cookie-free (a privacy-preserving counter such as a Cloudflare Worker with KV, or a service like GoatCounter), and likes need the same kind of tiny backend. Decide the counter before building the sort. *(2026-09-20)*
- **Theme map view.** Once there are eight to ten plots, a visual grouping by theme (a map, not a Venn diagram) alongside the card list. *(2026-09-20)*
- **Official leaderboards for the Tests.** Epoch lags official boards by a few weeks; a per-benchmark fetch of the official leaderboard where one is machine-readable (Scale AI for HLE, ARC Prize, swebench.com) would close the gap. *(2026-09-20)*
- **More benchmarks as harder ones arrive.** Adding one is a data edit; see `the-tests/README.md`. *(2026-09-20)*

## Plot ideas, in priority order

Ranked by how sharp the aha is, how clean and self-updating the data is, and how much work the build takes. Reorder freely. *(list started 2026-09-20)*

1. **What a house costs per month** (Economy). The monthly payment on the median house at that month's mortgage rate, from FRED's median sale price, 30-year rate and household income. Aha: the payment roughly doubled 2020 to 2023, a bigger shock than price alone shows. Fully automatic; a live ticker of today's payment. Best next build and the best test of the refresh workflow.
2. **The Ukraine ledger** (Warfare). Lives and money since February 2022, Ukraine against Russia: confirmed Russian deaths by name (Mediazona and BBC), Ukrainian figures with their stated ranges, and aid by donor from the Kiel Institute's Ukraine Support Tracker. Aha: the scale, and how differently the two sides count. Must show casualty numbers as ranges with sources, never as a single line. Kiel and Mediazona publish downloadable data.
3. **The price of sunlight** (Technology / Economy). Solar cost per watt since 1975 on a log axis beside solar's share of electricity, with batteries following twenty years behind. Aha: a 99 percent cost decline that became an S-curve of adoption, the same shape as The Curve. Our World in Data and the EIA API.
4. **The American exception** (Culture). Life expectancy against health spending per person, the US versus every peer, animated year by year since 1970. Aha: the US peels away from the pack around 1980, spending more and living less, then the overdose and COVID dip the peers never had. World Bank and OECD APIs.
5. **The arsenal** (Warfare). Nuclear warheads by country since 1945 from FAS. Aha: 85 percent of the peak stockpile dismantled, and the line just turned upward again, China fastest. Annual.
6. **Who's coming and who's being born** (Politics). US population change split into natural increase and net immigration, with CBO's projection to 2055. Aha: natural increase heads to zero, so immigration is the whole of growth. Census and CBO, annual.
7. **Data centers against every archive before them** (Technology). Size, power and compute of today's AI data centers against libraries, mainframes and early server farms. Aha: the scale jump. Needs a creative common unit (watts, or bits stored) for the historical comparison, which is the design problem to solve first.
8. **Crime in the big cities** (Politics). Rates by type for major US cities over 20 to 30 years, with police per capita, budgets and unemployment alongside. FBI Crime Data Explorer API. Aha depends on the city; must be designed around the 2021 NIBRS reporting change that broke the national series.

## Done

- The Report Card, "Since the peak" panel: NAEP from 2013 as change in points by percentile, parents' education and school-lunch eligibility, with subject and grade chips; one added milestone, Pew's 2013 smartphone majority, stated as a fact with the caveat in its note. *(2026-09-21)*
- The Report Card: PISA 2025 (published 2026-09-08) wired in from the OECD's own Annex B1 trend tables, all three subjects through 2025, with the OECD's U.S. sampling caveat shown; NAEP proficiency shares; Education theme. *(2026-09-21)*
- The Report Card, first draft: NAEP math and reading (grades 4 and 8, 1990 to 2024) from the Nation's Report Card API, PISA by country with subject chips, hover and pin, and an OECD rank table, spending per pupil in constant dollars from NCES with the OECD per-student comparison, three headline marks, shared milestones (NCLB, Common Core, ESSA, COVID, ARP). *(2026-09-21)*
- The Population Ledger, version 1: world choropleth (Equal Earth, no library) coloured by growth, natural change, net migration, fertility or median age; year slider 1950 to 2100 with play; world ledger for the chosen year; hover / pinned country ledger; both ends of the table. UN WPP 2024 medium variant, refreshed weekly. *(2026-09-21)*
- The Curve rebuilt as a scroll story: Moore opener, the Apollo / Wen Tsing Chow beat, draw, zoom-out, the turn, the AI layers, hand-off to the explorer. *(2026-09-20)*
- Data-driven landing cards (miniature + headline figure from each plot's `card.json`). Ledes on all three plots and the landing intro, from Luyen's own drafts. Landing page, The National Debt, The Curve, How Fast the Tests Fall; design comps reviewed and current design kept; theme colors on cards; Plotline mark and favicon; "Auto-updated" stamps with `meta.json`; weekly refresh workflow for the Epoch-based plots; `PRINCIPLES.md`. *(2026-09-20)*
