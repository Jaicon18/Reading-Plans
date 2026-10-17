#!/usr/bin/env python3
"""comparar.py — ETAPA 3: doble lectura comparada. Empareja los walls de dos lecturas INDEPENDIENTES del mismo plano
(canon A y canon B) y los cruza contra el inventario por script (inventario.py). Hace visible cualquier diferencia
en vez de que una lectura pise a la otra en silencio.

Qué hace
  1. Parte los walls de A y de B con la MISMA regla (particion.py, modo = particion.MODO_DEFAULT o --modo).
  2. Empareja por type + hoja + posición (bbox de las bands) y, si una lectura no trae geometría, por LF
     (solo si la diferencia es <= LF_MATCH_MAX; se marca "match por LF").
     Clasifica: coincide (|ΔLF| <= 2 %), difiere (con delta), solo en A, solo en B.
  3. Cruza contra el inventario:
       - todo tag del inventario (partition_tag) sin wall cercano de su type en NINGUNA lectura = ALERTA "tag sin wall"
         (cercano = el wall cita el id del tag en `tag_ids`, o su band pasa a <= radio_ft del centro del tag);
       - todo wall cuyo type no está en el schedule del inventario = ALERTA "type no inventariado";
       - type del schedule con walls en una hoja donde el inventario no tiene ningún tag de ese type = ALERTA.
  4. Una imagen por diferencia y por alerta con posición (A = azul, B = naranja, tag = rojo), reabierta y verificada.

Salida: <out_dir>/revision.md (corta, en inglés, para el estimador) + revision.json + img/*.png

Uso:  python3 comparar.py canon_A.json canon_B.json inventario.json out_dir [--modo run|tramo] [--pdf plano.pdf]
                         [--radio-ft 5]
"""
import json
import math
import os
import sys
from collections import OrderedDict, defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import particion as P  # noqa: E402

TOL_COINCIDE = 0.02      # <= 2 % de LF = coinciden
LF_MATCH_MAX = 0.10      # sin geometría: solo se empareja por LF si difieren <= 10 %
RADIO_FT = 5.0           # tag -> wall: el centro del tag a <= 5 ft de la band (los tags van con leader corto)
AZUL, NARANJA, ROJO = (0.05, 0.25, 0.95), (1.0, 0.55, 0.0), (1.0, 0.0, 0.0)


def _pagina(w, mapa):
    if w.get("page"):
        return int(w["page"])
    return mapa.get(w.get("sheet"))


def _rects(w):
    out = []
    for b in w.get("bands") or []:
        e = b["espesor"] / 2.0
        if b["ori"] == "H":
            out.append((b["lo"], b["eje"] - e, b["hi"], b["eje"] + e))
        else:
            out.append((b["eje"] - e, b["lo"], b["eje"] + e, b["hi"]))
    return out


def _dist_rect(p, r):
    dx = max(r[0] - p[0], 0, p[0] - r[2])
    dy = max(r[1] - p[1], 0, p[1] - r[3])
    return math.hypot(dx, dy)


def _solape(a, b, pad):
    """Fracción de solape de dos bbox (expandidas pad) sobre la menor; 0 si no se tocan."""
    if not a or not b:
        return 0.0
    A = (a[0] - pad, a[1] - pad, a[2] + pad, a[3] + pad)
    B = (b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad)
    ix = max(0.0, min(A[2], B[2]) - max(A[0], B[0]))
    iy = max(0.0, min(A[3], B[3]) - max(A[1], B[1]))
    menor = min((A[2] - A[0]) * (A[3] - A[1]), (B[2] - B[0]) * (B[3] - B[1]))
    return ix * iy / menor if menor > 0 else 0.0


