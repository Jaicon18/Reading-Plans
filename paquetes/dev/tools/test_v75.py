#!/usr/bin/env python3
"""test_v75.py — reglas v75 (arbitraje #23). Cada caso falla con el dato malo y pasa con el bueno. Datos SINTÉTICOS
(types X / Y / Z / W, hoja Z1.01, rooms 9xx, coordenadas inventadas)."""
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


@caso("R75.1 renglones de track: ninguno cae en el track de ceilings; el nombre viejo con 'soffit' sí caía")
def _():
    import canon
    import familias
    assert familias.familia("Bottom track - roof step and heads (vestibule / soffit)", "lf") == "bottom track (todos)"
    assert familias.familia("Track, ceilings / soffits / canopy", "lf") == "track de ceilings / soffits"
    for k, (nb, nt) in canon.TRACK_NOMBRES.items():
        n = (nb.format(sz='9"'), nt.format(sz='9"'))
        assert familias.familia(n[0], "lf") == "bottom track (todos)", n
        assert familias.familia(n[1], "lf") == "top / deflection track (todos)", n
    falla(canon.verificar_track_nombres, {"bottom": {"Track at soffit side": 1.0}, "top": {}},
          texto="R75.1")


@caso("R75.2 track: elemento sin fila en la Partition Takeoff va a 'other framing'; wall y elemento de un type, por tamaño")
def _():
    import canon
    data = {"walls": [{"id": "Y-1", "stud_size": '6"'}, {"id": "Y-2", "stud_size": '6"'},
                      {"id": "Z-9", "stud_size": '6"'}, {"id": "Z-8", "stud_size": '3-5/8"'}]}
    co = {"renglones": [{"id": "r:Y-1", "element": "wall", "bottom_lf": 10, "top_lf": 10},
                        {"id": "r:Y-2", "element": "wall", "bottom_lf": 2, "top_lf": 2},          # alcove (wall sin fila)
                        {"id": "r:Z-9", "element": "storefront_cripples", "bottom_lf": 4, "top_lf": 4},
                        {"id": "r:Z-8", "element": "column_wrap", "sheathing_none_reason": "sintético (v76 R76.2)", "bottom_lf": 3, "top_lf": 3}]}
    fam = {"bottom track (todos)": 19, "top / deflection track (todos)": 19}
    pt = {"types": {"Y": {"filas": [{"ids": ["Y-1"], "wall": "Y-1"}]}, "W": {"filas": [{"ids": ["Z-8"]}]}}}
    out = canon.track_by_element(data, co, fam, pt)
    b = out["bottom"]
    assert b['Bottom track 6"'] == 12, b                     # wall con tag + wall sin fila (alcove / stub)
    assert b['Bottom track 3-5/8"'] == 3, b                  # column wrap que es fila de un type
    assert b[canon.TRACK_NOMBRES["elemento"][0]] == 4, b     # cripples: no es fila de la Partition Takeoff
    assert abs(sum(b.values()) - 19) < 0.01
    sin_pt = canon.track_by_element(data, co, fam)            # compatibilidad: sin pt, por tamaño (v73)
    assert sin_pt["bottom"]['Bottom track 6"'] == 16, sin_pt


def _op(**kw):
    o = {"ref": "Q-1", "kind": "window", "ro_w_ft": 5.0, "head_ft": 7.0, "sill_ft": 3.0, "with_sill": True,
         "jamb_return": True, "substrate_none_reason": "sintético (v76 R76.4)", "jamb_return_source": "3/Z9.01", "jamb_return_label": "GYPSUM BOARD JAMB RETURN"}
    o.update(kw)
    return o


@caso("R75.3 jamb return: sill sin declarar = error; sill false = sin borde; label sin gypsum = error")
def _():
    import accesorios as A
    falla(A._sill_return, _op(), texto="R75.3")
    assert A._edge(_op(sill_return=False, sill_return_source="4/Z9.01")) == 5 + 2 * 7 - 2 * 3
    assert A._edge(_op(sill_return=True, sill_return_source="4/Z9.01", sill_return_label="GYP. BD. RETURN")) == \
        5 + 2 * 7 - 2 * 3 + 5
    falla(A._sill_return, _op(sill_return=True, sill_return_source="4/Z9.01", sill_return_label="BRAKE METAL SILL"),
          texto="R75.3")
    falla(A._label_gyp, _op(jamb_return_label="LINE OF JAMB RETURN BEYOND"), "jamb_return_source",
          "jamb_return_label", "jamb", texto="no rotula gypsum")
    falla(A._label_gyp, _op(jamb_return_label=""), "jamb_return_source", "jamb_return_label", "jamb", texto="R75.3")
    A._label_gyp(_op(), "jamb_return_source", "jamb_return_label", "jamb")
    assert A._sill_return(_op(jamb_return=False)) is True    # sin return: no se exige el sill


