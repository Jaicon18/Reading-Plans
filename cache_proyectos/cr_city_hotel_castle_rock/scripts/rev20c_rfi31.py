"""rev20c (COORDINACIÓN 13-nov 05:10 UTC, tras el usuario 'tienes que investigarlo, cien por ciento que ahi esta en los planos'):
RFI-31 se resuelve con lo IMPRESO (U-162 plano primero / U-178 (2)): A0.01 '2 HR RATED EXTERIOR WALL' sobre el muro, 1/A4.01 wood
siding, S1.01 / S1.02 no es CMU ni concreto, y en A0.07 el único type exterior wood stud 2 HR con wood siding L1-L3 es XW.6.3|2.
XW.6.3-L1-04 A / B: largo corregido a 4.33 LF [DERIVED (1692.48 - 1653.48) / 9 = 39.0 / 9], fuentes N/HOJA, recortes del lector
independiente (auditoria_rfi31/ev*.png). Idempotente."""
import json
import os
import shutil

W = '/root/cr/work'
CP = f'{W}/etapas/4_canon/takeoff_canon.json'
EV = f'{W}/auditoria_rfi31'
RI = f'{W}/etapas/4_canon/img/rfi'
os.makedirs(RI, exist_ok=True)
for a, b in (('ev01_A2.01_wall.png', 'RI_RFI31_A201_wall.png'), ('ev06_A0.01_codeplan.png', 'RI_RFI31_A001_2HR.png'),
             ('ev11_A4.01_south_elev.png', 'RI_RFI31_A401_siding.png'), ('ev05_A6.02_zoom_target_vs_XM.png', 'RI_RFI31_A602_skin.png')):
    if os.path.isfile(f'{EV}/{a}'):
        shutil.copy2(f'{EV}/{a}', f'{RI}/{b}')
C = json.load(open(CP))
SRC = ("RFI-31 resolved from the printed rating + finish: A0.01 L1 Code Plan '2 HR RATED EXTERIOR WALL' line under this wall [CONFIRMED]; "
       "1/A4.01 'WOOD SIDING, GREY' continuous to the corner (1/A5.00 wall end in siding) [CONFIRMED]; not CMU / concrete (A2.01 CMU hatch stops "
       "at x 1653.48, S1.01, S1.02 MSW-1 = stair shaft only) [CONFIRMED]; A0.07: the only wood-stud 2 HR exterior type with wood siding L1-L3 is "
       "XW.6.3 | 2 (U-162 / U-178 (2)); untagged on A2.01 / 1/A6.02. Length [DERIVED] A2.01 (1692.48 - 1653.48) / 9 = 39.0 / 9 = 4.33 LF")
n = 0
for w in C['existing_walls']:
    if w['id'] in ('XW.6.3-L1-04 A', 'XW.6.3-L1-04 B'):
        w['path'] = [[1653.48, 1286.15], [1692.48, 1286.15]]
        w['length_ft'] = 4.33
        w['source'] = SRC
        w['length_status'] = 'DERIVADO'
        w['rfi_note'] = ("Review Item: the drawing shows the exterior skin continuous with the stair's (14.6\" vs 14.0\" of XW.6.3 | 2) and no "
                         "exterior gypsum (X.6.3 skin graphic) - see 1/A6.02 and 1/A5.00; alternative B delta in Review Items")
        n += 1
json.dump(C, open(CP, 'w'), indent=1, ensure_ascii=False)
print('rev20c RFI-31: XW.6.3-L1-04 A / B ->', n, 'rows at 4.33 LF')
