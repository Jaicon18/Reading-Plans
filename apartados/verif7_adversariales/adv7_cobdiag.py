# adv7_cobdiag: CE_COBERTURA_DIAG (cob_diag_cortos, filtros v138 _cob_en_hatch / _cob_divisor_tag) con furrings REALES. Sintético (PDF en memoria).
import sys; sys.path.insert(0, sys.argv[1]); import compuerta_entrega as CE, pymupdf
esc = 18.0
doc = pymupdf.open(); pg = doc.new_page(width=1600, height=1000)
def par(x0, y0, x1, y1, dx, dy):
    sh = pg.new_shape(); sh.draw_line((x0, y0), (x1, y1)); sh.draw_line((x0 + dx, y0 + dy), (x1 + dx, y1 + dy))
    sh.finish(color=(0, 0, 0), width=0.7); sh.commit()
def cross(x0, n=6):   # cross-hatch de CMU (45 / 135) de 10 pt, como el test del autor
    sh = pg.new_shape()
    for k in range(n):
        sh.draw_line((x0 + k * 4, 412), (x0 + 10 + k * 4, 422)); sh.draw_line((x0 + 10 + k * 4, 412), (x0 + k * 4, 422))
    sh.finish(color=(0.1, 0.1, 0.1), width=0.24); sh.commit()
def tile_diag(x0, n=5):   # piso de loseta a 45 grados (baño): líneas cortas en las dos diagonales, del lado del cuarto
    sh = pg.new_shape()
    for k in range(n):
        sh.draw_line((x0 - 10 - k * 4, 414), (x0 - k * 4, 424)); sh.draw_line((x0 - k * 4, 414), (x0 - 10 - k * 4, 424))
    sh.finish(color=(0.5, 0.5, 0.5), width=0.18); sh.commit()
par(100, 400, 1580, 400, 0, 9)                        # muro largo H
par(300, 409, 300, 409 + 1.5 * esc, 9, 0)             # K0 stub real (control)
par(500, 409, 500, 409 + 1.5 * esc, 9, 0); cross(512)  # K1 control: furring contra CMU (hatch de UN lado) -> sale
par(700, 409, 700, 409 + 1.5 * esc, 9, 0); cross(712); tile_diag(699)   # K2 furring contra CMU + loseta a 45 del lado del cuarto
par(900, 409, 900, 409 + 1.5 * esc, 9, 0); pg.insert_text((912, 426), "F1", fontsize=7)   # K3 furring con su tag 'F1' al lado
par(1100, 409, 1100, 409 + 1.5 * esc, 9, 0); pg.insert_text((1112, 426), "3'-0\"", fontsize=6)  # K4 cota corta al lado del muro
f = CE.cob_diag_cortos(pg, esc, [])
xs = sorted(round(x["x"]) for x in f if x["tipo"] == "muro_corto")
print("salen (x):", xs)
for k, x in (("K0 stub real (control)", 304), ("K1 furring contra CMU, hatch de un lado (control del autor)", 504),
             ("K2 furring contra CMU + piso de loseta a 45 grados del lado del cuarto", 704), ("K3 furring con su tag 'F1' pegado", 904),
             ("K4 furring con su cota '3'-0\"' pegada", 1104)):
    print(k, "-> sale (no cubierto)?", any(abs(v - x) <= 6 for v in xs))
