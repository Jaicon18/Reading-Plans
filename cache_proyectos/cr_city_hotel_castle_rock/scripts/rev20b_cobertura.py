"""CR City Hotel rev20b (U-193, revisión de rojos del mapa de cobertura v119 por 3 revisores independientes; verificado con recortes):
muros nuestros sin cargar -> existing_walls (cada uno clonado del renglón gemelo ya cargado, con su fuente y su operación).
  1) UNTYPED-L3-12: stub W.4 al oeste de LINEN 322 (gemelo de UNTYPED-L2-12, mismas coordenadas en 1/A2.03).
  2) XW.6.6-L4-16 B: cara EXTERIOR (sheathing) del tramo de fachada este en la esquina NW del F&B 410; XW.6.6-L4-16 estaba excluido
     entero con el motivo 'non-rated face(s) inside F&B', que solo cubre la cara interior.
  3) FW.2-L2-15 / FW.2-L3-15 / FW.2-L3-14: cara norte (exterior del CMU) de la escalera SE en L2 y L3, hacia el corredor 218 / 318 y la
     entrada de 209 / 309 (capa de 2 1/8" = FW.2 dibujada en 2/A6.02, 3/A6.02, A2.02, A2.03); en L2 solo estaba el closet 209
     (FW.2-L2-14); en L3 nada. FW.2-L3-14 = espejo de FW.2-L2-14 (closet 309, guest room type 4, 9/A7.05).
Idempotente (quita y vuelve a poner sus renglones)."""
import copy
import json

P = '/root/cr/work/etapas/4_canon/takeoff_canon.json'
C = json.load(open(P))
EW = C['existing_walls']
EW[:] = [w for w in EW if not w.get('rev20b')]
by = {w['id']: w for w in EW}
REV = "U-193 coverage review (independent reviewer; Auditoria/COBERTURA_DISPOSICION.csv with its crop)"
NUEVOS = []


def clon(base, **kw):
    w = copy.deepcopy(by[base])
    for k in ('img_lectura', 'height_plan_check'):
        w.pop(k, None)
    w.update(kw)
    w['rev20b'] = True
    NUEVOS.append(w)


clon('UNTYPED-L2-12', id='UNTYPED-L3-12', floor='L3', sheet='A2.03', page=19, path=[[845.4, 1190.04], [845.4, 1211.64]], length_ft=2.40,
     location='L3 corridor 316 / 318 stub west of LINEN 322 | faces: 322 LINEN; corridor (L3 twin of UNTYPED-L2-12)',
     source="1/A5.06; A2.03 [DERIVED] length (A2.03 vector at printed scale 1/8\"=1'-0\" (9 pt/ft); (1211.64-1190.04)/9 = 2.40) | height: as the L2 "
            "twin UNTYPED-L2-12 (4/A5.05 corridor face 9'-10 3/4\") | type: NOT TYPED: no tag on A2.03; read as its L2 twin (W.4) | " + REV,
     img='/root/cr/work/etapas/7_imagenes/walls/UNTYPED-L3-12_A2.03.png')
clon('XW.6.6-L4-15 B', id='XW.6.6-L4-16 B', path=[[1007.35, 951.2], [1007.35, 996.48]], length_ft=5.03,
     location='L4 East facade at the NW corner of F&B 410 | faces: exterior, facing TERRACE 421 (the interior face is F&B, excluded)',
     source="1/A7.55; A2.04 [DERIVED] length (A2.04 vector at 9 pt/ft: exterior face to the exterior face of the F&B north wall (996.48-951.2)/9 = 5.03; "
            "cross-check 1/A7.55 at 18 pt/ft (953.3-863.0)/18 = 5.02; U-181 rev20b re-check) | height: as XW.6.6-L4-15 B (1/A5.06 eave, 9.8444) | type: segment untagged, east facade XW.6.6 family: exterior face "
            "'TYPE X 5/8\" EXTERIOR GYP BD' (A0.07) in both rating rows | " + REV,
     img='/root/cr/work/etapas/7_imagenes/walls/XW.6.6-L4-16_A2.04.png',
     faces_none_reason="other face (F&B 410 interior) inside the Food & Beverage space: 'INTERIOR OF FOOD AND BEVERAGE SPACE IS NOT IN SCOPE OF THIS "
                       "PERMIT' printed in F&B 410 on 1/A2.04 (excluded_walls XW.6.6-L4-16)")
clon('FW.2-L2-14', id='FW.2-L2-15', path=[[1486.0, 1185.8], [1594.56, 1185.8]], length_ft=12.06, height_ft=9.8958,
     location='L2 SE stair CMU north face, corridor 218 and 209 entry | faces: corridor 218 / 209 entry',
     source="2/A6.02; A2.02 [DERIVED] length (vector on 1/A2.02 at 9 pt/ft: (1594.56-1486.0)/9 = 12.06, corridor part up to the 209.1 door plane; the foyer part is in FW.2-L2-14) | height: corridor 9'-10 3/4\" (4/A5.05) | "
            "type: 2 1/8\" outer layer on the CMU drawn on 2/A6.02 and A2.02 = FW.2 geometry (A0.06 FW.2), same face as FW.2-L2-14 | " + REV,
     height_source="4/A5.05 corridor 9'-10 3/4\"", height_note="corridor face (4/A5.05)", structure_bo_ft=9.8958,
     img='/root/cr/work/etapas/7_imagenes/walls/FW.2-L2-15_A2.02.png')
