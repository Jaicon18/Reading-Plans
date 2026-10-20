#!/usr/bin/env python3
"""test_v76.py — reglas v76 (arbitraje #24). Cada caso falla con el dato malo y pasa con el bueno. Datos SINTÉTICOS
(types X / Y, hoja Z1.01, detalles N/Z9.0x, rooms 9xx, coordenadas inventadas)."""
import copy
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
F, N = [], [0]


def caso(nombre):
    def d(fn):
        N[0] += 1
        try:
            fn()
            print("OK  ", nombre)
        except Exception as e:                       # noqa: BLE001
            print("FALLA", nombre, type(e).__name__, e)
            F.append(nombre)
        return fn
    return d


def falla(fn, *a, texto=""):
    try:
        fn(*a)
    except ValueError as e:
        assert texto in str(e), e
        return
    raise AssertionError("no falló")


def W(id_, tag, ori, c0, c1, lo, hi, **kw):
    w = {"id": id_, "tag": tag, "element": "wall", "length_ft": round((hi - lo) / 18, 4),
         "band": {"ori": ori, "c0": c0, "c1": c1, "lo": lo, "hi": hi, "sheet": "Z1.01"}}
    w.update(kw)
    return w


# ------------------------------------------------------------------------------------------------------ R76.1
def _canopy():
    return {"walls": [{"id": "FX-1", "element": "fascia_box", "facade": "Q"}],
            "ceilings": [{"id": "CJ-1", "room": "CANOPY Q", "system": "canopy_joist", "facade": "Q",
                          "source": "4/Z9.02"}],
            "runs": [{"id": "CS-1", "element": "canopy_soffit", "facade": "Q"}]}


@caso("R76.1 fascia_box sin canopy_joist de su facade = error; con canopy_joist + run canopy_soffit = OK")
def _():
    import chequeos_v76 as C
    d = _canopy()
    assert C.r76_1(d)
    sin = dict(d, ceilings=[])
    falla(C.r76_1, sin, texto="R76.1")
    otra = copy.deepcopy(d)
    otra["ceilings"][0]["facade"] = "P"
    falla(C.r76_1, otra, texto="R76.1")
    none = dict(sin, canopy_soffit_none=[{"facade": "Q", "reason": "no soffit framed", "source": "4/Z9.02 'OPEN'"}])
    assert C.r76_1(none)
    malo = dict(sin, canopy_soffit_none=[{"facade": "Q", "reason": "x", "source": "plan"}])
    falla(C.r76_1, malo, texto="N/HOJA")


@caso("R76.1 canopy_joist sin run canopy_soffit (track) = error")
def _():
    import chequeos_v76 as C
    d = _canopy()
    d["runs"] = []
    falla(C.r76_1, d, texto="canopy_soffit")


@caso("R76.1 hand-off: otros_ceilings con soffit + framing 'para otra tarea' sin consumir = error")
def _():
    import chequeos_v76 as C
    d = _canopy()
    d["otros_ceilings"] = [{"room": "Exterior canopy soffits", "source": "7/Z9.03 '5/8\" SHEATHING ON CFMF'",
                            "note": "read by the exterior task; NOT quantified here"}]
    falla(C.r76_1, d, texto="hand-off")
    d["otros_ceilings"][0]["consumed_by"] = ["CJ-1"]
    assert C.r76_1(d)
    d["otros_ceilings"][0]["consumed_by"] = ["CJ-9"]
    falla(C.r76_1, d, texto="hand-off")
    d["otros_ceilings"][0].pop("consumed_by")
    d["ceilings"][0]["source"] = "7/Z9.03"            # un N/HOJA en común = consumido
    assert C.r76_1(d)
    d2 = _canopy()
    d2["otros_ceilings"] = [{"room": "Office 901", "source": "Z1.01", "note": "ACT"}]   # no es soffit: no aplica
    assert C.r76_1(d2)


