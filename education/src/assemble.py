#!/usr/bin/env python3
"""Assemble src/data.json for The Report Card from the raw pulls in src/raw/."""
import csv, json, re, html, pathlib, datetime, statistics
root = pathlib.Path(__file__).parent; raw = root/'raw'
OECD = {'AUS','AUT','BEL','CAN','CHL','COL','CRI','CZE','DNK','EST','FIN','FRA','DEU','GRC','HUN','ISL','IRL','ISR','ITA','JPN','KOR','LVA','LTU','LUX','MEX','NLD','NZL','NOR','POL','PRT','SVK','SVN','ESP','SWE','CHE','TUR','GBR','USA'}
NAMES = {'United States':'United States','Korea':'South Korea','Republic of Korea':'South Korea','Korea, Rep.':'South Korea','Hong Kong':'Hong Kong','Hong Kong SAR, China':'Hong Kong','Macao':'Macao','Macao SAR, China':'Macao','Russia':'Russia','Russian Federation':'Russia','Turkey':'Türkiye','Turkiye':'Türkiye','Slovakia':'Slovakia','Slovak Republic':'Slovakia','Czechia':'Czechia','Czech Republic':'Czechia','OECD members':'OECD average'}

# ---- PISA: {subject: {entity: {year: score}}}
pisa = {}
for subj, fn in (('math','pisa_math.csv'), ('reading','pisa_reading.csv')):
    d = {}
    for r in csv.DictReader(open(raw/fn, encoding='utf-8')):
        name = NAMES.get(r['entity'], r['entity']); code = r['code'] or ('OECD' if name=='OECD average' else '')
        if not code or code.startswith('OWID'): 
            if name != 'OECD average': continue
        d.setdefault(name, {'code': code, 'oecd': code in OECD, 'scores': {}})['scores'][int(r['year'])] = round(float(r[[k for k in r if k.startswith('pisa_')][0]]), 1)
    pisa[subj] = d
sci = {}
for r in json.load(open(raw/'pisa_science_wb.json'))[1]:
    if r['value'] is None: continue
    name = NAMES.get(r['country']['value'], r['country']['value']); code = r['countryiso3code'] or ('OECD' if name=='OECD average' else '')
    if not code and name != 'OECD average': continue
    sci.setdefault(name, {'code': code, 'oecd': code in OECD, 'scores': {}})['scores'][int(r['date'])] = round(r['value'], 1)
# the World Bank mirror carries the OECD average only for 2018; compute it from members for the other years
for y in sorted({y for e in sci.values() for y in e['scores']}):
    vals = [e['scores'][y] for n, e in sci.items() if e['oecd'] and y in e['scores']]
    if len(vals) >= 25 and y not in sci.setdefault('OECD average', {'code':'OECD','oecd':False,'scores':{}})['scores']:
        sci['OECD average']['scores'][y] = round(statistics.mean(vals), 1)
pisa['science'] = sci
# ---- OECD's own trend tables from PISA 2025 Results Volume I, Annex B1 (Tables I.B1.2a.36-38): the official
# rescaled series for every round, all three subjects, through 2025. Primary where present; OWID / World Bank fill the rest.
OECD_NAMES = {'Korea':'South Korea','Chinese Taipei':'Taiwan','Hong Kong (China)':'Hong Kong','Macao (China)':'Macao','Slovak Republic':'Slovakia',
              'Viet Nam':'Vietnam','B-S-J-Z (China)':'China (B-S-J-Z)','Palestinian Authority':'Palestine','United Kingdom':'United Kingdom'}
SKIP = {'OECD average-23','OECD average-35'}
pisaMeta = {'latestRound': None, 'caution': {}}
try:
    import openpyxl
    wb = openpyxl.load_workbook(raw/'pisa2025_tables.xlsx', read_only=True, data_only=True)
    for subj, sheet in (('science','Table I.B1.2a.36'), ('reading','Table I.B1.2a.37'), ('math','Table I.B1.2a.38')):
        rows = list(wb[sheet].iter_rows(values_only=True))
        hdr = next(r for r in rows if r and any(isinstance(c, str) and c.startswith('PISA 20') for c in r))
        cols = [(i, int(c[5:9])) for i, c in enumerate(hdr) if isinstance(c, str) and c.startswith('PISA 20') and 'PISA' not in c[9:]]
        codes = {NAMES.get(n, n): e['code'] for n, e in pisa[subj].items()}
        for r in rows:
            if not r or not isinstance(r[0], str): continue
            name = r[0].strip()
            if name in SKIP or len(name) > 40 or name.startswith(('Notes','Information','1.')): continue
            flag = name.endswith('*'); name = name.rstrip('*').strip(); name = OECD_NAMES.get(name, NAMES.get(name, name))
            vals = {y: r[i] for i, y in cols if isinstance(r[i], (int, float))}
            if not vals: continue
            e = pisa[subj].setdefault(name, {'code': codes.get(name, ''), 'oecd': codes.get(name, '') in OECD, 'scores': {}})
            if name == 'OECD average':
                # keep the OECD's per-round average for earlier rounds; take the new round from this table
                latest = max(vals); e['scores'][latest] = round(vals[latest], 1)
            else:
                for y, v in vals.items(): e['scores'][y] = round(v, 1)
            if flag: pisaMeta['caution'].setdefault(name, []).append(subj)
            pisaMeta['latestRound'] = max(pisaMeta['latestRound'] or 0, max(vals))
    print('OECD 2025 tables merged; latest round', pisaMeta['latestRound'], '| flagged', len(pisaMeta['caution']))
