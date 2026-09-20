#!/usr/bin/env python3
"""Build index.html for The Curve from src/template.html + src/data.json (+ src/events.json)."""
import json, pathlib, datetime as dt
root = pathlib.Path(__file__).parent
d = json.load(open(root/'src/data.json'))
events = json.load(open(root/'src/events.json'))

def r3(x):  # 3 significant figures, keeps the payload small
    if x is None: return None
    return float(f'{x:.3g}')

payload = {
  'retrieved': d['retrieved'],
  'sources': d['sources'],
  'chips': [[c['name'], c['year'], r3(c['count']), c['designer'], c['kind']] for c in d['transistors']['chips']],
  'models': [[m['name'], m['org'], m['date'], r3(m['compute']), r3(m['params']), m['confidence'][:1] if m['confidence'] else '', 1 if m['frontier'] else 0, m['domain'].split(',')[0]]
             for m in d['models']],
  'hardware': [[h['name'], h['maker'], h['date'], r3(h['flops'])] for h in d['hardware']],
  'benchmarks': [{'key': b['key'], 'name': b['name'], 'domain': b['domain'], 'release': b['release'], 'unit': b['unit'], 'n': b['n'],
                  'points': [[p['date'], p['display'] or p['model'], p['org'], r3(p['score'])] for p in b['points']],
                  'frontier': [[p['date'], p['display'] or p['model'], p['org'], r3(p['score'])] for p in b['frontier']]}
                 for b in d['benchmarks']],
  'events': events,
}
js = 'const DATA=' + json.dumps(payload, separators=(',', ':'), ensure_ascii=False) + ';'
tpl = open(root/'src/template.html', encoding='utf-8').read()
assert '/*__DATA__*/' in tpl
out = tpl.replace('/*__DATA__*/', js)
open(root/'index.html', 'w', encoding='utf-8').write(out)
json.dump({'plot':'the-curve','updated':d['retrieved'],'through':max(m['date'] for m in d['models'])},open(root/'meta.json','w'))
print('index.html', len(out.encode())//1024, 'KB; events', len(events), '; models', len(payload['models']), '; chips', len(payload['chips']))
