#!/usr/bin/env python3
"""evidencia.py — evidencia visual y estados #0 generados por PROGRAMA desde las coordenadas del canon (R80e.38).

El modelo no dibuja ni recorta: lee coordenadas (bands) y fuentes. Este programa:
  - por wall con band: recorte de su hoja con la band marcada en rojo -> img (y faces / openings del wall);
  - alturas, detalles, ceilings y demás ítems sin coordenadas: la página de la hoja que cita su fuente (N/HOJA u hoja)
    -> height_img / detail_img / img;
  - estados #0 que falten (length_status / height_status): CONFIRMADO solo si la fuente dice que la cota está impresa y
    cita la hoja; DERIVADO si la fuente trae su operación u hoja; si no, PENDIENTE.
Nunca pisa un img o un estado que la lectura ya trae. Todo lo que agrega queda listado en el resumen.

Uso: python3 evidencia.py <canon.json> <pdf> <sheet_map.md> <dir_img> [--canon-out <canon.json>] [--inventario <json>]
"""
import json
import os
import re
import sys

import fitz  # pymupdf
from PIL import Image, ImageDraw

HOJA = re.compile(r"\b([A-Z]{1,2}-?\d{3}[A-Z]?)\b")
IMPRESA = re.compile(r"CONFIRMAD|printed|impres|dimension(ed)? (string|on)", re.I)
DPI_HOJA, DPI_RECORTE, MARGEN = 40, 110, 48.0


def mapa_hojas(sheet_map):
    """SHEET_MAP.md (tabla | Page | Sheet |) -> {sheet: page index 0-based}."""
    m = {}
    for l in open(sheet_map, encoding="utf-8"):
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) >= 2 and c[0].isdigit():
            h = HOJA.search(c[1])
            if h:
                m.setdefault(h.group(1), int(c[0]) - 1)
    return m


def _txt(*v):
    return " ".join(json.dumps(x, ensure_ascii=False) if isinstance(x, (dict, list)) else str(x) for x in v if x)


class Evidencia:
    def __init__(self, pdf, hojas, d):
        self.doc, self.hojas, self.d = fitz.open(pdf), hojas, d
        os.makedirs(d, exist_ok=True)
        self.n = {"recortes": 0, "hojas": 0, "estados": 0, "img_asignadas": 0}
        self._hecho, self._render = {}, {}

    def hoja(self, texto):
        """Página completa de la primera hoja citada en el texto (N/HOJA u hoja) -> ruta relativa, o None."""
        for h in HOJA.findall(texto or ""):
            if h in self.hojas:
                k = "hoja_" + h
                if k not in self._hecho:
                    p = os.path.join(self.d, f"sheet_{h}.png")
                    self.doc[self.hojas[h]].get_pixmap(dpi=DPI_HOJA).save(p)
                    self._hecho[k] = os.path.basename(p)
                    self.n["hojas"] += 1
                return os.path.join(os.path.basename(self.d), self._hecho[k])
        return None

    def recorte(self, w):
        """Recorte de la hoja del wall con su band en rojo -> ruta relativa, o None (sin band / hoja desconocida)."""
        b, h = w.get("band") or {}, (w.get("band") or {}).get("sheet") or w.get("sheet")
        if h not in self.hojas or b.get("ori") not in ("H", "V", "BOX", "D"):
            return None
        if b["ori"] == "H":
            r = (b["lo"], min(b["c0"], b["c1"]), b["hi"], max(b["c0"], b["c1"]))
        elif b["ori"] == "V":
            r = (min(b["c0"], b["c1"]), b["lo"], max(b["c0"], b["c1"]), b["hi"])
        elif b["ori"] == "BOX":
            r = (b["x0"], b["y0"], b["x1"], b["y1"]) if "x0" in b else (b["c0"], b["lo"], b["c1"], b["hi"])  # c = x, lo..hi = y
        else:
            (x0, y0), (x1, y1) = b["p0"], b["p1"]
            r = (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))
        # las bands están en la página ROTADA (como se ve; mismo sistema que planmark): se recorta el render
        if h not in self._render:
            pix = self.doc[self.hojas[h]].get_pixmap(dpi=DPI_RECORTE)
            self._render[h] = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        im, F = self._render[h], DPI_RECORTE / 72.0
        caja = tuple(int(v * F) for v in (max(0, r[0] - MARGEN), max(0, r[1] - MARGEN), r[2] + MARGEN, r[3] + MARGEN))
        cr = im.crop(caja).copy()
        ImageDraw.Draw(cr).rectangle([(r[0] - 3) * F - caja[0], (r[1] - 3) * F - caja[1], (r[2] + 3) * F - caja[0],
                                      (r[3] + 3) * F - caja[1]], outline=(255, 0, 0), width=3)
        p = os.path.join(self.d, f"wall_{re.sub(r'[^A-Za-z0-9._-]', '_', str(w['id']))}.png")
        cr.save(p)
        self.n["recortes"] += 1
        return os.path.join(os.path.basename(self.d), os.path.basename(p))


