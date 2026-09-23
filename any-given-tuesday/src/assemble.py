#!/usr/bin/env python3
"""Assemble src/data.json for Any Given Tuesday from the nflverse weekly injury reports and weekly rosters."""
import csv, json, glob, pathlib, datetime, collections, statistics
root = pathlib.Path(__file__).parent; raw = root/'raw'
FR = {'ARZ':'ARI','BLT':'BAL','CLV':'CLE','HST':'HOU','SL':'LA','STL':'LA','SD':'LAC','OAK':'LV'}   # historical codes -> current franchise
fr = lambda t: FR.get(t, t)
NOT_INJURY = ('illness', 'not injury', 'personal', 'rest', 'resting', 'coach', 'load management', 'suspension')
BODY = {'Knee':'Knee','Ankle':'Ankle','Hamstring':'Hamstring','Concussion':'Concussion','Shoulder':'Shoulder','Calf':'Calf','Foot':'Foot and toe','Toe':'Foot and toe','Heel':'Foot and toe',
        'Neck':'Neck','Groin':'Groin','Quadricep':'Quad and thigh','Thigh':'Quad and thigh','Hip':'Hip','Back':'Back','Achilles':'Achilles',
        'Elbow':'Arm and hand','Hand':'Arm and hand','Wrist':'Arm and hand','Finger':'Arm and hand','Thumb':'Arm and hand','Forearm':'Arm and hand','Biceps':'Arm and hand','Triceps':'Arm and hand','Pectoral':'Chest and ribs','Chest':'Chest and ribs','Ribs':'Chest and ribs','Rib':'Chest and ribs','Oblique':'Core','Abdomen':'Core','Core':'Core'}
POS = {'QB':'QB','RB':'RB','FB':'RB','WR':'WR','TE':'TE','T':'OL','G':'OL','C':'OL','OL':'OL','OT':'OL','OG':'OL','DE':'DL','DT':'DL','NT':'DL','DL':'DL','LB':'LB','ILB':'LB','OLB':'LB','MLB':'LB','CB':'DB','S':'DB','FS':'DB','SS':'DB','DB':'DB','SAF':'DB','K':'ST','P':'ST','LS':'ST','KR':'ST','PR':'ST'}
def body(s):
    s = (s or '').strip(); k = s.split('/')[0].split(',')[0].strip().title()
    return BODY.get(k, 'Other' if s else 'Unspecified')
def is_injury(s):
    s = (s or '').lower(); return not any(k in s for k in NOT_INJURY)

teams = {r['team_abbr']: {'name': r['team_name'], 'nick': r['team_nick'], 'color': r['team_color'], 'color2': r['team_color2'], 'div': r['team_division']} for r in csv.DictReader(open(raw/'teams.csv'))}
teams = {t: v for t, v in teams.items() if t not in FR and t != 'LAR'}   # LAR duplicates LA in the colours file

seasons = {}
lost = collections.defaultdict(set)      # (season, team) -> {(player, week)}
outset = collections.defaultdict(set)    # Out on the weekly report
resset = collections.defaultdict(set)    # on a reserve list
types = collections.defaultdict(collections.Counter)   # season -> body part (Out listings)
posc = collections.defaultdict(collections.Counter)    # season -> position group (lost player-weeks)
tteam = collections.defaultdict(collections.Counter)   # (season, team) -> body part
pteam = collections.defaultdict(collections.Counter)   # (season, team) -> position group
weeks = collections.defaultdict(set)
latest = {}
for f in sorted(glob.glob(str(raw/'inj_*.csv'))):
    for r in csv.DictReader(open(f, encoding='utf-8')):
        if r['game_type'] != 'REG': continue
        s, w, t = int(r['season']), int(r['week']), fr(r['team']); weeks[s].add(w)
        if r['report_status'] != 'Out' or not is_injury(r['report_primary_injury']): continue
        key = (r['gsis_id'] or r['full_name'], w); outset[(s, t)].add(key); lost[(s, t)].add(key)
        b = body(r['report_primary_injury']); types[s][b] += 1; tteam[(s, t)][b] += 1
        p = POS.get(r['position'], 'Other'); posc[s][p] += 1; pteam[(s, t)][p] += 1
        latest.setdefault(s, {}).setdefault(w, []).append({'team': t, 'name': r['full_name'], 'pos': r['position'], 'inj': r['report_primary_injury']})