# ------------------------------------------------------------------------------------------------------ R76.2
@caso("R76.2 column wrap sin board: sheathing obligatorio; canon genera Σ faces x alto; strip a mano = error")
def _():
    import chequeos_v76 as C
    cw = {"id": "CW-9", "element": "column_wrap", "faces_ft": [1.5, 1.5, 1.5, 1.5], "height_ft": 10.0}
    falla(C.r76_2, {"walls": [cw]}, texto="R76.2")
    ok = dict(cw, sheathing={"material": "frt_5_8_ext", "source": "5/Z9.04 'EXTERIOR GRADE FRT PLYWOOD'"})
    assert C.r76_2({"walls": [ok]})
    (w, mat, sf, op), = C.sheathing_column_wraps({"walls": [ok]})
    assert mat == "frt_5_8_ext" and abs(sf - 60.0) < 1e-6, (sf, op)
    nr = dict(cw, sheathing_none_reason="5/Z9.04 draws stucco on lath, no sheathing")
    assert C.r76_2({"walls": [nr]})
    con_board = dict(cw, faces=[{"board": "5/8 regular", "height_ft": 10.0, "length_ft": 6.0}])
    assert C.r76_2({"walls": [con_board]})
    falla(C.r76_2, {"walls": [ok], "plywood_strips": [{"ref": "column wraps plywood", "lf": 6, "width_ft": 10}]},
          texto="R76.2")


# ------------------------------------------------------------------------------------------------------ R76.3
def _k():
    a = W("XK-1", "XK", "H", 100.0, 110.0, 200.0, 260.0)
    b = W("XK-2", "XK", "H", 113.0, 121.0, 260.0, 330.0)   # step: hueco de 3 pt entre caras (110 -> 113)
    lejos = W("XK-3", "XK", "H", 400.0, 408.0, 330.0, 360.0)
    return a, b, lejos


def _jog(lo, hi, L=None):
    return {"ref": "J-1", "length_ft": L if L is not None else round((hi - lo) / 18, 4), "height_ft": 8,
            "detail": "4/Z9.05", "faces_5_8": 2, "source": "Z1.01",
            "band": {"ori": "V", "c0": 256.0, "c1": 264.0, "lo": lo, "hi": hi, "sheet": "Z1.01"}}


@caso("R76.3 jog ballistic derivado: hueco entre caras; falta / cruza el espesor / largo distinto = error")
def _():
    import chequeos_v76 as C
    a, b, lejos = _k()
    req = C.jogs_k([a, b, lejos])
    assert req == [("XK-1", "XK-2", "V", 260.0, 110.0, 113.0)], req          # el lejano (lado opuesto) no
    falla(C.r76_3, {"walls": [a, b], "ballistic_jogs": []}, texto="falta el jog")
    assert C.r76_3({"walls": [a, b], "ballistic_jogs": [_jog(110.0, 113.0)]})
    falla(C.r76_3, {"walls": [a, b], "ballistic_jogs": [_jog(100.0, 113.0)]}, texto="espesor")   # cara a cara
    falla(C.r76_3, {"walls": [a, b], "ballistic_jogs": [_jog(110.0, 113.0, L=0.9)]}, texto="length_ft")
    assert C.r76_3({"walls": [a, lejos], "ballistic_jogs": []})                # sin step: sin jog


# ------------------------------------------------------------------------------------------------------ R76.4
def _ops():
    return {"walls": [{"id": "X-1", "element": "wall", "location": "exterior", "openings": [
        {"ref": "Q-1", "kind": "window", "ro_w_ft": 4.0, "head_ft": 7.0, "sill_ft": 3.0, "with_sill": True}]}],
        "constants": {}}


