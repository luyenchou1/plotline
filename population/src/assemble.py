#!/usr/bin/env python3
"""Assemble src/data.json (UN WPP 2024, medium variant) and src/geo.json (world-atlas 110m as GeoJSON)."""
import csv, json, pathlib, datetime as dt
root=pathlib.Path(__file__).parent; raw=root/'raw'
rows=list(csv.DictReader(open(raw/'wpp_med.csv',encoding='utf-8-sig')))
KEEP={'1':'world','2':'region','3':'subregion','4':'country'}
locs={}
def f(x,nd=1):
    try: return round(float(x),nd)
    except: return None
for r in rows:
    t=KEEP.get(r['LocTypeID'])
    if not t: continue
    if t=='country' and not r['ISO3_code']: continue
    L=locs.setdefault(r['LocID'],{'id':r['LocID'],'name':r['Location'],'type':t,'parent':r['ParentID'],'iso3':r['ISO3_code'] or None,'y':{}})
    yr=int(r['Time'])
    if yr<1950 or yr>2100: continue
    def i(x,m=1):
        try: return int(round(float(x)*m))
        except: return None
    L['y'][yr]=[i(r['TPopulation1July']),i(r['Births']),i(r['Deaths']),i(r['NetMigrations']),i(r['TFR'],100),i(r['MedianAgePop'],10),i(r['LEx'],10)]
# world's parent is itself; regions' parent is world (900)
out={'retrieved':dt.date.today().isoformat(),'source':'https://population.un.org/wpp/','variant':'Medium','years':[1950,2100],'lastEstimate':2023,
     'cols':'pop, births, deaths, mig are thousands of people (ints); tfr is x100; age and lex are x10',
     'locations':[]}
for L in locs.values():
    ys=list(range(1950,2101)); cols=['pop','births','deaths','mig','tfr','age','lex']
    rec={'id':L['id'],'name':L['name'],'type':L['type'],'parent':L['parent'],'iso3':L['iso3']}
    for ci,c in enumerate(cols): rec[c]=[(L['y'].get(y) or [None]*7)[ci] for y in ys]
    out['locations'].append(rec)
json.dump(out,open(root/'data.json','w'),separators=(',',':'))
# ---- geometry: TopoJSON -> GeoJSON (110m), coordinates rounded
topo=json.load(open(raw/'countries-110m.json'))
sc=topo['transform']['scale']; tr=topo['transform']['translate']
def arc(i):
    a=topo['arcs'][i if i>=0 else ~i]; x=y=0; pts=[]
    for dx,dy in a:
        x+=dx; y+=dy; pts.append([round(x*sc[0]+tr[0],2),round(y*sc[1]+tr[1],2)])
    return pts if i>=0 else pts[::-1]
def ring(arcs):
    pts=[]
    for i in arcs:
        seg=arc(i)
        if pts and pts[-1]==seg[0]: seg=seg[1:]
        pts+=seg
    return pts
feats=[]
for g in topo['objects']['countries']['geometries']:
    gid=str(int(g['id'])) if g.get('id') else None; name=g['properties']['name']
    if g['type']=='Polygon': coords=[ring(r) for r in g['arcs']]; geom={'type':'Polygon','coordinates':coords}
    else: coords=[[ring(r) for r in poly] for poly in g['arcs']]; geom={'type':'MultiPolygon','coordinates':coords}
    feats.append({'type':'Feature','id':gid,'properties':{'name':name},'geometry':geom})
json.dump({'type':'FeatureCollection','features':feats},open(root/'geo.json','w'),separators=(',',':'))
countries=[l for l in out['locations'] if l['type']=='country']
ids={l['id'] for l in countries}
print('locations',len(out['locations']),'countries',len(countries),'| geo features',len(feats),'matched',sum(1 for x in feats if x['id'] in ids),
      '| data.json',round((root/'data.json').stat().st_size/1024),'KB | geo.json',round((root/'geo.json').stat().st_size/1024),'KB')
print('unmatched:',[(x['id'],x['properties']['name']) for x in feats if x['id'] not in ids])
