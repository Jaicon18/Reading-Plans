#!/usr/bin/env python3
"""escala_pagina.py — U-152 / BE-148 (6-nov, CR City Hotel rev3c): ESCALA DE PÁGINA (/VP viewport con /Measure) en cada
página que tiene markups con /Measure, con la MISMA medida (/R) de sus markups.

Sin /VP, Bluebeam muestra la escala de página por defecto (0.125 = 1/8") también en las hojas a 1/4" aunque cada markup
traiga su /Measure correcto. Origen: cache_proyectos/herramientas/escala_pagina.py, copiada al skill en v81cf59.

- Una sola escala en la página: un viewport del tamaño de la página (BBox = MediaBox) con el /Measure de sus markups.
- Varias escalas (planta + ampliada en la misma hoja): el viewport de página con la escala más usada va PRIMERO y luego
  un viewport por cada otra escala, con BBox = unión de los /Rect de sus markups + margen (ISO 32000 12.9: el lector usa
  el ÚLTIMO viewport del arreglo que contiene el punto), así cada markup cae en un viewport con su misma /R.

Uso:  python3 -I escala_pagina.py <entrada.pdf> <salida.pdf>       (pone /VP)
      python3 -I escala_pagina.py revisar <pdf>                    (chequeo de CE_PDF_EDITABLE: 0 = PASS)
Funciones: poner(src, dst) -> [(pagina base 1, [R, ...])]; revisar(path) -> (faltas, info).
"""
import collections
import sys

MARGEN_PT = 36.0


def _r(m):
    try:
        return str(m.get("/R")).strip()
    except Exception:                                                   # noqa: BLE001
        return ""


def _medidas(page):
    """[(R, /Measure, rect)] de los markups con /Measure de la página."""
    out = []
    for a in page.obj.get("/Annots") or []:
        try:
            m = a.get("/Measure")
        except Exception:                                               # noqa: BLE001
            continue
        if m is None:
            continue
        try:
            rect = [float(v) for v in a.get("/Rect")]
        except Exception:                                               # noqa: BLE001
            rect = None
        out.append((_r(m), m, rect))
    return out


def _union(rects, mb):
    rs = [r for r in rects if r and len(r) == 4]
    if not rs:
        return list(mb)
    x0 = min(min(r[0], r[2]) for r in rs) - MARGEN_PT
    y0 = min(min(r[1], r[3]) for r in rs) - MARGEN_PT
    x1 = max(max(r[0], r[2]) for r in rs) + MARGEN_PT
    y1 = max(max(r[1], r[3]) for r in rs) + MARGEN_PT
    return [max(x0, mb[0]), max(y0, mb[1]), min(x1, mb[2]), min(y1, mb[3])]


def poner_doc(pdf):
    """pone /VP en el pikepdf.Pdf abierto -> [(pagina base 1, [R, ...])]."""
    import pikepdf
    from pikepdf import Array, Dictionary, Name
    puestas = []
    for i, page in enumerate(pdf.pages):
        meds = _medidas(page)
        if not meds:
            continue
        cuenta = collections.Counter(r for r, _, _ in meds)
        orden = [r for r, _ in cuenta.most_common()]
        mb = [float(x) for x in page.obj.MediaBox]
        vps = Array()
        for k, r in enumerate(orden):
            ej = next(m for rr, m, _ in meds if rr == r)
            bbox = mb if k == 0 else _union([rc for rr, _, rc in meds if rr == r], mb)
            vps.append(Dictionary(Type=Name.Viewport, BBox=Array(bbox), Name=pikepdf.String(f"Scale {r}"),
                                  Measure=ej))
        page.obj.VP = vps
        puestas.append((i + 1, orden))
    return puestas


def poner(src, dst):
    """copia src -> dst con /VP en cada página con markups /Measure. -> [(pagina base 1, [R, ...])]."""
    import pikepdf
    pdf = pikepdf.open(src, allow_overwriting_input=True)
    puestas = poner_doc(pdf)
    pdf.save(dst)
    pdf.close()
    return puestas


def _dentro(bbox, rect):
    cx, cy = (rect[0] + rect[2]) / 2.0, (rect[1] + rect[3]) / 2.0
    x0, x1 = sorted((bbox[0], bbox[2]))
    y0, y1 = sorted((bbox[1], bbox[3]))
    return x0 - 0.5 <= cx <= x1 + 0.5 and y0 - 0.5 <= cy <= y1 + 0.5


def revisar(path):
    """U-152 -> (faltas, info). Cada markup con /Measure debe caer (centro de su /Rect) en un viewport /VP de su página cuyo
    /Measure /R sea igual al suyo (se toma el ÚLTIMO viewport que lo contiene, como Bluebeam); falta /VP o /R distinto = falta.
    info = {paginas_con_medida, por_pagina {p: [R...]}, markups_medida}."""
    import pikepdf
    faltas, por_pag, n_med = [], {}, 0
    pdf = pikepdf.open(path)
    for i, page in enumerate(pdf.pages):
        meds = _medidas(page)
        if not meds:
            continue
        n_med += len(meds)
        vps = []
        for v in page.obj.get("/VP") or []:
            try:
                vps.append(([float(x) for x in v.get("/BBox")], _r(v.get("/Measure")) if v.get("/Measure") is not None else ""))
            except Exception:                                           # noqa: BLE001
                continue
        por_pag[i + 1] = sorted({r for _, r in vps})
        if not vps:
            rs = sorted(collections.Counter(r for r, _, _ in meds))
            faltas.append(f"p{i + 1}: {len(meds)} markup(s) con /Measure {rs} y SIN escala de página /VP (Bluebeam muestra "
                          f"la escala por defecto, 0.125 en una hoja a 1/4\")")
            continue
        malos = collections.Counter()
        for r, _, rect in meds:
            vr = None
            for bb, rv in vps:
                if rect is None or _dentro(bb, rect):
                    vr = rv
            if vr != r:
                malos[(r, vr)] += 1
        if malos:
            faltas.append(f"p{i + 1}: " + "; ".join(f"{n} markup(s) /R '{r}' en viewport /R '{vr}'" for (r, vr), n in malos.items()))
    pdf.close()
    return faltas, {"paginas_con_medida": len(por_pag), "por_pagina": por_pag, "markups_medida": n_med}


def main(argv):
    if len(argv) == 3 and argv[1] == "revisar":
        fs, info = revisar(argv[2])
        print(("FAIL" if fs else "PASS") + f" escala de página: {info['paginas_con_medida']} página(s) con markups /Measure "
              f"({info['markups_medida']} markups)")
        for p, rs in info["por_pagina"].items():
            print(f"  p{p}: /VP {rs}")
        for x in fs:
            print("  - " + x)
        return 1 if fs else 0
    if len(argv) == 3:
        for p, rs in poner(argv[1], argv[2]):
            print(f"p{p}: /VP {rs}" + ("  (AVISO: varias escalas en la hoja)" if len(rs) > 1 else ""))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
