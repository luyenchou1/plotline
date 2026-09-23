#!/bin/bash
# Re-fetch the nflverse weekly injury reports and weekly rosters (every season, cheap) into src/raw/ (git-ignored), then assemble.
set -uo pipefail
cd "$(dirname "$0")"; mkdir -p raw && cd raw
UA="Mozilla/5.0 (Plotline data fetch)"
get(){ curl -sL --retry 2 -A "$UA" -o "$2.tmp" "$1" && [ -s "$2.tmp" ] && mv "$2.tmp" "$2" && echo "ok  $2" || { rm -f "$2.tmp"; echo "KEPT $2"; }; }
Y=$(date -u +%Y)
for y in $(seq 2009 $Y); do
  get "https://github.com/nflverse/nflverse-data/releases/download/injuries/injuries_$y.csv" inj_$y.csv
  get "https://github.com/nflverse/nflverse-data/releases/download/weekly_rosters/roster_weekly_$y.csv" ros_$y.csv
done
get "https://raw.githubusercontent.com/nflverse/nflverse-pbp/master/teams_colors_logos.csv" teams.csv
get "https://github.com/nflverse/nfldata/raw/master/data/games.csv" games.csv
echo "fetched $(date -u +%F)"
cd .. && python3 assemble.py
