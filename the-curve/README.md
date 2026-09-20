# The Curve (in progress)

Compute, models and capability, each on a log axis, from the Intel 4004 to the current frontier.

## Data

Run `src/fetch.sh` to download the raw sources into `src/raw/` (git-ignored) and assemble `src/data.json`.

| Layer | Source | License |
|---|---|---|
| Transistors per chip (named CPUs, SoCs, GPUs) | Wikipedia, "Transistor count" | CC-BY-SA |
| Notable AI models: training compute (FLOP), parameters, dates | Epoch AI, Notable AI Models | CC-BY 4.0 |
| Accelerators: dense FP16/BF16 FLOP/s by release date | Epoch AI, Machine Learning Hardware | CC-BY 4.0 |
| Benchmark score histories (MMLU, GSM8K, MATH, GPQA Diamond, AIME, SWE-bench Verified, ARC-AGI 1 and 2, HLE, FrontierMath, METR time horizons) | Epoch AI, Benchmarking Hub | CC-BY 4.0 (external runs carry their original terms) |

`data.json` keeps every point (for hover) plus a running-best "frontier" sequence per benchmark.
