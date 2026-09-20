# Comp C: Poster

## Direction
Every plot is presented like a broadsheet front page: the headline number and the one-sentence claim are set huge in a wide grotesk, the chart is the illustration, and the theme colour is a flat band across the top of the panel rather than a rail on a card. The landing page is a vertical sequence of these panels (Economy, Technology, Politics) separated by hairlines, with the about text and a five-theme colour index at the foot. Everything sits left on a strong two-column grid with a lot of air, no gradients, no shadows, no radius.

## Palette
Light: Newsprint ground #E6E7E2, second surface #DBDDD6, ink #141613, secondary ink #40443F, muted #676B65, hairline #C3C6BE, gold milestone #A8790A, text on a colour field #F3F4EF.
Light theme accents (the accent is also the band field): Economy #167A50, Technology #1D4FCB, Politics #B3212B, Culture #6B3AB8, Warfare #A4471A.

Dark is its own composition: ink-black ground #14171A, second surface #1B1F23, ink #ECEDE8, secondary ink #C3C6BF, muted #8F948E, hairline #2C3136, gold #E0B53D. The band becomes a deep tint of the theme with light type on it, and the bright accent is saved for the line in the chart: Economy #2FA56F on field #0E3A27, Technology #4F82EE on #142455, Politics #E84E58 on #4A1418, Culture #9A6EF0 on #2C1A55, Warfare #DB7330 on #43200E.

Both five-accent sets pass the dataviz validator (lightness band, chroma floor, CVD separation, contrast) against their own ground.

## Type
Archivo (Google Fonts variable, width axis) does all the display work: width 125 at weight 900 for the headline numbers and the wordmark, width 72 at weight 700 for titles and claims, width 100 for labels and chart text. Source Serif 4 carries the lede, the intro and the card copy at 18 to 20px, so the personal writing reads at a conversational size under the display type. Fallbacks: Helvetica Neue / Arial and Georgia.

## What it does for the aha and the voice
The aha is the poster. On the landing page the Economy panel leads with $40.09T and the claim about $102,386 a second, and its illustration is the crossover itself with "Debt passes GDP · Feb 2013" written on it; the Technology panel leads with 5.6 months and draws the peel-away on a labelled log axis. On the plot page the crossover chart is set at full poster width with a light wash filling the wedge where debt sits above GDP, a single vertical note at Feb 2013, and one gold milestone diamond with a leader-line callout, so the eye lands on the crossing before reading a single axis label. The voice survives because the first-person lede sits in a quiet serif at reading size beside the huge condensed title rather than competing with it, and the copy on every panel is Luyen's own card text.

## Notes for review
- The debt lede in plot.html is a stand-in assembled only from facts in the brief (Treasury daily count, 33 years, GDP alongside, Feb 2013 crossover); Luyen's own lede replaces it.
- The chart lines are a sketch of the shape at the real endpoints ($40.09T, 123% debt to GDP, Feb 2013 crossover); the live page draws from Treasury and FRED data.
- The gold marker sits at the latest reading to show the milestone treatment; on the live page gold marks the laws and shocks.
- On phones the chart scrolls sideways inside its own container (720px minimum) so axis text stays legible; the page body never scrolls horizontally.
- The hover layer shows the year under the pointer only; values come from the live data layer.
