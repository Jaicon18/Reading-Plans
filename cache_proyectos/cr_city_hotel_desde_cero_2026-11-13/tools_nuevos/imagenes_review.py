#!/usr/bin/env python3
"""CB_U_118: cada Review Item con su imagen circulada. Orden: (1) un wall del canon citado en el texto -> su recorte (ya circulado);
(2) una frase entre comillas impresa en la hoja citada (N/HOJA) -> search_for en esa página, círculo rojo, recorte; (3) el N/HOJA
citado -> la burbuja / título de la vista en su hoja (search_for del número de detalle cerca del título), círculo y recorte;
(4) sin nada que circular -> se deja vacío (el chequeo lo muestra: nunca un círculo inventado). Uso: imagenes_review.py"""
import json, os, re
import pymupdf
W = "/root/cr0/work"; OUT = f"{W}/etapas/4_canon/img/review"; os.makedirs(OUT, exist_ok=True)
tk = json.load(open(f"{W}/takeoff.json")); c = json.load(open(f"{W}/etapas/4_canon/takeoff_canon.json"))
pdf = pymupdf.open("/root/cr0/bidset/CityHotel_ArchitecturalPlans_4.22.2026_SIN_MARKUPS.pdf")
pag = {}
for l in open(f"{W}/SHEET_MAP.md"):
    m = re.match(r"\|\s*(\d+)\s*\|\s*([A-Z]\d\.\d{2})\s*\|", l)
    if m: pag.setdefault(m.group(2), int(m.group(1)) - 1)
walls = {w["id"]: w for w in c["existing_walls"] if w.get("img")}
ids = sorted(walls, key=len, reverse=True)
def recorte(pi, r, nombre):
    p = pdf[pi]; R = pymupdf.Rect(r)
    clip = pymupdf.Rect(R.x0 - 220, R.y0 - 160, R.x1 + 220, R.y1 + 160) & p.rect
    sh = p.new_shape(); sh.draw_oval(pymupdf.Rect(R.x0 - 8, R.y0 - 8, R.x1 + 8, R.y1 + 8)); sh.finish(color=(1, 0, 0), width=4); sh.commit()
    p.get_pixmap(clip=clip, dpi=110).save(f"{OUT}/{nombre}.png")
    return f"etapas/4_canon/img/review/{nombre}.png"
n = {"wall": 0, "frase": 0, "vista": 0, "sin": 0}
for k, r in enumerate(tk["revisar"], 1):
    t = r["punto"]; img = ""
    wid = next((i for i in ids if re.search(r"(?<![\w.-])" + re.escape(i) + r"(?![\w.])", t)), None)
    if wid:
        img = os.path.join("etapas/4_canon", walls[wid]["img"]); n["wall"] += 1
    else:
        hojas = re.findall(r"\b(?:\d{1,2}(?:,\d{1,2})*/)?([A-Z]\d\.\d{2})\b", r.get("hoja_detalle", "") + " " + t)
        frases = [q for q in re.findall(r"'([^']{8,60})'|\"([^\"]{8,60})\"", t) for q in q if q]
        # cotas del texto en el formato impreso del set (8'-11 1/4" -> 8' - 11 1/4") y designaciones de type / assembly (FS-1, W.4, CH.6)
        debiles = [f"{a}' - {b}\"" for a, b in re.findall(r"(\d{1,2})'-(\d{1,2}(?: \d/\d)?)\"", t)]
        if re.search(r"(?i)regular|non-rated", t): debiles.append("ALL OTHER LOCATIONS")      # A0.06 general note 10
        if re.search(r"(?i)\bwet\b|W\.R\.|water", t): debiles.append("WATER-RESISTANT GYPSUM BOARD FOR WALLS")    # A0.06 general note 11
        debiles += list(dict.fromkeys(re.findall(r"\b(?:FS|MB|RS|GYP|WS|ACT)-\d\b|\b(?:XW|CH|FW|FI|DW|W)\.\d{1,2}(?:\.\d)?\b", t)))
        for h in dict.fromkeys(hojas):
            if h not in pag: continue
            for f in frases:
                hit = pdf[pag[h]].search_for(f[:40])
                if hit:
                    img = recorte(pag[h], hit[0], f"RI-{k:03d}"); n["frase"] += 1; break
            if img: break
        if not img:
            for nh in re.findall(r"\b(\d{1,2})/([A-Z]\d\.\d{2})\b", r.get("hoja_detalle", "") + " " + t):
                if nh[1] not in pag: continue
                p = pdf[pag[nh[1]]]
                ws = p.get_text("words")
                esc = [w for w in ws if re.match(r'(?i)^(scale|1/[48]"|1/2"|3/4"|1"|1-1/2"|3"|NTS)', w[4])]
                solo = lambda w: not any(v is not w and abs(v[1] - w[1]) < 4 and 0 <= w[0] - v[2] < 18 for v in ws)   # nada pegado a la izquierda
                # burbuja del título de la vista: número aislado con el rótulo de escala debajo-a-la-derecha (<= 260 pt, <= 40 pt abajo)
                tit = [w for w in ws if w[4] == nh[0] and solo(w) and any(0 < v[0] - w[2] < 45 and abs(v[1] - w[1]) < 12 and len(v[4]) > 2 and v[4].isupper() for v in ws) and not any(
                    re.match(r"^[A-Z]\d\.\d{2}$", v[4]) and 0 < v[1] - w[3] < 16 and abs(v[0] - w[0]) < 30 for v in ws) and any(0 < e[0] - w[2] < 260 and 0 < e[1] - w[1] < 40 for e in esc)]
                if tit:
                    w = tit[0]; img = recorte(pag[nh[1]], w[:4], f"RI-{k:03d}"); n["vista"] += 1; break
        if not img:                                       # respaldo: cota impresa / designación del type en la hoja citada
            for h in dict.fromkeys(hojas):
                if h not in pag: continue
                for f in debiles:
                    hit = pdf[pag[h]].search_for(f)
                    if hit:
                        img = recorte(pag[h], hit[0], f"RI-{k:03d}"); n["cota_type"] = n.get("cota_type", 0) + 1; break
                if img: break
        if not img: n["sin"] += 1
    r["imagen"] = img
json.dump(tk, open(f"{W}/takeoff.json", "w"), indent=1)
print("review items con imagen:", n)
