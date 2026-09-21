#!/bin/bash
# Re-fetch the raw sources for The Report Card into src/raw/ (git-ignored), then assemble src/data.json.
set -uo pipefail
cd "$(dirname "$0")"; mkdir -p raw && cd raw
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
get(){ curl -sL --retry 2 -A "$UA" -o "$2.tmp" "$1" && [ -s "$2.tmp" ] && mv "$2.tmp" "$2" && echo "ok  $2" || { rm -f "$2.tmp"; echo "KEPT $2 (fetch failed)"; }; }

# PISA mean scores, all countries and the OECD average (OECD via Our World in Data)
get "https://ourworldindata.org/grapher/pisa-test-score-mean-performance-on-the-mathematics-scale.csv?v=1&csvType=full&useColumnShortNames=true" pisa_math.csv
get "https://ourworldindata.org/grapher/pisa-test-score-mean-performance-on-the-reading-scale.csv?v=1&csvType=full&useColumnShortNames=true" pisa_reading.csv
# PISA science (World Bank EdStats mirror of OECD; runs through 2018)
get "https://api.worldbank.org/v2/country/all/indicator/LO.PISA.SCI?format=json&per_page=30000" pisa_science_wb.json
# OECD PISA 2025 Results Volume I, Annex B1 chapter 2 tables (StatLink), trend tables through 2025
get "https://stat.link/files/73451bc5-en/mrq53f.xlsx" pisa2025_tables.xlsx
# NCES Digest table 236.55, expenditure per pupil (newest edition that exists wins)
for ed in d25 d24 d23; do
  if curl -sL -A "$UA" -o nces.tmp "https://nces.ed.gov/programs/digest/${ed}/tables/dt${ed#d}_236.55.asp" && grep -q "Expenditure per pupil" nces.tmp; then mv nces.tmp nces_236_55.html; echo "ok  nces_236_55.html ($ed)"; break; fi
done; rm -f nces.tmp
# OECD expenditure per student, primary to post-secondary, constant USD PPP
get "https://sdmx.oecd.org/public/rest/data/OECD.EDU.IMEP,DSD_EAG_UOE_FIN@DF_UOE_INDIC_FIN_PERSTUD,3.2/.FIN_PERSTUD.ISCED11_1T4._T.INST_EDU.NORD.Q.USD_PPP_ST.?format=csvfilewithlabels&startPeriod=1995" oecd_perstud.csv
# NAEP main assessments, national public, mean scale score, one request per year (the API rejects year lists)
python3 - <<'PY'
import json,subprocess,os
UA=os.environ.get('UA','Mozilla/5.0 (Plotline)')
def get(subject,grade,subscale,y,stat='MN:MN'):
    for suf in ('','R3','R2'):
        u=f"https://www.nationsreportcard.gov/DataService/GetAdhocData.aspx?type=data&subject={subject}&grade={grade}&subscale={subscale}&variable=TOTAL&jurisdiction=NP&stattype={stat}&Year={y}{suf}"
        s=subprocess.run(['curl','-sL','-A',UA,u],capture_output=True,text=True).stdout
        try:
            d=json.loads(s)
            if d.get('status')==200 and d['result']: return round(d['result'][0]['value'],1)
        except Exception: pass
    return None
def getmulti(subject,grade,subscale,y,variable,stat,key):
    for suf in ('','R3','R2'):
        u=f"https://www.nationsreportcard.gov/DataService/GetAdhocData.aspx?type=data&subject={subject}&grade={grade}&subscale={subscale}&variable={variable}&jurisdiction=NP&stattype={stat}&Year={y}{suf}"
        s=subprocess.run(['curl','-sL','-A',UA,u],capture_output=True,text=True).stdout
        try:
            d=json.loads(s)
            if d.get('status')==200 and d['result']: return {r[key]:round(r['value'],1) for r in d['result'] if r.get('value') is not None and r[key]!='Information not available' and r[key]!='Unknown'}
        except Exception: pass
    return None
years=[1990,1992,1994,1996,1998,2000,2002]+list(range(2003,2020,2))+[2022,2024,2026,2028,2030]
out={}
for subject,subscale in (('mathematics','MRPCM'),('reading','RRPCM')):
    for grade in (4,8):
        res={y:get(subject,grade,subscale,y) for y in years}
        out[f'{subject}{grade}']={y:v for y,v in res.items() if v is not None}
        prof={y:get(subject,grade,subscale,y,'ALC:AP') for y in out[f'{subject}{grade}']}   # percent at or above Proficient
        out[f'{subject}{grade}_prof']={y:v for y,v in prof.items() if v is not None}
        # breakdowns, 2013 on: percentiles, parents' education (grade 8 only), school-lunch eligibility (served through 2022)
        yrs=[y for y in out[f'{subject}{grade}'] if y>=2013]
        out[f'{subject}{grade}_pct']={y:v for y in yrs if (v:=getmulti(subject,grade,subscale,y,'TOTAL','PC:P1,PC:P2,PC:P5,PC:P7,PC:P9','stattype'))}
        out[f'{subject}{grade}_lunch']={y:v for y in yrs if (v:=getmulti(subject,grade,subscale,y,'SLUNCH3','MN:MN','varValueLabel'))}
        if grade==8: out[f'{subject}{grade}_pared']={y:v for y in yrs if (v:=getmulti(subject,grade,subscale,y,'PARED','MN:MN','varValueLabel'))}
old=json.load(open('naep.json')) if os.path.exists('naep.json') else {}
if sum(len(v) for v in out.values())>=sum(len(v) for v in old.values()): json.dump(out,open('naep.json','w')); print('ok  naep.json',{k:len(v) for k,v in out.items()})
else: print('KEPT naep.json (fewer rows came back)')
PY
echo "fetched $(date -u +%F)"
cd .. && python3 assemble.py
