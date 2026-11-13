"""rev20b (U-176 / BE-CR35): las dos lecturas ciegas H-A / H-B de los renglones nuevos de la revisión de cobertura U-193 (dos subagentes
independientes, registrados en la bitácora como revisor_alturas) se agregan a alturas/A y alturas/B (ALTURAS_IMPRESAS.csv + recortes en img/).
Fuente: auditoria_cobertura_rev20b/alturas_A|B/ALTURAS.csv (copia de lo que entregaron). Idempotente (reemplaza sus renglones por Wall ID).
Si A y B coinciden (<= 0.05 ft) y difieren del canon, el canon toma el valor impreso de los lectores (como rev19 U-176); si A != B se
resuelve en ALTURAS_AB_RESOLUCION.csv con la razón."""
import csv
import json
import os
import re
import shutil

W = '/root/cr/work'
SRC = f'{W}/auditoria_cobertura_rev20b'
CP = f'{W}/etapas/4_canon/takeoff_canon.json'
CAMPOS = ['Wall ID', 'Printed H', 'Source', 'Operation', 'Status', 'Image']
lect = {}
for k in ('A', 'B'):
    f = f'{SRC}/alturas_{k}/ALTURAS.csv'
    rows, vistos = [], set()
    for r in (csv.DictReader(open(f, encoding='utf-8-sig')) if os.path.isfile(f) else []):
        r['Wall ID'] = re.sub(r"\s*\((?:corridor|linen|room|exterior|interior)[^)]*face\)$", "", r['Wall ID'].strip())   # una fila por Wall ID
        if r['Wall ID'] not in vistos:
            vistos.add(r['Wall ID']); rows.append(r)
    dst = f'{W}/alturas/{k}/ALTURAS_IMPRESAS.csv'
    base = list(csv.DictReader(open(dst, encoding='utf-8-sig')))
    ids = {r['Wall ID'] for r in rows}
    base = [r for r in base if r['Wall ID'] not in ids]
    for r in rows:
        im = os.path.basename(str(r.get('Image') or ''))
        if im and os.path.isfile(f'{SRC}/alturas_{k}/{im}'):
            shutil.copy2(f'{SRC}/alturas_{k}/{im}', f'{W}/alturas/{k}/img/{im}')
        base.append({c: (f'img/{im}' if c == 'Image' and im else r.get(c, '')) for c in CAMPOS})
    with open(dst, 'w', newline='', encoding='utf-8-sig') as fo:
        wr = csv.DictWriter(fo, fieldnames=CAMPOS, extrasaction='ignore'); wr.writeheader(); wr.writerows(base)
    lect[k] = {r['Wall ID']: r for r in rows}
C = json.load(open(CP))
cambios = []
for w in C['existing_walls']:
    a, b = lect.get('A', {}).get(w['id']), lect.get('B', {}).get(w['id'])
    if not (a and b):
        continue
    ha, hb = float(a['Printed H']), float(b['Printed H'])
    if abs(ha - hb) <= 0.05 and abs(ha - float(w['height_ft'])) > 0.05:
        cambios.append((w['id'], w['height_ft'], ha))
        w['height_note'] = (f"U-176 rev20b: both blind readers agree on {ha:.4f} ({a['Source'][:120]}); canon had {w['height_ft']}: changed to "
                            f"the readers' printed value | " + str(w.get('height_note') or ''))[:1500]
        w['height_ft'] = round(ha, 4)
        w['height_source'] = a['Source']
