#!/usr/bin/env python3
"""Build index.html (standalone, with CSV download) and artifact.html (for claude.ai artifacts)
from src/template.html + src/data.json."""
import json, datetime as dt, pathlib
root = pathlib.Path(__file__).parent
d = json.load(open(root/'src/data.json'))
epoch = dt.date(1993,4,1)
rows=[]
for r in d['raw']:
    day=(dt.date.fromisoformat(r[0])-epoch).days
    tot=round(float(r[1])/1e9,3)
    pub=None if r[2] is None else round(float(r[2])/1e9,3)
    itg=None if r[3] is None else round(float(r[3])/1e9,3)
    rows.append([day,tot,pub,itg])
last=d['raw'][-1]
payload={
  'epoch':epoch.isoformat(),
  'rows':rows,
  'last':{'date':last[0],'total':float(last[1]),'public':float(last[2]),'intra':float(last[3])},
  'events':[{'date':e[0],'name':e[1],'title':e[2],'text':e[3],'url':e[4]} for e in d['events']],
  'unemployment':d['employment'],'inflation':d['inflation'],'fedfunds':d['interest'],
  'terms':[['Bill Clinton','Clinton','1993-01-20','2001-01-20'],['George W. Bush','G.W. Bush','2001-01-20','2009-01-20'],['Barack Obama','Obama','2009-01-20','2017-01-20'],['Donald Trump (first term)','Trump I','2017-01-20','2021-01-20'],['Joe Biden','Biden','2021-01-20','2025-01-20'],['Donald Trump (second term)','Trump II','2025-01-20',None]],
  'retrieved':'2026-09-20',
  'gdp':[[r.split(',')[0],float(r.split(',')[1])] for r in open(root/'src/gdp.csv').read().strip().split('\n')[1:] if r.split(',')[0]>='1992-10-01' and r.split(',')[1] not in ('','.')],
}
js='const DATA='+json.dumps(payload,separators=(',',':'))+';'
tpl=open(root/'src/template.html').read()
assert '/*__DATA__*/' in tpl
full=tpl.replace('/*__DATA__*/',js)
open(root/'index.html','w').write('<!doctype html><html lang="en"><head>'+full.split('<!--HEAD-->')[1].split('<!--/HEAD-->')[0]+'</head><body>'+full.split('<!--BODY-->')[1].split('<!--/BODY-->')[0]+'</body></html>')
art=full.replace('<!--HEAD-->','').replace('<!--/HEAD-->','').replace('<!--BODY-->','').replace('<!--/BODY-->','')
art=art.replace('<!--DOWNLOAD-->','').replace('<!--/DOWNLOAD-->','')
# strip the download control for the artifact build (viewer sandbox blocks page-initiated downloads)
import re
art=re.sub(r'<!--DL-->.*?<!--/DL-->','',art,flags=re.S)
art=re.sub(r"const dl=\$\('#download'\);.*?\n",'',art,flags=re.S)  # no page-initiated downloads in the artifact build
open(root/'artifact.html','w').write(art)
print('index.html',len(open(root/'index.html').read())//1024,'KB; artifact.html',len(art)//1024,'KB')