except Exception as ex:
    print('OECD 2025 tables not used:', ex)

# any round where the OECD average is missing but 30+ members have a score: mean of members (marked in the notes)
for subj in pisa:
    oa = pisa[subj].setdefault('OECD average', {'code':'OECD','oecd':False,'scores':{}})
    for y in sorted({y for e in pisa[subj].values() for y in e['scores']}):
        vals = [e['scores'][y] for n, e in pisa[subj].items() if e['oecd'] and y in e['scores']]
        if len(vals) >= 30 and y not in oa['scores']: oa['scores'][y] = round(statistics.mean(vals), 1)
for subj in pisa:
    for e in pisa[subj].values(): e['scores'] = [[y, s] for y, s in sorted(e['scores'].items())]

# ---- NAEP: {series: [[year, score], ...]}
naep = {k: [[int(y), v] for y, v in sorted(d.items(), key=lambda kv: int(kv[0]))] for k, d in json.load(open(raw/'naep.json')).items()}

# ---- NCES per-pupil current expenditure, fall enrollment, constant dollars
s = open(raw/'nces_236_55.html', encoding='iso-8859-1').read()
base = re.search(r'Constant (\d{4}-\d{2}) dollars', s).group(1)
spend = []
for row in re.findall(r'<tr[^>]*>(.*?)</tr>', s, flags=re.S):
    cells = [html.unescape(re.sub(r'<[^>]+>', '', c)).strip() for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', row, flags=re.S)]
    if not cells or not re.match(r'^(19|20)\d\d-\d\d', cells[0]): continue
    nums = [int(c.replace('$','').replace(',','')) for c in cells[1:] if re.match(r'^\$?[\d,]{2,}$', c)]
    if len(nums) >= 8: spend.append([int(cells[0][:4]) + 1, nums[7]])   # school year 2020-21 -> 2021; column 8 = current exp., fall enrollment, constant $
spend.sort()

# ---- OECD per-student spending, latest year with broad coverage, plus the US series
rows = [r for r in csv.DictReader(open(raw/'oecd_perstud.csv', encoding='utf-8')) if r['OBS_VALUE']]
by = {}
for r in rows: by.setdefault(r['REF_AREA'], {})[int(r['TIME_PERIOD'])] = round(float(r['OBS_VALUE']))
years = sorted({y for d in by.values() for y in d})
latest = max(y for y in years if sum(1 for c in OECD if y in by.get(c, {})) >= 30 and y in by.get('USA', {}))
oecd_spend = sorted(([c, by[c][latest]] for c in OECD if latest in by.get(c, {})), key=lambda x: -x[1])
oecd_spend_year = latest

out = {'retrieved': datetime.date.today().isoformat(), 'pisa': pisa, 'pisaMeta': pisaMeta, 'naep': naep,
       'spend': {'series': spend, 'base': base, 'source': 'NCES Digest of Education Statistics, table 236.55'},
       'oecdSpend': {'year': oecd_spend_year, 'rows': oecd_spend, 'unit': 'USD PPP per student, constant 2020 prices, primary to post-secondary non-tertiary'}}
json.dump(out, open(root/'data.json', 'w'), separators=(',', ':'), ensure_ascii=False)
us = pisa['math']['United States']['scores']; oa = pisa['math']['OECD average']['scores']
print('pisa math entities', len(pisa['math']), 'US', us[0], us[-1], '| OECD avg', oa[0], oa[-1], '| science years', sorted({y for e in sci.values() for y,_ in e['scores']}))
print('naep', {k: (v[0], v[-1]) for k, v in naep.items()})
print('spend', spend[0], spend[-1], 'base', base, '| oecd spend', oecd_spend_year, oecd_spend[:3], 'US rank', [c for c,_ in oecd_spend].index('USA')+1, 'of', len(oecd_spend))
print('data.json', round((root/'data.json').stat().st_size/1024), 'KB')
