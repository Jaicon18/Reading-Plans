#!/usr/bin/env python3
"""Tests de inventario_tags.py (Etapa 1) con un PDF SINTÉTICO armado aquí mismo (ningún dato de un proyecto real).
Correr: python3 test_inventario_tags.py"""
import json
import os
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import pymupdf as fitz  # noqa: E402
import inventario_tags as I  # noqa: E402

PROYECTO = "DEMO PROJECT 0000"


class Hoja:
    """Página sintética; todo se escribe en coordenadas DISPLAY aunque la página esté rotada."""

    def __init__(self, doc, numero, titulo, rot=0):
        if rot in (90, 270):
            self.p = doc.new_page(width=792, height=1224)
            self.p.set_rotation(rot)
        else:
            self.p = doc.new_page(width=1224, height=792)
        self.rot = rot
        self.texto(1090, 600, PROYECTO, 10)
        self.texto(1090, 615, "123 MAIN ST", 10)
        if titulo:
            self.texto(1090, 700, titulo, 14)
        if numero:
            self.texto(1100, 760, numero, 24)

    def texto(self, x, y, t, size):
        self.p.insert_text(fitz.Point(x, y) * self.p.derotation_matrix, t, fontsize=size, rotate=self.rot)

    def rect(self, r):
        self.p.draw_rect(fitz.Rect(r) * self.p.derotation_matrix, color=(0, 0, 0), width=0.6)

    def circulo(self, c, r):
        self.p.draw_circle(fitz.Point(c) * self.p.derotation_matrix, r, color=(0, 0, 0), width=0.6)

    def linea(self, a, b):
        self.p.draw_line(fitz.Point(a) * self.p.derotation_matrix, fitz.Point(b) * self.p.derotation_matrix,
                         color=(0, 0, 0), width=1.5)

    def tag(self, x, y, t, size=8):
        """Tag de partition type en caja (texto con baseline en y)."""
        w = fitz.get_text_length(t, fontsize=size)
        self.texto(x, y, t, size)
        self.rect((x - 3, y - size - 1, x + w + 3, y + 3))
        return (x + w / 2, y - size / 2 + 1)


def pdf_sintetico(ruta):
    doc = fitz.open()
    h = Hoja(doc, "Z0.01", "COVER SHEET")
    h.texto(100, 100, "SHEET INDEX", 12)
    h = Hoja(doc, "Z5.01", "PARTITION TYPES")
    h.texto(100, 100, "PARTITION TYPE X1 & X2", 12)
    h.texto(100, 300, "PARTITION Q", 12)
    h.texto(100, 400, "WALL BASE", 12)              # no es un type
    h.texto(100, 450, "PARTITION MAY OCCUR,", 12)   # no es un type
    for k, t in enumerate(("X1", "X2", "Q", "R5")):  # columna del schedule (R5 no aparece en planta)
        h.texto(600, 100 + 18 * k, t, 9)
        h.texto(700, 100 + 18 * k, "YES", 9)
    # planta rotada 90 (como los sets reales)
    h = Hoja(doc, "Z1.01", "FLOOR PLAN", rot=90)
    for y in (200, 400, 600):
        h.linea((100, y), (900, y))
    esperados = {"X1": [], "X2": [], "Q": []}
    for x, y in ((150, 190), (450, 390), (750, 590)):
        esperados["X1"].append(h.tag(x, y, "X1"))
    esperados["X2"].append(h.tag(300, 590, "X2"))
    for x, y in ((600, 190), (220, 390)):
        esperados["Q"].append(h.tag(x, y, "Q"))
    h.tag(820, 390, "Y7")                            # en símbolo pero no está en el schedule
    h.circulo((60, 60), 16)                          # grid bubble: letra grande en círculo grande
    h.texto(54, 66, "Q", 16)
    h.circulo((500, 700), 14)                        # section bubble Q / Z9.99 (hoja inexistente)
    h.texto(497, 697, "Q", 8)
    h.texto(489, 708, "Z9.99", 7)
    h.texto(300, 750, "SEE TYPE X1 NOTE", 8)         # texto suelto
    h.texto(150, 120, "12' - 6\"", 8)
    # planta sin rotar: ampliación con un X2
    h = Hoja(doc, "Z1.02", "ENLARGED PLAN")
    h.linea((100, 300), (600, 300))
    esperados["X2"].append(h.tag(350, 290, "X2"))
    # página raster
    p = doc.new_page(width=1224, height=792)
    pix = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 40, 40), 0)
    pix.set_rect(pix.irect, (200, 200, 200))
    p.insert_image(fitz.Rect(100, 100, 500, 500), pixmap=pix)
    doc.save(ruta)
    return esperados


def correr():
    d = tempfile.mkdtemp()
    ruta = os.path.join(d, "sintetico.pdf")
    esperados = pdf_sintetico(ruta)
    inv = I.inventario(ruta, os.path.join(d, "out"))
    return inv, esperados, d


INV, ESP, DIR = correr()


def test_indice_de_hojas():
    hs = INV["sheets"]
    assert [h["sheet"] for h in hs[:4]] == ["Z0.01", "Z5.01", "Z1.01", "Z1.02"], [h["sheet"] for h in hs]
    assert hs[2]["title"] == "FLOOR PLAN", hs[2]
    assert PROYECTO not in (hs[1]["title"] or ""), "el nombre del proyecto (repetido) no es el título"
    assert hs[1]["es_schedule_partition"] and hs[2]["titulo_planta"]