@caso("R76.4 abertura exterior sin substrate = error; plywood exige el ancho; strip a mano de head / jamb = error")
def _():
    import chequeos_v76 as C
    import accesorios as A
    d = _ops()
    es = A.es_exterior
    falla(C.r76_4, d, C.aberturas_ext(d, es), texto="R76.4")
    op = d["walls"][0]["openings"][0]
    op["substrate"] = {"label": "3/4\" FRT PLYWOOD", "source": "6/Z9.06", "material": "frt_3_4", "sill": True}
    falla(C.r76_4, d, C.aberturas_ext(d, es), texto="opening_substrate_width_ft")
    d["constants"]["opening_substrate_width_ft"] = {"value": 0.5, "source": "6/Z9.06"}
    assert C.r76_4(d, C.aberturas_ext(d, es))
    d["plywood_strips"] = [{"ref": "Windows head and jambs plywood", "lf": 10, "width_ft": 0.5}]
    falla(C.r76_4, d, C.aberturas_ext(d, es), texto="R76.4")
    d["plywood_strips"] = [{"ref": "Pier-9 plywood at storefront jambs", "lf": 10, "width_ft": 0.5, "uso": "pier"}]
    assert C.r76_4(d, C.aberturas_ext(d, es))                                 # piers: otra decisión


@caso("R76.4 canon genera el strip: ventana con sill = R.O. + 2 x (head - sill) + R.O.")
def _():
    import canon
    d = _ops()
    d["walls"][0]["openings"][0]["substrate"] = {"label": "3/4\" FRT PLYWOOD", "source": "6/Z9.06",
                                                  "material": "frt_3_4", "sill": True}
    d["constants"]["opening_substrate_width_ft"] = {"value": 0.5, "source": "6/Z9.06"}
    fam, filas = {canon.F_PLY: 0.0}, []
    canon.PLY.clear()
    canon.PLY_USO.clear()
    canon._opening_substrate(d, fam, filas)
    assert abs(fam[canon.F_PLY] - (4 + 2 * 4 + 4) * 0.5) < 1e-6, fam


# ------------------------------------------------------------------------------------------------------ R76.5
@caso("R76.5 pier con tag de type y location exterior sigue en su type; sin caras interiores = error")
def _():
    import partition_types as PTY
    import chequeos_v76 as C
    p = {"id": "PX-1", "tag": "X1", "element": "pier", "location": "exterior", "stud_size": '6"', "length_ft": 6.0}
    assert PTY.tipo(p, {}) == "X1"
    assert PTY.tipo(dict(p, tag="EXT"), {}) == "EXT-6CFMF"
    assert PTY.tipo(dict(p, tag="CANOPY-COL", element="column_wrap"), {}) != "X1"
    falla(C.r76_5, {"walls": [p]}, texto="R76.5")
    ok = dict(p, faces=[{"side": "A", "room": "901 Lobby", "board": "5/8 regular", "height_ft": 10, "length_ft": 2.0},
                        {"side": "A", "room": "901 Lobby", "board": "5/8 regular", "height_ft": 10, "length_ft": 1.5}])
    assert C.r76_5({"walls": [ok]})
    assert abs(PTY._lf(ok) - 3.5) < 1e-9


@caso("R76.5 parte sin tag (part_of) interior de un box con tag suma sus caras al LF del box")
def _():
    import partition_types as PTY
    box = {"id": "CX-1", "tag": "X1", "element": "column_wrap", "stud_size": '3-5/8"', "length_ft": 1.0,
           "height_ft": 10, "faces": [{"side": "A", "room": "901", "board": "5/8 regular", "height_ft": 10,
                                       "length_ft": 1.0}],
           "band": {"ori": "BOX", "c0": 100, "c1": 118, "lo": 200, "hi": 218, "sheet": "Z1.01"}}
    parte = {"id": "CX-1-N", "element": "column_wrap", "part_of": "CX-1", "stud_size": '3-5/8"', "length_ft": 1.5,
             "height_ft": 10, "faces": [{"side": "A", "room": "901", "board": "5/8 regular", "height_ft": 10,
                                         "length_ft": 1.5}],
             "band": {"ori": "BOX", "c0": 100, "c1": 118, "lo": 190, "hi": 200, "sheet": "Z1.01"}}
    out = PTY.partition_types({"walls": [box, parte], "constants": {}})
    x = out["types"]["X1"]
    assert x["walls"] == 1 and abs(x["lf"] - 2.5) < 0.01, x


