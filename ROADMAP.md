# Plotline roadmap

Living list. Ordered roughly by what's next; dated when added. Done items move to the bottom.

## Next

- **Auto-refresh for The National Debt.** Write `national-debt/src/fetch.py` (Treasury Debt to the Penny API, FRED CSVs for GDP, unemployment, CPI, fed funds) so the weekly workflow covers all three plots. *(added 2026-09-20)*
- **The Mamdani Scorecard** (Politics). No prior copy exists on this machine; rebuild from city sources or locate the earlier work. *(2026-09-20)*
- **Custom domain.** `CNAME` at the repo root plus DNS once a domain is chosen; the Plotline name has no clean .com, .io or .news. *(2026-09-20)*

## Later

- **Views and likes, and ordering by them.** An indicator of how often each plot is viewed (and possibly liked), so the landing page can surface the most-viewed plots and offer sorting and filtering by theme, views and publication date. Constraint: the site promises no accounts and no tracking, so counting has to be aggregate and cookie-free (a privacy-preserving counter such as a Cloudflare Worker with KV, or a service like GoatCounter), and likes need the same kind of tiny backend. Decide the counter before building the sort. *(2026-09-20)*
- **Theme map view.** Once there are eight to ten plots, a visual grouping by theme (a map, not a Venn diagram) alongside the card list. *(2026-09-20)*
- **Official leaderboards for the Tests.** Epoch lags official boards by a few weeks; a per-benchmark fetch of the official leaderboard where one is machine-readable (Scale AI for HLE, ARC Prize, swebench.com) would close the gap. *(2026-09-20)*
- **More benchmarks as harder ones arrive.** Adding one is a data edit; see `the-tests/README.md`. *(2026-09-20)*

## Plot ideas, in priority order

Ranked by how sharp the aha is, how clean and self-updating the data is, and how much work the build takes. Reorder freely. *(list started 2026-09-20)*

1. **What a house costs per month** (Economy). The monthly payment on the median house at that month's mortgage rate, from FRED's median sale price, 30-year rate and household income. Aha: the payment roughly doubled 2020 to 2023, a bigger shock than price alone shows. Fully automatic; a live ticker of today's payment. Best next build and the best test of the refresh workflow.
2. **The world's population, two arguments at once** (Culture). Fertility, growth and median age for major developed and developing nations, UN World Population Prospects. Aha: the same dataset supports both the "overpopulation" and the "depopulation" camps, depending on which countries you look at: Japan, Korea and Italy shrinking while Nigeria and Pakistan double; world fertility falling below replacement within decades. Design around a country picker and the crossover from growth to decline per country. UN data refreshes every two years, plus annual estimates.
3. **The Ukraine ledger** (Warfare). Lives and money since February 2022, Ukraine against Russia: confirmed Russian deaths by name (Mediazona and BBC), Ukrainian figures with their stated ranges, and aid by donor from the Kiel Institute's Ukraine Support Tracker. Aha: the scale, and how differently the two sides count. Must show casualty numbers as ranges with sources, never as a single line. Kiel and Mediazona publish downloadable data.
4. **The price of sunlight** (Technology / Economy). Solar cost per watt since 1975 on a log axis beside solar's share of electricity, with batteries following twenty years behind. Aha: a 99 percent cost decline that became an S-curve of adoption, the same shape as The Curve. Our World in Data and the EIA API.
5. **The American exception** (Culture). Life expectancy against health spending per person, the US versus every peer, animated year by year since 1970. Aha: the US peels away from the pack around 1980, spending more and living less, then the overdose and COVID dip the peers never had. World Bank and OECD APIs.
6. **Education: the US against the OECD** (Culture). PISA scores by subject over time, US against the OECD average and the leaders, with NAEP for the finer US trend. Aha: flat for twenty years while spending rose. PISA refreshes only every three years.
7. **The arsenal** (Warfare). Nuclear warheads by country since 1945 from FAS. Aha: 85 percent of the peak stockpile dismantled, and the line just turned upward again, China fastest. Annual.
8. **Who's coming and who's being born** (Politics). US population change split into natural increase and net immigration, with CBO's projection to 2055. Aha: natural increase heads to zero, so immigration is the whole of growth. Census and CBO, annual.
9. **Data centers against every archive before them** (Technology). Size, power and compute of today's AI data centers against libraries, mainframes and early server farms. Aha: the scale jump. Needs a creative common unit (watts, or bits stored) for the historical comparison, which is the design problem to solve first.
10. **Crime in the big cities** (Politics). Rates by type for major US cities over 20 to 30 years, with police per capita, budgets and unemployment alongside. FBI Crime Data Explorer API. Aha depends on the city; must be designed around the 2021 NIBRS reporting change that broke the national series.

## Done

- The Curve rebuilt as a scroll story: Moore opener, the Apollo / Wen Tsing Chow beat, draw, zoom-out, the turn, the AI layers, hand-off to the explorer. *(2026-09-20)*
- Data-driven landing cards (miniature + headline figure from each plot's `card.json`). Ledes on all three plots and the landing intro, from Luyen's own drafts. Landing page, The National Debt, The Curve, How Fast the Tests Fall; design comps reviewed and current design kept; theme colors on cards; Plotline mark and favicon; "Auto-updated" stamps with `meta.json`; weekly refresh workflow for the Epoch-based plots; `PRINCIPLES.md`. *(2026-09-20)*
