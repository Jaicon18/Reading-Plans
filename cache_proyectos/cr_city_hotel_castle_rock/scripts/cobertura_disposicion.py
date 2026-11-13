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
    'M-A2.01-52': ('CUBIERTO', 'untagged: loaded conservative XW.6.3-L1-04 A / B (4.11 LF) + RFI-31 with delta'),
    'M-A2.01-57': ('CUBIERTO', 'untagged: loaded conservative XW.6.3-L1-04 A / B + RFI-31 with delta'),
    'M-A2.01-74': ('CUBIERTO', 'untagged niche build-out: open RFI-CR-04 with delta (+315.8 SF if furring), canon NT-L1-01 / 02'),
    'M-A7.30-19': ('CUBIERTO', 'untagged niche build-out: open RFI-CR-04 with delta, canon NT-L1-01 / 02'),
    'M-A7.30-20': ('CUBIERTO', 'untagged niche build-out: open RFI-CR-04 with delta, canon NT-L1-01 / 02'),
    'M-A7.45-34': ('CUBIERTO', 'untagged niche build-out: open RFI-CR-04 with delta, canon NT-L1-01 / 02'),
    'M-A7.30-10': ('CUBIERTO', 'stair 127 lining (L1 view): loaded conservative LIN-127-L1-* + RFI-30 with delta'),
    'M-A7.30-11': ('CUBIERTO', 'stair 127 lining (L1 view): loaded conservative LIN-127-L1-* + RFI-30 with delta'),
    'M-A7.30-23': ('CUBIERTO', 'stair 127 lining (L1 view): loaded conservative LIN-127-L1-* + RFI-30 with delta'),
    'M-A2.01-90': ('CUBIERTO', 'FALTA loaded in rev20b: XW.6.3-L1-01 S (lobby-strip face, outside the RFI-05 Retail 124 boundary)'),
    'M-A7.30-26': ('CUBIERTO', 'FALTA loaded in rev20b: XW.6.3-L1-01 S (same as M-A2.01-90)'),
}
for i in (9, 10, 11, 12, 13, 14, 15, 16, 28, 30, 31, 33, 40, 41, 46, 47, 52, 53):
    CIERRE[f'M-A6.01-{i}'] = ('CUBIERTO', 'stair 127 lining (untagged): loaded conservative LIN-127-L1..L4-N/S/E/W (2,325.5 SF) + RFI-30 with delta')
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
