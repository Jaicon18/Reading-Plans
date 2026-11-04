#!/usr/bin/env python3
"""Imagen de altura circulada (U-118) por wall de corte: busca en el OCR con cajas (tesseract TSV, 200 dpi) de la hoja que
cita la fuente cada valor impreso de la altura, recorta cada aparición con elipse roja y arma un panel rotulado.
Uso: hacer_alturas.py <dir_ocr> <dir_salida>  -> h_<wall>.png + alturas.json (wall -> png, apariciones)"""
import csv, json, os, re, sys
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = None
OCR, OUT = sys.argv[1], sys.argv[2]
# wall: (hoja, [regex de cada valor impreso que la fuente cita])
OBJ = {   # wall: [(hoja, regex de un valor impreso que cita la fuente), ...]
    "S21-N": [("A3.2", r"114'-7"), ("A3.2", r"116'-4")], "S21-E": [("A3.2", r"114'-7")], "S21-W1": [("A3.2", r"116'-4")],
    "S21-W2": [("A3.2", r"116'-4")], "S21-S": [("A3.4", r"114'-7"), ("A3.2", r"116'-4")],
    "EXT-MS1-8": [("A3.1", r"120'-8"), ("A3.1", r"(?<!\d)100'-0")], "EXT-MS1-6": [("A3.1", r"120'-8"), ("A3.1", r"(?<!\d)100'-0")],
    "EXT-MS2-8": [("A3.1", r"120'-8"), ("A3.1", r"(?<!\d)100'-0")], "EXT-MS2-6": [("A3.1", r"120'-8"), ("A3.1", r"(?<!\d)100'-0")],
    "HEAD-A-8": [("A3.1", r"111'-4", "SHEATHING"), ("A3.1", r"120'-8")], "HEAD-A-6": [("A3.1", r"111'-4", "SHEATHING"), ("A3.1", r"120'-8")],
    "CORN-S": [("A3.4", r"119'-4")],
    "S42-02": [("A4.2", r"106'-1"), ("A3.2", r"114'-7"), ("A3.2", r"116'-4")],
    "S42-03": [("A4.2", r"106'-1"), ("A3.2", r"114'-7"), ("A3.2", r"116'-4")],
    "VH-C": [("A3.2", r"114'-7"), ("A3.2", r"116'-4")], "VH-B1": [("A3.2", r"114'-7"), ("A3.2", r"116'-4")],
    "VH-B2": [("A3.2", r"114'-7"), ("A3.2", r"116'-4")],
}


def palabras(h):
    rows = list(csv.DictReader(open(f"{OCR}/{h}_200.tsv"), delimiter="\t", quoting=csv.QUOTE_NONE))
    return [r for r in rows if (r.get("text") or "").strip()]


res = {}
CACHE = {}
for wid, objs in OBJ.items():
    tiles = []
    for ob in objs:
        h, rx = ob[0], ob[1]
        kw = ob[2] if len(ob) > 2 else None
        if h not in CACHE:
            CACHE[h] = (palabras(h), Image.open(f"{OCR}/{h}_200.png").convert("RGB"))
        ws, sheet = CACHE[h]
        hits = [w for w in ws if re.search(rx, w["text"].replace("’", "'"))]
        if kw:   # rótulo del valor (palabra impresa justo encima / al lado): descarta la misma cota de otro rótulo
            hits = [w for w in hits if any(kw in v["text"].upper() and abs(int(v["top"]) - int(w["top"])) < 60
                                           and -80 < int(v["left"]) - int(w["left"]) < 400 for v in ws)]
        hits = hits[:2]
        for w in hits:
            x, y, ww, hh = int(w["left"]), int(w["top"]), int(w["width"]), int(w["height"])
            box = (max(0, x - 260), max(0, y - 160), min(sheet.width, x + ww + 260), min(sheet.height, y + hh + 160))
            im = sheet.crop(box).copy()
            d = ImageDraw.Draw(im)
            ox, oy = x - box[0], y - box[1]
            d.ellipse([ox - 30, oy - 18, ox + ww + 30, oy + hh + 18], outline=(255, 0, 0), width=5)
            d.text((6, 6), f"{h}  '{w['text']}'", fill=(255, 0, 0))
            tiles.append((im, f"{h}:{w['text']}"))
    if not tiles:
        res[wid] = {"png": None, "apariciones": []}
        continue
    W = sum(t[0].width for t in tiles) + 10 * (len(tiles) - 1)
    H = max(t[0].height for t in tiles) + 30
    panel = Image.new("RGB", (W, H), "white")
    dp = ImageDraw.Draw(panel)
    dp.text((6, 4), f"{wid}: printed height source ({', '.join(sorted({o[0] for o in objs}))})", fill=(255, 0, 0))
    x = 0
    for im, _ in tiles:
        panel.paste(im, (x, 30))
        x += im.width + 10
    p = os.path.join(OUT, f"h_{wid}.png")
    panel.save(p)
    res[wid] = {"png": os.path.basename(p), "apariciones": [t[1] for t in tiles]}
json.dump(res, open(os.path.join(OUT, "alturas.json"), "w"), indent=1)
for k, v in res.items():
    print(k, v["apariciones"])