# ------------------------------------------------------------------------------------------------------ R76.6
@caso("R76.6 perímetro de ceiling: menor que 4·√área = error; canon resta las transiciones con edge_of")
def _():
    import chequeos_v76 as C
    c = {"room": "905 Hall", "system": "furring", "area_sf": 100.0, "perimeter_ft": 10.0}
    falla(C.r76_6_perimetro, c, texto="R76.6")             # 10 < 2·√(100π) = 35.4
    assert C.r76_6_perimetro(dict(c, perimeter_ft=40.0))
    d = {"ceilings": [dict(c, perimeter_ft=40.0)],
         "walls": [{"id": "T-1", "element": "ceiling_transition", "length_ft": 10.0}]}
    falla(C.bordes_transicion, d, texto="edge_of")
    d["walls"][0]["edge_of"] = ["905 Hall"]
    assert C.bordes_transicion(d) == {"905 Hall": 10.0}
    d["walls"][0]["edge_of"] = ["906 Otro"]
    falla(C.bordes_transicion, d, texto="no es un ceiling")


# ------------------------------------------------------------------------------------------- R71.8 (verificar)
def _libro(filas_ms, tams_pt, otros=()):
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Partition Takeoff"
    ws.append(["Partition / Scope", "Wall #", "Length (LF)", "Height (FT)", "Layers", "Stud Size"])
    ws.append(["TYPE X1"])
    for t in tams_pt:
        ws.append(["X1 #1", "1", 10, 10, 1, t])
    ws.append(["TYPE OTHER FRAMING (NOT A PARTITION)"])
    for t in otros:
        ws.append(["grille #1", "1", 5, 2, 1, t])
    ms = wb.create_sheet("Material Summary")
    ms.append(["MATERIAL SUMMARY"])
    ms.append([""])
    ms.append(["Material", "Unit", "Net"])
    for n, u, v in filas_ms:
        ms.append([n, u, v])
    return wb


@caso("R71.8 verificar (v76): renglones de parapet / heads / other framing suman; tamaño solo en OTHER FRAMING no exige renglón")
def _():
    import plantilla_excel as PXL
    ms = [('Bottom track 6"', "LF", 10), ('Bottom track 3-5/8"', "LF", 5), ("Parapet bottom track", "LF", 7),
          ("Bottom track - other framing (not a partition type, see source)", "LF", 2),
          ('Top / deflection track 6"', "LF", 10), ('Top / deflection track 3-5/8"', "LF", 5),
          ("Parapet top track", "LF", 7), ("Top / deflection track - other framing (not a partition type, see source)",
                                          "LF", 2),
          ("Power-driven fasteners, slab pins for the bottom track", "PCS", 99)]
    tot = {"bottom track": 24.0, "top / deflection track": 24.0}
    wb = _libro(ms, ['6"', '3-5/8"'], otros=['2-1/2"'])
    assert PXL.verificar_r71_track(wb, tot) == [], PXL.verificar_r71_track(wb, tot)
    wb2 = _libro(ms, ['6"', '3-5/8"', '1-5/8"'])
    e = PXL.verificar_r71_track(wb2, tot)
    assert any("1-5/8" in x for x in e), e
    wb3 = _libro(ms, ['6"', '3-5/8"'])
    e = PXL.verificar_r71_track(wb3, {"bottom track": 30.0, "top / deflection track": 24.0})
    assert any("R71.8b" in x for x in e), e


