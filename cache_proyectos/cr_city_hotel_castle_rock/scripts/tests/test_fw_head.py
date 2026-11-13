"""BE-CR46 (CR rev20d, COORDINACIÓN 13-nov): el head del TYPE manda sobre la cota de muro. A0.06 FURRED WOOD - HEAD: board a 6" sobre la
LINE OF CEILING -> altura de una cara FW = C.H. del cuarto + 6" (nunca la B.O. de estructura de 4/A5.05). Sobre el canon: toda cara FW de L2 / L3
(no cement board) hacia baño / shower / toilet <= 9'-0" (GYP-1 8'-6" + 6"), hacia corridor <= 9'-5" (8'-11" A.F.F. + 6"), y ninguna franja
de 0'-2 7/8" sobre cement board en una cara FW. Uso: test_fw_head.py <canon.json> -> rc 1 con la lista. Caso: canon rev20c -> FAIL; rev20d -> 0."""
import json
import re
import sys

C = json.load(open(sys.argv[1]))
RX_BATH = re.compile(r"(?i)bath|shower|toilet|\bwc\b|vanity")
f = []
for w in C.get('existing_walls', []):
    if not str(w.get('type_id', '')).startswith('FW') or w.get('floor') not in ('L2', 'L3') or 'cement' in str(w.get('board', '')):
        continue
    h = float(w['height_ft'])
    caras = re.sub(r"\(dry part[^)]*\)", "", str(w.get('location', '')).split('faces:')[-1])
    if abs(h - 0.2396) < 0.001:
        f.append(f"{w['id']}: WR strip {h} on a FW face (the FW board stops 6\" above the ceiling = top of the cement board)")
    elif RX_BATH.search(caras) and h > 9.0 + 1e-6:
        f.append(f"{w['id']}: FW face to a bath at {h} > 9'-0\" (A0.06 FURRED WOOD head: GYP-1 8'-6\" + 6\")")
    elif re.search(r"(?i)corridor", caras) and h > 9.4167 + 1e-6:
        f.append(f"{w['id']}: FW face to a corridor at {h} > 9'-5\" (A0.06 FURRED WOOD head: 7/A7.23 8'-11\" A.F.F. + 6\")")
print("\n".join(f) if f else "OK: every FW face at the C.H. of its room + 6\" (A0.06 FURRED WOOD head)")
sys.exit(1 if f else 0)
