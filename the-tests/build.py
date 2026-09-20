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
json.dump({'plot': 'the-tests', 'updated': d['retrieved'], 'through': through}, open(root/'meta.json', 'w'))
print('index.html', len(out.encode())//1024, 'KB; benchmarks', len(benchmarks))
