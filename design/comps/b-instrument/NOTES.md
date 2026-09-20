# Comp B: Instrument panel

## Direction

The site is a set of live instruments for reading the world, closer to an observatory console than a trading terminal: dark-first, dense, and precise, with the numbers themselves doing the design work. The landing page is a control room of plots, each one a panel with its live headline figure, a sparkline, source stamp and "Updated" line, grouped under theme rails (Economy, Technology, Politics, with Culture and Warfare shown as empty rails so the room is honest about what is not built yet). A visible 32px grid runs under everything, panels sit on it with hairline borders and small corner ticks, and every figure is set in a real monospace with tabular numerals.

## Palette

Dark (default when the system prefers dark)

- Ground `#0B0F14` (near-black with a blue bias)
- Panel `#10151C`
- Grid `#151C25`, hairline `#222B36`, strong line `#465361`
- Ink `#E4E9EE`, secondary `#9BA7B3`, muted `#6B7784`
- Signal amber `#F0A63A` (live ticker, the aha readouts, the gold milestone)
- Reference blue `#5AA3D6` (GDP line, the 2012 index line)
- Chart series, validated with the dataviz palette script against `#0B0F14`: transistors `#3D8FC4`, training compute `#C08118`, accelerators `#35A87A`, parameters `#D6633F`

Light (a printed instrument card, designed rather than inverted)

- Ground `#F2F3EF` (paper with a cool green tint)
- Panel `#FBFBF8`
- Grid `#E1E4DD`, hairline `#CBD0C9`, strong line `#8F9891`
- Ink `#14181C`, secondary `#48525B`, muted `#77818A`
- Signal amber `#A85F06`
- Reference blue `#2A73B0`
- Chart series, validated against `#F2F3EF`: transistors `#2A73B0`, training compute `#B5720A`, accelerators `#1F8F62`, parameters `#C4482A`

No glow, no scanlines, no gradients. The only motion is a slow opacity pulse on the live dot (off under reduced motion) and the debt ticker itself.

## Type

- Instrument Sans (400 / 500 / 600) for headings, ledes and body. A precise grotesk with a slightly narrow set, so long first-person sentences stay readable at 17px while the headings feel engineered.
- Geist Mono (400 / 500) for every figure, label, stamp, axis tick and tooltip. Small tracked uppercase labels (11px, 0.1em) are the instrument-panel voice; the hero figures run up to 44px in the same mono so the numbers carry the page.
- Fallbacks: ui-sans-serif / system-ui, and ui-monospace / SF Mono / Menlo.

## What it does for the aha and the voice

On the landing page the aha is the headline figure on each panel: the debt is a fourteen-digit live count in signal amber, advancing at the real +$102,386 per second from the Sep 17, 2026 anchor, and the Curve panel leads with "x2 every 5.6 mo" against "x2 every 25.5 mo" one line below. Each sparkline carries the crossing in miniature: debt passing GDP in Feb 2013 as a gold diamond, and training compute peeling off the transistor line at a gold 2012 marker. On the plot page the four exponentials share one labeled log axis indexed to 2012, so the four lines pass through a single gold AlexNet marker and the slopes after it are the whole story; the doubling-time readouts sit directly under the chart in the same mono as the axis, and a crosshair tooltip gives the multiple of the 2012 level for each series as you move across the years.

The voice survives the precision by being placed where the instruments are quiet: the landing headline and intro sit in Instrument Sans at reading size above the rails, and on the plot page the lede runs beside the title in a plain 17px paragraph with only the first letter picked out in signal amber. The tension between a warm, first-person sentence and a tracked mono readout is the intended feeling of the site: one person's curiosity, read off a set of instruments.
