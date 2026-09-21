#!/usr/bin/env python3
"""Build index.html, meta.json and card.json for The Population Ledger.
The page loads src/data.json and src/geo.json at runtime (they are copied next to index.html), so the HTML stays small."""
import json, pathlib, shutil
root = pathlib.Path(__file__).parent
d = json.load(open(root/'src'/'data.json'))
tpl = open(root/'src'/'template.html', encoding='utf-8').read()
assert '/*__DATA__*/' in tpl
out = tpl.replace('/*__DATA__*/', '/* data is fetched from data.json and geo.json */')
open(root/'index.html', 'w', encoding='utf-8').write(out)
shutil.copy(root/'src'/'data.json', root/'data.json')
shutil.copy(root/'src'/'geo.json', root/'geo.json')
json.dump({'plot': 'population', 'updated': d['retrieved'], 'through': str(d['lastEstimate'])}, open(root/'meta.json', 'w'))

# card: world births vs deaths, 1950-2100, with the crossing year
W = next(L for L in d['locations'] if L['type'] == 'world')
years = list(range(1950, 2101))
b = W['births']; de = W['deaths']
mx = max(max(b), max(de)) * 1.05
cross = next((y for y, bb, dd in zip(years, b, de) if dd is not None and bb is not None and dd > bb and y > 2000), None)
n = len(years)
samp = list(range(0, n, 3)) + [n-1]
card = {'kind': 'crossover',
        'a': [[round(k/(n-1), 4), round(b[k]/mx, 4)] for k in samp],
        'b': [[round(k/(n-1), 4), round(de[k]/mx, 4)] for k in samp],
        'cross': [round((cross-1950)/(n-1), 4), round(de[cross-1950]/mx, 4)] if cross else None,
        'figure': f"{W['pop'][min(2100,int(d['retrieved'][:4]))-1950]*1000/1e9:.2f} billion", 'label': f"people in the world, {min(2100,int(d['retrieved'][:4]))}; deaths pass births in {cross}",
        'updated': d['retrieved']}
json.dump(card, open(root/'card.json', 'w'), separators=(',', ':'))
print('index.html', len(out.encode())//1024, 'KB; data.json', (root/'data.json').stat().st_size//1024, 'KB; deaths pass births in', cross)
