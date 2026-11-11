"""Column wrap markups (CF-01 / CF-02, 5/A2.0): markups_bluebeam.py draws a BOX band as its closed 4-side footprint and shares
the wall LF over the 4 pieces (Bluebeam Length 3.32 ft per column vs Excel 2.38 LF). The 4th side is against the existing
storefront pier and is NOT furred (canon faces_ft = 3 exposed sides). Here, by program: the piece lying on the pier side
(visible x = band c1) is removed and each remaining piece gets its own real length as LF (Bluebeam Length = LF; sum = Excel LF)
and SF = LF x H. Tool limit #6 of TOOL_LIMITS_CALC.md, fixed in the project chain (tool fix goes into the next skill version).
Use: python3 -I scripts/cf_markups.py <in.pdf> <out.pdf>"""
import json, re, sys
import pymupdf as fitz
K = '/root/xf/work'
c = json.load(open(f'{K}/etapas/4_canon/takeoff_canon.json'))
CF = {w['id']: w for w in c['walls'] if w.get('element') == 'column_wrap'}
d = fitz.open(sys.argv[1]); n_del = n_fix = 0
for p in d:
    R = p.rotation_matrix
    for a in list(p.annots() or []):
        m = re.search(r'\b(CF-\d\d)\s*$', a.info.get('content', ''))
        if not m or m.group(1) not in CF:
            continue
        w = CF[m.group(1)]; b = w['band']; H = w['height_ft']
        v = [fitz.Point(x, y) * R for x, y in a.vertices]
        if all(abs(q.x - b['c1']) < 1.0 for q in v):          # side against the existing pier: not furred
            p.delete_annot(a); n_del += 1; continue
        L = round(abs(v[1] - v[0]) / 18.0, 3)
        txt = a.info['content']
        txt = re.sub(r'· [\d.]+ LF ·', f'· {L} LF ·', txt, 1)
        txt = re.sub(r'· [\d.,]+ SF wall \(LF×H\) · [\d.,]+ SF board', f'· {L*H:.2f} SF wall (LF×H) · {L*H:.2f} SF board', txt, 1)
        a.set_info(content=txt); a.update(); n_fix += 1
d.save(sys.argv[2], garbage=3, deflate=True)
print('CF pieces removed (pier side):', n_del, 'relabelled:', n_fix)
sys.exit(0 if n_del == 2 * len(CF) // 2 * 1 and n_fix else 1)
