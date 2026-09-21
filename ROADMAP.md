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

## Done

- The Curve rebuilt as a scroll story: Moore opener, the Apollo / Wen Tsing Chow beat, draw, zoom-out, the turn, the AI layers, hand-off to the explorer. *(2026-09-20)*
- Data-driven landing cards (miniature + headline figure from each plot's `card.json`). Ledes on all three plots and the landing intro, from Luyen's own drafts. Landing page, The National Debt, The Curve, How Fast the Tests Fall; design comps reviewed and current design kept; theme colors on cards; Plotline mark and favicon; "Auto-updated" stamps with `meta.json`; weekly refresh workflow for the Epoch-based plots; `PRINCIPLES.md`. *(2026-09-20)*