for f in sorted(glob.glob(str(raw/'ros_*.csv'))):
    for r in csv.DictReader(open(f, encoding='utf-8')):
        if r['game_type'] != 'REG' or r['status'] != 'RES': continue
        if r['status_description_abbr'] in ('R59',): continue      # COVID-19 reserve list (2021 on; 2020 cannot be separated)
        s, w, t = int(r['season']), int(r['week']), fr(r['team']); weeks[s].add(w)
        key = (r['gsis_id'] or r['full_name'], w)
        if key in outset[(s, t)]: continue
        resset[(s, t)].add(key); lost[(s, t)].add(key)
        p = POS.get(r['position'], 'Other'); posc[s][p] += 1; pteam[(s, t)][p] += 1

# regular-season records from the nflverse games file
rec = collections.defaultdict(lambda: [0, 0, 0])
for r in csv.DictReader(open(raw/'games.csv', encoding='utf-8')):
    if r['game_type'] != 'REG' or r['home_score'] in ('', 'NA') or int(r['season']) < 2009: continue
    s = int(r['season']); h, a = fr(r['home_team']), fr(r['away_team']); hs, as_ = int(r['home_score']), int(r['away_score'])
    if hs > as_: rec[(s, h)][0] += 1; rec[(s, a)][1] += 1
    elif hs < as_: rec[(s, a)][0] += 1; rec[(s, h)][1] += 1
    else: rec[(s, h)][2] += 1; rec[(s, a)][2] += 1
allseasons = sorted(weeks)
out = {'retrieved': datetime.date.today().isoformat(), 'seasons': [], 'teams': teams,
       'source': 'nflverse weekly injury reports and weekly rosters (CC BY 4.0)'}
for s in allseasons:
    nweeks = max(weeks[s]); T = {}
    for t in teams:
        L = lost[(s, t)]; players = {k[0] for k in L}
        T[t] = {'out': len(outset[(s, t)]), 'res': len(resset[(s, t)]), 'lost': len(L), 'players': len(players), 'rec': rec.get((s, t), [0, 0, 0]),
                'types': dict(tteam[(s, t)].most_common(6)), 'pos': dict(pteam[(s, t)])}
    n = len(teams)
    league = {'out': round(sum(v['out'] for v in T.values())/n, 1), 'res': round(sum(v['res'] for v in T.values())/n, 1),
              'lost': round(sum(v['lost'] for v in T.values())/n, 1), 'players': round(sum(v['players'] for v in T.values())/n, 1)}
    seasons_entry = {'season': s, 'weeks': nweeks, 'complete': s < allseasons[-1] or nweeks >= 18, 'league': league, 'teams': T,
                     'types': dict(types[s].most_common()), 'pos': dict(posc[s])}
    out['seasons'].append(seasons_entry)
cur = allseasons[-1]; filed = [w for w in weeks[cur] if latest.get(cur, {}).get(w)]; cw = max(filed) if filed else max(weeks[cur])   # newest week whose report has been filed
out['latest'] = {'season': cur, 'week': cw, 'outList': sorted(latest.get(cur, {}).get(cw, []), key=lambda x: (x['team'], x['pos']))}
json.dump(out, open(root/'data.json', 'w'), separators=(',', ':'), ensure_ascii=False)
for e in out['seasons']: print(e['season'], 'weeks', e['weeks'], 'league', e['league'], '| NYG', {k: e['teams']['NYG'][k] for k in ('out','res','lost','players')})
print('latest', cur, 'week', cw, len(out['latest']['outList']), 'listed Out;', 'data.json', round((root/'data.json').stat().st_size/1024), 'KB')
