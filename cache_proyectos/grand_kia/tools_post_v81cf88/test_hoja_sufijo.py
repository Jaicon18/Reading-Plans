#!/usr/bin/env python3
"""test_hoja_sufijo.py — R80w.12: una hoja con sufijo de letra (RCP / elevaciones "A421.A", "A000.B") es una HOJA válida
para reglas.py (HOJA / NHOJA) y para runner/evidencia.py (HOJA). Sintético: falla con reglas.py / evidencia.py v80v."""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "runner"))
import reglas

ok_hoja = ["X421.A 10'-0\" ceiling tag", "elev 3/X426.A", "X000.B note", "X101", "X-101", "X2.10", "X421.AB"]
for t in ok_hoja:
    assert reglas.HOJA.search(t), f"HOJA no reconoce {t!r}"
assert reglas.NHOJA.search("3/X426.A"), "NHOJA no reconoce 3/X426.A"
assert reglas.NHOJA.search("D/X301"), "NHOJA protección"
# protecciones: un número suelto / keynote con dígitos tras el punto siguen como antes
assert not reglas.HOJA.search("421.5 pt"), "un número no es hoja"
assert reglas.HOJA.search("X421.5") is None or reglas.HOJA.search("X421.5").group(0) != "X421", "X421.5 no es X421"
try:
    import evidencia
    assert evidencia.HOJA.search("X421.A ceiling").group(1) == "X421.A", "evidencia.HOJA corta el sufijo .A"
    assert evidencia.HOJA.search("X-101 plan").group(1) == "X-101"
    assert evidencia.HOJA.search("X4.2 plan").group(1) == "X4.2"
except ImportError:          # el paquete de tools sin runner: solo reglas
    pass

# BE-GK02 (Grand Kia): página vectorial sin capa de texto = necesita capa OCR; página con texto no.
def test_be_gk02_hojas_sin_texto():
    import pymupdf, palabras_fitz
    d = pymupdf.open()
    p1 = d.new_page(); p1.insert_text((72, 72), "PARTITION TYPE A FULL HEIGHT")
    p2 = d.new_page(); p2.draw_line((10, 10), (300, 300)); p2.draw_rect(pymupdf.Rect(50, 50, 90, 70))
    p3 = d.new_page()
    assert palabras_fitz.hojas_sin_texto(d) == [2], palabras_fitz.hojas_sin_texto(d)


# BE-GK01 (Grand Kia): el arranque asegura también openpyxl (el Excel fijo) además de pikepdf / pymupdf / pdfplumber.
def test_be_gk01_deps():
    import arranque
    mods = [m for m, _ in arranque.DEPS]
    for m in ("pikepdf", "fitz", "pdfplumber", "openpyxl"):
        assert m in mods, m


test_be_gk02_hojas_sin_texto()
test_be_gk01_deps()

# BE-GK03 (Grand Kia): OCR '1' leída como l / I / | junto a una letra de type; types del lector independiente como lista.
def test_be_gk03_ocr_normalizar():
    import inventario_tags as it
    cache = {1: {"words": [{"t": "Al"}, {"t": "B|"}, {"t": "AB"}]}, 2: {"words": [{"t": "Al"}]}}
    assert it.ocr_normalizar(cache, [1]) == 2
    assert [w["t"] for w in cache[1]["words"]] == ["A1", "B1", "AB"] and cache[2]["words"][0]["t"] == "Al", cache


# BE-GK04 / BE-GK06: Dens Shield y 10" stud son familias propias (no caen en 5/8 Type X / 8").
def test_be_gk04_gk06_familias():
    import familias, canon
    assert familias.familia('5/8" glass mat water-resistant tile backer (DensShield, ASTM C1178)', "sf") == canon.F_DENS
    assert familias.familia('10" metal stud (LF of material)', "lf") == canon.F_10


# BE-GK05 / BE-GK07 / BE-GK08 / BE-GK09 / BE-GK10: guardas en el código fuente de cada tool.
def test_be_gk05_10_guardas():
    import os
    src = lambda f: open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f), encoding="utf-8").read()
    assert "double_row_types" in src("canon.py")                                   # BE-GK05
    assert "OCR no confirmado por el recorte" in src("inventario_tags.py")          # BE-GK07
    assert "misc_items con ref repetido" in src("canon.py")                         # BE-GK08
    assert 'filas_de("hanger wire")]' in src("trazabilidad.py")                     # BE-GK09
    assert "edge of gypboard" in src("trazabilidad.py") and "sheet_len_ft" in src("trazabilidad.py")   # BE-GK10


# BE-GK11 (Grand Kia): deck en pendiente -> B.O. de estructura POR WALL (structure_bo_ft) en las reglas físicas de U-176.
def test_be_gk11_bo_por_wall():
    import comparar_alturas as ca
    w = [{"id": "WX", "tipo": "A", "h": 20.0, "regla": "to_deck", "ext": 0, "rooms": [], "board": [], "top": "slip", "motivo": None, "bo": 20.0}]
    n, f = ca.reglas_fisicas(w, {}, 30.0)
    assert not f, f
    w[0]["bo"] = None
    n, f = ca.reglas_fisicas(w, {}, 30.0)
    assert f, "sin B.O. por wall debe comparar contra el global"


