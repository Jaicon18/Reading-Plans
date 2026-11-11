"""Grand Kia U-142: every schedule material -> its Material Summary row or out of scope with its printed reason.
1) the per-type texts name the stud size of the type (A550 keynotes 5 / 8 / 12 / 13: A/B/G 3-5/8", C/D/H 6", E 8", F 2-1/2")
   so the track / stud material maps to the row of that size;
2) entrega.json schedules_ms {regex: MS row} / schedules_fuera {regex: reason} (first match wins, ordered most specific first)."""
import json, re
W = '/root/gk/work'
SZ = {}
for f in ('indep/fichas.json', 'indep/fichas_prepos.json'):
    F = json.load(open(f'{W}/{f}'))
    for k, t in F['types'].items():
        m = re.match(r'\s*([\d\-/]+")', str(t.get('stud') or ''))
        if not m:
            continue
        SZ[k] = m.group(1)
        tr = str(t.get('track') or '')
        if tr and not tr.startswith(m.group(1)):
            t['track'] = f'{m.group(1)} track (type {k}): {tr}'
    json.dump(F, open(f'{W}/{f}', 'w'), indent=1, ensure_ascii=False)
for f in ('indep/schedules_indep.json', 'indep/schedules_indep_prepos.json'):
    S = json.load(open(f'{W}/{f}'))
    for r in S['schedules'][0]['rows']:
        sz = SZ.get(str(r['id']))
        if not sz:
            continue
        r['trade_items'] = [(f'{sz} {x}' if x in ('metal studs+tracks', 'deflection track 13/A540', 'top track') else x) for x in r.get('trade_items') or []]
    json.dump(S, open(f'{W}/{f}', 'w'), indent=1, ensure_ascii=False)
ROWS = {'3-5/8"': ('3-5/8" metal stud (LF of material)', 'Top slip / deflection track 3-5/8"', 'Top track 3-5/8" - standard'),
        '6"': ('6" metal stud (LF of material)', 'Top slip / deflection track 6"', 'Top track 6" - standard'),
        '8"': ('8" stud (all gauges)', 'Top slip / deflection track 8"', 'Top slip / deflection track 8"'),
        '2-1/2"': ('2-1/2" stud', 'Top slip / deflection track 2-1/2"', 'Top track 2-1/2" - standard')}
MS = {}
for sz, (stud, defl, top) in ROWS.items():
    e = re.escape(sz)
    MS[f'^{e} track \\(type \\w+\\): Top:? deflection'] = defl
    MS[f'^{e} track \\(type \\w+\\): Top track at ceiling'] = top
    MS[f'^{e} metal studs\\+tracks$'] = stud
    MS[f'^{e} deflection track 13/A540$'] = defl
    MS[f'^{e} top track$'] = top
MS.update({
    r'1-1/2" CRC bridging|mid-height 1-1/2" channel': 'Bracing 1-1/2" C.R. channel',
    r'(?i)control joint|USG 093': 'Control joint, gypsum board',
    r'(?i)\bL5\b': 'Level 5 finish',
    r'(?i)^L4|finish L2|L4 finish': 'Joint compound, all purpose',
    r'(?i)dens ?shield': '5/8" glass mat water-resistant tile backer',
    r'(?i)drywall grid|suspended gyp bd ceiling system|gyp bd on suspended ceiling framing': 'USG drywall suspension main tee',
    r'(?i)access panels': 'Access panel 30"x30"',
    r'(?i)S403 241-244, 1000S162-43': '10" metal stud (LF of material)',
    r'(?i)CFS soffit framing \(structural': '3-5/8" metal stud (LF of material) - 362S162-33',
    r'(?i)HM frame in metal stud wall': '3-5/8" metal stud (LF of material)',
    r'(?i)Alum frame in stud wall': 'METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim - J molding',
    r'(?i)14 GA deep-leg': 'Top slip / deflection track 3-5/8"',
    r'(?i)bottom track shot pins': 'Power-driven fasteners, slab pins for the bottom track',
    r'(?i)diag brace': 'Metal stud brace to structure',
    r'(?i)metal corner bead': 'METAL trim - corner bead, casing bead, shadow molding, gypsum edge trim - corner bead',
    r'(?i)metal track, gyp bd ceiling on framing': 'Ceiling / soffit track',
    r'(?i)Hilti SDM 20 PDF': 'Power-driven fasteners and duct sleeves',
    r'(?i)BOT\. OF GYP\. BD\.|angled gyp/framing|metal stud framing \(see struct\)|metal stud \+ gyp bd backing|metal stud framing \+ gyp bd, Fry': '5/8" gypsum board, regular',
    r'(?i)gauge deferred to drawings': '3-5/8" metal stud (LF of material)',
    r'(?i)drawings show 1/2" glass mat sheathing': '1/2" EXTERIOR gypsum sheathing',
})
FU = {
    r'(?i)^Fry Reglet': "Fry Reglet 'F' reveal supplied with the ACR-1 Fry package (A140: ACR-1 'TO BE SOURCED FROM FRY REGLET INCLUSIVE WITH GRAPH SYSTEM'); Review Item RI-30",
    r'(?i)ACT - not drywall|^not drywall$': 'acoustical ceiling tile ACT-1, other trade, ACT package (ACT section not in this spec book)',
    r'(?i)^base only': 'tile base, tile trade (tile section not in this spec book); a 4" base prints no tile backer board',
    r'(?i)FRP by': 'FRP panels, spec 06 64 00 (by others); the gyp bd substrate behind them is carried by its wall type',
    r'(?i)ACM-1|by others \[DERIVED from spec TOC\]': "ACM-1 metal composite panels (A111 keynote 41: 'ACM CLADDING BY PATTISON SIGN GROUP'), not framing / drywall",
    r'(?i)No rated metal stud / gypsum assembly': 'informational row: no rated metal stud / gyp bd assembly is drawn (47/A551 U906 is the CMU wall, by others)',
    r'(?i)patch existing gyp ceiling': 'patch of existing gyp bd ceilings (A131 keynotes 21 / 30): extent not printed, not quantified; estimator allowance (Review Item)',
}
E = json.load(open(f'{W}/entrega.json'))
E['schedules_ms'] = MS; E['schedules_fuera'] = FU
json.dump(E, open(f'{W}/entrega.json', 'w'), indent=1, ensure_ascii=False)
print(len(MS), 'ms patterns,', len(FU), 'out-of-scope patterns; sizes', SZ)
