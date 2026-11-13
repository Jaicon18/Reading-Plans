"""Bug (CR rev20d, COORDINACIÓN 13-nov 22:20 UTC): comparar_alturas.sala() reduce '201 Guest Room Type 1 - Bath' y '201 Guest Room Type 1 - Room'
a la misma llave '201' (gana la última fila del CSV) y _rooms_de_location('... | faces: bath 201') da '201': la cara del baño se compara con el
C.H. de la habitación (9.24) y no con el de su propio cielo (GYP-1 8'-6" = 8.5, A7.05). Caso real: UNTYPED-L2-08 (FW furring, bath 201) H 9.0 =
8'-6" + 6" (A0.06 FURRED WOOD head) sale 'por debajo del cielo' 9.24. Esperado: el baño es su propio espacio con su C.H.; la cara 'bath 201'
(o 'shower 201', '201 bath', 'toilet 201') se cruza con '201 ... - Bath'. Uso: python3 test_cruce_cuartos_bano.py <tools_dir>"""
import os, sys, tempfile, csv
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else '/root/skill/take-off-metal-frame-drywall/tools')
import comparar_alturas as CA
d = tempfile.mkdtemp(); p = os.path.join(d, 'ALTURAS_CUARTOS.csv')
with open(p, 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f); w.writerow(['Room', 'C.H. (ft)', 'Source', 'Image'])
    w.writerow(['201 Guest Room Type 1 - Bath', '8.5000', "A7.00 unit RCP 'GYP-1 8'-6\"'", ''])
    w.writerow(['201 Guest Room Type 1 - Room (untagged = bottom of floor/ceiling assembly, A7.00 note 1)', '9.2396', '4/A5.05', ''])
cuartos = dict(CA.leer_cuartos(p))
can = {'existing_walls': [{'id': 'UNTYPED-L2-08', 'height_ft': 9.0, 'location': 'L2 bath 201 plumbing furring | faces: bath 201',
                           'type_id': 'FW.4-0', 'height_source': "A0.06 FURRED WOOD - HEAD: board to 6\" above the LINE OF CEILING; bath 'GYP-1 8'-6\"' + 6\""}]}
ws = CA.walls_de_canon(can)
n, f, filas = CA.cruce_cuartos(ws, cuartos)
print('cuartos:', cuartos, '| rooms of the face:', ws[0]['rooms'], '| fallas:', f)
assert not f, "BUG: the bath face is compared with the room C.H. instead of the bath C.H. (8.5)"
print('OK')