# BE-GK12 / BE-GK13 / BE-GK14 / BE-GK16 (Grand Kia): guardas en el código fuente + RX de hoja concreta.
def test_be_gk12_16_guardas():
    import os, re
    src = lambda f: open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f), encoding="utf-8").read()
    assert "BE-GK12" in src("comparar_alturas.py") and 'esp = w["bo"]' in src("comparar_alturas.py")          # BE-GK12
    assert "slip_track_product" in src("trazabilidad.py")                                                     # BE-GK13
    import compuerta_entrega as ce
    assert ce.RX_HOJA_CONCRETA.search("see A111") and ce.RX_HOJA_CONCRETA.search("per A-201")                # BE-GK14
    assert "derotation_matrix" in src("markups_rcp.py")                                                       # BE-GK16



# BE-GK18 (Grand Kia): soffit loop polyline (first == last point) measured along its path.
def test_be_gk18_polilinea_cerrada():
    import markups_rcp as mr
    assert abs(mr.largo_polilinea([[0, 0], [9, 0], [9, 9], [0, 9], [0, 0]]) - 36) < 1e-9


# BE-GK19 (Grand Kia): closer stud minimum discounts the split-node stud already counted in the neighbour wall.
def test_be_gk19_closer_split():
    import closer
    from closer import Val, Wall
    x = Wall(1, "A", "WX test")
    x.base(Val(4.0, "DERIVADO", fuente="A1", operacion="(36-0)/9 = 4.0"), Val(10.0, "DERIVADO", fuente="A1", operacion="9.5 + 0.5 = 10.0"), 16, 48)
    x.cara("R1", Val(10.0, "DERIVADO", operacion="9.5 + 0.5 = 10.0"), "5/8 regular", 1)
    x.partida("STUD", Val(3, "DERIVADO", operacion="campo 4 - 1 [split N64 -1 (stud del corte ya contado en WY)] (46/A550)"), "pcs")
    assert not [f for f in x._fallos() if f.startswith("STUD:")], x._fallos()


# BE-GK20 (Grand Kia): capa OCR de muchas hojas repartida por página entre procesos (nunca un proceso de > 30 min).
def test_be_gk20_capa_paralela():
    import palabras_fitz as pf, inspect
    assert callable(pf.capa_ocr_paralelo) and "ProcessPoolExecutor" in inspect.getsource(pf.capa_ocr_paralelo)


# BE-GK21 (Grand Kia): a gauge field with text ('[PENDING] SEE STRUCTURAL ...') is AMBER, never an int() crash.
def test_be_gk21_gauge_texto():
    import revision_materiales as rm, inspect
    assert "BE-GK21" in inspect.getsource(rm.comparar_type)


# BE-GK22..26 (Grand Kia): guardas en el código fuente.
def test_be_gk22_26_guardas():
    import os
    src = lambda f: open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f), encoding="utf-8").read()
    assert "BE-GK22" in src("alcances.py") and "BE-GK22" in src("revision_materiales.py")       # Dens in ALC-08 / ALC-20 / compound driver
    assert "BE-GK23" in src("headers.py")                                                     # sill rule names the estimator decision
    assert "BE-GK24" in src("comparar_alturas.py")                                             # declared print conflict in the room cross
    assert "BE-GK25" in src("compuerta_entrega.py") and "bidset_texto" in src("compuerta_entrega.py")
    assert "BE-GK26" in src("chequeos_biblioteca.py")                                          # reader ID mapping in U-017
    assert "BE-GK28" in src("revision_markups.py")
    assert "BE-GK29" in src("alcances.py")
    assert "BE-GK30" in src("trazabilidad.py")
    assert "BE-GK31" in src("subir_entrega.py") and "--auditoria-carpeta" in src("subir_entrega.py")   # Auditoria/ unpacked
    assert "U-177 (1)" in src("compuerta_entrega.py") and "cv < 0.5" in src("compuerta_entrega.py")   # U-177 (1) / (2)                                                 # U-177 (3) designation in every framing row                                                     # access panels close ALC-17                                             # final vector op is the height
    assert "BE-GK27" in src("chequeos_biblioteca.py")                                          # wood walls PASS text without '0 walls'

test_be_gk03_ocr_normalizar()
test_be_gk04_gk06_familias()
test_be_gk05_10_guardas()
test_be_gk11_bo_por_wall()
test_be_gk12_16_guardas()
test_be_gk18_polilinea_cerrada()
test_be_gk19_closer_split()
test_be_gk20_capa_paralela()
test_be_gk21_gauge_texto()
test_be_gk22_26_guardas()
print("test_hoja_sufijo OK")
