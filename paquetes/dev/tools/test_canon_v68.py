#!/usr/bin/env python3
"""Tests v68 (arbitraje #16A/#16B, 2026-10-17): lo que varió entre dos pruebas con el mismo plano. Datos SINTÉTICOS
(E24: ningún número de examen). Correr: python3 test_canon_v68.py"""
import copy
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import board_caras as B  # noqa: E402
import canon as K  # noqa: E402
import corridas as C  # noqa: E402
import test_canon as T  # noqa: E402
import vigas_sobre_walls as V  # noqa: E402


def _falla(d, txt):
    T._falla(d, txt)


def test_mr_solo_detras_del_fixture():
    """#16B: 5/8 MR en el exterior wall (pared lateral de grab bars) además del chase."""
    d = T.base()
    d["walls"][2]["faces"][1] = {"room": "922", "board": "5/8 MR", "layers": 1, "height_ft": 9.0}
    _falla(copy.deepcopy(d), "5/8 MR sin wet_fixture")
    d["wet_fixtures"] = [{"ref": "LAV", "kind": "lavatory", "wall": "I1", "room": "922", "source": "1/A08.01"}]
    _falla(copy.deepcopy(d), "back_source")
    d["wet_fixtures"][0]["back_source"] = "1/A08.01 lavatory contra I1; P00.01 carrier"
    f = K.calcular(d)["familias"]
    assert abs(f["5/8\" gyp MOISTURE RESISTANT"] - 10.0 * 9.0) < 0.01, f


def test_ballistic_jogs_y_largo_con_fuente():
    """#16A/#16B: contorno ballistic sin el jog del A1K SW y un A1K de 2.573 contra la cota impresa."""
    d = T.base()
    d["details"]["4/A12.01"] = {"layers_per_face": 1, "k_panel": {"panel_to_ft": 8.0},
                                "sealant": {"bottom_faces": 2, "top_faces": 2, "source": "4/A12.01"}}
    d["walls"].append({"id": "K1", "tag": "A1K", "stud_size": "3-5/8\"", "oc_in": 24, "rows": 1, "length_ft": 3.0,
                       "height_ft": 12.0, "detail": "4/A12.01", "source": "A02.01",
                       "faces": [{"room": "c", "board": "5/8 regular", "layers": 1, "height_ft": 12.0,
                                  "k_customer": True}]})
    d["nodes"] += [{"id": "k1a", "kind": "free", "wall": "K1"}, {"id": "k1b", "kind": "free", "wall": "K1"}]
    d["constants"]["ballistic_contour_ft"] = {"value": 3.0, "source": "A02.01"}
    _falla(copy.deepcopy(d), "ballistic_jogs")
    d["ballistic_jogs"] = []
    _falla(copy.deepcopy(d), "length_printed_ft ni length_source")
    d["walls"][-1]["length_printed_ft"] = 3.0
    K.calcular(d)


def test_parapet_plies_del_detalle():
    d = T.base()
    d["parapets"][0]["plies_blocking"] = 1
    _falla(d, "plies_blocking {value, source}")
    d = T.base()
    d["parapets"][0]["plies_blocking"] = {"value": 2, "source": "4/A09.26"}
    f = K.calcular(d)["familias"]
    d["parapets"][0]["plies_blocking"] = {"value": 1, "source": "4/A09.26"}
    f1 = K.calcular(d)["familias"]
    assert abs(f["FRT blocking"] - f1["FRT blocking"] - 27.667) < 0.01


def test_blocking_rotulo_obligatorio_y_frt():
    """#16B: millwork / toilet accessories como 'metal' sin rótulo; la sheet note dice FRTW / FRT."""
    d = T.base()
    d["blocking_items"].append({"ref": "MW cleat", "lf": 8.0, "material": "metal", "source": "A12.03"})
    _falla(copy.deepcopy(d), "blocking sin label")
    d["blocking_items"][-1]["label"] = "PROVIDE FRTW BLOCKING AT ALL MILLWORK VERTICAL SURFACE CLEAT"
    _falla(copy.deepcopy(d), "dice FRT")
    d["blocking_items"][-1]["material"] = "FRT"
    f = K.calcular(d)["familias"]
    d2 = T.base()
    assert abs(f["FRT blocking"] - K.calcular(d2)["familias"]["FRT blocking"] - 8.0) < 0.01
    d3 = T.base()                                             # 'PROVIDE BLOCKING' a secas no es FRT
    d3["blocking_items"].append({"ref": "stop", "lf": 2.0, "material": "FRT", "source": "A00.30",
                                 "label": "PROVIDE BLOCKING AT EACH WALL STOP"})
    _falla(d3, "solo donde el detalle lo rotula")


