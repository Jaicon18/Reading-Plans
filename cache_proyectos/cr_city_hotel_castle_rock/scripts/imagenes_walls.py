#!/usr/bin/env python3
"""CR City Hotel rev2 - evidencia visual por wall (U-118 / BE-CR25: en rev1 U-118 pasaba en vacío con walls = 0).
(1) img: por wall físico (id base + hoja) un recorte de su hoja con el path circulado en ROJO (rectángulo alrededor del path
    + elipse), etapas/7_imagenes/walls/<id>_<hoja>.png; las entradas que ya traen una imagen existente de la lectura la conservan.
(2) height_img: por fuente de altura (primera N/HOJA de height_source) la hoja citada con la cota impresa circulada en rojo
    (search_for de cada cota ft-in del texto, variantes "11' - 0\"" / "11'-0\""); sin cota encontrada se circula la
    burbuja / título de la vista. etapas/7_imagenes/alturas/<N>_<HOJA>.png.
Escribe img / height_img (rutas absolutas) en el canon."""
import json, os, re, collections
import pymupdf as fitz
W = '/root/cr/work'
CP = f'{W}/etapas/4_canon/takeoff_canon.json'
c = json.load(open(CP))
D = fitz.open(f'{W}/plans/bidset_SIN_MARKUPS.pdf')
HS = list(json.load(open(f'{W}/set_texto.json'))['hojas'])
OW, OH = f'{W}/etapas/7_imagenes/walls', f'{W}/etapas/7_imagenes/alturas'
os.makedirs(OW, exist_ok=True); os.makedirs(OH, exist_ok=True)
ROJO = (1, 0, 0)


def existe(p):
    if not p:
        return None
    for d in ('', f'{W}/etapas/2_lectura/A', f'{W}/etapas/2_lectura/B', f'{W}/etapas/3_revision', f'{W}/etapas/4_canon', W, f'{W}/etapas'):
        q = os.path.join(d, p) if d else p
        if os.path.isfile(q):
            return os.path.abspath(q)
    return None


# (1) imagen por wall
grupos = collections.defaultdict(list)
for e in c['existing_walls']:
    grupos[(re.sub(r" [A-Z]$", "", e['id']), e['sheet'], e['page'])].append(e)
n1 = 0
for (base, sh, pg), es in grupos.items():
    pts = [tuple(map(float, q)) for e in es for q in e['path']]
    x0, y0 = min(p[0] for p in pts), min(p[1] for p in pts)
    x1, y1 = max(p[0] for p in pts), max(p[1] for p in pts)
    page = D[pg - 1]
    r = fitz.Rect(x0 - 6, y0 - 6, x1 + 6, y1 + 6)
    clip = fitz.Rect(r.x0 - 120, r.y0 - 120, r.x1 + 120, r.y1 + 120) & page.rect
    sc = min(3.0, 520 / max(clip.width, clip.height))
    pix = page.get_pixmap(matrix=fitz.Matrix(sc, sc), clip=clip)
    out = f"{OW}/{re.sub(r'[^A-Za-z0-9.-]+', '_', base)}_{sh}.png"
    # dibujar sobre una copia en memoria para no tocar el PDF
    doc2 = fitz.open(); p2 = doc2.new_page(width=clip.width, height=clip.height)
    p2.insert_image(p2.rect, pixmap=pix)
    rr = fitz.Rect(r.x0 - clip.x0, r.y0 - clip.y0, r.x1 - clip.x0, r.y1 - clip.y0)
    p2.draw_rect(rr, color=ROJO, width=2.2)
    p2.draw_oval(fitz.Rect(rr.x0 - 14, rr.y0 - 14, rr.x1 + 14, rr.y1 + 14), color=ROJO, width=1.4)
    p2.insert_text((6, 14), f"{base} - {sh} (wall path circled)", fontsize=9, color=ROJO)
    p2.get_pixmap(matrix=fitz.Matrix(sc, sc)).save(out)
    n1 += 1
    for e in es:
        if existe(e.get('img')) and existe(e.get('img')) != out:
            e['img_lectura'] = existe(e['img'])      # imagen de la lectura A / B (se conserva como referencia)
        e['img'] = out

# (2) imagen por fuente de altura
RX_NH = re.compile(r"\b(\d{1,2})\s*/\s*(A\d\.\d{2})\b")
RX_SH = re.compile(r"\b(A\d\.\d{2})\b")
RX_FT = re.compile(r"(\d{1,2})'\s*-?\s*(\d{1,2})(?:\s+(\d{1,2}/\d{1,2}))?\"")


def variantes(m):
    ft, inch, fr = m.group(1), m.group(2), m.group(3)
    i = f"{inch} {fr}" if fr else inch
    return [f"{ft}' - {i}\"", f"{ft}'-{i}\"", f"{ft}' -{i}\"", f"{ft}'- {i}\""]


hecho = {}
n2 = 0
for e in c['existing_walls']:
    hs = str(e.get('height_source') or '')
    m = RX_NH.search(hs)
    if m:
        n, sh = m.group(1).lstrip('0') or m.group(1), m.group(2)
    else:
        m2 = RX_SH.search(hs)
        if m2:
            n, sh = '', m2.group(1)
        else:   # sin hoja en el texto: la sección típica de altura del piso (4/A5.05 L2-L3, 1/A5.06 L4, 5/A5.04 L1)
            n, sh = {'L1': ('5', 'A5.04'), 'L2': ('4', 'A5.05'), 'L3': ('4', 'A5.05'), 'L4': ('1', 'A5.06')}.get(e['floor'], ('4', 'A5.05'))
    if sh not in HS:
        continue
    dims = tuple(sorted({v for mm in RX_FT.finditer(hs) for v in variantes(mm)}))
    key = (n, sh, dims)
    if key not in hecho:
        page = D[HS.index(sh)]
        rects = [r for v in dims for r in page.search_for(v)]
        if not rects and n:
            rects = [fitz.Rect(w[:4]) for w in page.get_text('words') if w[4] == n and (w[3] - w[1]) > 6]
        doc2 = fitz.open(); doc2.insert_pdf(D, from_page=HS.index(sh), to_page=HS.index(sh))
        p2 = doc2[0]
        for r in rects[:40]:
            p2.draw_oval(fitz.Rect(r.x0 - 8, r.y0 - 8, r.x1 + 8, r.y1 + 8), color=ROJO, width=2.5)
        p2.insert_text((30, 40), f"height source {n + '/' if n else ''}{sh}: printed dimension(s) circled", fontsize=22, color=ROJO)
        out = f"{OH}/H_{(n + '_') if n else ''}{sh}_{len(hecho):02d}.png"
        p2.get_pixmap(dpi=55).save(out)
        hecho[key] = (out, len(rects))
        n2 += 1
    e['height_img'] = hecho[key][0]
json.dump(c, open(CP, 'w'), indent=1)
sin = sum(1 for e in c['existing_walls'] if not e.get('height_img'))
print('walls img', n1, '| height imgs', n2, '| entradas sin height_img', sin)
for k, (o, nr) in hecho.items():
    if nr == 0:
        print('  sin cota encontrada:', k[0], k[1], o)
