#!/usr/bin/env python3
"""Assemble src/data.json for The Curve from the raw sources in src/raw/ (see fetch.sh).

Layers
  transistors : named CPU/GPU chips, transistor count by year (Wikipedia "Transistor count")
  compute     : notable AI models, training compute in FLOP (Epoch AI notable_ai_models)
  params      : the same models' parameter counts where published
  hardware    : peak per-accelerator dense FP16/BF16 FLOP/s by release year (Epoch AI ml_hardware)
  benchmarks  : running-best frontier score over time per benchmark (Epoch AI Benchmarking Hub)
"""
import csv, json, re, datetime as dt, pathlib, collections
from html.parser import HTMLParser

root = pathlib.Path(__file__).parent
raw = root / 'raw'
out = {'retrieved': dt.date.today().isoformat(), 'sources': {}}

# ---------- transistors (Wikipedia) ----------
class TP(HTMLParser):
    def __init__(s):
        super().__init__(); s.tables=[]; s.cur=None; s.row=None; s.cell=None
    def handle_starttag(s,t,a):
        if t=='table': s.cur=[]
        elif t=='tr' and s.cur is not None: s.row=[]
        elif t in('td','th') and s.row is not None: s.cell=''
        elif t=='br' and s.cell is not None: s.cell+=' '
        elif t=='sup' and s.cell is not None: s.cell+='<sup>'
    def handle_endtag(s,t):
        if t in('td','th') and s.row is not None and s.cell is not None: s.row.append(re.sub(r'\s+',' ',s.cell).strip()); s.cell=None
        elif t=='tr' and s.cur is not None and s.row is not None:
            if s.row: s.cur.append(s.row)
            s.row=None
        elif t=='table' and s.cur is not None: s.tables.append(s.cur); s.cur=None
        elif t=='sup' and s.cell is not None: s.cell+='</sup>'
    def handle_data(s,d):
        if s.cell is not None: s.cell+=d
def clean(x): return re.sub(r'<sup>.*?</sup>','',x).replace(' ','').strip()
def num(x):
    x=clean(x).replace(',','').replace('~','').replace('+','')
    m=re.search(r'([\d.]+)\s*(trillion|billion|million|thousand)?',x,re.I)
    if not m: return None
    v=float(m.group(1)); u=(m.group(2) or '').lower()
    return v*{'trillion':1e12,'billion':1e9,'million':1e6,'thousand':1e3}.get(u,1)
def year(x):
    m=re.search(r'(19|20)\d\d',clean(x)); return int(m.group(0)) if m else None
def short_chip(name):
    # "Intel 80486 (32-bit, 8 KB cache)" -> "Intel 80486"
    return re.sub(r'\s*\(.*$','',name).strip()

p=TP(); p.feed(open(raw/'wiki_transistor_count.html',encoding='utf-8').read())
tables=[t for t in p.tables if len(t)>50 and clean(t[0][0])=='Processor']
chips=[]
for t,kind in zip(tables[:2],['cpu','gpu']):
    for row in t[1:]:
        if len(row)<4: continue
        c=num(row[1]); y=year(row[2])
        if not c or not y: continue
        chips.append({'name':short_chip(clean(row[0])),'full':clean(row[0]),'count':c,'year':y,'designer':clean(row[3]),'kind':kind})
chips.sort(key=lambda r:(r['year'],r['count']))
# frontier per year (max count that year across both kinds), plus keep every chip for hover
out['transistors']={'chips':chips,'note':'Per-chip transistor counts from public specifications as compiled on Wikipedia "Transistor count" (CPUs/SoCs and GPUs); the frontier line follows the highest count released each year.'}
out['sources']['transistors']='https://en.wikipedia.org/wiki/Transistor_count'

# ---------- AI models (Epoch) ----------
def fnum(x):
    try: return float(x)
    except: return None
models=[]
for r in csv.DictReader(open(raw/'notable_ai_models.csv',encoding='utf-8')):
    d=r['Publication date']; c=fnum(r['Training compute (FLOP)']); pcount=fnum(r['Parameters'])
    if not d or (c is None and pcount is None): continue
    models.append({'name':r['Model'],'org':r['Organization'],'date':d,'domain':r['Domain'],
                   'compute':c,'params':pcount,'confidence':r['Confidence'],'frontier':r.get('Frontier model','')=='True',
                   'country':r['Country (of organization)'],'access':r['Model accessibility'],'link':r['Link']})