def emparejar(wa, wb, esc):
    """Greedy: primero por solape geométrico, luego (sin geometría) por LF cercano."""
    pares, usados_a, usados_b = [], set(), set()
    cand = []
    for i, a in enumerate(wa):
        for j, b in enumerate(wb):
            s = _solape(a.get("bbox_pt"), b.get("bbox_pt"), 0.5 * esc)
            if s > 0:
                cand.append((-s, abs(a["lf"] - b["lf"]), i, j))
    for _, _, i, j in sorted(cand):
        if i not in usados_a and j not in usados_b:
            pares.append((i, j, "position"))
            usados_a.add(i)
            usados_b.add(j)
    cand = []
    for i, a in enumerate(wa):
        for j, b in enumerate(wb):
            if i in usados_a or j in usados_b:
                continue
            if a.get("bbox_pt") and b.get("bbox_pt"):
                continue                       # los dos tienen geometría y no se tocan: son walls distintos
            m = max(a["lf"], b["lf"]) or 1.0
            if abs(a["lf"] - b["lf"]) / m <= LF_MATCH_MAX:
                cand.append((abs(a["lf"] - b["lf"]), i, j))
    for _, i, j in sorted(cand):
        if i not in usados_a and j not in usados_b:
            pares.append((i, j, "LF only (no geometry)"))
            usados_a.add(i)
            usados_b.add(j)
    solo_a = [i for i in range(len(wa)) if i not in usados_a]
    solo_b = [j for j in range(len(wb)) if j not in usados_b]
    return pares, solo_a, solo_b


def _tag_ids(canon):
    """id de segmento del canon -> tag_ids del inventario que ese segmento cita."""
    return {w["id"]: set(w.get("tag_ids") or []) for w in canon.get("walls") or []}


