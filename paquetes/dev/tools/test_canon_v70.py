#!/usr/bin/env python3
"""Tests v70 de canon.py con datos SINTÉTICOS (base() de test_canon.py; ningún proyecto real).
Correr: python3 test_canon_v70.py

(a) canopy_soffit en walls -> ValueError (doble cuenta de canopy joists; va en runs / ceilings).
(b) roof_step / ceiling_transition / soffit_side / ceiling_bulkhead / vestibule_head / grille_head sin faces ni
    faces_none_reason -> ValueError.
(c) clave de wall fuera del esquema con números -> ValueError que nombra la clave y el campo; sin números -> aviso.
(d) canopy_joist: la operación imprime el RUN y, evaluada, da el número de joists.
(e) constants.deck_breaks con `sheet`: solo se compara con bandas de esa hoja.
R70.1 ceiling no furring sin system_callout; R70.6 pier interior con parts = caras interiores; R70.7 storefront desde
el piso fuera del LF del EXT.
"""
import copy
import math
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import canon as K  # noqa: E402
from test_canon import base, _falla  # noqa: E402


def test_a_canopy_soffit_en_walls_rechazado():
    d = base()
    d["constants"]["canopy_soffit_track_lines"] = {"value": 2, "source": "sintético"}
    cs = {"id": "CS-1", "tag": "OTHER", "element": "canopy_soffit", "stud_size": "3-5/8\"", "oc_in": 16, "rows": 1,
          "length_ft": 20.0, "height_ft": 3.0, "openings": [], "facade": "N", "source": "1/Z9.01",
          "wall_line_ft": {"value": 18.0, "source": "Z1.01"}}
    d["ceilings"] = [{"room": "canopy N", "system": "canopy_joist", "system_callout": {"detail": "9/Z9.33", "on_plan": True, "source": "sintético: bubble sobre este ceiling"}, "area_sf": 80.0, "ns_ft": 4.0, "ew_ft": 20.0,
                      "source": "2/Z9.01"}]
    d["constants"]["carrying_direction"] = {"value": "N-S", "source": "sintético"}
    mal = copy.deepcopy(d)
    mal["walls"].append(dict(cs))
    _falla(mal, "canopy_soffit en walls")
    d.setdefault("runs", []).append(dict(cs, orientation="horizontal"))     # en runs: aceptado
    K.calcular(d)


def test_b_elementos_con_board_exigen_faces():
    d = base()
    d["constants"]["roof_step_rows_drawn"] = {"value": 1, "source": "sintético"}
    rs = {"id": "RS-1", "tag": "RS", "element": "roof_step", "stud_size": "3-5/8\"", "oc_in": 16, "rows": 1,
          "length_ft": 10.0, "height_ft": 2.0, "openings": [], "source": "3/Z9.02", "faces": []}
    mal = copy.deepcopy(d)
    mal["walls"].append(dict(rs))
    _falla(mal, "declare faces or faces_none_reason")
    for el in K.BOARD_ELEMS:
        m2 = copy.deepcopy(mal)
        m2["walls"][-1]["element"] = el
        m2["walls"][-1].pop("faces")
        try:
            K._v70_checks(m2, [])
            raise AssertionError(f"{el} sin faces aceptado")
        except ValueError as e:
            assert "faces_none_reason" in str(e), e
    ok = copy.deepcopy(mal)
    ok["walls"][-1]["faces_none_reason"] = "el detalle sintético no dibuja board"
    K._v70_checks(ok, [])


def test_c_claves_fuera_de_esquema():
    d = base()
    d["walls"][1]["plywood"] = {"material": "frt_3_4", "height_ft": 10.0, "length_ft": 12.0, "source": "9/Z9.03"}
    d["walls"][1]["blocking"] = 24.0
    try:
        K.calcular(copy.deepcopy(d))
        raise AssertionError("plywood fuera de esquema aceptado")
    except ValueError as e:
        m = str(e)
        assert "plywood -> plywood_strips" in m and "blocking -> blocking_items" in m, m
    d["walls"][1].pop("plywood")
    d["walls"][1].pop("blocking")
    d["walls"][1]["comentario_lectura"] = "texto sin números"
    d["walls"][1]["ancho_info"] = {"value": 3.5}                 # sufijo de traza: aceptado
    out = K.calcular(d)
    assert any("comentario_lectura" in a for a in out["avisos"]), "clave sin números debía avisar"
    assert not any("ancho_info" in a for a in out["avisos"])
    # las claves v69 de etapas y las que canon.py lee son del esquema
    for k in ("sheet", "page", "tag_ids", "band", "source", "notes", "length_source", "faces_none_reason",
              "band_length_ok_reason", "stops_under_beam", "zones"):
        assert k in K.WALL_KEYS, k


