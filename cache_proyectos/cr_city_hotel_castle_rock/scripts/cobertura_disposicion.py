"""U-193 (rev20b): Auditoria/COBERTURA_DISPOSICION.csv = disposición FINAL de cada rojo del mapa de cobertura, en el formato de
compuerta_entrega v119 (leer_disposicion): hoja, tipo, id, x, y, decision (CUBIERTO / NO ES NUESTRO / NO ES MURO), motivo, nhoja,
revisor (subagente registrado en la bitácora: bitacora.py subagente revisor_cobertura <id>), imagen (ROJOS/<archivo>.png relativa a
Auditoria/), + row_or_rfi, reviewer_class. Fuente: las clasificaciones de los 3 revisores independientes
(auditoria_cobertura_rev20b/{L1,L2L4,STAIRS}/disposicion.csv, cada una con su recorte) y la revisión manual de las hojas ciegas
(auditoria_cobertura_rev20b/CIEGAS/ciegas.csv, tipo=hoja_ciega). FALTA cargado en rev20b -> CUBIERTO con su renglón.
Uso: cobertura_disposicion.py <carpeta_entrega>"""
import csv
import os
import re
import shutil
import sys
from collections import Counter

W = '/root/cr/work'
A = f'{W}/auditoria_cobertura_rev20b'
E = sys.argv[1]
REVISOR = {'L1': 'a54c5aa2dda330962', 'STAIRS': 'a883b0b62fb5a6820', 'L2L4': 'aa7a91d6a2c875b35', 'CIEGAS': 'aba330cfcbae464f3'}
CIERRE = {   # id del rojo -> (decision, renglón / RFI que lo cubre)
    'EXTRA-A2.03-stub322': ('CUBIERTO', 'FALTA loaded in rev20b: UNTYPED-L3-12 (W.4, 2.40 LF, 2 faces)'),
    'M-A2.04-93': ('CUBIERTO', 'FALTA loaded in rev20b: XW.6.6-L4-16 B (exterior sheathing, 5.03 LF)'),
    'M-A7.55-20': ('CUBIERTO', 'FALTA loaded in rev20b: XW.6.6-L4-16 B (same wall as M-A2.04-93)'),
    'M-A7.55-21': ('CUBIERTO', 'FALTA loaded in rev20b: XW.6.6-L4-16 B (same wall as M-A2.04-93)'),
    'M-A6.02-11': ('CUBIERTO', 'FALTA loaded in rev20b: FW.2-L2-15 (12.06 LF) + FW.2-L2-14 extended to the 209.1 door (6.59 LF)'),
    'M-A6.02-5': ('CUBIERTO', 'FALTA loaded in rev20b: FW.2-L3-15 (12.06 LF) + FW.2-L3-14 (6.59 LF)'),
    'M-A2.01-52': ('CUBIERTO', 'untagged: XW.6.3-L1-04 A / B (4.33 LF) - RFI-31 resolved from the printed rating + finish (A0.01 2 HR, 1/A4.01 wood siding, A0.07 XW.6.3 | 2)'),
    'M-A2.01-57': ('CUBIERTO', 'untagged: XW.6.3-L1-04 A / B - RFI-31 resolved from the printed rating + finish (A0.01, 1/A4.01, A0.07)'),
    'M-A2.01-74': ('CUBIERTO', 'untagged niche build-out (TF-1 face, 2/A7.35 / 3/A7.35): loaded FW.6-0 assumed type, canon NT-L1-01 / 02, RFI-33 with delta'),
    'M-A7.30-19': ('CUBIERTO', 'untagged niche build-out (TF-1 face): loaded FW.6-0 assumed type, canon NT-L1-01 / 02, RFI-33 with delta'),
    'M-A7.30-20': ('CUBIERTO', 'untagged niche build-out (TF-1 face): loaded FW.6-0 assumed type, canon NT-L1-01 / 02, RFI-33 with delta'),
    'M-A7.45-34': ('CUBIERTO', 'untagged niche build-out (TF-1 face): loaded FW.6-0 assumed type, canon NT-L1-01 / 02, RFI-33 with delta'),
    'M-A7.30-10': ('CUBIERTO', 'stair 127 lining (L1 view): ALTERNATE #1 (ADD), user decision on RFI-30 - not in the base bid, priced apart (LIN-127-L1-* in excluded_walls)'),
    'M-A7.30-11': ('CUBIERTO', 'stair 127 lining (L1 view): ALTERNATE #1 (ADD), user decision on RFI-30 - not in the base bid, priced apart (LIN-127-L1-* in excluded_walls)'),
    'M-A7.30-23': ('CUBIERTO', 'stair 127 lining (L1 view): ALTERNATE #1 (ADD), user decision on RFI-30 - not in the base bid, priced apart (LIN-127-L1-* in excluded_walls)'),
    'M-A2.01-90': ('CUBIERTO', 'FALTA loaded in rev20b: XW.6.3-L1-01 S (lobby-strip face, outside the RFI-05 Retail 124 boundary)'),
    'M-A7.30-26': ('CUBIERTO', 'FALTA loaded in rev20b: XW.6.3-L1-01 S (same as M-A2.01-90)'),
}
for i in (9, 10, 11, 12, 13, 14, 15, 16, 28, 30, 31, 33, 40, 41, 46, 47, 52, 53):
    CIERRE[f'M-A6.01-{i}'] = ('CUBIERTO', 'stair 127 lining (untagged): ALTERNATE #1 (ADD), user decision on RFI-30 - not in the base bid, priced apart (LIN-127-L1..L4 in excluded_walls, 2,325.5 SF)')
