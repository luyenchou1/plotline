#!/usr/bin/env python3
"""Build index.html, meta.json and card.json for The Report Card."""
import json, pathlib
root = pathlib.Path(__file__).parent
d = json.load(open(root/'src'/'data.json'))
d['milestones'] = json.load(open(root/'src'/'milestones.json'))
tpl = open(root/'src'/'template.html', encoding='utf-8').read()
assert '/*__DATA__*/' in tpl
out = tpl.replace('/*__DATA__*/', 'const DATA=' + json.dumps(d, separators=(',', ':'), ensure_ascii=False) + ';')
open(root/'index.html', 'w', encoding='utf-8').write(out)
naep_through = max(y for s in d['naep'].values() for y, _ in s)
pisa_through = max(y for subj in d['pisa'].values() for e in subj.values() for y, _ in e['scores'])
json.dump({'plot': 'education', 'updated': d['retrieved'], 'through': str(max(naep_through, pisa_through))}, open(root/'meta.json', 'w'))

# card: spending per pupil (filled, accent) against 8th-grade math (thin line), both indexed to 1990 on the same frame
sp = [r for r in d['spend']['series'] if r[0] >= 1990]; m8 = d['naep']['mathematics8']
x0, x1 = 1990, max(sp[-1][0], m8[-1][0])
X = lambda y: round((y - x0) / (x1 - x0), 4)
spmax = max(v for _, v in sp); spmin = sp[0][1]
m8_2000 = next(v for y, v in m8 if y == 2000); m8_last = m8[-1][1]
card = {'kind': 'crossover',
        'a': [[X(y), round(0.15 + 0.75 * (v - spmin) / (spmax - spmin), 4)] for y, v in sp],
        'b': [[X(y), round(0.15 + 0.75 * (v - 260) / 30, 4)] for y, v in m8],
        'cross': None,
        'figure': (f"{round(d['naep']['mathematics8_prof'][-1][1])}%" if d['naep'].get('mathematics8_prof') else f'{round(m8_2000)} → {round(m8_last)}'),
        'label': (f"of 8th graders proficient in math, {d['naep']['mathematics8_prof'][-1][0]}, after a third more real spending per pupil since 2000" if d['naep'].get('mathematics8_prof') else f'8th-grade math score, 2000 and {m8[-1][0]}, while real spending per pupil rose'),
        'updated': d['retrieved']}
json.dump(card, open(root/'card.json', 'w'), separators=(',', ':'))
print('index.html', len(out.encode())//1024, 'KB; through', naep_through, pisa_through, '; card', card['figure'])