def test_ceiling_detalle_manda_el_sistema():
    """#16B: 116 CSR soffit (10/A09.33 dibuja studs a estructura) como furring con hangers."""
    d = T.base()
    del d["ceilings"][0]["detail_none_reason"]
    _falla(copy.deepcopy(d), "ceiling suspendido sin detail")
    d["ceilings"][0]["detail"] = "10/A09.33"
    d["details"]["10/A09.33"] = {"layers_per_face": 1, "ceiling_system": "framed_soffit"}
    _falla(d, "ceiling_system framed_soffit")


def test_quiebre_de_deck():
    """walls que cruzan un grid (cambio de B.O.D.) con una sola altura."""
    d = T.base()
    del d["constants"]["deck_breaks"]
    _falla(copy.deepcopy(d), "deck_breaks")
    d["constants"]["deck_breaks"] = {"value": [{"ori_walls": "V", "coord_pt": 500.0}], "source": "S2.20 grid B"}
    d["walls"][2]["band"] = {"sheet": "A02.01", "ori": "V", "c0": 100.0, "c1": 107.0, "lo": 420.0, "hi": 600.0}
    _falla(copy.deepcopy(d), "cruza el quiebre")
    d["walls"][2]["band"]["hi"] = 499.5                      # termina en el quiebre: no lo cruza
    K.calcular(d)


def test_stops_under_beam_perfil_y_peralte():
    """#16A: 'W12 (high roof) / W14x22 (low roof)' con un solo peralte para walls bajo W14x30 / W18x35."""
    d = T.base()
    w = d["walls"][2]
    w["stops_under_beam"] = {"profile": "W12 / W14x22", "depth_ft": 1.017, "source": "S2.20"}
    _falla(copy.deepcopy(d), "no es una marca única")
    w["stops_under_beam"] = {"profile": "W14x30", "depth_ft": 1.017, "source": "S2.20"}
    _falla(copy.deepcopy(d), "d AISC")
    w["stops_under_beam"] = {"profile": "W14x30", "depth_ft": 1.15, "source": "S2.20",
                             "bod_ft": {"value": 16.0, "source": "S2.20"}}
    _falla(copy.deepcopy(d), "E26")
    w["height_ft"] = round(16.0 - 13.8 / 12.0, 3)
    for f in w["faces"]:
        f["height_ft"] = min(f["height_ft"], w["height_ft"])
    K.calcular(d)


def test_pier_con_parts_como_column_wrap():
    """#16A: piers del storefront con parts [6" x2, 3-5/8" x2] -> canon los ignoraba si element = pier."""
    d = T.base()
    p = d["walls"][1]
    p["parts"] = [{"stud_size": "6\"", "studs_drawn": {"value": 2, "source": "1/A09.25"}},
                  {"stud_size": "3-5/8\"", "studs_drawn": {"value": 2, "source": "1/A09.25"}}]
    d["nodes"] = [n for n in d["nodes"] if n.get("wall") != "P1" and "P1" not in (n.get("walls") or [])] + \
        [{"id": "b", "kind": "free", "wall": "N1"}]
    o = K.calcular(d)
    fp = [x for x in o["filas"] if str(x.get("ref", "")).startswith("P1.")]
    assert len(fp) == 2 and all(x["pcs"] == 2 for x in fp), fp