clon('FW.2-L2-14', id='FW.2-L3-14', floor='L3', sheet='A2.03', page=19, path=[[1594.56, 1185.8], [1653.83, 1185.8]], length_ft=6.59,
     location='L3 SE stair CMU north face, 309 foyer/closet (mirror of FW.2-L2-14) | faces: guest room 309 foyer',
     source="3/A6.02; A2.03 [DERIVED] length (vector on 1/A2.03 at 9 pt/ft: 309 foyer + closet from the 309.1 door plane (1653.83-1594.56)/9 = 6.59; U-181 rev20b re-check: the foyer part takes the room height 9.2396) | height: 9'-2 7/8\" (4/A5.05) | type: tag "
            "PT0204 on 9/A7.05 (guest room type 4 = 309) | " + REV,
     img='/root/cr/work/etapas/7_imagenes/walls/FW.2-L3-14_A2.03.png')
clon('FW.2-L2-14', id='FW.2-L3-15', floor='L3', sheet='A2.03', page=19, path=[[1486.0, 1185.8], [1594.56, 1185.8]], length_ft=12.06, height_ft=9.8958,
     location='L3 SE stair CMU north face, corridor 318 and 309 entry | faces: corridor 318 / 309 entry',
     source="3/A6.02; A2.03 [DERIVED] length (vector on 1/A2.03 at 9 pt/ft: (1594.56-1486.0)/9 = 12.06, corridor part up to the 309.1 door plane; the foyer part is in FW.2-L3-14) | height: corridor 9'-10 3/4\" (4/A5.05) | "
            "type: 2 1/8\" outer layer on the CMU drawn on 3/A6.02 and A2.03 = FW.2 geometry (A0.06 FW.2) | " + REV,
     height_source="4/A5.05 corridor 9'-10 3/4\"", height_note="corridor face (4/A5.05)", structure_bo_ft=9.8958,
     img='/root/cr/work/etapas/7_imagenes/walls/FW.2-L3-15_A2.03.png')
# (5) COORDINACIÓN 12-nov: pilastra XW.6.3-0, cara oeste al sur de 926.6: da al lobby strip (recorte A2.01 / A7.30), no al Retail 124
# (124 queda al SE, pasando la puerta 124.2 y el pavimento exterior): el cierre de RFI-05 cubre solo caras al Retail 124 -> se CARGA
clon('XW.6.3-L1-01', id='XW.6.3-L1-01 S', path=[[1052.4, 926.4], [1052.4, 955.44]], length_ft=3.23,
     location='L1 Pier at the lobby entrance / retail door 124.2 (grid 7, G), south part of the lobby-side face | faces: LOBBY strip (GYP-1 / WS-1 11\'-0\" ceiling)',
     height_diff_reason="south part of the pier faces the LOBBY strip under the 11'-0\" ceiling field (1/A3.01 GYP-1 11'-0\"; 1/A7.31 WS-1 11'-0\" tag next to the pier; 6/A7.31 finish stops at that ceiling); the 12'-0 3/4\" C.H. of the room is the coffer field, not at the pier (1/A7.31): U-176 physical rule met (H = C.H. of the ceiling it touches); both blind readers 11'-0\"",
     source="3/A9.03; A2.01 [DERIVED] length (A2.01 vector at 9 pt/ft, pier WEST face x 1052.4 from the vestibule south side to the pier step: (955.44-926.4)/9 = 3.23; 1/A7.31 at 18 pt/ft 3.27; U-181 rev20b re-check) | RFI-05 boundary (1/A2.01 '*NOTE: GYPSUM BOARD & FINISH "
            "IN RETAIL SPACE BY FUTURE TENANT' covers only the faces INSIDE Retail 124): this face looks into the lobby strip (crop 1/A2.01, 1/A7.30), "
            "Retail 124 is SE beyond door 124.2 and the exterior paving -> ours, delta +35.53 SF 5/8\" Type X (3.23 x 11.0) | " + REV,
     img='/root/cr/work/etapas/7_imagenes/walls/XW.6.3-L1-01S_A2.01.png')
