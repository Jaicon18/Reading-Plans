#!/usr/bin/env python3
"""Tests de comparar.py con dos canon de JUGUETE fabricados aquí (no se usan resultados de pruebas anteriores) y un
inventario y un PDF sintéticos. Correr: python3 test_comparar.py"""
import copy
import json
import os
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import pymupdf as fitz  # noqa: E402
import comparar as C  # noqa: E402

E = 18.0


def w(id_, tag, ori, eje, lo, hi, sheet="Z1.01", esp=4.0, **kw):
    d = {"id": id_, "tag": tag, "length_ft": round((hi - lo) / E, 4), "sheet": sheet,
         "band": {"ori": ori, "c0": eje - esp / 2, "c1": eje + esp / 2, "lo": lo, "hi": hi}}
    d.update(kw)
    return d


def canon(walls):
    return {"constants": {"plan_scale_pt_per_ft": {"value": E, "source": "sintético"}}, "walls": walls}


def lectura_a():
    return canon([
        w("A1", "X1", "H", 100, 100, 460),               # 20.00 ft  -> igual en B  [ciego-ok]
        w("A2", "X1", "V", 600, 100, 460),               # 20.00 ft  -> B mide 21.00 (5 %)  [ciego-ok]
        w("A3", "X1", "H", 300, 100, 280),               # solo en A
        w("A4", "X2", "H", 500, 100, 280, tag_ids=["PT0004"]),
        {"id": "A5", "tag": "X2", "length_ft": 12.0, "sheet": "Z1.01"},   # sin geometría
    ])


def lectura_b():
    return canon([
        w("B1", "X1", "H", 100, 100, 460.5),             # 20.03 ft: 0.14 % -> coincide  [ciego-ok]
        w("B2", "X1", "V", 600, 100, 478),               # 21.00 ft  [ciego-ok]
        w("B3", "X1", "H", 700, 100, 280),               # solo en B
        w("B4", "X2", "H", 500, 100, 280),
        {"id": "B5", "tag": "X2", "length_ft": 12.5, "sheet": "Z1.01"},   # sin geometría, 4 % -> match por LF
        w("B6", "ZZ", "H", 800, 100, 200),               # type que no existe en el inventario
    ])


def pdf(ruta):
    doc = fitz.open()
    p = doc.new_page(width=1224, height=1000)
    p.insert_text((1100, 960), "Z1.01", fontsize=24)
    for (x0, y0, x1, y1) in ((100, 98, 460, 102), (598, 100, 602, 478), (100, 298, 280, 302), (100, 698, 280, 702)):
        p.draw_rect(fitz.Rect(x0, y0, x1, y1), color=(0, 0, 0), width=1)
    doc.save(ruta)


def inventario(ruta_pdf):
    tag = lambda i, t, x, y: {"id": i, "type": t, "page": 1, "sheet": "Z1.01", "center_pt": [x, y],
                              "bbox_pt": [x - 5, y - 4, x + 5, y + 4], "simbolo": {"radio": 7}}
    return {"pdf": "sintetico.pdf", "pdf_path": ruta_pdf,
            "sheets": [{"page": 1, "sheet": "Z1.01", "title": "FLOOR PLAN"}],
            "partition_types": {"schedule": [{"type": "X1"}, {"type": "X2"}, {"type": "X9"}]},
            "ocurrencias": {"partition_tag": [tag("PT0001", "X1", 280, 88), tag("PT0002", "X1", 612, 280),
                                              tag("PT0003", "X1", 190, 312), tag("PT0004", "X2", 900, 900),
                                              tag("PT0005", "X2", 1000, 300)],
                            "partition_candidato": []}}


def correr(modo="tramo"):
    d = tempfile.mkdtemp()
    ruta = os.path.join(d, "sintetico.pdf")
    pdf(ruta)
    inv = inventario(ruta)
    rev = C.comparar(lectura_a(), lectura_b(), inv, modo)
    fallas = C.imagenes(rev, ruta, os.path.join(d, "img"))
    return rev, fallas, d


REV, FALLAS, DIR = correr()


def test_coinciden_y_difieren():
    co = {(d["A"]["wall"], d["B"]["wall"]) for d in REV["coinciden"]}
    di = {(d["A"]["wall"], d["B"]["wall"]): d for d in REV["difieren"]}
    assert ("A1", "B1") in co and ("A4", "B4") in co, co
    assert ("A2", "B2") in di and abs(di[("A2", "B2")]["delta_lf"] - 1.0) < 0.01, di
    assert ("A5", "B5") in di and di[("A5", "B5")]["via"].startswith("LF only"), di


