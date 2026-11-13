"""BE-CR45 (CR rev20d, COORDINACIÓN 13-nov): cara de ducha vs cement board, por programa, sobre el canon FINAL (después de toda cara cargada
tarde, no solo las originales de banos_cbu). Para cada shower (etapas/4_canon/out/banos_cbu.json: caja del shower pan + lados sólidos):
 (a) DOBLE CONTEO: ninguna fila de board NO cement de un type NON-rated (-0) en la cara del lado (<= 10 pt de la caja, cara hacia el shower
     según 'faces:') con altura > 0.5 ft sobre el tramo del shower (debe quedar solo la franja H - 9'-0");
 (b) MARKUP EN LA CARA: cada fila de cement board del shower está a <= 3.5 pt del lado de la caja (la línea de la cara real, no la de atrás).
Uso: test_ducha_cbu.py <canon.json> [banos_cbu.json] -> rc 1 con la lista si falla. Caso de prueba: el canon de rev20c da 6 (a) + 6 (b)."""
import json
import re
import sys

CP = sys.argv[1]
BP = sys.argv[2] if len(sys.argv) > 2 else '/root/cr/work/etapas/4_canon/out/banos_cbu.json'
C = json.load(open(CP))
B = json.load(open(BP))
rows = [w for w in C.get('existing_walls', []) + C.get('walls', []) if isinstance(w, dict) and w.get('path')]
byid = {w['id']: w for w in rows}
fallas = []


def segs(w):
    return [p for p in (w.get('paths') or [w['path']]) if len(p) >= 2]


for s in B['showers']:
    fl, room = s['floor'], s['room']
    x0, x1, y0, y1 = s['box']
    for cb in s['cbu']:
        side = cb['side']
        vert = side in ('W', 'E')
        lado = (x0 if side == 'W' else x1) if vert else (y0 if side == 'N' else y1)
        lo_b, hi_b = (y0, y1) if vert else (x0, x1)
        # (b) markup del cement board en la cara: ninguna otra fila de board más cerca del lado del shower, colineal y sobre el tramo
        w = byid.get(cb['id'])
        if w:
            k = 0 if vert else 1
            lc = w['path'][0][k]
            for r in rows:
                if r.get('floor') != fl or 'cement' in str(r.get('board', '')).lower() or r['id'] == cb['id']:
                    continue
                for p in segs(r):
                    if abs(p[0][k] - p[-1][k]) > 0.5:
                        continue
                    lr = p[0][k]
                    if not (min(lc, lado) + 0.3 < lr <= max(lc, lado) + 0.3 or (abs(lr - lado) < abs(lc - lado) - 0.3 and abs(lr - lado) <= 3.5)):
                        continue
                    q = 1 - k
                    ov = min(max(p[0][q], p[-1][q]), hi_b) - max(min(p[0][q], p[-1][q]), lo_b)
                    if ov > 9 and abs(lr - lado) < abs(lc - lado):
                        fallas.append(f"(b) {fl} {room} {side}: cement board {cb['id']} drawn at {lc} but the shower face is {r['id']} at {lr} (line behind, not the shower face)")
                        break
        # (a) doble conteo en la cara del shower
        for r in rows:
            if r.get('floor') != fl or 'cement' in str(r.get('board', '')).lower() or float(r.get('height_ft') or 0) <= 0.5:
                continue
            if not str(r.get('type_id', '')).endswith('-0'):
                continue
            caras = str(r.get('location', '')).split('faces:')[-1].lower()
            k = 0 if vert else 1
            dist = min(abs(p[0][k] - lado) for p in segs(r))
            furring = str(r.get('type', '')).startswith('F')
            if not (('shower' in caras and dist <= 10) or (furring and dist <= 3.5)):
                continue
            for p in segs(r):
                (a, b), (c, d2) = p[0], p[-1]
                if vert and abs(a - c) < 0.5 and abs(a - lado) <= 10:
                    ov = min(max(b, d2), hi_b) - max(min(b, d2), lo_b)
                elif not vert and abs(b - d2) < 0.5 and abs(b - lado) <= 10:
                    ov = min(max(a, c), hi_b) - max(min(a, c), lo_b)
                else:
                    continue
                if ov > 9:
                    fallas.append(f"(a) {fl} {room} {side}: {r['id']} ({r['board']}, {r['type_id']}) {ov / 9:.2f} LF x {r['height_ft']} ft over the shower "
                                  f"+ cement board {cb['id']} = double count on a NON-rated face")
print("\n".join(fallas) if fallas else "OK: 0 double counts, every cement board on its shower face")
sys.exit(1 if fallas else 0)