@caso("R75.4 storefront_cripples sin su storefront declarado = error; con el mismo ancho u opening_ref pasa")
def _():
    import accesorios as A
    sf = {"ref": "SQ-1", "kind": "storefront", "ro_w_ft": 7.5}
    cr = {"id": "Z-7", "element": "storefront_cripples", "length_ft": 7.5}
    falla(A._storefront_de_cripples, {"walls": [cr], "openings_extra": []}, texto="R75.4")
    A._storefront_de_cripples({"walls": [cr], "openings_extra": [sf]})
    A._storefront_de_cripples({"walls": [dict(cr, length_ft=9.0, opening_ref="SQ-1")], "openings_extra": [sf]})
    falla(A._storefront_de_cripples, {"walls": [dict(cr, opening_ref="SQ-9")], "openings_extra": [sf]}, texto="R75.4")


@caso("R75.5 cambio de type colineal: en el jamb = error; en la cara del perpendicular (T) = OK; RFI = OK")
def _():
    import chequeos_v75 as C
    perp = W("X-5", "X", "H", 300.0, 307.0, 60.0, 101.0)            # llega a la línea (c 100–111) en y 300–307
    malo = [W("Y-1", "Y", "V", 100.0, 111.0, 200.0, 260.0), W("Z-1", "Z", "V", 100.0, 111.0, 260.0, 500.0), perp]
    assert C.cambios_sin_nodo(malo) == [("Y-1", "Z-1", 260.0)]
    falla(C.verificar_r75_5, {"walls": malo}, texto="R75.5")
    bueno = [W("Y-1", "Y", "V", 100.0, 111.0, 200.0, 300.0), W("Z-1", "Z", "V", 100.0, 111.0, 300.0, 500.0), perp]
    assert C.cambios_sin_nodo(bueno) == []
    rfi = copy.deepcopy(malo)
    rfi[0]["type_change_rfi"] = {"alternativas": ["nodo", "jamb"], "delta_lf": 2.2, "source": "Z1.01"}
    C.verificar_r75_5({"walls": rfi})


@caso("R75.6 lado de alcove dueño de la esquina con el wall de su línea = error")
def _():
    import chequeos_v75 as C
    linea = [W("Y-1", "Y", "V", 100.0, 111.0, 0.0, 200.0), W("Y-2", "Y", "V", 100.0, 111.0, 260.0, 400.0)]
    lado_malo = W("X-7", "X", "H", 200.0, 207.0, 60.0, 111.0)       # cruza la banda de la línea (100–111)
    lado_bueno = W("X-7", "X", "H", 200.0, 207.0, 60.0, 100.0)      # termina en la cara de la línea
    pt = {"other_framing": [{"element": "alcove", "ids": ["X-7"], "abre_en": ["Y-1", "Y-2"]}]}
    assert C.alcove_con_esquina({"walls": linea + [lado_malo]}, pt) == [("X-7", 11.0)]
    assert C.alcove_con_esquina({"walls": linea + [lado_bueno]}, pt) == []


@caso("R75.7 return corto medido desde la cara interior del tramo largo = error; desde la exterior o declarado = OK")
def _():
    import chequeos_v75 as C
    frente = W("W-1", "W", "H", 500.0, 506.0, 100.0, 280.0)          # 10 ft
    malo = W("W-2", "W", "V", 100.0, 106.0, 506.0, 512.0)             # arranca en la cara interior (c1)
    bueno = W("W-2", "W", "V", 100.0, 106.0, 500.0, 512.0)            # arranca en la cara exterior (c0)
    pt = {"types": {"W": {"filas": [{"ids": ["W-1", "W-2"]}]}}}
    assert C.returns_sin_esquina({"walls": [frente, malo]}, pt) == [("W-2", "W-1")]
    assert C.returns_sin_esquina({"walls": [frente, bueno]}, pt) == []
    decl = dict(malo, return_basis={"value": "inner_face", "source": "5/Z9.01"})
    assert C.returns_sin_esquina({"walls": [frente, decl]}, pt) == []
    box = [W("W-3", "W", "H", 500.0, 506.0, 100.0, 120.0), W("W-4", "W", "V", 100.0, 106.0, 506.0, 512.0)]
    pt2 = {"types": {"W": {"filas": [{"ids": ["W-3", "W-4"]}]}}}
    assert C.returns_sin_esquina({"walls": box}, pt2) == []            # box chico: no aplica


print(f"test_v75: {N[0] - len(F)}/{N[0]} OK")
sys.exit(1 if F else 0)