def test_solo_a_solo_b():
    assert [d["A"]["wall"] for d in REV["solo_A"]] == ["A3"], REV["solo_A"]
    assert sorted(d["B"]["wall"] for d in REV["solo_B"]) == ["B3", "B6"], REV["solo_B"]


def test_tolerancia_2_pct():
    b = lectura_b()
    b["walls"][0] = w("B1", "X1", "H", 100, 100, 100 + 360 * 1.025)   # 2.5 % -> ya no coincide  [ciego-ok]
    rev = C.comparar(lectura_a(), b, inventario(None), "tramo")
    assert any(d["A"]["wall"] == "A1" for d in rev["difieren"]), rev["difieren"]


def test_alertas_inventario():
    k = [(a["kind"], a["type"], a.get("tag", {}).get("id")) for a in REV["alertas"]]
    assert ("tag sin wall", "X2", "PT0005") in k, k            # nadie lo leyó
    assert ("tag sin wall", "X2", "PT0004") not in k, k        # A lo cita por tag_ids
    assert ("tag sin wall", "X1", "PT0003") not in k, k        # A3 pasa por ahí (solo A)
    assert any(a["kind"] == "type no inventariado" and a["type"] == "ZZ" for a in REV["alertas"]), k
    cov = {c["tag"]: c for c in REV["cobertura_tags"]}
    assert cov["PT0004"]["A"]["via"] == "tag_ids" and cov["PT0003"]["B"]["walls"] == []


def test_mismo_modo_para_las_dos():
    r1 = C.comparar(lectura_a(), lectura_b(), inventario(None), "run")
    assert r1["modo"] == "run"
    a = lectura_a()
    a["walls"].append(w("A6", "X1", "V", 460, 100, 200))      # esquina con A1: en "run" se une a A1
    r2 = C.comparar(a, lectura_b(), inventario(None), "run")
    pares = {(d["A"]["wall"], d["B"]["wall"]) for d in r2["difieren"]}
    assert ("A1+A6", "B1") in pares, (pares, [d["A"]["wall"] for d in r2["coinciden"]])


def test_imagenes_verificadas():
    assert not FALLAS, FALLAS
    con_img = [d for d in REV["difieren"] + REV["solo_A"] + REV["solo_B"] + REV["alertas"] if d.get("img")]
    assert con_img and all(d["img_verificada"] for d in con_img), [(d.get("img"), d.get("img_verificada"))
                                                                    for d in con_img]
    for d in con_img:
        assert os.path.exists(os.path.join(DIR, "img", d["img"]))


def test_verificador_rechaza_color_fuera_de_lugar():
    d = [x for x in REV["solo_A"] if x.get("img")][0]
    clip = fitz.Rect(0, 0, 1224, 1000)
    doc = fitz.open(os.path.join(DIR, "sintetico.pdf"))
    ruta = os.path.join(DIR, "limpio.png")
    doc[0].get_pixmap(clip=clip, dpi=72).save(ruta)            # imagen SIN marcas
    assert not C._verificar(ruta, clip, 1.0, [(C.AZUL, fitz.Rect(100, 298, 280, 302))]), d


def test_md_en_ingles():
    m = C.md(REV, "A.json", "B.json", "inv.json")
    for s in ("Matching walls", "Items to review", "only in reading A", "TAG SIN WALL", "Sheet Z1.01"):
        assert s in m, s
    assert "X1" in m.split("## Items")[0]


def test_cli(tmp=None):
    d = tempfile.mkdtemp()
    ruta = os.path.join(d, "s.pdf")
    pdf(ruta)
    for n, c in (("a.json", lectura_a()), ("b.json", lectura_b()), ("i.json", inventario(ruta))):
        json.dump(c, open(os.path.join(d, n), "w"))
    rc = C.main(["comparar.py", os.path.join(d, "a.json"), os.path.join(d, "b.json"), os.path.join(d, "i.json"),
                 os.path.join(d, "out")])
    assert rc == 0
    j = json.load(open(os.path.join(d, "out", "revision.json")))
    assert j["modo"] == C.P.MODO_DEFAULT and os.path.exists(os.path.join(d, "out", "revision.md"))


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
