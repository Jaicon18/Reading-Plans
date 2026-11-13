# adv8_cobdiag_cr: cob_diag_cortos v137 vs candidato hoja por hoja en el PDF REAL de markups de CR rev20b; furrings FALTA; filtrados
import sys, json, math, importlib.util, pymupdf
def load(p, n):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s)
    sys.path.insert(0, p.rsplit('/', 1)[0]); s.loader.exec_module(m); sys.path.pop(0); return m
C7 = load('/tmp/verif8/v137/take-off-metal-frame-drywall/tools/compuerta_entrega.py', 'c7')
C8 = load('/tmp/verif8/take-off-metal-frame-drywall/tools/compuerta_entrega.py', 'c8')
doc = pymupdf.open('/tmp/claude-0/crmk/CR_mk.pdf')
FALTA = [("A6.00", 1683.1, 297.4), ("A6.02", 1036.9, 1024.0), ("A6.02", 1036.9, 639.7), ("A7.50", 1556.4, 907.2)]
tot7 = tot8 = 0; filtrados = []; nuevos = []; furr = {}
for i, pg in enumerate(doc):
    es, _ = C7.cob_tipo_hoja(doc, pg); esc = C7.cob_escala(doc, pg) if es else None
    if not esc: continue
    segs, exc, clg = C7._cob_markups(doc, pg)
    e = C7.cob_estilos_muro(pg.get_drawings(), segs, esc) or C7.cob_estilos_pares(pg.get_drawings(), esc)
    reg = C7._cob_region(pg, segs, exc, clg, esc)
    a = [f for f in C7.cob_diag_cortos(pg, esc, segs, reg, estilos=e) if not f['cubierto']]
    b = [f for f in C8.cob_diag_cortos(pg, esc, segs, reg, estilos=e) if not f['cubierto']]
    lab = pg.get_label() or str(i + 1)
    tot7 += len(a); tot8 += len(b)
    for f in a:
        if not any(math.hypot(g['x'] - f['x'], g['y'] - f['y']) <= 0.75 * esc for g in b):
            filtrados.append({"hoja": lab, "pagina": i, "esc": esc, **f})
    for g in b:
        if not any(math.hypot(g['x'] - f['x'], g['y'] - f['y']) <= 0.75 * esc for f in a):
            nuevos.append({"hoja": lab, **g})
    for h, x, y in FALTA:
        if lab == h:
            d7 = min([math.hypot(f['x'] - x, f['y'] - y) / esc for f in a] or [99]); d8 = min([math.hypot(f['x'] - x, f['y'] - y) / esc for f in b] or [99])
            furr[(h, x, y)] = (round(d7, 2), round(d8, 2))
    if a or b: print(lab, len(a), '->', len(b), flush=True)
print('TOTAL no cubiertos', tot7, '->', tot8, '| filtrados', len(filtrados), '| nuevos solo cand', len(nuevos))
for k, v in furr.items(): print('FALTA', k, 'dist ft v137 / cand:', v, 'OK' if v[1] <= 0.75 else 'PERDIDO')
json.dump({"filtrados": filtrados, "nuevos": nuevos}, open('/tmp/verif8/adv8/cobdiag_cr_filtrados.json', 'w'), indent=0)