def comparar(canon_a, canon_b, inv, modo=None, radio_ft=RADIO_FT):
    modo = modo or P.MODO_DEFAULT
    pa, pb = P.particion(canon_a, modo), P.particion(canon_b, modo)
    esc = pa["escala_pt_por_ft"]
    if abs(pb["escala_pt_por_ft"] - esc) > 1e-6:
        raise ValueError(f"escalas distintas entre lecturas: A {esc} pt/ft vs B {pb['escala_pt_por_ft']} pt/ft")
    cnt = defaultdict(int)
    for h in inv.get("sheets") or []:
        if h.get("sheet"):
            cnt[h["sheet"]] += 1
    mapa = {h["sheet"]: h["page"] for h in inv.get("sheets") or [] if h.get("sheet") and cnt[h["sheet"]] == 1}
    sched = [t["type"] for t in (inv.get("partition_types") or {}).get("schedule") or []]
    cand = {o["text"] for o in (inv.get("ocurrencias") or {}).get("partition_candidato") or []}
    tags = (inv.get("ocurrencias") or {}).get("partition_tag") or []

    def filas(p, lado):
        out = []
        for t, d in p["types"].items():
            for w in d["filas"]:
                out.append(dict(w, type=t, lectura=lado))
        return out
    fa, fb = filas(pa, "A"), filas(pb, "B")
    avisos = [f"A: {x}" for x in pa["avisos"]] + [f"B: {x}" for x in pb["avisos"]]
    for w in fa + fb:
        w["page"] = _pagina(w, mapa)
        if w["page"] is None and w["sheet"] in cnt:
            avisos.append(f"{w['lectura']} {w['wall']} ({w['type']}): hoja {w['sheet']} repetida en el PDF y el wall "
                          f"no trae `page` -> no se puede ubicar")
    claves = OrderedDict()
    for w in fa + fb:
        claves.setdefault((w["type"], w["sheet"]), None)
    coinciden, difieren, solo_a, solo_b = [], [], [], []
    for (t, sh) in claves:
        wa = [w for w in fa if w["type"] == t and w["sheet"] == sh]
        wb = [w for w in fb if w["type"] == t and w["sheet"] == sh]
        pares, sa, sb = emparejar(wa, wb, esc)
        for i, j, via in pares:
            a, b = wa[i], wb[j]
            m = max(a["lf"], b["lf"]) or 1.0
            d = {"type": t, "sheet": sh, "page": a["page"] or b["page"], "A": a, "B": b, "via": via,
                 "delta_lf": round(b["lf"] - a["lf"], 3), "delta_pct": round(100.0 * abs(b["lf"] - a["lf"]) / m, 2)}
            (coinciden if abs(b["lf"] - a["lf"]) / m <= TOL_COINCIDE else difieren).append(d)
        solo_a += [{"type": t, "sheet": sh, "page": wa[i]["page"], "A": wa[i]} for i in sa]
        solo_b += [{"type": t, "sheet": sh, "page": wb[j]["page"], "B": wb[j]} for j in sb]

    # --- cruce con el inventario ---
    alertas = []
    tid_a, tid_b = _tag_ids(canon_a), _tag_ids(canon_b)
    radio = radio_ft * esc
    cobertura = []
    for o in tags:
        res = {}
        for lado, fx, tid in (("A", fa, tid_a), ("B", fb, tid_b)):
            ws = [w for w in fx if w["type"] == o["type"] and w["page"] == o["page"]]
            por_id = [w for w in ws if any(o["id"] in tid.get(x, ()) for x in w["ids"])]
            por_pos = [w for w in ws if any(_dist_rect(o["center_pt"], r) <= radio for r in _rects(w))]
            sin_geo = [w for w in ws if not w.get("bands")]
            res[lado] = {"walls": [w["wall"] for w in (por_id or por_pos)],
                         "via": "tag_ids" if por_id else ("position" if por_pos else None),
                         "sin_geometria": len(sin_geo)}
        c = {"tag": o["id"], "type": o["type"], "sheet": o["sheet"], "page": o["page"], "center_pt": o["center_pt"],
             "A": res["A"], "B": res["B"]}
        cobertura.append(c)
        if not res["A"]["walls"] and not res["B"]["walls"]:
            nv = res["A"]["sin_geometria"] + res["B"]["sin_geometria"]
            alertas.append({"kind": "tag sin wall", "type": o["type"], "sheet": o["sheet"], "page": o["page"],
                            "tag": o, "detalle": f"tag {o['id']} {o['type']} has no wall of its type within "
                                                 f"{radio_ft} ft in reading A nor B"
                            + (f" ({nv} wall(s) of that type without geometry could not be checked)" if nv else "")})
    tags_por = defaultdict(int)
    for o in tags:
        tags_por[(o["type"], o["page"])] += 1
    vistos = set()
    for w in fa + fb:
        k = (w["type"], w["lectura"])
        if w["type"] not in sched:
            if k in vistos:
                continue
            vistos.add(k)
            extra = (" — the tag exists on the drawings but NOT in the partition schedule (RFI)" if w["type"] in cand
                     else " — not a schedule type (exterior / other framing / typo?)")
            alertas.append({"kind": "type no inventariado", "type": w["type"], "sheet": w["sheet"],
                            "page": w["page"], "wall": w, "detalle": f"reading {w['lectura']} uses type "
                                                                       f"{w['type']}{extra}"})
        elif w["page"] is not None and tags_por[(w["type"], w["page"])] == 0:
            alertas.append({"kind": "wall sin tag en la hoja", "type": w["type"], "sheet": w["sheet"],
                            "page": w["page"], "wall": w,
                            "detalle": f"reading {w['lectura']} wall {w['wall']} ({w['type']}) is on a sheet where the "
                                       f"inventory found no {w['type']} tag"})
    resumen = OrderedDict()
    for t in list(dict.fromkeys([w["type"] for w in fa + fb])):
        resumen[t] = {"A_walls": sum(1 for w in fa if w["type"] == t), "B_walls": sum(1 for w in fb if w["type"] == t),
                      "A_lf": round(sum(w["lf"] for w in fa if w["type"] == t), 2),
                      "B_lf": round(sum(w["lf"] for w in fb if w["type"] == t), 2),
                      "coinciden": sum(1 for d in coinciden if d["type"] == t),
                      "difieren": sum(1 for d in difieren if d["type"] == t),
                      "solo_A": sum(1 for d in solo_a if d["type"] == t),
                      "solo_B": sum(1 for d in solo_b if d["type"] == t),
                      "tags_inventario": sum(1 for o in tags if o["type"] == t)}
    return {"modo": modo, "tolerancia_pct": TOL_COINCIDE * 100, "radio_ft": radio_ft, "escala_pt_por_ft": esc,
            "resumen": resumen, "coinciden": coinciden, "difieren": difieren, "solo_A": solo_a, "solo_B": solo_b,
            "alertas": alertas, "cobertura_tags": cobertura, "avisos": avisos}


