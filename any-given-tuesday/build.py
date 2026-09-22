#!/usr/bin/env python3
"""Build index.html, meta.json and card.json for Any Given Tuesday."""
import json, pathlib
root = pathlib.Path(__file__).parent
d = json.load(open(root/'src'/'data.json'))
d['milestones'] = json.load(open(root/'src'/'milestones.json'))
# latest week with any Out listing (the newest week's report may not be filed yet)
tpl = open(root/'src'/'template.html', encoding='utf-8').read()
assert '/*__DATA__*/' in tpl
out = tpl.replace('/*__DATA__*/', 'const DATA=' + json.dumps(d, separators=(',', ':'), ensure_ascii=False) + ';')
open(root/'index.html', 'w', encoding='utf-8').write(out)
cur = d['seasons'][-1]
json.dump({'plot': 'any-given-tuesday', 'updated': d['retrieved'], 'through': f"{cur['season']} wk {cur['weeks']}"}, open(root/'meta.json', 'w'))
# card: league average (filled) vs Giants (line), player-weeks lost per team per week, 2016 on
RES_OK = 2016
rows = [s for s in d['seasons'] if s['complete'] and s['season'] >= RES_OK]
mx = max(max(s['league']['lost']/s['weeks'], s['teams']['NYG']['lost']/s['weeks']) for s in rows) * 1.08
X = lambda i: round(i/(len(rows)-1), 4)
lg = sum(s['league']['lost'] for s in rows); ny = sum(s['teams']['NYG']['lost'] for s in rows)
card = {'kind': 'crossover',
        'a': [[X(i), round(s['league']['lost']/s['weeks']/mx, 4)] for i, s in enumerate(rows)],
        'b': [[X(i), round(s['teams']['NYG']['lost']/s['weeks']/mx, 4)] for i, s in enumerate(rows)],
        'cross': None,
        'figure': f"+{round((ny/lg-1)*100)}%", 'label': f"Giants player-weeks lost against an average team, {rows[0]['season']} to {rows[-1]['season']}",
        'updated': d['retrieved']}
json.dump(card, open(root/'card.json', 'w'), separators=(',', ':'))
print('index.html', len(out.encode())//1024, 'KB; through', cur['season'], cur['weeks'], '; card', card['figure'])