# (4) RFI-30: forro de la escalera 127 (3 3/8" en 7-10/A6.01, sin type / material impreso; barrido U-172 / U-191 sin respuesta): valor
# conservador CARGADO (U-048 / U-052), 5/8" Type X una cara sobre furring (como FW.1 de la misma escalera; furring de madera excluido U-139)
VISTA = {'L1': (1512.8, 1665.1, 14.0, "11/A6.01 '24 RISERS @ 7\" EACH 14'-0\"' (10/A6.01)"),
         'L2': (1121.6, 1273.9, 11.0, "11/A6.01 '19 RISERS @ 6.95\" EACH 11'-0\"' (9/A6.01)"),
         'L3': (721.4, 873.7, 11.0, "11/A6.01 '19 RISERS @ 6.95\" EACH 11'-0\"' (8/A6.01)"),
         'L4': (305.9, 458.1, 10.51, "11/A6.01 lining top (underside of roof) to LEVEL 4: (791.2-602.0)/18 = 10.51 (7/A6.01)")}
for lv, (xw, xe, h, hs) in VISTA.items():
    xc = (xw + xe) / 2
    lados = {'N': [[round(xc - 73.53, 2), 1136.1], [round(xc + 73.53, 2), 1136.1]], 'S': [[round(xc - 73.53, 2), 1444.3], [round(xc + 73.53, 2), 1444.3]],
             'W': [[xw, 1138.95], [xw, 1441.89]], 'E': [[xe, 1138.95], [xe, 1441.89]]}
    for ld, pth in lados.items():
        lf = 8.17 if ld in 'NS' else 16.83
        clon('FW.1-L1-01', id=f'LIN-127-{lv}-{ld}', floor=lv, sheet='A6.01', page=42, path=pth, length_ft=lf, height_ft=h, faces=1,
             location=f'{lv} Lobby stair 127 interior lining, {ld} side (stair side of the CMU) | faces: STAIR 1 127',
             source=("7-10/A6.01 [CONFIRMED] lining '3 3/8\"' on the stair side of the CMU, all 4 sides, full height in 11/A6.01; length "
                     + ("8'-8 3/4\" - 2 x 3 3/8\" = 8.17 [DERIVED]" if ld in 'NS' else "5'-4\" + 6'-5\" + 5'-1\" = 16.83 [CONFIRMED]")
                     + f" | height: {hs} | type: NOT PRINTED (U-172 / U-191 sweep: specs 09 22 16 / 09 29 00 / 05 40 00, A6.0x sections, A0.06 / A0.07 "
                     "types, code plans: no answer) -> conservative LOADED as 5/8\" Type X one face on furring (as FW.1 of the same stair), RFI-30 | " + REV),
             height_source=hs, height_note=hs, structure_bo_ft=h, keynote='11/A6.01',
             img='/root/cr/work/etapas/7_imagenes/walls/LIN-127_A6.01.png')
# (6) RFI-31: muro sur del exit passage del Stair 2 al este de 126.1 (grid 14, A2.01; sin tag): conservador CARGADO como el XW.6.3 vecino
for suf, base in (('A', 'XW.6.3-L1-03 A'), ('B', 'XW.6.3-L1-03 B')):
    clon(base, id=f'XW.6.3-L1-04 {suf}', path=[[1653.0, 1286.15], [1690.0, 1286.15]], length_ft=4.11,
         location='L1 Stair 2 exit passage south wall east of door 126.1 (grid 14) | faces: ' + ('exterior' if suf == 'A' else 'exit passage'),
         source="1/A2.01 [DERIVED] length (A2.01 vector at 9 pt/ft: (1690.0-1653.0)/9 = 4.11) | type: NOT PRINTED (no tag on A2.01 nor 2/A6.02; U-172 / "
                "U-191 sweep without answer) -> conservative LOADED as the adjacent grid-14 facade XW.6.3-L1-03 (drawn alike), RFI-31 | " + REV,
         img='/root/cr/work/etapas/7_imagenes/walls/XW.6.3-L1-04_A2.01.png')
C['excluded_walls'] = [x for x in C.get('excluded_walls') or [] if x.get('id') != 'XW.6.3-L1-01 (retail part)']
# U-181 rev20b re-check: el tramo del foyer de 209 (desde el plano de la puerta 209.1, x 1594.56) va a la altura del cuarto (9.2396):
# FW.2-L2-14 (closet 209) se extiende al oeste hasta ese plano; el tramo del corredor queda en FW.2-L2-15 (9.8958)
_f = by['FW.2-L2-14']
if _f['path'][0][0] != 1594.56:
    _f['path'] = [[1594.56, 1185.8], [1653.83, 1185.8]]
    _f['length_ft'] = 6.59
    _f['source'] = str(_f['source']) + " | U-193 / U-181 rev20b: extended west to the 209.1 door plane (foyer face, room height): (1653.83-1594.56)/9 = 6.59"
EW += NUEVOS
for x in C.get('excluded_walls') or []:
    if x.get('id') == 'XW.6.6-L4-16' and 'U-193 coverage review' not in str(x.get('reason')):
        x['reason'] = str(x['reason']) + " | U-193 coverage review: INTERIOR (F&B) face only; the exterior face is counted as XW.6.6-L4-16 B"
json.dump(C, open(P, 'w'), indent=1, ensure_ascii=False)
print("rev20b cobertura:", [(w['id'], w['length_ft'], round(w['height_ft'], 2), w['faces']) for w in NUEVOS])
