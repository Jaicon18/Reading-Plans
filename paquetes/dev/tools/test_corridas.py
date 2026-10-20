#!/usr/bin/env python3
"""Tests de corridas.py v62 (+ arbitraje #12) con las corridas de un proyecto de prueba #11A (arbitraje #11).
Correr: python3 test_corridas.py"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corridas as C  # noqa: E402


def otras_sinteticas():
    """Corridas no-wall SINTÉTICAS declaradas por ELEMENTO (caso de la falla #11A), más el roof step."""
    return {
        "bracing": {"spacing_in": 48, "source": "F/1/S5.20"},
        "section_details": [{"source": "4/A02.02", "runs": 3}],
        "runs": [
            {"id": "CAN-FASCIA", "element": "fascia_box", "orientation": "vertical", "length_ft": 230.0,
             "height_ft": 1.75, "source": "7/A09.26"},
            {"id": "CSR-W", "element": "soffit_side", "orientation": "vertical", "length_ft": 12.0,
             "height_ft": 7.25, "source": "10/A09.33"},
            {"id": "CSR-E", "element": "soffit_side", "orientation": "vertical", "length_ft": 12.0,
             "height_ft": 7.25, "source": "10/A09.33"},
            {"id": "TR104", "element": "ceiling_transition", "edge_of": [], "orientation": "vertical", "length_ft": 75.0,
             "height_ft": 4.5, "source": "7/A09.33"},
            {"id": "RSTEP-1", "element": "roof_step", "orientation": "vertical", "length_ft": 50.0,
             "height_ft": 3.1, "source": "4/A02.02"},
            {"id": "RSTEP-2", "element": "roof_step", "orientation": "vertical", "length_ft": 50.0,
             "height_ft": 1.142, "source": "4/A02.02"},
            {"id": "RSTEP-3", "element": "roof_step", "orientation": "vertical", "length_ft": 50.0,
             "height_ft": 3.44, "source": "4/A02.02"},
            {"id": "VH1", "element": "vestibule_head", "orientation": "vertical", "length_ft": 15.0,
             "height_ft": 5.375, "source": "6/A12.10"},
            {"id": "GRILLE", "element": "grille_head", "orientation": "vertical", "length_ft": 12.0,
             "height_ft": 1.5, "source": "4/A08.21"},
            {"id": "COLWRAP-1", "element": "column_wrap", "sheathing_none_reason": "sintético (v76 R76.2)", "orientation": "vertical", "length_ft": 5.0,
             "height_ft": 10.5, "source": "5/A09.25"},
        ]}


def test_familia_por_elemento_no_por_orientacion():
    t = C.calcular(otras_sinteticas())["totales_lf"]
    # CEIL: fascia 2 x 230 + CSR 2 x 2 x 12 + TR 2 x 75 = 460 + 48 + 150
    assert abs(t["track de ceilings / soffits"] - 658.0) < 0.01, t
    # WALL: roof step 3 x 50 + VH1 15 + grille 12 + column wrap 5, bottom y top CADA UNO
    assert abs(t["bottom track (todos)"] - 182.0) < 0.01, t
    assert abs(t["top / deflection track (todos)"] - 182.0) < 0.01, t


def test_bracing_vano_rfi():
    d = {"bracing": {"spacing_in": 48, "source": "F/1/S5.20"},
         "runs": [{"id": "E", "element": "wall", "orientation": "vertical", "length_ft": 24.0, "height_ft": 14.25,
                   "openings": [{"ro_w_ft": 8.0, "sill_ft": 6.5, "head_ft": 8.5}], "source": "A09.27"}]}
    out = C.calcular(d)
    r = out["renglones"][0]
    # filas a 4, 8 y 12 ft; solo la de 8 ft está dentro del vano 6.5-8.5: 53.4 literal 3 x 24 = 72 y RFI 8
    assert r["bracing_rows"] == 3 and abs(r["bracing_lf"] - 72.0) < 0.01, r
    assert abs(out["rfi_bracing_huecos_lf"] - 8.0) < 0.01 and out["rfi"], out
    d["bracing"]["through_openings"] = False
    assert abs(C.calcular(d)["renglones"][0]["bracing_lf"] - 64.0) < 0.01


def test_purlin_075():
    d = {"bracing": {"spacing_in": 48, "source": "F/1/S5.20"},
         "runs": [{"id": "A1", "element": "wall", "orientation": "vertical", "length_ft": 20.0, "height_ft": 15.25,
                   "purlin": True, "source": "3/A12.01"}]}
    assert abs(C.calcular(d)["totales_lf"]["purlin (track to deck)"] - 15.0) < 0.01


def test_purlin_doble_row_una_pieza():
    """#12A/#12B: G 1-5/8" doble row -> 0.75 x L, UNA pieza (v61 multiplicaba x rows; 59.1)."""
    d = {"bracing": {"spacing_in": 48, "source": "F/1/S5.20"},
         "runs": [{"id": "G1-105/106", "element": "wall", "orientation": "vertical", "length_ft": 11.5,
                   "height_ft": 15.25, "rows": 2, "purlin": True, "source": "5/A12.01"}]}
    o = C.calcular(d)
    assert abs(o["totales_lf"]["purlin (track to deck)"] - 8.625) < 0.01, o["totales_lf"]
    assert abs(o["totales_lf"]["purlin (track to deck)"] - 17.25) > 1     # el dato malo de #12


def test_bottom_track_doors_rfi_y_descuento():
    """#12A RFI-30: door 3.0 en wall 16.5 x 1 row: bottom 16.5 sin descuento + RFI con el delta."""
    run = {"id": "W-t", "element": "wall", "orientation": "vertical", "length_ft": 16.5, "height_ft": 15.25,
           "openings": [{"kind": "door", "ro_w_ft": 3.0, "sill_ft": 0, "head_ft": 7.333}], "source": "3/A12.01"}
    d = {"bracing": {"spacing_in": 48, "source": "F/1/S5.20"}, "runs": [dict(run)]}
    o = C.calcular(d)
    assert abs(o["totales_lf"]["bottom track (todos)"] - 16.5) < 0.01 and o["doors_ro_lf"] == 3.0, o
    assert "-3.0" in o["rfi_doors"]
    d["bottom_track_deduct_doors"] = {"value": True, "source": "4/A12.01"}
    _falla(d, "decisión usuario #10")                   # v64: ni con fuente se descuenta
    d["bottom_track_deduct_doors"] = {"value": False}
    o = C.calcular(d)
    assert abs(o["totales_lf"]["bottom track (todos)"] - 16.5) < 0.01, o["totales_lf"]
    assert abs(o["totales_lf"]["top / deflection track (todos)"] - 16.5) < 0.01


def test_v64_column_wrap_bottom_y_top():
    """Decisión usuario #8 (5/A09.25): 4 faces x 1'-3" = 5.0 -> bottom 5.0 y top 5.0."""
    d = {"bracing": {"spacing_in": 48, "source": "F/1/S5.20"},
         "runs": [{"id": "CW", "element": "column_wrap", "sheathing_none_reason": "sintético (v76 R76.2)", "orientation": "vertical", "length_ft": 4 * 15 / 12,
                   "height_ft": 10.5, "source": "5/A09.25"}]}
    t = C.calcular(d)["totales_lf"]
    assert abs(t["bottom track (todos)"] - 5.0) < 0.01 and abs(t["top / deflection track (todos)"] - 5.0) < 0.01
    d["runs"][0].update(bottom_track=False, track_source="5/A09.25")
    _falla(d, "decisión usuario #8")


def test_v64_transicion_y_canopy_dos_tracks():
    """Decisiones usuario #9 y #13: ceiling_transition y canopy_soffit con track en los dos extremos."""
    for el, src in (("ceiling_transition", "7/A09.33"), ("canopy_soffit", "7/A09.26")):
        d = {"bracing": {"spacing_in": 48, "source": "F/1/S5.20"},
             "runs": [{"id": "X", "element": el, "orientation": "horizontal", "length_ft": 75.0, "track_lines": 1,
                       "track_lines_source": src, "source": src}]}
        _falla(d, "track_lines 2")
        d["runs"][0]["track_lines"] = 2
        if el == "canopy_soffit":                      # v66: línea de wall medida aparte
            d["runs"][0]["wall_line_ft"] = {"value": 75.0, "source": "A04.01"}
        assert abs(C.calcular(d)["totales_lf"]["track de ceilings / soffits"] - 150.0) < 0.01


def _falla(d, txt):
    try:
        C.calcular(d)
    except ValueError as e:
        assert txt in str(e), str(e)
        return
    raise AssertionError("debía fallar: " + txt)


def test_dato_malo_fascia_como_bottom_top():
    """#11A: canopy fascia (studs verticales) con bottom/top track -> la tool lo rechaza (58.2 c)."""
    d = otras_sinteticas()
    d["runs"][0]["bottom_track"] = True
    _falla(d, "track de ceilings / soffits")


def test_dato_malo_drop_declarado_como_wall():
    """#11B: drop/transición de Waiting 904 (7/A09.33) declarado 'wall' para cargarlo a bottom/top."""
    d = otras_sinteticas()
    d["runs"][3]["element"] = "wall"
    t = C.calcular(d)["totales_lf"]
    assert t["bottom track (todos)"] > 182.5          # sin ceiling_details el número cambia de familia
    d["ceiling_details"] = ["7/A09.33", "10/A09.33", "7/A09.26"]
    _falla(d, "es un detalle de ceiling/soffit")


def test_track_lines_distinto_sin_fuente():
    d = otras_sinteticas()
    d["runs"][0]["track_lines"] = 1
    _falla(d, "distinto del default")


def test_roof_step_una_corrida():
    d = otras_sinteticas()
    d["runs"] = [r for r in d["runs"] if r["id"] not in ("RSTEP-2", "RSTEP-3")]
    _falla(d, "4/A02.02")


def test_horizontal_con_bracing():
    d = otras_sinteticas()
    d["runs"].append({"id": "J", "element": "canopy_soffit", "orientation": "horizontal", "length_ft": 55.0, "wall_line_ft": {"value": 50.0, "source": "A04.01"},
                      "bracing_rows": 1, "bracing_rows_source": "F/1/S5.20", "source": "7/A09.26"})
    _falla(d, "framing horizontal")


if __name__ == "__main__":
    n = 0
    for k, f in list(globals().items()):
        if k.startswith("test_") and callable(f):
            f()
            n += 1
            print("OK", k)
    print(f"{n} tests OK")