def _evalua(op):
    m = re.search(r"ROUNDUP\(([\d.]+)/(?:\(([\d.]+)/12\)|([\d.]+))\)\+1 = (\d+) joists x ([\d.]+) = ([\d.]+)", op)
    assert m, op
    run = float(m.group(1))
    oc = float(m.group(2)) / 12.0 if m.group(2) else float(m.group(3))
    n = int(m.group(4))
    return run, math.ceil(run / oc) + 1, n, float(m.group(5)), float(m.group(6))


def test_d_operacion_canopy_joist_imprime_el_run():
    d = base()
    d["constants"]["carrying_direction"] = {"value": "N-S", "source": "sintético"}
    d["ceilings"] = [{"room": "canopy X", "system": "canopy_joist", "system_callout": {"detail": "9/Z9.33", "on_plan": True, "source": "sintético: bubble sobre este ceiling"}, "area_sf": round(47.9 * 12.6, 2), "ns_ft": 12.6,
                      "ew_ft": 47.9, "joist_dir": {"value": "N-S", "source": "7/Z9.04"}, "source": "3/Z9.04"}]
    out = K.calcular(d)
    op = [f["operacion"] for f in out["filas"] if f.get("room") == "canopy X"][0]
    run, calc, n, largo, lf = _evalua(op)
    assert abs(run - 47.9) < 1e-9, op                     # el RUN, no el largo del joist (12.6)
    assert calc == n == 37, (op, calc, n)
    assert abs(largo - 12.6) < 1e-9 and abs(lf - n * largo) < 0.01, op
    # oc que no es exacto en 3 decimales y run justo en el borde: el texto sigue reproduciendo n
    d["ceilings"] = [{"room": "canopy Y", "system": "canopy_joist", "system_callout": {"detail": "9/Z9.33", "on_plan": True, "source": "sintético: bubble sobre este ceiling"}, "area_sf": 64.0, "ns_ft": 4.0, "ew_ft": 16.0,
                      "joist_dir": {"value": "N-S", "source": "7/Z9.04"}, "source": "3/Z9.04"}]
    out = K.calcular(d)
    op = [f["operacion"] for f in out["filas"] if f.get("room") == "canopy Y"][0]
    run, calc, n, _, _ = _evalua(op)
    assert calc == n == 13, (op, calc, n)


def _datos_deck(walls, breaks):
    return {"constants": {"deck_breaks": {"value": breaks, "source": "S9.01 sintético"}}, "walls": walls}


def test_e_deck_breaks_por_hoja():
    par = {"id": "P-1", "element": "parapet", "height_ft": 4.0, "length_ft": 20.0, "sheet": "Z2.02",
           "band": {"sheet": "Z2.02", "ori": "V", "c0": 98, "c1": 102, "lo": 900, "hi": 1300}}
    wal = {"id": "W-1", "element": "wall", "height_ft": 12.0, "length_ft": 20.0, "sheet": "Z2.01",
           "band": {"sheet": "Z2.01", "ori": "V", "c0": 498, "c1": 502, "lo": 1000, "hi": 1400}}
    br = [{"ori_walls": "V", "coord_pt": 1200.0, "sheet": "Z2.01"}]
    K._v68_checks(_datos_deck([par], br))                   # parapet en otra hoja: no se compara
    try:
        K._v68_checks(_datos_deck([par, wal], br))
        raise AssertionError("wall en la hoja del quiebre debía fallar")
    except ValueError as e:
        assert "W-1" in str(e) and "quiebre" in str(e), e
    br_sin = [{"ori_walls": "V", "coord_pt": 1200.0}]        # sin sheet: se compara con todas (como antes)
    try:
        K._v68_checks(_datos_deck([par], br_sin))
        raise AssertionError("sin sheet debía comparar con todas las bandas")
    except ValueError as e:
        assert "P-1" in str(e), e


def _techo(sysm, **kw):
    c = {"room": "R9", "system": sysm, "area_sf": 120.0, "span_ft": 12.0, "run_ft": 10.0, "source": "Z4.01"}
    c.update(kw)
    return c


