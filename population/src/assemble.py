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
def unwrap(pts):
    """Walk a ring keeping each longitude step under 180 degrees, so a ring that Natural Earth closes across the
    antimeridian (Russia's Chukotka tip, Wrangel Island, Fiji's Vanua Levu) becomes continuous, running past 180."""
    out=[pts[0][:]]; off=0.0
    for k in range(1,len(pts)):
        lon=pts[k][0]+off; prev=out[-1][0]
        if lon-prev>180: off-=360; lon-=360
        elif prev-lon>180: off+=360; lon+=360
        out.append([lon,pts[k][1]])
    return out
def clip(ring,X,keep_left):
    """Sutherland-Hodgman clip of a ring against the vertical line lon=X; keep the side asked for."""
    inside=(lambda p:p[0]<=X) if keep_left else (lambda p:p[0]>=X)
    def inter(p,q):
        t=(X-p[0])/(q[0]-p[0]); return [X,p[1]+(q[1]-p[1])*t]
    out=[]
    for i in range(len(ring)):
        p,q=ring[i-1],ring[i]; pin,qin=inside(p),inside(q)
        if qin:
            if not pin: out.append(inter(p,q))
            out.append(q)
        elif pin: out.append(inter(p,q))
    return out if len(out)>=4 else None
def polygons(rings):
    """Decode one polygon (outer ring + holes) into one or two GeoJSON polygons within [-180, 180]."""
    rs=[unwrap(ring(r)) for r in rings]
    lo=min(q[0] for r in rs for q in r); hi=max(q[0] for r in rs for q in r)
    if hi-lo>=350:                                     # Antarctica: spans the whole width, leave it
        return [[[[round(max(-180.0,min(180.0,q[0])),2),q[1]] for q in r] for r in rs]]
    if hi>180 or lo<-180:
        X=180.0 if hi>180 else -180.0; shift=-360.0 if hi>180 else 360.0
        a=[clip(r,X,True) if X>0 else clip(r,X,False) for r in rs]
        b=[clip(r,X,False) if X>0 else clip(r,X,True) for r in rs]
        b=[[[q[0]+shift,q[1]] for q in r] for r in b if r]
        a=[r for r in a if r]
        outp=[]
        for poly in (a,b):
            if poly: outp.append([[[round(max(-180.0,min(180.0,q[0])),2),round(q[1],2)] for q in r] for r in poly])
        return outp
    return [[[[round(q[0],2),q[1]] for q in r] for r in rs]]
feats=[]
for g in topo['objects']['countries']['geometries']:
    gid=str(int(g['id'])) if g.get('id') else None; name=g['properties']['name']
    polys=[g['arcs']] if g['type']=='Polygon' else g['arcs']
    coords=[q for poly in polys for q in polygons(poly)]
    geom={'type':'Polygon','coordinates':coords[0]} if len(coords)==1 else {'type':'MultiPolygon','coordinates':coords}
    feats.append({'type':'Feature','id':gid,'properties':{'name':name},'geometry':geom})
json.dump({'type':'FeatureCollection','features':feats},open(root/'geo.json','w'),separators=(',',':'))
countries=[l for l in out['locations'] if l['type']=='country']
ids={l['id'] for l in countries}
print('locations',len(out['locations']),'countries',len(countries),'| geo features',len(feats),'matched',sum(1 for x in feats if x['id'] in ids),
      '| data.json',round((root/'data.json').stat().st_size/1024),'KB | geo.json',round((root/'geo.json').stat().st_size/1024),'KB')
print('unmatched:',[(x['id'],x['properties']['name']) for x in feats if x['id'] not in ids])