def test_frt_plywood_por_material_y_sealant_aparte():
    d = T.base()
    d["plywood_strips"].append({"ref": "backboard", "lf": 10.0, "width_ft": 8.0, "source": "A11.03",
                                "material": "frt_3_4"})
    d["plywood_strips"].append({"ref": "column wrap 5/8\" ext grade", "lf": 6.0, "width_ft": 10.0,
                                "source": "5/A09.25", "material": "frt_5_8_ext"})
    d["sealant_base_exterior"] = {"lf": 40.0, "source": "5/A09.26"}
    o = K.calcular(d)
    m = {x["key"]: x for x in o["materiales"]}
    tot = sum(x["net"] for x in o["materiales"] if x["family"] == "FRT plywood (SF)")
    assert abs(tot - o["familias"]["FRT plywood (SF)"]) < 0.05
    assert abs(m["frt_3_4"]["net"] - (80.0 + 32.0 * 0.583)) < 0.02, m["frt_3_4"]
    assert m["frt_5_8_ext"]["unit"] == "SF" and m["nailbase_5_8_polyiso"]["net"] > 0
    assert m["exterior"]["net"] == 40.0 and m["acoustical"]["net"] > 0
    assert abs(m["exterior"]["net"] + m["acoustical"]["net"] - o["familias"]["acoustical sealant"]) < 0.05
    assert all(x["material"].isascii() for x in o["materiales"])          # nombres del Excel en inglés
    # contrato con plantilla_excel (v68): por material + sealant exterior, y plantilla los acepta
    import plantilla_excel as P
    assert abs(sum(o["frt_plywood_by_material"].values()) - o["familias"]["FRT plywood (SF)"]) < 0.05
    assert o["sealant_exterior_lf"] == 40.0
    assert P.desglose_frt(o) and P.sealant_exterior(o) == 40.0
    for bad in ({"ref": "strip sin espesor", "lf": 1.0, "width_ft": 1.0, "source": "A02.01"},
                {"ref": "3/4\" FRT plywood", "lf": 1.0, "width_ft": 1.0, "source": "A02.01", "material": "frt_5_8"},
                {"ref": "CSR soffit FRTW blocking", "lf": 1.0, "width_ft": 1.0, "source": "10/A09.33",
                 "material": "frt_3_4"}):
        e = T.base()
        e["plywood_strips"].append(bad)
        _falla(e, "plywood_strip")


def test_hanger_wire_pcs_y_lf():
    o = K.calcular(T.base())
    h = [x for x in o["materiales"] if x["key"] == "hanger_wire"][0]
    assert h["pcs"] == o["hanger_pcs"]["total_pcs"] and h["net"] == o["hanger_pcs"]["lf_derivado"]


def test_corridas_source_con_comas_en_parentesis():
    assert C._src('C/A09.21 (6", 16 ga), 7/S5.20', "x")
    try:
        C._src("6/A12.01, sin forma", "x")
    except ValueError:
        pass
    else:
        raise AssertionError("una parte sin N/HOJA fuera de paréntesis debía fallar")


def test_vigas_perfil_por_rotulo():
    v = {"p0": (100.0, 200.0), "p1": (100.0, 500.0), "lw": 2.2}
    rot = [("W14X30", 112.0, 350.0), ("W18X35", 300.0, 350.0), ("W12X19", 100.0, 900.0)]
    pf = V.perfil(v, rot)
    assert pf["profile"] == "W14X30" and pf["depth_ft"] == round(13.8 / 12, 3), pf
    assert V.perfil(v, [("W99X1", 101.0, 300.0)]) is None
    walls = [{"id": "W1", "tag": "A1", "band": {"ori": "V", "c0": 97.0, "c1": 104.0, "lo": 210.0, "hi": 480.0}}]
    r = V.cruzar([dict(v, perfil=pf)], walls)
    assert r[0]["profile"] == "W14X30" and r[0]["depth_ft"] == round(13.8 / 12, 3)


def test_board_fondo_de_soffit_con_sus_capas():
    """#16A RFI-28: 9/A12.01 caras 2 layers, fondo del soffit 1 layer -> la face soffit_bottom se rechazaba."""
    d = {"details": {"9/X": {"layers_per_face": 2}},
         "walls": [{"id": "BH", "detail": "9/X", "length_printed_ft": 7.0,
                    "faces": [{"room": "a", "board": "5/8 regular", "layers": 2, "height_ft": 6.0},
                              {"room": "a-soffit", "board": "5/8 regular", "layers": 1, "height_ft": 0.5,
                               "soffit_bottom": True}]}]}
    try:
        B.calcular(copy.deepcopy(d))
    except ValueError:
        pass
    else:
        raise AssertionError("sin soffit_bottom_layers debía fallar")
    d["details"]["9/X"]["soffit_bottom_layers"] = {"value": 1, "source": "9/X"}
    o = B.calcular(d)
    assert abs(o["totales_sf"]["5/8 regular"] - (7.0 * 6.0 * 2 + 7.0 * 0.5)) < 0.01


