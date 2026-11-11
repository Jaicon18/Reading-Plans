"""U-159 table completed for every room number the gate reads on the sheets whose text mentions the RCP (A2.0 and A3.0):
- A2.0 rooms 100-104 = the same rooms of the A3.0 RCP: their EXCLUDED markup is drawn on A3.0 (draw_sheet A3.0, same polygon / reason);
- printed numbers that are NOT rooms (disposition not_a_room, BE-XF03): '600' and '162' of the A3.0 steel designator example
  ('600 S 162 54' of 2/A3.0 ALLOWABLE CEILING SPANS legend) and '200D' of the A2.0 hardware groups (threshold / door shoe model) - each
  with a circled crop re-opened. Use: python3 -I scripts/rcp_cuartos_extra.py"""
import json, os
import pymupdf as fitz
from PIL import Image, ImageDraw
K = '/root/xf/work'; P = f'{K}/etapas/6_markups/rcp_cuartos.json'
t = json.load(open(P)); rooms = t['rooms']
have = {(r['sheet'], r['room']) for r in rooms}
doc = fitz.open(f'{K}/plans/bidset_SIN_MARKUPS.pdf'); IMG = f'{K}/etapas/6_markups/no_room'; os.makedirs(IMG, exist_ok=True)
def crop(pg, term, name, idx=0):
    p = doc[pg - 1]; R = p.rotation_matrix
    rs = sorted([r * R for r in p.search_for(term)], key=lambda r: (r.y0, r.x0))
    r = rs[idx]; r.normalize()
    clip = fitz.Rect(r.x0 - 160, r.y0 - 60, r.x1 + 160, r.y1 + 60) & p.rect
    pix = p.get_pixmap(dpi=130, clip=clip); im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    s = pix.width / clip.width; d = ImageDraw.Draw(im)
    d.ellipse([(r.x0 - clip.x0 - 8) * s, (r.y0 - clip.y0 - 8) * s, (r.x1 - clip.x0 + 8) * s, (r.y1 - clip.y0 + 8) * s], outline=(255, 0, 0), width=4)
    f = f'{IMG}/{name}.png'; im.save(f); return f
for r in [x for x in rooms if x['sheet'] == 'A3.0' and x['room'] in ('100', '101', '102', '103', '104')]:
    if ('A2.0', r['room']) not in have:
        rooms.append(dict(r, sheet='A2.0', draw_sheet='A3.0',
                          note=f"room {r['room']} printed on the A2.0 partition plan; its ceiling is shown on the A3.0 RCP, where its EXCLUDED markup is drawn"))
NR = [("A3.0", "600", 6, "600", "steel member designator legend of A3.0 ('MEMBER DEPTH: (EXAMPLE: 6\" = 600 X 1/100 INCHES)', designator '600 S 162 54'), not a room"),
      ("A3.0", "162", 6, "162", "flange width '162' (1-5/8\") of the A3.0 steel designator legend example '600 S 162 54', not a room"),
      ("A2.0", "200D", 5, "200D", "threshold model '200D' (hardware group A1) of the A2.0 HARDWARE GROUPS, not a room")]
for sh, n, pg, term, why in NR:
    if (sh, n) not in have:
        rooms.append({"sheet": sh, "room": n, "disposition": "not_a_room", "reason": why, "nhoja": sh, "img": crop(pg, term, f"{sh}_{n}_not_a_room")})
json.dump(t, open(P, 'w'), indent=1, ensure_ascii=False)
print('rooms', len(rooms), [(r['sheet'], r['room'], r['disposition']) for r in rooms])
