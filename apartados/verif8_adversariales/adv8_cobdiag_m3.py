# adv8_cobdiag_m3: qué filtro v138 quita el par #3 de la muestra (CR A6.00 (404.0, 746.5)) y su geometría
import sys, math, pymupdf
sys.path.insert(0, "/tmp/verif8/take-off-metal-frame-drywall/tools"); import compuerta_entrega as CE
doc = pymupdf.open('/tmp/claude-0/crmk/CR_mk.pdf'); pg = doc[40]
es, _ = CE.cob_tipo_hoja(doc, pg); esc = CE.cob_escala(doc, pg)
segs, exc, clg = CE._cob_markups(doc, pg); e = CE.cob_estilos_muro(pg.get_drawings(), segs, esc) or CE.cob_estilos_pares(pg.get_drawings(), esc)
reg = CE._cob_region(pg, segs, exc, clg, esc)
od, oh = CE._cob_divisor_tag, CE._cob_en_hatch
def near(f): return math.hypot(f["x"] - 404.0, f["y"] - 746.5) <= 0.75 * esc
def d2(f, *a, **k):
    r = od(f, *a, **k)
    if near(f): print("divisor_tag", f, "->", r)
    return r
def h2(f, *a, **k):
    r = oh(f, *a, **k)
    if near(f): print("en_hatch", f, "->", r)
    return r
CE._cob_divisor_tag, CE._cob_en_hatch = d2, h2
out = CE.cob_diag_cortos(pg, esc, segs, reg, estilos=e)
print("esc", esc, "sale?", [f for f in out if near(f)])
dr = [d for d in pg.get_drawings() if any(it[0] == "l" and abs((it[1].x + it[2].x) / 2 - 404) < 14 and min(it[1].y, it[2].y) < 760 and max(it[1].y, it[2].y) > 735 for it in d["items"])]
for d in dr: print(d.get("color"), round(d.get("width") or 0, 2), d.get("dashes"), [(round(it[1].x, 1), round(it[1].y, 1), round(it[2].x, 1), round(it[2].y, 1)) for it in d["items"] if it[0] == "l" and abs((it[1].x + it[2].x) / 2 - 404) < 14][:4])