# A != B (> 0.05 ft): resolución con su razón (U-176), en alturas/ALTURAS_AB_RESOLUCION.csv; el canon queda como dice 'Printed H'
RESOL = {
    'FW.2-L2-15': (9.8958, "A 9.2396 (18\" truss zone 1'-9 1/8\") / B 9.8958 (corridor joist zone 1'-1 1/4\"): this face is the CORRIDOR 218 face of the "
                   "stair at the corridor strip grid 13-14 (same zone as UNTYPED-L2-12, 4/A5.05 9'-10 3/4\"); larger printed value taken (U-146): canon kept"),
    'FW.2-L3-15': (9.8958, "A 9.2396 / B 9.8958: corridor 318 face, same corridor strip as FW.2-L2-15 (4/A5.05 9'-10 3/4\"): larger printed value (U-146), canon kept"),
    'FW.2-L3-14': (9.2396, "A 9.2396 (unit foyer under FT-1 18\" trusses, A7.05 unit note 1 = bottom of the floor / ceiling assembly) / B 9.8958 "
                   "(corridor zone): this piece is INSIDE guest room 309 (mirror of FW.2-L2-14 = 9.2396): reader A + the L2 twin, canon kept"),
    'XW.6.6-L4-16 B': (9.8444, "A 8.9375 (1/A5.03 underside of roof at grids 5.2-6) / B 10.1875 (A4.00 eave dims to the drip line): the exterior "
                       "sheathing face runs into the same 04/A9.05 eave as XW.6.6-L4-15 B next to it (rev19 A/B 9.8015 / 9.8444 resolved 9.8444): "
                       "value of the twin, inside the A-B range, canon kept"),
    'XW.6.3-L1-04 A': (14.0, "A 8.0000 (unlabeled 8'-0\" in 5/A6.02 = door-head line, reader flags it) / B 14.0000 (5/A6.02 + 4/A5.05 L1-L2 14'-0\"): "
                       "exterior sheathing runs floor to floor like XW.6.3-L1-03 A (14.0): B + twin, canon kept"),
    'XW.6.3-L1-04 B': (12.0625, "A 8.0000 (unlabeled 8'-0\" in 5/A6.02) / B 12.1146 (3/A5.03 to underside of the L2 assembly, other location): "
                       "interior face as the twin XW.6.3-L1-03 B (A3.01 / A7.31 GYP-1 12'-0 3/4\" under the FS-1 membrane), canon kept"),
}
for _l in ('N', 'S', 'E', 'W'):
    RESOL[f'LIN-127-L4-{_l}'] = (10.51, "A 10.5521 (11/A6.01 lining to the underside of the roof sheathing, by scale) / B 8.9375 (1/A5.06 west alley "
                                 "wall, underside of roof framing): the lining runs up the open stair shaft in 11/A6.01 to the roof deck: A (within 0.05 "
                                 "of the canon 10.51 = (791.2-602.0)/18), canon kept")
OPS = {   # rev20b final #1 (CE_ALTURAS_3LADOS): estado + operación de cada resolución
    'FW.2-L2-15': ('CONFIRMED', "printed 9'-10 3/4\" = 9.8958 ft (4/A5.05, corridor zone)"),
    'FW.2-L3-15': ('CONFIRMED', "printed 9'-10 3/4\" = 9.8958 ft (4/A5.05, corridor zone)"),
    'FW.2-L3-14': ('CONFIRMED', "printed 9'-2 7/8\" = 9.2396 ft (4/A5.05, unit foyer under FT-1)"),
    'XW.6.3-L1-04 A': ('CONFIRMED', "printed 14'-0\" = 14.0 ft (4/A5.05 / 5/A6.02 L1-L2)"),
    'XW.6.3-L1-04 B': ('DERIVED', "14'-0\" - 1'-11 1/4\" = 12'-0 3/4\" = 12.0625 ft (4/A5.05, 2/A7.31)"),
    'XW.6.6-L4-16 B': ('DERIVED', "twin XW.6.6-L4-15 B resolved value = 9.8444 ft (A 8.9375 <= 9.8444 <= B 10.1875; 04/A9.05 same eave)"),
}
for _l in 'NSEW':
    OPS[f'LIN-127-L4-{_l}'] = ('DERIVED', '(791.2 - 602.0) / 18 = 10.51 ft (11/A6.01 at 1/4" = 1\'-0", lining top to LEVEL 4)')
RP = f'{W}/alturas/ALTURAS_AB_RESOLUCION.csv'
res = list(csv.DictReader(open(RP, encoding='utf-8-sig')))
camp = list(res[0].keys())
res = [r for r in res if r['Wall ID'] not in RESOL]
for wid, (h, why) in RESOL.items():
    ra, rb = lect.get('A', {}).get(wid), lect.get('B', {}).get(wid)
    if not (ra and rb):
        continue
    im = os.path.basename(str(ra.get('Image') or ''))
    st_, op_ = OPS.get(wid, ('DERIVED', f"resolved A {float(ra['Printed H']):.4f} / B {float(rb['Printed H']):.4f} -> {h:.4f} (reason in Resolution)"))
    res.append({'Wall ID': wid, 'Resolution': why, 'Image': f'{W}/alturas/A/img/{im}' if im else '', 'Printed H': f'{h:.4f}',
                'Source': ra['Source'] if abs(float(ra['Printed H']) - h) <= 0.05 else rb['Source'], 'Operation': op_, 'Status': st_})
with open(RP, 'w', newline='', encoding='utf-8-sig') as fo:
    wr = csv.DictWriter(fo, fieldnames=camp, extrasaction='ignore'); wr.writeheader(); wr.writerows(res)
json.dump(C, open(CP, 'w'), indent=1, ensure_ascii=False)
print("rev20b alturas A/B:", {k: len(v) for k, v in lect.items()}, "| canon <- lectores:", cambios)