def _pon(o, k, v, n):
    if v and not o.get(k):
        o[k] = v
        n["img_asignadas"] += 1


def _estado(w, k, n):
    if w.get(f"{k}_ft") is None or w.get(f"{k}_status") or w.get("status"):
        return
    src = _txt(w.get(f"{k}_source"), w.get(f"{k}_op"))
    if IMPRESA.search(src) and HOJA.search(_txt(w.get(f"{k}_source"))):
        w[f"{k}_status"] = "CONFIRMADO"
    elif src.strip():
        w[f"{k}_status"] = "DERIVADO"
        if not w.get(f"{k}_op"):
            w[f"{k}_op"] = "per source: " + str(w.get(f"{k}_source"))
    else:
        w[f"{k}_status"] = "PENDIENTE"
    n["estados"] += 1


def _rect(b):
    if b.get("ori") == "H":
        return b["lo"], min(b["c0"], b["c1"]), b["hi"], max(b["c0"], b["c1"])
    if b.get("ori") == "V":
        return min(b["c0"], b["c1"]), b["lo"], max(b["c0"], b["c1"]), b["hi"]
    if b.get("ori") == "BOX":
        return (b["x0"], b["y0"], b["x1"], b["y1"]) if "x0" in b else (b["c0"], b["lo"], b["c1"], b["hi"])
    if b.get("ori") == "D":
        (x0, y0), (x1, y1) = b["p0"], b["p1"]
        return min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)
    return None


def tags_a_walls(c, inventario, tol_ft=6.0):
    """tag_ids por COORDENADAS: cada partition tag del inventario (id PT, type, hoja, centro) va al wall del mismo type
    en la misma hoja cuya band queda más cerca (<= tol_ft x escala de la hoja). Nunca pisa tag_ids de la lectura.
    -> (asignados, tags sin wall)"""
    cs = c.get("constants") or {}
    esc = lambda h: float(((cs.get("plan_scale_by_sheet") or {}).get(h) or {}).get("value")
                          or (cs.get("plan_scale_pt_per_ft") or {}).get("value") or 9.0)
    tags = [t for v in (inventario.get("ocurrencias") or {}).values() for t in v
            if str(t.get("id", "")).startswith("PT") and t.get("center_pt")]
    walls = [w for w in c.get("walls") or [] if w.get("element", "wall") == "wall" and _rect(w.get("band") or {})]
    asign, sin = {}, []
    for t in tags:
        x, y = t["center_pt"]
        best = None
        for w in walls:
            b = w["band"]
            if (b.get("sheet") or w.get("sheet")) != t.get("sheet") or str(w.get("tag")).upper() != str(t.get("type")).upper():
                continue
            x0, y0, x1, y1 = _rect(b)
            d = max(x0 - x, 0, x - x1) ** 2 + max(y0 - y, 0, y - y1) ** 2
            if d ** 0.5 <= tol_ft * esc(t.get("sheet")) and (best is None or d < best[0]):
                best = (d, w)
        if best:
            asign.setdefault(best[1]["id"], []).append(t["id"])
        else:
            sin.append(t["id"])
    n = 0
    for w in walls:
        if w["id"] in asign and not w.get("tag_ids"):
            w["tag_ids"] = sorted(asign[w["id"]])
            w["tag_ids_source"] = "[DERIVED] nearest band of the same type on the same sheet (evidencia.py, inventario)"
            n += 1
    return n, sin