def test_transicion_vertical_studs_a_estructura():
    """#16A <n> (B.O.D. - GB) vs #16B <n> (escalón GB/ACT) en la misma transición: el vertical stud va a estructura."""
    d = T.base()
    d["constants"]["transition_trim_per_lf"] = {"value": 2, "source": "7/X9.33"}
    tr = {"id": "TRX", "tag": "OTHER", "element": "ceiling_transition", "faces_none_reason": "sintético (v70): el board no es objeto de este test", "stud_size": "3-5/8\"", "oc_in": 16,
          "rows": 1, "length_ft": 12.0, "height_ft": 0.5, "source": "7/X9.33",
          "edges": [{"edge": "N", "against": "ACT", "length_ft": 12.0, "source": "X4.01"}],
          "kickers": {"oc_in": 48, "angle_deg": 45, "source": "7/X9.33"},
          "vertical_studs": {"oc_in": 16, "height_ft": 0.5, "source": "7/X9.33",
                             "bod_ft": {"value": 14.0, "source": "S2.20"}, "ceiling_ft": {"value": 10.0, "source": "A04.01"}}}
    d["walls"].append(tr)
    d["nodes"] += [{"id": "x1", "kind": "free", "wall": "TRX"}, {"id": "x2", "kind": "free", "wall": "TRX"}]
    _falla(copy.deepcopy(d), "a estructura")                       # escalón 0.5 != 14.0 - 10.0
    sin = copy.deepcopy(d)
    del sin["walls"][-1]["vertical_studs"]["bod_ft"]
    _falla(sin, "bod_ft")
    tr["height_ft"] = tr["vertical_studs"]["height_ft"] = 4.0
    en_runs = copy.deepcopy(d)                                      # #16B: la transición en runs = mismos studs
    en_runs.setdefault("runs", []).append(en_runs["walls"].pop())
    en_runs["nodes"] = [n for n in en_runs["nodes"] if n.get("wall") != "TRX"]
    en_runs["runs"][-1]["orientation"] = "vertical"
    sin_tr = copy.deepcopy(en_runs)
    sin_tr["runs"].pop()
    f_0 = K.calcular(sin_tr)["familias"]["3-5/8\" stud (todos los gauges)"]
    f_w = K.calcular(copy.deepcopy(d))["familias"]["3-5/8\" stud (todos los gauges)"]
    f_r = K.calcular(en_runs)["familias"]["3-5/8\" stud (todos los gauges)"]
    assert abs(f_w - f_r) < 0.01 and f_r > f_0 + 10 * 4.0 - 0.01, (f_w, f_r, f_0)
    mal = copy.deepcopy(d)                                          # #16B: borde contra wall sumado
    mal["walls"][-1]["edges"].append({"edge": "S", "against": "wall", "length_ft": 3.0, "source": "X4.01"})
    _falla(mal, "no es transición")
    mal = copy.deepcopy(d)
    mal["walls"][-1]["length_ft"] = 15.0
    _falla(mal, "Σ edges")
    mal = copy.deepcopy(d)
    del mal["walls"][-1]["edges"]
    _falla(mal, "sin edges")
    mal = copy.deepcopy(d)                                          # #16B TR-116 sobre el CSR (framed_soffit)
    mal["ceilings"].append({"room": "CSR", "system": "framed_soffit", "system_callout": {"detail": "9/Z9.33", "on_plan": True, "source": "sintético: bubble sobre este ceiling"}, "area_sf": 41.0, "span_ft": 12.0,
                            "run_ft": 3.42, "source": "10/X9.33", "drop_lines": {"value": 1, "source": "10/X9.33"}})
    mal["walls"].append({"id": "CSR-D", "tag": "CSR", "element": "ceiling_bulkhead", "faces_none_reason": "sintético (v70): el board no es objeto de este test", "stud_size": "3-5/8\"",
                         "oc_in": 16, "rows": 1, "length_ft": 12.0, "height_ft": 7.25, "source": "10/X9.33",
                         "soffit_of": "CSR", "openings": []})
    mal["nodes"] += [{"id": "cs1", "kind": "free", "wall": "CSR-D"}, {"id": "cs2", "kind": "free", "wall": "CSR-D"}]
    K.calcular(copy.deepcopy(mal))                                  # el soffit completo sin room en la transición pasa
    mal["walls"][-2]["room"] = "CSR"
    _falla(mal, "drop_lines (doble conteo")
    o = K.calcular(d)
    v = [r for r in o["filas"] if r["familia"] == "vertical studs @ transition"][0]
    assert v["pcs"] == 10 and "4.0" in v["operacion"], v


def test_parapet_y_wraps_no_van_en_runs():
    """v68: parapet / column_wrap / pier en runs perdían sus studs sin aviso (mismo hueco que la transición)."""
    for el in ("parapet", "column_wrap", "pier"):
        d = T.base()
        d.setdefault("runs", []).append({"id": "R-" + el, "element": el, "orientation": "vertical",
                                         "length_ft": 5.0, "height_ft": 3.0, "source": "X2.02"})
        _falla(d, "va en walls")


if __name__ == "__main__":
    n = 0
    for k, f in list(globals().items()):
        if k.startswith("test_") and callable(f):
            f()
            n += 1
            print("OK", k)
    print(f"{n} tests OK")