# --------------------------------------------------------------------------------------------------------- imágenes
def imagenes(rev, pdf, out_dir, dpi=110, margen=40.0):
    """Un PNG por diferencia / alerta con posición. Se reabre y se verifica que cada color está donde debe."""
    try:
        import pymupdf as fitz
    except ImportError:
        return ["pymupdf no disponible: sin imágenes"]
    if not pdf or not os.path.exists(pdf):
        return [f"PDF no disponible ({pdf}): revision.md sin imágenes"]
    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(pdf)
    fallas = []
    items = [("DIF", d) for d in rev["difieren"]] + [("ONLYA", d) for d in rev["solo_A"]] + \
            [("ONLYB", d) for d in rev["solo_B"]] + [("ALERT", d) for d in rev["alertas"]]
    for n, (k, d) in enumerate(items, 1):
        pg = d.get("page")
        ws = [x for x in (d.get("A"), d.get("B"), d.get("wall")) if x]
        rects = [(w["lectura"], r) for w in ws for r in _rects(w)]
        tag = d.get("tag")
        if not pg or (not rects and not tag):
            d["img"] = None
            d["img_nota"] = "no image: no page or no geometry"
            continue
        xs = [r[0] for _, r in rects] + [r[2] for _, r in rects]
        ys = [r[1] for _, r in rects] + [r[3] for _, r in rects]
        if tag:
            xs += [tag["center_pt"][0]]
            ys += [tag["center_pt"][1]]
        tmp = fitz.open()
        tmp.insert_pdf(doc, from_page=pg - 1, to_page=pg - 1)
        page = tmp[0]
        clip = fitz.Rect(min(xs) - margen, min(ys) - margen, max(xs) + margen, max(ys) + margen) & page.rect
        esperados = []
        for lado, r in rects:
            col = AZUL if lado == "A" else NARANJA
            off = 0 if lado == "A" else 2.5            # B un poco desplazado para que no tape a A
            rr = fitz.Rect(r[0] - 2 - off, r[1] - 2 - off, r[2] + 2 + off, r[3] + 2 + off)
            a = page.add_rect_annot(rr * page.derotation_matrix)
            a.set_colors(stroke=col)
            a.set_border(width=2.0)
            a.update()
            esperados.append((col, rr))
        if tag:
            cx, cy = tag["center_pt"]
            rr = fitz.Rect(cx - 12, cy - 12, cx + 12, cy + 12)
            a = page.add_circle_annot(rr * page.derotation_matrix)
            a.set_colors(stroke=ROJO)
            a.set_border(width=2.0)
            a.update()
            esperados.append((ROJO, rr))
        nombre = f"{n:03d}_{k}_{d['type']}_{d.get('sheet') or 'p'}_p{pg}.png".replace("/", "_")
        ruta = os.path.join(out_dir, nombre)
        page.get_pixmap(clip=clip, dpi=dpi).save(ruta)
        tmp.close()
        ok = _verificar(ruta, clip, dpi / 72.0, esperados)
        d["img"] = nombre
        d["img_verificada"] = ok
        if not ok:
            fallas.append(f"{nombre}: un color esperado no aparece en su lugar")
    return fallas


def _verificar(ruta, clip, z, esperados):
    import pymupdf as fitz
    pix = fitz.Pixmap(ruta)
    for col, rr in esperados:
        tgt = tuple(int(c * 255) for c in col)
        hits = tot = 0
        x0, y0 = (rr.x0 - clip.x0) * z, (rr.y0 - clip.y0) * z
        x1, y1 = (rr.x1 - clip.x0) * z, (rr.y1 - clip.y0) * z
        pts = [(x0 + (x1 - x0) * u / 10.0, y) for u in range(11) for y in (y0, y1)] + \
              [(x, y0 + (y1 - y0) * u / 10.0) for u in range(11) for x in (x0, x1)]
        if col == ROJO:
            cx, cy, r = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2
            pts = [(cx + r * math.cos(k * math.pi / 8), cy + r * math.sin(k * math.pi / 8)) for k in range(16)]
        for (x, y) in pts:
            tot += 1
            for dx in range(-3, 4):
                for dy in range(-3, 4):
                    xi, yi = int(round(x + dx)), int(round(y + dy))
                    if 0 <= xi < pix.width and 0 <= yi < pix.height:
                        p = pix.pixel(xi, yi)[:3]
                        if sum(abs(p[c] - tgt[c]) for c in range(3)) < 120:
                            hits += 1
                            break
                else:
                    continue
                break
        if tot and hits / tot < 0.6:
            return False
    return True


