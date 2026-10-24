#!/usr/bin/env python3
"""cotas_banda.py — v73: cotas IMPRESAS paralelas a la banda de un wall (regla R73.1, "la cota impresa manda").

Por qué existe: una corrida midió en vector el largo de un wall con hatch (type K) cuando el plano imprimía la cota
de ese mismo tramo; el número salió distinto del impreso y ninguna compuerta lo vio porque el canon solo traía
`hatch_extent`. Desde v73 todo wall K (y todo wall que se quiera revisar) lleva `dim_scan`, la salida de esta tool:
las cotas impresas cuya línea de texto es paralela a la banda, cae a menos de `win` pt de ella y tiene su centro
dentro del tramo [lo, hi] (con margen). La compuerta (chequeos_v73.r73_1) exige que el largo del wall sea una de
esas cotas cuando alguna es compatible (± 35 %), o que el wall declare por qué no aplica.

Coordenadas: pt de la página MOSTRADA (page.rect, ya rotada), las mismas del canon (`band`).
Uso:
  python3 cotas_banda.py <plano.pdf> <pagina_1based> '<band json>' [--win 72]
  -> JSON {"found": [{text, value_ft, center, dist_pt}], "source": "...", "win_pt": N}
Como módulo: cotas(page, band, win=72) / dim_scan(pdf_path, page_1based, band, win=72)
"""
import json
import re
import sys

DIM = re.compile(r"^\s*(\d{1,3})\s*'\s*(?:-\s*)?(?:(\d{1,2})(?:\s+(\d{1,2})/(\d{1,2}))?\s*\")?\s*(?:HOLD|CLR\.?|EQ\.?|TYP\.?)?\s*$",
                 re.I)
DIM_IN = re.compile(r"^\s*(\d{1,2})(?:\s+(\d{1,2})/(\d{1,2}))?\s*\"\s*(?:HOLD|CLR\.?)?\s*$", re.I)


def valor_ft(t):
    """"3' - 5\"" -> 3.4167; "5'-6 1/2\"" -> 5.5417; "4\"" -> 0.3333; texto que no es cota -> None."""
    t = str(t).replace("’", "'").replace("”", '"').replace("″", '"').replace("′", "'")
    m = DIM.match(t)
    if m:
        pies = int(m.group(1))
        pul = int(m.group(2) or 0)
        fr = (int(m.group(3)) / int(m.group(4))) if m.group(3) else 0.0
        return round(pies + (pul + fr) / 12.0, 4)
    m = DIM_IN.match(t)
    if m:
        fr = (int(m.group(2)) / int(m.group(3))) if m.group(2) else 0.0
        return round((int(m.group(1)) + fr) / 12.0, 4)
    return None


def _lineas(page):
    """Líneas de texto en coordenadas de la página mostrada: (texto, (x0, y0, x1, y1), dir 'H'|'V')."""
    import pymupdf as fitz
    M = page.rotation_matrix
    out = []
    for b in page.get_text("dict").get("blocks", []):
        for ln in b.get("lines", []):
            t = "".join(s.get("text", "") for s in ln.get("spans", []))
            if not t.strip():
                continue
            r = fitz.Rect(ln["bbox"]) * M
            dx, dy = ln.get("dir", (1, 0))
            vx, vy = dx * M.a + dy * M.c, dx * M.b + dy * M.d
            out.append((t.strip(), (r.x0, r.y0, r.x1, r.y1), "H" if abs(vx) >= abs(vy) else "V"))
    return out


def cotas(page, band, win=72.0, margen=12.0):
    """Cotas impresas paralelas a la banda {ori H|V, c0, c1, lo, hi} a menos de `win` pt de ella."""
    ori = str(band.get("ori", "")).upper()
    if ori not in ("H", "V"):
        return []
    c0, c1 = sorted((float(band["c0"]), float(band["c1"])))
    lo, hi = sorted((float(band["lo"]), float(band["hi"])))
    out = []
    for t, (x0, y0, x1, y1), d in _lineas(page):
        if d != ori:
            continue
        v = valor_ft(t)
        if v is None:
            continue
        if ori == "H":
            ce, cp = (x0 + x1) / 2.0, (y0 + y1) / 2.0
        else:
            ce, cp = (y0 + y1) / 2.0, (x0 + x1) / 2.0
        if not (lo - margen <= ce <= hi + margen):
            continue
        dist = 0.0 if c0 <= cp <= c1 else min(abs(cp - c0), abs(cp - c1))
        if dist <= win:
            out.append({"text": t, "value_ft": v, "center": [round((x0 + x1) / 2, 2), round((y0 + y1) / 2, 2)],
                        "dist_pt": round(dist, 2)})
    return sorted(out, key=lambda x: x["dist_pt"])


def dim_scan(pdf_path, page_1based, band, win=72.0):
    import pymupdf as fitz
    doc = fitz.open(pdf_path)
    pg = doc[int(page_1based) - 1]
    f = cotas(pg, band, win)
    return {"found": f, "win_pt": win, "source": f"cotas_banda.py p{int(page_1based)} band "
                                                 f"{band.get('ori')} {band.get('c0')}-{band.get('c1')} / "
                                                 f"{band.get('lo')}-{band.get('hi')}"}


def main(argv):
    a = list(argv[1:])
    win = 72.0
    if "--win" in a:
        i = a.index("--win")
        win = float(a[i + 1])
        del a[i:i + 2]
    if len(a) != 3:
        print(__doc__)
        return 2
    print(json.dumps(dim_scan(a[0], int(a[1]), json.loads(a[2]), win), ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
