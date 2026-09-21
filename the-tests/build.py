#!/usr/bin/env python3
"""Build index.html for How Fast the Tests Fall.
Data comes from the shared pull in ../the-curve/src/data.json (Epoch AI Benchmarking Hub);
descriptions and official-leaderboard links live in src/benchmarks.json."""
import json, pathlib
root = pathlib.Path(__file__).parent
d = json.load(open(root.parent/'the-curve'/'src'/'data.json'))
desc = json.load(open(root/'src'/'benchmarks.json'))

def r3(x):
    return None if x is None else float(f'{x:.3g}')

benchmarks = []
for b in d['benchmarks']:
    info = desc.get(b['key'], {})
    benchmarks.append({
        'key': b['key'], 'name': info.get('name', b['name']), 'domain': b['domain'], 'release': b['release'], 'unit': b['unit'], 'n': b['n'],
        'desc': info.get('desc', ''), 'paper': info.get('paper', ''), 'board': info.get('board', ''), 'boardName': info.get('boardName', ''),
        'points': [[p['date'], p['display'] or p['model'], p['org'], r3(p['score'])] for p in b['points']],
        'frontier': [[p['date'], p['display'] or p['model'], p['org'], r3(p['score'])] for p in b['frontier']],
    })
payload = {'retrieved': d['retrieved'], 'benchmarks': benchmarks, 'milestones': json.load(open(root/'src'/'milestones.json'))}
js = 'const DATA=' + json.dumps(payload, separators=(',', ':'), ensure_ascii=False) + ';'
tpl = open(root/'src'/'template.html', encoding='utf-8').read()
assert '/*__DATA__*/' in tpl
out = tpl.replace('/*__DATA__*/', js)
open(root/'index.html', 'w', encoding='utf-8').write(out)
through = max(p['date'] for b in d['benchmarks'] for p in b['points'])

# ---- card.json: months-to-80% per benchmark in publication order, and the headline median
import datetime as _dt
_rows=[]
for b in benchmarks:
    if b['unit']!='fraction' or not b['release']: continue
    rel=_dt.date.fromisoformat(b['release']); solved=None
    for pdate,name,org,score in b['frontier']:
        if score is not None and score>=0.8: solved=_dt.date.fromisoformat(pdate); break
    now=_dt.date.fromisoformat(d['retrieved'])
    months=(max(solved,rel)-rel).days/30.44 if solved else (now-rel).days/30.44
    _rows.append({'rel':rel,'months':months,'open':solved is None})
_rows.sort(key=lambda r:r['rel']); _maxm=max(r['months'] for r in _rows)
_recent=sorted(r['months'] for r in _rows if r['rel']>=_dt.date(2024,1,1) and not r['open'])
_med=_recent[len(_recent)//2] if _recent else None
_card={'kind':'dots','rows':[{'x':round(r['months']/_maxm,4),'open':r['open']} for r in _rows],
 'figure':(str(round(_med))+' months') if _med is not None else 'n/a','label':'median time to 80% for benchmarks published since 2024','updated':d['retrieved']}
json.dump(_card,open(root/'card.json','w'),separators=(',',':'))

json.dump({'plot': 'the-tests', 'updated': d['retrieved'], 'through': through}, open(root/'meta.json', 'w'))
print('index.html', len(out.encode())//1024, 'KB; benchmarks', len(benchmarks))