def test_raster_no_inventariable():
    ni = INV["no_inventariables"]
    assert len(ni) == 1 and ni[0]["page"] == 5 and "NO INVENTARIABLE POR SCRIPT" in ni[0]["motivo"], ni


def test_types_del_schedule():
    ts = [t["type"] for t in INV["partition_types"]["schedule"]]
    assert set(ts) == {"X1", "X2", "Q", "R5"}, ts
    for malo in ("BASE", "MAY", "OCCUR", "YES"):
        assert malo not in ts


def test_conteo_por_type_y_hoja():
    c = INV["partition_types"]["conteo"]
    assert c["X1"]["total_planta"] == 3 and c["X1"]["por_hoja"] == {"Z1.01 (p.3)": 3}, c["X1"]
    assert c["X2"]["total_planta"] == 2 and c["X2"]["por_hoja"] == {"Z1.01 (p.3)": 1, "Z1.02 (p.4)": 1}, c["X2"]
    assert c["Q"]["total_planta"] == 2, c["Q"]          # sin el grid bubble ni el section bubble
    assert c["R5"]["total_planta"] == 0


def test_posiciones_display():
    for t, pts in ESP.items():
        got = sorted((o["page"], round(o["center_pt"][0]), round(o["center_pt"][1]))
                     for o in INV["ocurrencias"]["partition_tag"] if o["type"] == t)
        for (x, y) in pts:
            assert any(abs(gx - x) <= 2 and abs(gy - y) <= 2 for _, gx, gy in got), (t, x, y, got)


def test_grid_y_texto_suelto_son_ambiguos():
    amb = INV["ocurrencias"]["partition_ambiguo"]
    mot = {(o["type"], o["motivo"].split(" ")[0]) for o in amb}
    assert ("Q", "tamaño") in mot, mot                 # grid bubble
    assert ("X1", "sin") in mot, mot                   # "SEE TYPE X1 NOTE"


def test_section_bubble_y_hoja_inexistente():
    refs = [o["ref"] for o in INV["ocurrencias"]["detail_bubble"]]
    assert "Q/Z9.99" in refs, refs
    assert any("Q/Z9.99" in a for a in INV["avisos"]), INV["avisos"]


def test_candidato_fuera_de_schedule():
    assert "Y7" in {o["text"] for o in INV["ocurrencias"]["partition_candidato"]}


def test_cota():
    assert any(o["text"].startswith("12' - 6") for o in INV["ocurrencias"]["cota"]), INV["ocurrencias"]["cota"]


def test_recortes_verificados():
    occ = INV["ocurrencias"]["partition_tag"]
    assert occ and all(o.get("png_verificado") for o in occ), [(o["id"], o.get("png_verificado")) for o in occ]
    for o in occ:
        assert os.path.exists(os.path.join(DIR, "out", "recortes", o["png"]))
    assert not [a for a in INV["avisos"] if a.startswith("PNG NO VERIFICADO")], INV["avisos"]


def test_verificador_rechaza_marca_corrida():
    """Una marca dibujada lejos del tag tiene que fallar la verificación (el círculo no cae sobre el tag)."""
    o = dict(INV["ocurrencias"]["partition_tag"][0])
    doc = fitz.open(os.path.join(DIR, "sintetico.pdf"))
    page = doc[o["page"] - 1]
    cx, cy = o["center_pt"]
    mal = (cx + 45, cy + 45)                          # marca corrida 45 pt
    tmp = fitz.open()
    tmp.insert_pdf(doc, from_page=o["page"] - 1, to_page=o["page"] - 1)
    tp = tmp[0]
    a = tp.add_circle_annot(fitz.Rect(mal[0] - 10, mal[1] - 10, mal[0] + 10, mal[1] + 10) * tp.derotation_matrix)
    a.set_colors(stroke=(1, 0, 0))
    a.set_border(width=2)
    a.update()
    clip = fitz.Rect(cx - 70, cy - 70, cx + 70, cy + 70) & tp.rect
    ruta = os.path.join(DIR, "mal.png")
    tp.get_pixmap(clip=clip, dpi=150).save(ruta)
    ok, det = I.verificar_png(ruta, clip, (cx, cy), 10, 150 / 72, page, o)
    assert not ok and "anillo" in det, det


def test_json_y_md():
    j = json.load(open(os.path.join(DIR, "out", "inventario.json")))
    assert j["partition_types"]["conteo"]["X1"]["total_planta"] == 3
    m = open(os.path.join(DIR, "out", "inventario.md")).read()
    assert "| X1 |" in m and "NO INVENTARIABLE" in m and "Y7" in m


if __name__ == "__main__":
    fallas = 0
    for k, f in sorted(globals().items()):
        if k.startswith("test_") and callable(f):
            try:
                f()
                print("OK  ", k)
            except AssertionError as e:
                fallas += 1
                print("FALLA", k, e)
    print(f"{'TODOS OK' if not fallas else str(fallas) + ' FALLA(S)'}")
    sys.exit(1 if fallas else 0)
