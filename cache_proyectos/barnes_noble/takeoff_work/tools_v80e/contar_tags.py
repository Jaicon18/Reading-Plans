#!/usr/bin/env python3
"""contar_tags.py v65 — cuenta las fixtures por TAG en una hoja del bid set (texto vectorial), DETERMINISTA.

Por qué existe (arbitraje #14, 17-oct-2026): #14B cargó un tag de fixture x <n> cuando la hoja E dibuja <n> tags
(+<n> LF de framed openings). El conteo a ojo varía entre agentes; el texto del PDF no.

Uso:
  python3 contar_tags.py bidset.pdf <hoja E> <tag> [<tag> ...] [--png salida.png] [--json salida.json]
Busca la página cuyo número de hoja (el texto con forma de sheet number de mayor tamaño) es la hoja pedida;
cuenta las palabras IGUALES al tag (no substrings) y devuelve {tag: {"count", "sheet", "page", "pts": [[x, y]...]}}.
Con --png dibuja un círculo rojo en cada ocurrencia (evidencia visual; reabrirla antes de entregar).
La salida va directo a framed_openings.py como "tag_counts".

v66 (arbitraje #15A/#15B, 2026-10-17): en las hojas E los tags de luminaria llevan sufijo de circuito / switch
("R-11C,d", "R-14B,c"): la coincidencia exacta los contaba 0. Ahora cada palabra se NORMALIZA quitando el sufijo
",x" final (1 a 3 caracteres) y se compara exacto contra el tag ("R-11CE,a" sigue siendo R-11CE, no R-11C).
Cada tag reporta count (normalizado), count_exacto (sin sufijo) y variantes {texto: n} para revisar.
"""
import json
import re
import sys

RX_SHEET = re.compile(r"[A-Z]{1,2}\d{1,2}\.\d{2}")


def pagina_de_hoja(doc, hoja):
    for i, p in enumerate(doc):
        best = (0, None)
        for b in p.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                for s in ln["spans"]:
                    t = s["text"].strip()
                    if RX_SHEET.fullmatch(t) and s["size"] > best[0]:
                        best = (s["size"], t)
        if best[1] == hoja:
            return i
    raise ValueError(f"hoja {hoja} no encontrada en el bid set")


RX_SUFIJO = re.compile(r",[A-Za-z0-9]{0,3}$")


def normalizar(texto):
    """'R-11C,d' -> 'R-11C'; 'R-11C,' -> 'R-11C'; 'XX3' -> 'XX3'. Solo el sufijo de circuito al final."""
    return RX_SUFIJO.sub("", str(texto).strip())


def contar_en_palabras(words, tags):
    """words: lista (x0, y0, x1, y1, texto, ...) de PyMuPDF. Coincidencia exacta del texto NORMALIZADO (v66)."""
    out = {t: {"count": 0, "count_exacto": 0, "variantes": {}, "pts": []} for t in tags}
    for w in words:
        crudo = str(w[4]).strip()
        t = normalizar(crudo)
        if t in out:
            out[t]["count"] += 1
            out[t]["count_exacto"] += int(crudo == t)
            out[t]["variantes"][crudo] = out[t]["variantes"].get(crudo, 0) + 1
            out[t]["pts"].append([round((w[0] + w[2]) / 2, 1), round((w[1] + w[3]) / 2, 1)])
    return out


def contar(pdf, hoja, tags):
    import pymupdf as fitz
    doc = fitz.open(pdf)
    pg = pagina_de_hoja(doc, hoja)
    res = contar_en_palabras(doc[pg].get_text("words"), tags)
    for v in res.values():
        v.update(sheet=hoja, page=pg)
    return res, doc, pg


def marcar(doc, pg, res, png, dpi=60):
    import pymupdf as fitz
    p = doc[pg]
    for v in res.values():
        for x, y in v["pts"]:
            r = fitz.Rect(x - 14, y - 14, x + 14, y + 14)
            p.draw_circle(fitz.Point(x, y), 16, color=(1, 0, 0), width=2.5)
            del r
    p.get_pixmap(dpi=dpi).save(png)


def main(argv):
    args = [a for a in argv[1:]]
    png = js = None
    if "--png" in args:
        i = args.index("--png"); png = args[i + 1]; del args[i:i + 2]
    if "--json" in args:
        i = args.index("--json"); js = args[i + 1]; del args[i:i + 2]
    if len(args) < 3:
        print(__doc__)
        return 2
    try:
        res, doc, pg = contar(args[0], args[1], args[2:])
    except ValueError as e:
        print(f"ERROR contar_tags.py: {e}", file=sys.stderr)
        return 1
    if png:
        marcar(doc, pg, res, png)
    s = json.dumps(res, indent=1)
    if js:
        open(js, "w").write(s)
    print(json.dumps({k: v["count"] for k, v in res.items()}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