# -------------------------------------------------------------------------------------------------------- reporte
def _w(w):
    return f"{w['wall']} {w['lf']:.2f} LF" + (f" ({w['tramos']} straight segments)" if w.get("tramos", 1) > 1 else "")


def _img(d):
    if d.get("img"):
        return f" — ![img](img/{d['img']})" + ("" if d.get("img_verificada") else " (IMAGE NOT VERIFIED)")
    return f" — {d.get('img_nota', 'no image')}" if "img_nota" in d else ""


def md(rev, a_name, b_name, inv_name):
    L = [f"# Double-reading review — {a_name} vs {b_name}", "",
         f"Inventory: {inv_name} · partition rule: **{rev['modo']}** · match tolerance: {rev['tolerancia_pct']:.0f} % "
         f"of LF · tag-to-wall radius: {rev['radio_ft']} ft", "",
         "## Matching walls (one line per type)", ""]
    for t, r in rev["resumen"].items():
        L.append(f"- **{t}**: {r['coinciden']} walls match · A {r['A_walls']} walls / {r['A_lf']} LF · "
                 f"B {r['B_walls']} walls / {r['B_lf']} LF · inventory tags {r['tags_inventario']}")
    n = 0
    L += ["", "## Items to review", ""]
    for d in rev["difieren"]:
        n += 1
        L.append(f"{n}. **{d['type']}** — Sheet {d['sheet']} (p.{d['page']}) — LF differs {d['delta_lf']:+.2f} LF "
                 f"({d['delta_pct']:.1f} %): A {_w(d['A'])} vs B {_w(d['B'])} [matched by {d['via']}]{_img(d)}")
    for d in rev["solo_A"]:
        n += 1
        L.append(f"{n}. **{d['type']}** — Sheet {d['sheet']} (p.{d['page']}) — only in reading A: {_w(d['A'])}{_img(d)}")
    for d in rev["solo_B"]:
        n += 1
        L.append(f"{n}. **{d['type']}** — Sheet {d['sheet']} (p.{d['page']}) — only in reading B: {_w(d['B'])}{_img(d)}")
    if n == 0:
        L.append("None: both readings agree wall by wall.")
    L += ["", "## Alerts (inventory cross-check)", ""]
    for k, d in enumerate(rev["alertas"], 1):
        L.append(f"{k}. **{d['kind'].upper()}** — {d['type']} — Sheet {d.get('sheet')} (p.{d.get('page')}): "
                 f"{d['detalle']}{_img(d)}")
    if not rev["alertas"]:
        L.append("None.")
    if rev["avisos"]:
        L += ["", "## Notes", ""] + [f"- {x}" for x in rev["avisos"]]
    L += ["", "Legend: blue = reading A, orange = reading B, red circle = inventory tag."]
    return "\n".join(L) + "\n"


def main(argv):
    a = list(argv[1:])
    opts = {"--modo": None, "--pdf": None, "--radio-ft": None}
    for k in list(opts):
        if k in a:
            i = a.index(k)
            opts[k] = a[i + 1]
            del a[i:i + 2]
    if len(a) != 4:
        print(__doc__)
        return 2
    ca, cb, inv = (json.load(open(x)) for x in a[:3])
    out = a[3]
    os.makedirs(out, exist_ok=True)
    rev = comparar(ca, cb, inv, opts["--modo"], float(opts["--radio-ft"] or RADIO_FT))
    pdf = opts["--pdf"] or inv.get("pdf_path")
    fallas = imagenes(rev, pdf, os.path.join(out, "img"))
    rev["avisos"] += fallas
    with open(os.path.join(out, "revision.json"), "w") as f:
        json.dump(rev, f, indent=1, ensure_ascii=False)
    with open(os.path.join(out, "revision.md"), "w") as f:
        f.write(md(rev, os.path.basename(a[0]), os.path.basename(a[1]), os.path.basename(a[2])))
    print(f"modo {rev['modo']}: coinciden {len(rev['coinciden'])} · difieren {len(rev['difieren'])} · solo A "
          f"{len(rev['solo_A'])} · solo B {len(rev['solo_B'])} · alertas {len(rev['alertas'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
