#!/bin/bash
# Re-fetch the raw sources for The Curve into src/raw/ (git-ignored), then run assemble.py.
# All sources are open data: Epoch AI (CC-BY 4.0), Wikipedia (CC-BY-SA), Our World in Data (CC-BY).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p raw && cd raw
UA="Mozilla/5.0 (Plotline data fetch)"
curl -sL -A "$UA" "https://epoch.ai/data/epochdb/notable_ai_models.csv" -o notable_ai_models.csv
curl -sL -A "$UA" "https://epoch.ai/data/epochdb/ml_hardware.csv"       -o ml_hardware.csv
curl -sL -A "$UA" "https://epoch.ai/data/benchmark_data.zip"            -o benchmark_data.zip
rm -rf benchmark_data && mkdir benchmark_data && unzip -o -q benchmark_data.zip -d benchmark_data
curl -sL -A "$UA" "https://en.wikipedia.org/wiki/Transistor_count"      -o wiki_transistor_count.html
curl -sL -A "$UA" "https://ourworldindata.org/grapher/transistors-per-microprocessor.csv?v=1&csvType=full&useColumnShortNames=true" -o owid_transistors.csv
echo "fetched $(date -u +%F)"
cd .. && python3 assemble.py