models.sort(key=lambda m:m['date'])
out['models']=models
out['sources']['models']='https://epoch.ai/data/notable-ai-models'

# ---------- hardware (Epoch) ----------
hw=[]
for r in csv.DictReader(open(raw/'ml_hardware.csv',encoding='utf-8')):
    d=r['Release date']; f=fnum(r['Tensor-FP16/BF16 performance (FLOP/s)']) or fnum(r['FP32 (single precision) performance (FLOP/s)'])
    if not d or not f: continue
    hw.append({'name':r['Hardware name'],'maker':r['Manufacturer'],'date':d,'flops':f,'transistors':(fnum(r['Transistors (millions)']) or 0)*1e6 or None,'tdp':fnum(r['TDP (W)'])})
hw.sort(key=lambda h:h['date'])
out['hardware']=hw
out['sources']['hardware']='https://epoch.ai/data/machine-learning-hardware'

# ---------- benchmarks (Epoch Benchmarking Hub) ----------
bd=raw/'benchmark_data'
meta={r['benchmark']:r for r in csv.DictReader(open(bd/'benchmark_metadata.csv',encoding='utf-8'))}
BENCH=[
 # key, file, score column, metadata name, display, domain, scale note
 ('mmlu','mmlu_external.csv','EM','MMLU','MMLU','Broad knowledge, 57 subjects',1),
 ('gsm8k','gsm8k_external.csv','EM','GSM8K','GSM8K','Grade-school math',1),
 ('math5','math_level_5.csv','mean_score','MATH level 5','MATH (level 5)','Competition math, hardest tier',1),
 ('gpqa','gpqa_diamond.csv','mean_score','GPQA diamond','GPQA Diamond','PhD-level science questions',1),
 ('aime','otis_mock_aime_2024_2025.csv','mean_score','OTIS Mock AIME 2024-2025','AIME (OTIS mock)','Olympiad-qualifier math',1),
 ('swe','swe_bench_verified.csv','mean_score','SWE-Bench verified','SWE-bench Verified','Real GitHub issues, fixed end to end',1),
 ('arcagi','arc_agi_external.csv','Score','ARC-AGI','ARC-AGI',"Abstract visual puzzles (ARC-AGI-1)",1),
 ('arcagi2','arc_agi_2_external.csv','Score','ARC-AGI-2','ARC-AGI-2','Harder abstract puzzles',1),
 ('hle','hle_external.csv','Accuracy','HLE',"Humanity's Last Exam",'Expert questions across 100+ fields',1),
 ('fm13','frontiermath_tiers_1_3_v2.csv','mean_score','FrontierMath-Tiers-1-3-v2-Private','FrontierMath (tiers 1–3)','Research-level math, unpublished problems',1),
 ('metr','metr_time_horizons_external.csv','Time horizon','METR time horizons','METR 50% time horizon','Length of software task completed half the time (minutes)',None),
]
benchmarks=[]
for key,fname,col,mname,disp,dom,scale in BENCH:
    rows=list(csv.DictReader(open(bd/fname,encoding='utf-8')))
    pts=[]
    for r in rows:
        d=r.get('Release date'); v=fnum(r.get(col))
        if not d or v is None: continue
        name=r.get('Name') or r.get('Model version') or ''
        pts.append({'date':d,'model':r.get('Model version') or name,'display':name,'org':r.get('Organization',''),'score':v})
    pts.sort(key=lambda x:x['date'])
    # running best (frontier) sequence
    best=[]; run=-1e9
    for x in pts:
        if x['score']>run: run=x['score']; best.append(x)
    m=meta.get(mname,{})
    benchmarks.append({'key':key,'name':disp,'domain':dom,'release':m.get('release_date'),'random':fnum(m.get('random_baseline')),'ceiling':fnum(m.get('score_ceiling')),
                       'unit':'minutes' if key=='metr' else 'fraction','points':pts,'frontier':best,'n':len(pts)})
out['benchmarks']=benchmarks
out['sources']['benchmarks']='https://epoch.ai/benchmarks'

json.dump(out,open(root/'data.json','w'),separators=(',',':'))
print('chips',len(chips),'| models',len(models),'| hardware',len(hw),'| benchmarks',[(b['key'],b['n'],len(b['frontier'])) for b in benchmarks])
print('data.json',round((root/'data.json').stat().st_size/1024),'KB')
