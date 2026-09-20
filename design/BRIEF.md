# Plotline design brief (for comps)

## What the site is
Plotline is Luyen Chou's personal site of "plots": small, self-contained interactive data visualizers about current events, each built from primary sources (Treasury, FRED, Epoch AI, city records). No accounts, no tracking, static pages on GitHub Pages. Tagline in use: "Current events, drawn from the data."

Two plots are live, one is coming:
- **The National Debt** (theme: Economy). Live ticker of the debt, a zoomable 33-year chart with GDP alongside it, milestones as gold markers, debt-to-GDP, by-presidential-term table, "how long each trillion took". The aha: the debt line crossing above GDP in Feb 2013.
- **The Curve** (theme: Technology). Transistors per chip, AI training compute, accelerator throughput and model parameters on one log axis, indexed to 2012; benchmark saturation small multiples; largest training runs. The aha: the AI lines peel away from Moore's Law (2 years per doubling) to ~6 months per doubling after 2012.
- **The Mamdani Scorecard** (theme: Politics), in progress.

Future themes: Economy, Technology, Politics, Culture, Warfare. There will eventually be 10–20 plots. Each plot shows a subtle "Updated <date>" line.

## Voice (this matters)
The site should feel like an expression of one person's curiosity about understanding the world through data, not a cold journalistic resource. Each plot opens with a short first-person lede ("why I made this"). Luyen's writing: first person, warm, direct, flowing mid-length sentences, spaced hyphens " - " never em dashes, plain idiom, no bold-label bullets, no manufactured drama, no negation pivots ("not X, but Y"). Use the real copy below; do not invent facts.

Real copy you may use verbatim:
- Landing headline (current): "The numbers behind the news, in a form you can explore."
- Landing intro (current): "Each plot here is a small interactive built directly from primary sources: Treasury, FRED, city records, the agencies themselves. No accounts, no tracking, and every figure cites where it came from."
- The Curve lede: "I've shown a version of this chart to rooms full of educators two years running, because most people have heard of Moore's Law but have never seen what sits on top of it. Chips have doubled their transistor count roughly every two years for fifty-five years, which is astonishing on its own. The AI curves stacked on that foundation double every five or six months. That gap is the thing I most wanted to see for myself, so this page starts there - every line is a real chip, model or test run, and every point has a source."
- Debt card: "Thirty-three years of Treasury's daily count, with GDP alongside it, the laws and shocks that bent the curve, and how long each trillion took."
- Curve card: "Chips have doubled every two years since 1971. The AI built on them doubles every six months. Four exponentials on one axis, and how fast the tests fall."
- Real numbers for hero treatments: debt $40.09T (Sep 17, 2026), +$102,386 per second (90-day pace), debt-to-GDP 123%, debt passed GDP Feb 2013; AI training compute ×2 every 5.6 months since 2012, transistors ×2 every 25.5 months since 1971.

## The current design (the baseline to beat, or keep)
IBM Plex Sans + IBM Plex Mono, cool green-tinted neutrals, green accent (#1d7a4e light / #4cc38a dark), gold for milestones, rounded cards, a mono wordmark with a small rising-line glyph, light and dark themes, compact stat tiles, everything derived from data. Live at https://luyenchou1.github.io/plotline/ (landing) and https://luyenchou1.github.io/plotline/the-curve/ (a plot). Luyen does not dislike it. Comps should be genuinely different directions, not variations.

## Hard constraints for every comp
- Two standalone HTML files in your assigned folder: `index.html` (the landing page, with all three plot cards and the about text) and `plot.html` (the top of a plot page: site nav with "Updated Sep 20, 2026", title, first-person lede, hero numbers, and the main chart area rendered as a real inline SVG sketch of the debt-vs-GDP crossover or the four-exponentials peel-away, with axes, a milestone marker and a callout so the chart treatment can be judged). Plus a short `NOTES.md`: the direction in three sentences, the palette as named hex values, the type pairing, and what the design does for the "aha" and the voice.
- Fonts only from Google Fonts (link tag) with real fallback stacks. No other external resources; inline everything else. No images except inline SVG.
- Light and dark themes via CSS tokens on :root, `@media (prefers-color-scheme: dark)` guarded with `:root:not([data-theme="light"])`, and `:root[data-theme="dark"]`; include a small theme toggle button that stamps data-theme and stores it in localStorage under `plotline-theme`.
- Works at phone width (375px) with a 16px gutter, no horizontal scroll. Real content, no lorem.
- Charts follow honest-viz rules: one y-axis per chart, no dual axes, recessive grid, thin marks, log axis labeled when used.
- Avoid the generic AI look: no cream + serif + terracotta, no purple gradients, no Inter/Space Grotesk as the safe choice, no emoji section markers, no centered-everything, no identical rounded cards with accent rails. The design should be specific to this subject: data, curiosity, current events.
- Keep the wordmark text "Plotline" but you may redesign the mark.

Load the `artifact-design` and `dataviz` skills before you start, and follow them.