CLASE = {'YA_CONTADO': 'CUBIERTO', 'NO_ES_NUESTRO': 'NO ES NUESTRO', 'NO_ES_MURO': 'NO ES MURO'}
RX_NH = re.compile(r"\b[0-9A-Z]{1,3}/[A-Z]{1,3}[-.]?\d")
os.makedirs(f'{E}/Auditoria/ROJOS', exist_ok=True)
TIPO = {(r['hoja'], r['id']): r['tipo'] for r in csv.DictReader(open(f'{A}/COBERTURA.csv', encoding='utf-8-sig'))}
filas = []


def img_rel(d, r):
    src = ''
    for c in str(r.get('evidencia_img') or r.get('img') or '').split(';'):
        c = c.strip()
        for cand in (c, os.path.join(A, d, c), os.path.join(A, d, 'img', os.path.basename(c)), os.path.join(A, d, os.path.basename(c))):
            if c and os.path.isfile(cand):
                src = cand
                break
        if src:
            break
    if not src:
        return ''
    dst = f"{d}_{os.path.basename(src)}"
    shutil.copy2(src, f'{E}/Auditoria/ROJOS/{dst}')
    return f'ROJOS/{dst}'


for d in ('L1', 'L2L4', 'STAIRS'):
    for r in csv.DictReader(open(f'{A}/{d}/disposicion.csv', encoding='utf-8-sig')):
        dec, ren = CIERRE.get(r['id'], (CLASE.get(r['clase'], r['clase']), ''))
        nh = r['nhoja'] if RX_NH.search(str(r['nhoja'])) else f"1/{r['hoja']}; {r['nhoja']}"
        filas.append({'hoja': r['hoja'], 'tipo': TIPO.get((r['hoja'], r['id']), 'muro'), 'id': r['id'], 'x': r['x'], 'y': r['y'],
                      'decision': dec, 'motivo': (ren + ' | ' if ren else '') + r['motivo'], 'nhoja': nh, 'revisor': REVISOR[d],
                      'imagen': img_rel(d, r), 'reviewer_class': r['clase'], 'type': r['type'], 'LF': r['LF'], 'H': r['H']})
# U-199 (5b) rev20c: muros cortos / diagonales sin markup (CE_COBERTURA_DIAG), 7 revisores independientes por hoja (auditoria_u199/diag/G1..G7)
DG = '/root/cr/work/auditoria_u199/diag'
REV_DG = {'G1': 'a9736bf14e0834fc7', 'G2': 'a2b7a5c37247b7f9d', 'G3': 'a79bd9f1799eb018e', 'G4': 'aca19ad82ffda6892', 'G5': 'ae0b90fd59cf00251',
          'G6': 'ab25eba5ee0855fb3', 'G7': 'a2cf1571bdbb22fa0', 'NICHO': 'a77f6c21feead7f9c'}   # ids de los subagentes revisores (bitácora: revisor_cobertura)
