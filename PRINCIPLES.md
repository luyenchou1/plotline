# Plotline principles

A living record of the design principles and patterns we settle on while building the site. Add to it whenever a decision is made in conversation; date the additions. The site is Luyen's, so the principles are written as his, with the patterns that follow from them.

## What the site is for

- Plotline is an expression of one person's curiosity about understanding the world through data. It should read as that, warm and first-person, and never as a cold journalistic resource. *(2026-09-20)*
- Each entry is a **plot**, never a "story" or a "chart page". *(2026-09-20)*
- Every plot is built from primary sources, every figure cites where it came from, and there are no accounts and no tracking.

## No complexity for complexity's sake

- A great plot is not the one with the most interactive features. It has just the right amount to be genuinely interesting, tell a powerful story and engage the reader without confusing or frustrating them. Every control has to earn its place; if a reader would not miss it, remove it. *(2026-09-20)*
- The corollary for building: when a review finds a screen "too much" (the row of doubling-rate chips under The Curve, the two competing label systems on one chart), the fix is to take things away, not to add a toggle. *(2026-09-20)*

## Every plot has an aha

- This is visual storytelling, not information visualization. Each plot is shaped to lead the reader to one or two epiphanies without labeling them as such. The design question for every plot is: what is the aha, and does the default view deliver it? *(2026-09-20)*
  - The National Debt: the debt line crossing above GDP in February 2013.
  - The Curve: the AI lines peeling away from Moore's Law after 2012, and Moore's Law turning out to be the slowest of the four exponentials.
  - How Fast the Tests Fall: benchmarks that once took years to solve now fall in months.
- A plot answers one question. When a section answers a different question (the benchmark panels inside The Curve, for example), it becomes its own plot, with a cross-link. *(2026-09-20)*

## Each plot is its own thing

- Plots do not share a design framework. Each gets the layout and interaction that best tells its story: single page, vertical scroll, new interactive elements, whatever fits. The site stays interesting because the plots differ. *(2026-09-20)*
- What stays consistent is the shared furniture, so a reader never has to relearn it: the site nav with the "Auto-updated" stamp, the light/dark toggle, callouts and pinned callouts, gold milestone markers with their dialogs, source links, and the notes section at the foot. *(2026-09-20)*
- Milestones are always visually distinct from data: gold, small caps, on the baseline. Data labels never compete with them; in a view where the data is labeled, milestone labels stay off until hovered. *(2026-09-20)*
- Explain for a layperson. Each view of a chart carries a short explainer that says what the series is, where it comes from, and the headline rate in plain words, with an anchor a reader can feel (the Moon landing's six-transistor chips against today's chip). Rates live in the explainer text, not in a row of chips under the chart. *(2026-09-20)*
- Honest charts: one y-axis per chart, no dual axes; a log axis is labeled as one and a fitted axis says it does not start at zero; the evaluation protocol is named wherever numbers differ across sources. Where a linear view tells the story better (the vertical takeoff), offer it, with log one click away. *(2026-09-20)*
- A plot may open as a scroll story: a pinned chart that changes state as short text steps scroll past it, then hands off to the full explorer. Keep it to six or seven steps, let the data do the moving, give reduced-motion readers the same steps without tweens, and stack the text under the chart on phones. The Curve is the first. *(2026-09-20)*
- A personal beat belongs in a story when it is true and on the data: Luyen's uncle Wen Tsing Chow was the scientific advisor on the Saturn V/Apollo guidance computer, so he sits at the Apollo point on The Curve. Source it like any other fact. *(2026-09-20)*
- Images on a public page need a license we can name: Wikimedia Commons CC files with attribution in the caption, U.S. government publications (public domain), or press images under their stated terms. A photo found on a blog is not usable until its origin is known. *(2026-09-20)*
- Drama comes from the data and the framing, not from motion. A replay that draws the line through time is fine; decorative animation is not.
- A plot with a time control may run itself once on first load, from the start of the record up to today, so the first thing a reader sees is the data moving. It stops at the present, never runs into projections on its own, yields to the first touch of the control, waits for a background tab to be looked at, and is skipped for readers with reduced motion. Drive it from the frame clock, not timers, so the pace holds. The Population Ledger is the first. *(2026-09-21)*
- Diverging colour on maps: blue for the side a reader would call good (growth, immigration, fertility above replacement), red for the other, neutral grey at the line. Say which is which in words next to the legend. *(2026-09-21)*

## The landing cards

- A card shows the plot's aha in miniature and one headline figure, both drawn from the plot's own data: each build writes a `card.json` (kind, a few dozen normalized points, figure, label, updated date) and the landing page draws the card from it. Nothing on a card is hand-drawn or typed in, so cards update with the data. *(2026-09-20)*
- Cards share one skeleton in a fixed order (kicker, title, a 72px chart slot, figure, blurb, date) so the graphics line up across a row whatever the text length; a plot that is not live yet keeps the skeleton with an empty slot. Cards do not list sources; every plot has several and the card would always be incomplete. *(2026-09-20)*

## Plots update themselves

- Auto-updating is a feature to sell, not hide. Every plot shows "Auto-updated <date>" subtly in its nav line, the landing cards show the same date, and a scheduled job re-fetches, rebuilds and commits. Going to a plot should always show the latest record holder and the latest state of the art. *(2026-09-20)*
- Every number on a page is computed from the data file at build time. Nothing is typed into the page. *(2026-09-20)*
- Prefer machine-readable primary sources (Treasury's API, FRED CSVs, Epoch AI's datasets). Where the official leaderboard is not machine-readable, say which source the plot follows and how it lags. *(2026-09-20)*
- Plots are built to grow: adding a benchmark, a milestone or a data series is a data-file edit plus a rebuild, never a page edit. Each plot's README says how. *(2026-09-20)*
- Check currency before shipping: compare the plot's frontier against the official leaderboard and note protocol differences (HLE: Scale's official numbers versus Artificial Analysis's text-only subset). *(2026-09-20)*

## Themes

- Plots are grouped by theme: Economy, Technology, Politics, Culture, Warfare, Education. Each theme has a color (Economy green, Technology blue, Politics red, Culture purple, Warfare rust, Education teal, validated for both themes) used sparingly on the landing cards: the kicker, the sparkline and the top edge, never the whole card. Themes appear as card kickers now; a visual grouping (a map view rather than a Venn diagram) is planned once there are enough plots to warrant it. *(2026-09-20)* Education became its own theme rather than a corner of Culture, since it is Luyen's own field and will carry several plots. *(2026-09-21)*

## Voice

- Each plot opens with a short first-person lede, "why I made this", in Luyen's voice: warm, direct, flowing sentences, spaced hyphens never em dashes, plain idiom, no bold-label bullets, no manufactured drama, no negation pivots. Explainers and notes are plainer but still a person talking. Luyen edits every lede. *(2026-09-20)*

## Process

- Luyen reviews each plot by walking through it and giving commentary; the commentary is collected, then applied as a batch. Design comps are produced as full pages to compare against the live design. The current "ledger green" design was kept after a four-way comparison. *(2026-09-20)*
