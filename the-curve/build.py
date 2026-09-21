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
  'models': [[m['name'], m['org'], m['date'], r3(m['compute']), r3(m['params']), m['confidence'][:1] if m['confidence'] else '', 1 if m['frontier'] else 0, m['domain'].split(',')[0], m.get('link','')]
             for m in d['models']],
  'hardware': [[h['name'], h['maker'], h['date'], r3(h['flops']), h.get('link','')] for h in d['hardware']],
  'events': events,
}
js = 'const DATA=' + json.dumps(payload, separators=(',', ':'), ensure_ascii=False) + ';'
tpl = open(root/'src/template.html', encoding='utf-8').read()
assert '/*__DATA__*/' in tpl
out = tpl.replace('/*__DATA__*/', js)
open(root/'index.html', 'w', encoding='utf-8').write(out)

# ---- card.json: four record lines indexed to 2012, and the compute doubling time
import math
def _P(ds): return dt.date.fromisoformat(ds if len(ds)==10 else (ds+'-15' if len(ds)==7 else ds+'-07-01'))
def _rec(pts):  # pts: [(date, value)] -> running-max record points
    pts=sorted(pts); out=[]; mx=-1
    for t,v in pts:
        if v>mx: mx=v; out.append((t,v))
    return out
def _rec_at(rec,day):
    r=None
    for t,v in rec:
        if t<=day: r=v
        else: break
    return r
def _doubling(rec,a,b):
    pts=[(t,v) for t,v in rec if a<=t<=b]
    ra=_rec_at(rec,a); rb=_rec_at(rec,b)
    if ra: pts=[(a,ra)]+pts
    if rb: pts=pts+[(b,rb)]
    if len(pts)<3: return None
    xs=[(t-dt.date(1970,1,1)).days/365.25 for t,_ in pts]; ys=[math.log2(v) for _,v in pts]
    n=len(pts); sx=sum(xs); sy=sum(ys); sxy=sum(x*y for x,y in zip(xs,ys)); sxx=sum(x*x for x in xs)
    slope=(n*sxy-sx*sy)/(n*sxx-sx*sx); return 12/slope if slope>0 else None
_layers={
 'transistors':[(dt.date(c['year'],7,1),c['count']) for c in d['transistors']['chips']],
 'compute':[(_P(m['date']),m['compute']) for m in d['models'] if m['compute']],
 'hardware':[(_P(h['date']),h['flops']) for h in d['hardware']],
 'params':[(_P(m['date']),m['params']) for m in d['models'] if m['params'] and not (m['date']<'2010' and m['params']>1e9)],
}
_recs={k:_rec(v) for k,v in _layers.items()}
_base=dt.date(2012,7,1); _t0=dt.date(1971,1,1); _t1=dt.date.fromisoformat(d['retrieved'])
_lines=[]; _lo=1e9; _hi=-1e9
for k in ['transistors','hardware','params','compute']:
    rec=_recs[k]; b=_rec_at(rec,_base); pts=[]
    for yr in range(1971,_t1.year+1):
        day=min(dt.date(yr,7,1),_t1); v=_rec_at(rec,day)
        if v is None or not b: continue
        y=math.log10(v/b); pts.append(((day-_t0).days/(_t1-_t0).days,y)); _lo=min(_lo,y); _hi=max(_hi,y)
    _lines.append(pts)
_lines=[[[round(x,4),round((y-_lo)/(_hi-_lo),4)] for x,y in pts] for pts in _lines]
_dc=_doubling(_recs['compute'],_base,_t1)
_card={'kind':'fan','lines':_lines,'base':[round((_base-_t0).days/(_t1-_t0).days,4),round((0-_lo)/(_hi-_lo),4)],
 'figure':'×2 / '+f"{_dc:.1f}"+' mo','label':'AI training compute doubling time since 2012','updated':d['retrieved']}
json.dump(_card,open(root/'card.json','w'),separators=(',',':'))

json.dump({'plot':'the-curve','updated':d['retrieved'],'through':max(m['date'] for m in d['models'])},open(root/'meta.json','w'))
print('index.html', len(out.encode())//1024, 'KB; events', len(events), '; models', len(payload['models']), '; chips', len(payload['chips']))