CLASE_DG = {'CUBIERTO': 'CUBIERTO', 'NO ES MURO': 'NO ES MURO', 'NO ES NUESTRO': 'NO ES NUESTRO', 'FALTA': 'CUBIERTO'}   # FALTA cargado por la cadena -> CUBIERTO
for g in sorted(os.listdir(DG)) if os.path.isdir(DG) else []:
    pc = f'{DG}/{g}/disposicion.csv'
    if not os.path.isfile(pc):
        continue
    for r in csv.DictReader(open(pc, encoding='utf-8-sig')):
        dec0 = str(r.get('decision') or '').strip().upper()
        if r.get('id') == 'D-A6.01-2':        # LIN-127 está fuera del base (ALTERNATE #1, decisión del usuario sobre RFI-30): no es 'cubierto' en el base
            dec0 = 'NO ES NUESTRO'
            r['motivo'] = ("3 3/8\" stair 127 lining (LIN-127-L1-S): NOT in the base bid - ALTERNATE #1 (ADD), user decision on RFI-30 "
                           "(7-10/A6.01, 11/A6.01); priced apart in the Proposal")
        src = next((os.path.join(DG, g, 'img', os.path.basename(c.strip())) for c in str(r.get('img') or '').split(';')
                    if c.strip() and os.path.isfile(os.path.join(DG, g, 'img', os.path.basename(c.strip())))), '')
        dst = ''
        if src:
            dst = f"ROJOS/DIAG_{g}_{os.path.basename(src)}"
            shutil.copy2(src, f'{E}/Auditoria/{dst}')
        nh = r.get('nhoja') or ''
        nh = nh if RX_NH.search(nh) else f"1/{r['hoja']}; {nh}"
        filas.append({'hoja': r['hoja'], 'tipo': r.get('tipo') or 'muro_corto', 'id': r.get('id'), 'x': r.get('x'), 'y': r.get('y'),
                      'decision': CLASE_DG.get(dec0, dec0),
                      'motivo': ('FALTA loaded in the take-off by the chain (row DG-...) | ' if dec0 == 'FALTA' else '') + f"[{r.get('familia') or ''}] " + str(r.get('motivo') or ''),
                      'nhoja': nh, 'revisor': REV_DG.get(g, g), 'imagen': dst, 'reviewer_class': dec0, 'type': r.get('type') or '',
                      'LF': r.get('LF') or '', 'H': r.get('H') or ''})
for _x, _y, _w in ((948.4, 493.4, 'NT-L1-01'), (946.4, 1222.0, 'NT-L1-02')):
    _nic = f'/root/cr/work/auditoria_u199/diag/NICHO/NICHO_{_x}_{_y}.png'
    if os.path.isfile(_nic):
        shutil.copy2(_nic, f'{E}/Auditoria/ROJOS/DIAG_NICHO_{_x}_{_y}.png')
    filas.append({'hoja': 'A7.30', 'tipo': 'muro_corto', 'id': f'D-A7.30-NICHO-{_w}', 'x': _x, 'y': _y, 'decision': 'CUBIERTO',
                  'motivo': f"curved niche recess of the TF-1 build-out {_w} (3/A7.35, 2/A7.35): the arc is carried in the take-off by its H / V steps "
                            f"(markup TO-{_w}), developed board counted in {_w}; independent check R3 (quarter arc of the recess, nothing else drawn there)", 'nhoja': '1/A7.30', 'revisor': REV_DG['NICHO'],
                  'imagen': f'ROJOS/DIAG_NICHO_{_x}_{_y}.png', 'reviewer_class': 'CUBIERTO', 'type': 'FW.6-0', 'LF': '', 'H': ''})
cg = f'{A}/CIEGAS/ciegas.csv'
if os.path.isfile(cg):                                   # hojas donde el detector es ciego: revisión manual de TODOS los cielos
    por = {}
    for r in csv.DictReader(open(cg, encoding='utf-8-sig')):
        por.setdefault(r['hoja'], []).append(r)
    for h, rs in por.items():
        falta = [r for r in rs if r['decision'].upper().startswith('FALTA')]
        ov = next((os.path.join(A, 'CIEGAS', f) for f in os.listdir(f'{A}/CIEGAS') if f.startswith(f'{h}_overview')), '')
        dst = ''
        if ov:
            dst = f'ROJOS/CIEGAS_{os.path.basename(ov)}'
            shutil.copy2(ov, f'{E}/Auditoria/{dst}')
        cnt = Counter(r['decision'].upper() for r in rs)
        filas.append({'hoja': h, 'tipo': 'hoja_ciega', 'id': f'HOJA-{h}', 'x': '', 'y': '',
                      'decision': 'CUBIERTO' if not falta else 'FALTA',
                      'motivo': f"room numbers are not text on this sheet: every ceiling reviewed by hand ({len(rs)}: "
                                + ", ".join(f"{k} {v}" for k, v in cnt.items()) + "); " + "; ".join(f"{r['room']} {r['decision']}" for r in rs)[:900],
                      'nhoja': f"1/{h}", 'revisor': REVISOR['CIEGAS'], 'imagen': dst, 'reviewer_class': 'hoja_ciega', 'type': '', 'LF': '', 'H': ''})
with open(f'{E}/Auditoria/COBERTURA_DISPOSICION.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=list(filas[0]))
    w.writeheader(); w.writerows(filas)
abiertos = [x for x in filas if x['decision'] not in ('CUBIERTO', 'NO ES NUESTRO', 'NO ES MURO')]
sin_img = [x for x in filas if not x['imagen']]
print("COBERTURA_DISPOSICION:", len(filas), "renglones;", dict(Counter(x['decision'] for x in filas)), "| abiertos:", len(abiertos), "| sin imagen:", len(sin_img))
