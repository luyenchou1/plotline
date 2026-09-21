#!/bin/bash
# Re-fetch the raw sources for The Population Ledger into src/raw/ (git-ignored), then assemble src/data.json.
set -euo pipefail
cd "$(dirname "$0")"; mkdir -p raw && cd raw
UA="Mozilla/5.0 (Plotline data fetch)"
curl -sL -A "$UA" -o wpp_med.csv.gz "https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_Demographic_Indicators_Medium.csv.gz"
gunzip -kf wpp_med.csv.gz
curl -sL -A "$UA" -o countries-110m.json "https://cdn.jsdelivr.net/npm/world-atlas@2.0.2/countries-110m.json"
echo "fetched $(date -u +%F)"
cd .. && python3 assemble.py
