# adv8_cobdiag_muestra: muestra aleatoria (semilla fija) de 15 pares filtrados por v138 en CR; recorte con pymupdf get_pixmap(clip) y montaje
import json, random, pymupdf, collections
d = json.load(open('/tmp/verif8/adv8/cobdiag_cr_filtrados.json'))
F = d["filtrados"]; print("filtrados por hoja:", dict(collections.Counter(f["hoja"] for f in F)), "| tipos:", dict(collections.Counter(f["tipo"] for f in F)))
print("nuevos solo cand:", d["nuevos"])
random.seed(8); M = random.sample(F, 15)
doc = pymupdf.open('/tmp/claude-0/crmk/CR_mk.pdf')
T = 340; out = pymupdf.open(); 
for parte, grupo in enumerate((M[:8], M[8:])):
    pg_out = out.new_page(width=4 * T, height=2 * (T + 20))
    for k, f in enumerate(grupo):
        pg = doc[f["pagina"]]; e = f["esc"]; r = 3.0 * e
        clip = pymupdf.Rect(f["x"] - r, f["y"] - r, f["x"] + r, f["y"] + r)
        pix = pg.get_pixmap(clip=clip, matrix=pymupdf.Matrix(T / (2 * r), T / (2 * r)), annots=False)
        x0, y0 = (k % 4) * T, (k // 4) * (T + 20)
        pg_out.insert_image(pymupdf.Rect(x0, y0 + 20, x0 + T, y0 + 20 + T), pixmap=pix)
        pg_out.draw_circle((x0 + T / 2, y0 + 20 + T / 2), T * 0.75 / 6, color=(1, 0, 0), width=1.2)   # radio 0.75 ft
        n = parte * 8 + k + 1
        pg_out.insert_text((x0 + 4, y0 + 14), f"#{n} {f['hoja']} ({f['x']},{f['y']}) {f['tipo']} {f['largo_ft']}ft ang{f.get('ang')}", fontsize=9)
        pg_out.draw_rect(pymupdf.Rect(x0, y0 + 20, x0 + T, y0 + 20 + T), color=(0, 0, 1), width=0.5)
    out[parte].get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5)).save(f"/tmp/verif8/adv8/muestra_{parte + 1}.png")
for n, f in enumerate(M, 1): print(n, f["hoja"], f["x"], f["y"], f["tipo"], f["largo_ft"], f.get("ang"), f.get("d"))
json.dump(M, open('/tmp/verif8/adv8/muestra15.json', 'w'))
