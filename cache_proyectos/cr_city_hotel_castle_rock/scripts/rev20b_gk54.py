"""rev20b (v81cf120 BE-GK54): las exclusiones 'duplicate / same wall as X' llevan gap_proof con N/HOJA y el gap medido en 0 (es la MISMA
línea dibujada: subconjunto del path de X o el mismo jamb). En CR los muros están en existing_walls (no en walls), por eso la compuerta no
puede leer la band de X: la prueba va escrita. NT-L1-02 NO es el mismo muro que NT-L1-01 (otro nicho, mismo motivo): se reescribe el motivo.
Idempotente."""
import json

CP = '/root/cr/work/etapas/4_canon/takeoff_canon.json'
GAP = {
    'FI.2-L1-04': "gap 0\" (1/A7.45): the west part (x 493-810) lies on the same drawn kitchen north furring line as FI.2-L1-03 "
                  "(x 494.5-1203.8, same y); excluded together with it (F&B note, A7.45)",
    'W.6.1-L1-15': "gap 0\" (1/A7.30): same line-3 arched wall D.1-H, drawn once at y 413.85 = W.6-L1-04 path (x 1110.2-1780.3)",
    'W.6.1-L1-16': "gap 0\" (1/A7.30): same line-3 arched wall H-K, drawn once at y 413.85 = W.6-L1-04 path (x 1110.2-1780.3)",
    'FI.2-L1-01': "gap 0\" (1/A7.50): the A7.50 view-limit piece of the grid-14 furring is the same drawn line as FI.2-L1-06 (A2.01 y 1284.65)",
    'FW.2-L4-11': "gap 0\" (11/A6.01): same lobby stair north piece as FW.2-L4-07 (A6.01 y 1119.4, west of door 414.1), re-measured",
    'FW.4-L4-06': "gap 0\" (11/A6.01): same FEC box as FW.4-L4-15 (A6.01 y 1101.4-1122.6), re-measured",
    'W.62-L4-04': "gap 0\" (1/A2.04): same 406 jamb return as W.62-L4-10 (A2.04 x 796.2)",
}
C = json.load(open(CP))
n = 0
for e in C['excluded_walls']:
    if e.get('id') in GAP:
        e['gap_proof'] = GAP[e['id']]; n += 1
    if e.get('id') == 'NT-L1-02' and str(e.get('reason', '')).startswith('same as NT-L1-01'):
        e['reason'] = ("not loaded for the same reason as NT-L1-01 (a separate untagged niche build-out south of Stair 1, A7.30): "
                       "no type on any sheet and no board shown -> RFI-CR-04")
        n += 1
# rev20b (v127 diagnóstico, CB_U_114 / CE_REGLAS R80e.84 / CB_U_184_ELEV): estado de altura de los renglones nuevos = el de su fuente
# (cota impresa -> CONFIRMADO con N/HOJA; calculada -> DERIVADO con su operación) y sin la etiqueta interna 'rev20b' en texto visible.
CONF = {   # id -> fuente impresa (N/HOJA + cota)
    'FW.2-L2-15': "4/A5.05 corridor 9'-10 3/4\" (printed)", 'FW.2-L3-15': "4/A5.05 corridor 9'-10 3/4\" (printed)",
    'FW.2-L3-14': "4/A5.05 9'-2 7/8\" (printed: floor to the underside of the 1'-9 1/8\" FT-1 floor assembly, unit foyer)",
    'XW.6.3-L1-01 S': "1/A7.31 WS-1 11'-0\" ceiling tag at the pier (printed); 1/A5.03 11'-0\" L1 to interior ceiling (printed)",
    'XW.6.3-L1-04 A': "4/A5.05 / 5/A6.02 L1-L2 14'-0\" (printed; exterior sheathing floor to floor)",
}
for lv, h in (('L1', "11/A6.01 L1-L2 14'-0\" (printed, '24 RISERS @ 7\" EACH')"), ('L2', "11/A6.01 L2-L3 11'-0\" (printed, '19 RISERS @ 6.95\" EACH')"),
              ('L3', "11/A6.01 L3-L4 11'-0\" (printed, '19 RISERS @ 6.95\" EACH')")):
    for ld in 'NSEW':
        CONF[f'LIN-127-{lv}-{ld}'] = h
DER = {   # id -> fuente con su operación
    'XW.6.3-L1-04 B': "2/A7.31 + 4/A5.05: 14'-0\" (printed L1-L2) - 1'-11 1/4\" (printed RATED ASSEMBLY) = 12'-0 3/4\" = 12.0625 ft (GYP-1 12'-0 3/4\" tag, A3.01)",
    'XW.6.6-L4-16 B': "1/A5.06 + 04/A9.05 eave, same eave as the twin XW.6.6-L4-15 B: resolved A/B value 9.8444 ft (ALTURAS_AB_RESOLUCION; A 8.9375 / B 10.1875, larger-side twin value)",
}
tw = next((w for w in C['existing_walls'] if w['id'] == 'XW.6.6-L4-15 B'), {})
n2 = 0
for w in C['existing_walls']:
    if w['id'] in CONF:
        w['height_status'] = 'CONFIRMADO'; w['height_source'] = CONF[w['id']]; n2 += 1
    elif w['id'] in DER:
        w['height_status'] = 'DERIVADO'; w['height_source'] = DER[w['id']]; n2 += 1
    if w['id'] == 'XW.6.6-L4-16 B' and tw.get('height_plan_check'):
        w['height_plan_check'] = str(tw['height_plan_check']) + " (same facade line, A2.04 NW corner of 410)"
import re as _re
def _limpia(o):
    if isinstance(o, dict):
        return {k: (v if k == 'rev20b' else _limpia(v)) for k, v in o.items()}
    if isinstance(o, list):
        return [_limpia(x) for x in o]
    if isinstance(o, str) and 'rev20b' in o:
        return _re.sub(r"\s*\brev20b\b:?", " (12-nov coverage review)", o)
    return o
for k in ('existing_walls', 'misc_items', 'ceilings', 'excluded_walls', 'rfis'):
    if k in C:
        C[k] = _limpia(C[k])
print('rev20b_gk54: estado de altura', n2, 'renglones; texto rev20b limpiado')
json.dump(C, open(CP, 'w'), indent=1, ensure_ascii=False)
print('rev20b_gk54:', n, 'exclusiones')