# ------------------------------------------------------------------------------------------------- blocking wood
@caso("blocking 2X sin rótulo FRT: material FRT = error (o frt_basis); material wood = familia de madera, renglón propio")
def _():
    import canon
    it = {"ref": "BX-1", "lf": 6.0, "label": "2X BLOCKING BETWEEN STUDS", "source": "3/Z9.07"}
    fam = {"FRT blocking": 0.0, "metal stud blocking (362CR / STUD BLOCKING)": 0.0}
    falla(canon._parapets_blocking, {"blocking_items": [dict(it, material="FRT")]}, dict(fam), [], [], texto="wood")
    ok = dict(it, material="FRT", frt_basis={"source": "1/Z0.01 'ALL WOOD BLOCKING SHALL BE FRT'"})
    f2 = dict(fam)
    canon._parapets_blocking({"blocking_items": [ok]}, f2, [], [])
    assert f2["FRT blocking"] == 6.0
    canon.BLK_MADERA.clear()
    f3 = dict(fam)
    canon._parapets_blocking({"blocking_items": [dict(it, material="wood")]}, f3, [], [])
    assert f3["FRT blocking"] == 6.0 and canon.BLK_MADERA["wood"] == 6.0
    falla(canon._parapets_blocking, {"blocking_items": [dict(it, material="wood", label="FRT 2X BLOCKING")]},
          dict(fam), [], [], texto="wood")


@caso("A_BLOCKING (reglas): el source no hace FRT un rótulo que no lo dice")
def _():
    import reglas

    class Ctx:
        canon = {"blocking_items": [{"ref": "BX-1", "material": "FRT", "label": "2X BLOCKING",
                                     "source": "3/Z9.07 NOT labeled FRT"}]}
    assert reglas.a_blocking(Ctx()), "debió fallar"
    Ctx.canon["blocking_items"][0]["frt_basis"] = {"source": "1/Z0.01 'ALL WOOD SHALL BE FRT'"}
    assert not reglas.a_blocking(Ctx())


@caso("fos_chain_faces: caja parcial con una cadena por face (o vector) pasa canon y A_WRAP_FOS")
def _():
    import canon
    import reglas
    w = {"id": "CX-2", "element": "column_wrap", "tag": "X1", "stud_size": '3-5/8"', "oc_in": 16, "height_ft": 10,
         "source": "3/Z9.08",
         "length_ft": 2.5, "faces_ft": [1.0, 1.5],
         "fos_chain_faces": [{"value": [0.5, 0.5], "source": "3/Z9.08 FOS"},
                             {"measured_op": "27 pt / 18", "source": "Z1.01 vector"}]}
    fam = {k: 0.0 for k in canon.FAMS}
    canon._column_wraps({"walls": [w]}, fam, [])
    malo = dict(w, fos_chain_faces=[{"value": [0.5], "source": "3/Z9.08"}, {"measured_op": "x", "source": "v"}])
    falla(canon._column_wraps, {"walls": [malo]}, {k: 0.0 for k in canon.FAMS}, [], texto="fos_chain_faces")

    class Ctx:
        canon = None

        @staticmethod
        def walls(els):
            return [w]
    assert not reglas.a_wrap_fos(Ctx())


@caso("bitácora: test_ciego.py o test_ciego_tools.py cumple el paso E24; armar_ciego lleva test_ciego.py")
def _():
    import bitacora
    import armar_ciego
    e = [t for t, s, v, d in bitacora.OBLIGATORIAS if "test_ciego" in t]
    assert e and set(e[0].split("|")) == {"test_ciego.py", "test_ciego_tools.py"}, e
    assert "test_ciego.py" in armar_ciego.QUEDAN


@caso("nombre del nailbase con el espesor impreso del polyiso; sin la constante = error si hay nailbase")
def _():
    import canon
    d = {"plywood_strips": [{"ref": "roof step face", "material": "nailbase_5_8_polyiso", "lf": 1, "width_ft": 1}],
         "constants": {}}
    canon.POLY[0] = canon._polyiso(d)
    falla(canon._ply, {canon.F_PLY: 0.0}, "nailbase_5_8_polyiso", 1.0, "nailbase", texto="nailbase_polyiso_in")
    d["constants"]["nailbase_polyiso_in"] = {"value": "3 1/4\"", "source": "D/Z9.09 'BONDED TO 3 1/4\" POLYISO'"}
    assert canon._polyiso(d) == '3-1/4"'
    assert canon._polyiso({"constants": {}}) == ""


print(f"test_v76: {N[0] - len(F)}/{N[0]} OK")
sys.exit(1 if F else 0)
