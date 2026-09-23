# Plotline view counter

A Cloudflare Worker with one Durable Object (SQLite) that counts page views per plot. No cookies, no login, nothing stored about a visitor: daily uniques come from a salted hash of IP, browser string and date that is never written in raw form and is discarded after 90 days. Visitors with Do Not Track on are not counted. Only pages served from github.io report, so local previews do not.

- Worker: `plotline-counter` on the account's workers.dev subdomain, deployed with `npx wrangler deploy` from this folder.
- Each page posts `{p: plot, r: referrer host}` to `/hit` on load (snippet at the foot of every template and the landing page).
- Statistics are private: `./stats.sh` prints totals, the last 14 days of views and visitors, referrers and countries. It reads the key from `~/.config/plotline/counter.key`, which is also set as the Worker secret `STATS_KEY`.
