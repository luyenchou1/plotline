# How Fast the Tests Fall

Every major AI benchmark on one calendar, counted from the day each was published, with a one-test detail view and curated model-release milestones.

## Data

Shared with The Curve: `../the-curve/src/fetch.sh` downloads Epoch AI's Benchmarking Hub archive and `../the-curve/src/assemble.py` writes `../the-curve/src/data.json`; this plot's `build.py` reads that file. The weekly refresh workflow rebuilds both.

## Adding a benchmark

Harder tests will keep arriving. To add one:

1. Find its file in `../the-curve/src/raw/benchmark_data/` (Epoch's archive; the file name is the benchmark's slug, external ones end in `_external`) and its exact name in `benchmark_metadata.csv`, which supplies the publication date.
2. Add a row to `BENCH` in `../the-curve/src/assemble.py`: key, file, score column, metadata name, display name, one-line domain.
3. Add a matching entry to `src/benchmarks.json`: description in plain words, paper link, official leaderboard link and its name.
4. Run `python3 ../the-curve/src/assemble.py && python3 build.py`. The row appears in publication order automatically; the headline median, the tabs and the detail view all follow.

Scores must be fractions 0 to 1 for the "solved at" logic; a benchmark with a different unit (like METR's minutes) needs its own panel, as METR has.

## Adding a release milestone

Append to `src/milestones.json`: date, short name, title, a two-sentence note that describes only what the data shows, and a source URL. Take dates from the Epoch data, not memory. Keep the list to about eight; the lane above the chart holds three rows of labels and hides the rest until hovered.