def grosor(c):
    """thickness_measured_in desde la band (c1 - c0) / escala x 12, con su operación. Nunca pisa la lectura."""
    cs = c.get("constants") or {}
    n = 0
    for w in c.get("walls") or []:
        b = w.get("band") or {}
        if b.get("ori") not in ("H", "V") or w.get("thickness_measured_in") is not None:
            continue
        h = b.get("sheet") or w.get("sheet")
        e = float(((cs.get("plan_scale_by_sheet") or {}).get(h) or {}).get("value")
                  or (cs.get("plan_scale_pt_per_ft") or {}).get("value") or 9.0)
        t = round(abs(b["c1"] - b["c0"]) / e * 12, 2)
        w["thickness_measured_in"] = t
        w["thickness_check"] = f"[DERIVED] band faces {b['c0']} / {b['c1']} pt on {h} at {e} pt/ft = {t} in"
        n += 1
    return n


def hoja_de_medida(c):
    """R80e.52: una medida de band (length_source "band 67.6 pt / 9", "vector ...") sin hoja citada lleva la hoja donde se
    midió: band.sheet (un hecho del dato, no texto para una compuerta). Y length_op = la misma operación si falta."""
    n = 0
    for w in c.get("walls") or []:
        src = str(w.get("length_source") or "")
        h = (w.get("band") or {}).get("sheet") or w.get("sheet")
        if h and src and not HOJA.search(src) and re.search(r"band|vector|\bpt\b", src, re.I):
            w["length_source"] = f"{h} {src}"
            n += 1
        if w.get("length_source") and not w.get("length_op") and re.search(r"[/x+=]", str(w.get("length_source"))):
            w["length_op"] = w["length_source"]
    return n


def aplicar(c, ev, inventario=None):
    if inventario:
        ev.n["tag_ids"], ev.n["tags_sin_wall"] = tags_a_walls(c, inventario)
    ev.n["thickness"] = grosor(c)
    ev.n["hoja_de_medida"] = hoja_de_medida(c)
    for w in c.get("walls") or []:
        rec = ev.recorte(w)
        pag = ev.hoja(_txt(w.get("source"), w.get("length_source"), w.get("sheet")))
        _pon(w, "img", rec or pag, ev.n)
        _pon(w, "height_img", ev.hoja(_txt(w.get("height_source"))) or w.get("img"), ev.n)
        det = ev.hoja(_txt(w.get("detail"), w.get("detail_source"), w.get("type_source")))
        _pon(w, "detail_img", det or w.get("img"), ev.n)
        _pon(w, "stud_img", ev.hoja(_txt(w.get("stud_source"), w.get("gauge_source"))) or w.get("detail_img"), ev.n)
        for f in w.get("faces") or []:
            if isinstance(f, dict):
                _pon(f, "img", w.get("img"), ev.n)
        for o in w.get("openings") or []:
            if isinstance(o, dict):
                _pon(o, "img", w.get("img"), ev.n)
        _estado(w, "length", ev.n)
        _estado(w, "height", ev.n)
    for z in c.get("ceilings") or []:
        if isinstance(z, dict):
            _pon(z, "img", ev.hoja(_txt(z.get("source"), z.get("height_source"))), ev.n)
    for k, v in (c.get("details") or {}).items():
        if isinstance(v, dict):
            _pon(v, "img", ev.hoja(_txt(k, v.get("source"))), ev.n)
    for lista in ("blocking_items", "mep_penetrations", "wet_fixtures", "sealant_items", "tile_base", "vendor_ends",
                  "recessed_sweep", "trim_items", "accesorios_rfi", "rfis", "exclusions"):
        for x in c.get(lista) or []:
            if isinstance(x, dict):
                _pon(x, "img", ev.hoja(_txt(x.get("source"), x.get("back_source"), x.get("motivo"))), ev.n)
    return ev.n


def main(argv):
    if len(argv) < 5:
        print(__doc__)
        return 2
    out = argv[argv.index("--canon-out") + 1] if "--canon-out" in argv else argv[1]
    c = json.load(open(argv[1]))
    inv = json.load(open(argv[argv.index("--inventario") + 1])) if "--inventario" in argv else None
    n = aplicar(c, Evidencia(argv[2], mapa_hojas(argv[3]), argv[4]), inv)
    json.dump(c, open(out, "w"), indent=1, ensure_ascii=False)
    print(json.dumps({"evidencia": n}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
