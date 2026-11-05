"""U-137 / U-141: bubble sweep by text pairs (detail number ABOVE sheet number, inside ~20 pt) on every sheet, in the
visible (rotated) frame, plus one-line 'N/SHEET' refs. Writes burbujas_candidatas.json and crops for eye verification."""
import json, re, sys, os
import pymupdf as fitz
pdf, out = sys.argv[1], sys.argv[2]
sm = json.load(open('/root/cc/work/sheetmap.json')); inv = {v: k for k, v in sm.items()}
SH = re.compile(r'^(G|D|A|M|E|P|FA)\d{3}$')
d = fitz.open(pdf); res = {}
os.makedirs(out + '/img', exist_ok=True)
for pno, p in enumerate(d):
    sheet = inv[pno + 1]; R = p.rotation_matrix
    W = []
    for w in p.get_text('words'):
        r = fitz.Rect(w[:4]) * R
        W.append((r, w[4]))
    found = []
    for r, t in W:
        if not SH.match(t) or r.y0 > p.rect.height * 0.0 and r.x0 > (p.rect.width if p.rotation in (0,180) else p.rect.height) * 0.92:
            continue  # skip title block column
        for r2, t2 in W:
            if re.fullmatch(r'[0-9]{1,2}|[A-H]', t2) and abs((r2.x0 + r2.x1) / 2 - (r.x0 + r.x1) / 2) < 12 and 0 < r.y0 - r2.y1 < 16:
                found.append({"n": t2, "hoja": t, "x": round((r.x0 + r.x1) / 2, 1), "y": round((r2.y0 + r.y1) / 2, 1)})
    for r, t in W:
        m = re.fullmatch(r'([0-9]{1,2}|[A-H])/((?:G|D|A|M|E|P)\d{3})', t)
        if m:
            found.append({"n": m.group(1), "hoja": m.group(2), "x": round((r.x0+r.x1)/2,1), "y": round((r.y0+r.y1)/2,1), "una_linea": True})
    # dedupe
    u = []
    for f in found:
        if not any(abs(f['x'] - g['x']) < 4 and abs(f['y'] - g['y']) < 4 and f['hoja'] == g['hoja'] for g in u):
            u.append(f)
    if u:
        pix_page = p
        for i, f in enumerate(u):
            clip = fitz.Rect(f["x"] - 40, f["y"] - 40, f["x"] + 40, f["y"] + 40)
            clip.normalize()
            p.get_pixmap(dpi=150, clip=clip).save(f"{out}/img/{sheet}_{i:02d}.png")
            f['img'] = f"img/{sheet}_{i:02d}.png"
        res[sheet] = u
json.dump(res, open(out + '/burbujas_candidatas.json', 'w'), indent=1)
print({k: len(v) for k, v in res.items()}, sum(len(v) for v in res.values()))