def test_r70_1_system_callout():
    d = base()
    d["ceilings"] = [x for x in d["ceilings"] if x.get("system") == "furring"]
    sc = {"detail": "6/Z9.33", "on_plan": True, "source": "Z4.01 bubble 6/Z9.33 sobre R9"}
    for sysm, extra in (("stud_joist", {"joist_source": "6/Z9.33", "detail": "6/Z9.33"}),
                        ("framed_soffit", {"detail": "10/Z9.33", "drop_lines": {"value": 0, "source": "10/Z9.33"}})):
        mal = copy.deepcopy(d)
        mal["ceilings"].append(_techo(sysm, **extra))
        _falla(copy.deepcopy(mal), "R70.1")
        m2 = copy.deepcopy(mal)
        m2["ceilings"][-1]["source"] = "Z4.01 legend SUSPENDED GYPSUM BOARD CEILING"
        _falla(copy.deepcopy(m2), "SUSPENDED")
        m3 = copy.deepcopy(mal)
        m3["ceilings"][-1]["system_callout"] = dict(sc, on_plan=False)        # típico, no dibujado sobre ESTE ceiling
        _falla(m3, "R70.1")
        mal["ceilings"][-1]["system_callout"] = sc
        K._v70_checks(mal, [])
    ok = copy.deepcopy(d)
    ok["ceilings"].append(_techo("furring", source="Z4.01 legend SUSPENDED"))  # furring no necesita callout
    K._v70_checks(ok, [])


def _pier(L, **kw):
    w = {"id": "PR-1", "tag": "Q7", "element": "pier", "stud_size": "3-5/8\"", "oc_in": 16, "rows": 1,
         "length_ft": L, "height_ft": 12.0, "source": "1/Z9.25", "detail": "1/Z9.25",
         "parts": [{"stud_size": "6\"", "studs_drawn": {"value": 4, "source": "1/Z9.25"}},
                   {"stud_size": "3-5/8\"", "studs_drawn": {"value": 4, "source": "1/Z9.25"}}],
         "faces": [{"room": "R2 interior", "board": "5/8 regular", "layers": 1, "height_ft": 12.0, "length_ft": 3.0},
                   {"room": "exterior L (no gypsum)", "board": "5/8 regular", "layers": 1, "height_ft": 12.0,
                    "length_ft": 4.5}]}
    w.update(kw)
    return w


def test_r70_6_pier_interior_no_suma_perimetro():
    try:
        K._v70_checks({"walls": [_pier(7.5)]}, [])
        raise AssertionError("perímetro completo aceptado")
    except ValueError as e:
        assert "R70.6" in str(e) and "PR-1" in str(e), e
    K._v70_checks({"walls": [_pier(3.0)]}, [])                                   # caras interiores
    K._v70_checks({"walls": [_pier(7.5, type_lf_basis="RFI: caja completa por criterio")]}, [])
    K._v70_checks({"walls": [_pier(7.5, tag="EXT")]}, [])                        # exterior: no aplica
    p = _pier(7.5)
    p["parts"][0]["faces_ft"], p["parts"][1]["faces_ft"] = [2.0, 2.5], [1.5, 1.5]
    try:
        K._v70_checks({"walls": [p]}, [])
        raise AssertionError("perímetro por parts aceptado")
    except ValueError as e:
        assert "R70.6" in str(e), e


def test_r70_7_storefront_desde_el_piso():
    w = {"id": "X-9", "tag": "EXT", "element": "wall", "length_ft": 30.0, "openings": [
        {"ref": "SF-9", "kind": "storefront", "ro_w_ft": 10.0, "head_ft": 9.0, "sill_ft": 0}]}
    try:
        K._v70_checks({"walls": [copy.deepcopy(w)]}, [])
        raise AssertionError("storefront desde el piso aceptado")
    except ValueError as e:
        assert "R70.7" in str(e) and "storefront_cripples" in str(e), e
    cw = copy.deepcopy(w)
    cw["openings"][0].pop("sill_ft")
    cw["openings"][0]["kind"] = "curtain_wall"
    try:
        K._v70_checks({"walls": [cw]}, [])
        raise AssertionError("curtain wall sin sill aceptado")
    except ValueError as e:
        assert "R70.7" in str(e), e
    K._v70_checks({"walls": [dict(copy.deepcopy(w), storefront_in_lf_reason="vano dentro del run por criterio")]}, [])
    alto = copy.deepcopy(w)
    alto["openings"][0]["sill_ft"] = 3.0                                          # storefront sobre muro bajo
    K._v70_checks({"walls": [alto]}, [])


if __name__ == "__main__":
    fallas = 0
    for k, f in sorted(globals().items()):
        if k.startswith("test_") and callable(f):
            try:
                f()
                print("OK  ", k)
            except Exception as e:  # noqa: BLE001
                fallas += 1
                print("FALLA", k, type(e).__name__, str(e)[:300])
    print(f"{'TODOS OK' if not fallas else str(fallas) + ' FALLA(S)'}")
    sys.exit(1 if fallas else 0)
