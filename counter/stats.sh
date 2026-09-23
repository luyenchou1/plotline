#!/bin/bash
# Print Plotline view statistics (private). The key lives in ~/.config/plotline/counter.key.
KEY=$(cat ~/.config/plotline/counter.key)
curl -s "https://plotline-counter.luyen-9ce.workers.dev/stats?key=$KEY" | python3 -c '
import json,sys,collections
d=json.load(sys.stdin)
print("Totals (views):");[print(f"  {t["plot"]:<20}{t["views"]:>8}") for t in d["totals"]]
by=collections.defaultdict(dict)
for r in d["daily"]: by[r["day"]][r["plot"]]=(r["views"],r["visitors"])
print("\nLast 14 days (views / visitors):")
for day in sorted(by)[-14:]:
    print("  "+day+"  "+"  ".join(f"{p}:{v}/{u}" for p,(v,u) in sorted(by[day].items())))
print("\nTop referrers:");[print(f"  {r["plot"]:<20}{r["ref"]:<32}{r["views"]:>6}") for r in d["referrers"][:15]]
print("\nTop countries:");[print(f"  {c["plot"]:<20}{c["country"]:<6}{c["views"]:>6}") for c in d["countries"][:15]]
'
