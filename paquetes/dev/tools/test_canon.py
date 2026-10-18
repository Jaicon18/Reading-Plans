#!/usr/bin/env python3
"""Tests de canon.py v64 (arbitraje #11 + #12 + #13 + decisiones del usuario 2026-10-16). Cada test de 'dato malo' reproduce un error real de #11A/#11B.
Correr: python3 test_canon.py"""
import copy
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import canon as K  # noqa: E402

C = {"bracing_spacing_in": {"value": 48, "source": "F/1/S5.20"}, "sheet_len_ft": {"value": 12, "source": "4/S5.20"},
     "stud_bay_in": {"value": 14.375, "source": "60.10"}, "furring_oc_in": {"value": 16, "source": "RFI-11"},
     "carrying_oc_in": {"value": 48, "source": "RFI-11"}, "hanger_oc_in": {"value": 48, "source": "RFI-11"},
     "deck_breaks": {"value": [], "source": "S2.20 NO SLOPE (sintético)"}}


def base():
    return {
        "constants": copy.deepcopy(C),
        "details": {"3/A12.01": {"layers_per_face": 1,
                                 "sealant": {"bottom_faces": 2, "top_faces": 0, "source": "3/A12.01"}},
                    "C/A09.21": {"layers_per_face": 1,
                                 "sealant": {"bottom_faces": 0, "top_faces": 0, "source": "C/A09.21 sin bead"}}},
        "walls": [
            {"id": "N1", "tag": "EXT", "stud_size": "6\"", "oc_in": 16, "rows": 1, "length_ft": 26.0,
             "height_ft": 14.25, "line": "G", "from_ft": 0.0, "to_ft": 26.0, "detail": "C/A09.21",
             "faces": [{"room": "100", "board": "5/8 regular", "layers": 1, "height_ft": 14.25}],
             "openings": [{"ref": "GL-2 #1", "kind": "window", "ro_w_ft": 7.0, "head_ft": 8.5, "sill_ft": 6.5,
                           "with_sill": True, "source": "A09.02", "header_type": "6\" C box beam",
                           "header_type_source": "11/A09.27", "pieces": 4, "pieces_source": "11/A09.27",
                           "jamb_return": True, "jamb_return_source": "11/A09.27"}],
             "source": "A02.01"},
            {"id": "P1", "tag": "PIER", "element": "pier", "stud_size": "3-5/8\"", "oc_in": 16, "rows": 1,
             "length_ft": 1.667, "height_ft": 14.25, "line": "G", "from_ft": 26.0, "to_ft": 27.667,
             "source": "2/A09.25"},
            {"id": "I1", "tag": "A1", "stud_size": "3-5/8\"", "oc_in": 16, "rows": 1, "length_ft": 10.0,
             "height_ft": 15.25, "detail": "3/A12.01", "purlin": True,
             "faces": [{"room": "104", "board": "5/8 regular", "layers": 1, "height_ft": 15.25},
                       {"room": "122", "board": "5/8 regular", "layers": 1, "height_ft": 9.0}],
             "openings": [], "source": "A02.01"},
            {"id": "FAS", "tag": "OTHER", "element": "fascia_box", "stud_size": "3-5/8\" canopy", "oc_in": 16,
             "rows": 1, "length_ft": 30.0, "height_ft": 1.75, "openings": [], "source": "7/A09.26", "facade": "N",
             "height_source": "7/A09.26 T/STUD - B/STUD"},
        ],
        "nodes": [{"id": "a", "kind": "free", "wall": "N1"}, {"id": "b", "kind": "L", "walls": ["N1", "P1"]},
                  {"id": "c", "kind": "free", "wall": "P1"}, {"id": "d", "kind": "free", "wall": "I1"},
                  {"id": "e", "kind": "free", "wall": "I1"}, {"id": "f", "kind": "free", "wall": "FAS"},
                  {"id": "g", "kind": "free", "wall": "FAS"}],
        "ceiling_details": ["7/A09.26", "7/A09.33", "10/A09.33"],
        "ceilings": [{"room": "113", "system": "furring", "area_sf": 76.0, "span_ft": 8.0, "run_ft": 9.5,
                      "perimeter_ft": 35.0, "hanger_drop_ft": {"value": 4.25, "source": "S2.20"},
                      "source": "A04.01", "detail_none_reason": "A04.01 sin burbuja de detalle (sintético)"},
                     {"room": "104", "system": "stud_joist", "system_callout": {"detail": "9/Z9.33", "on_plan": True, "source": "sintético: bubble sobre este ceiling"}, "area_sf": 525.0, "span_ft": 30.0, "run_ft": 17.5,
                      "perimeter_ft": 17.5, "hanger_drop_ft": {"value": 4.5, "source": "S2.20"},
                      "joist_source": "6/A09.33", "source": "6/A09.33", "detail": "6/A09.33"}],
        "header_schedule": {"source": "7/S5.20", "rows": [
            {"max_span_ft": 3.333, "type": "SINGLE TRACK 18 GA", "pieces": 1, "piece": "track"},
            {"max_span_ft": 6.0, "type": "DOUBLE TRACK 18 GA", "pieces": 2, "piece": "track"},
            {"max_span_ft": 8.0, "type": "2-362CSJ20", "pieces": 2, "piece": "362CSJ20"}]},
        "sill_rule": {"double_over_ft": 4.0, "source": "2/S5.20"},
        "opening_schedule": {"sources": ["A00.30", "A09.02", "S2.20", "M01.01"], "items": [{"ref": "GL-2 #1"}]},
        "trim_items": [{"ref": "CSR soffit corner bead", "kind": "corner_bead", "lf": 40.0, "source": "10/A09.33"}],
        "facades": [{"id": "N", "base_strip_lf": 27.667, "solid_lf": 27.667, "height_nailbase_ft": 16.75,
                     "openings_sf": 16.0, "has_canopy": True, "source": "A09.02"}],
        "canopies": [{"id": "C-N", "facade": "N", "band_lf": 27.667, "source": "7/A09.26"}],
        "band": {"t_stud_ft": {"value": 12.5, "source": "7/A09.26"}, "b_stud_ft": {"value": 10.5, "source": "7/A09.26"},
                 "height_ft": {"value": 2.0, "source": "7/A09.26"}},
        "parapets": [{"id": "PAR-N", "lf": 27.667, "roofside_h_ft": 2.0,
                      "plies_blocking": {"value": 2, "source": "4/A09.26 2 plies dibujados"}, "source": "4/A09.26"}],
        "blocking_items": [{"ref": "artwork", "lf": 5.333, "material": "metal", "width_in": 48, "source": "A11.01",
                            "label": "PROVIDE BLOCKING"},
                           {"ref": "wall phone", "lf": 1.333, "material": "metal", "width_in": 10.5,
                            "source": "A02.01", "no_label_reason": "A02.01 sin rótulo de blocking"},
                           {"ref": "grille jamb", "lf": 23.0, "material": "FRT", "label": "FRT WOOD BLOCKING (TYP)",
                            "source": "3/A08.21"}],
        "plywood_strips": [{"ref": "GL-2 #1 head/sill/jambs", "lf": 32.0, "width_ft": 0.583, "source": "10/A09.27",
                            "material": "frt_3_4"}],
        "tile_base": [{"room": "113", "perimeter_ft": 35.0, "perimeter_basis": "net",
                       "gross_ft": {"value": 35.0, "source": "1/A08.01"}, "height_ft": {"value": 0.5, "source": "CT-12C 6\" A08.01"},
                       "doors": [], "source": "A08.01"}],
        "frp": {"top_ft": {"value": 5.0, "source": "A/A08.01"}, "rooms": ["113"]},
    }


def test_familias():
    f = K.calcular(base())["familias"]
    # tracks: N1 26 + P1 1.667 + I1 10 (bottom y top cada uno); fascia 2 x 30 a ceiling/soffit
    assert abs(f["bottom track (todos)"] - 37.667) < 0.01, f
    assert abs(f["top / deflection track (todos)"] - 37.667) < 0.01, f
    # fascia 2 x 30 + ceiling_perimeter generado desde ceilings (<n> + <n>)
    assert abs(f["track de ceilings / soffits"] - (60.0 + 35.0 + 17.5)) < 0.01, f
    assert abs(f["purlin (track to deck)"] - 7.5) < 0.01, f
    # header (7 + 1.333) x 4 piezas (box 11/A09.27, #20); sill (7 + 1.333) x 2 (double > 4'-0" 2/S5.20, #18)
    assert abs(f["header / box beam"] - 33.33) < 0.01 and abs(f["sill track"] - 16.67) < 0.01, f
    # ceiling 113 furring: ROUNDUP(8/1.333)+1 = 7 x <n>; 104 stud_joist: sin furring, joists a 3-5/8"
    assert abs(f["furring channel"] - 66.5) < 0.01, f
    # glass mat = base 27.667 x 0.5 + banda 27.667 x <n>; nailbase descuenta la MISMA banda
    assert abs(f["5/8\" glass mat sheathing"] - (13.8335 + 55.334)) < 0.01, f
    # FRT plywood = nailbase + strip de aberturas (SF), nunca blocking LF
    nail = 27.667 * 16.75 - 16.0 - 55.334
    # v63: + sheathing del fascia_box 30 x <n> (canon.py, 7/A09.26)
    assert abs(f["FRT plywood (SF)"] - (nail + 32.0 * 0.583 + 30.0 * 1.75)) < 0.02, f
    assert abs(f["cement board"] - 17.5) < 0.01, f
    # FRT blocking = parapet 2 plies + grille jamb rotulado; metal = artwork + edge (N1 y I1 > 12 ft, 1 fila c/u)
    assert abs(f["FRT blocking"] - (2 * 27.667 + 23.0)) < 0.01, f
    assert abs(f["metal stud blocking (362CR / STUD BLOCKING)"] - (5.333 + 26.0 + 10.0)) < 0.01, f
    assert abs(f["5/8\" EXTERIOR gyp sheathing"] - 27.667 * 2.0) < 0.01, f
    # v65: FRP = perímetro tile_base x top 5.0; sealant I1 (3/A12.01 abajo, 2 faces) = 10 x 2
    assert abs(f["FRP"] - 35.0 * 5.0) < 0.01, f
    assert abs(f["acoustical sealant"] - 20.0) < 0.01, f


def _falla(d, txt):
    try:
        K.calcular(d)
    except ValueError as e:
        assert txt in str(e), str(e)
        return
    raise AssertionError("debía fallar: " + txt)


def test_dato_malo_pier_dentro_del_wall():
    """#11B: el wall exterior del G front medido a través del pier + pier aparte = doble conteo."""
    d = base()
    d["walls"][0]["to_ft"] = 27.667
    d["walls"][0]["length_ft"] = 27.667
    _falla(d, "se solapan")


def test_dato_malo_canopy_sin_banda():
    """#11A/#11B: banda del canopy oeste olvidada en glass mat."""
    d = base()
    d["canopies"] = []
    _falla(d, "has_canopy")


def test_dato_malo_fascia_a_bottom_top():
    d = base()
    d["walls"][3]["element"] = "wall"
    d["walls"][3]["source"] = "7/A09.26"
    _falla(d, "es un detalle de ceiling/soffit")


def test_dato_malo_steel_header_sin_fuente():
    d = base()
    d["walls"][0]["openings"][0]["header"] = "steel_by_others"
    d["walls"][0]["openings"][0]["or_steel"] = True
    _falla(copy.deepcopy(d), "#19")                       # 'BOX BEAM OR STEEL' = metal stud box beam (v65b)
    del d["walls"][0]["openings"][0]["or_steel"]
    d["walls"][0]["openings"][0]["ref"] = "W-1"
    d["opening_schedule"]["items"] = [dict(i, ref="W-1") if i.get("ref") == "GL-2 #1" else i
                                      for i in d["opening_schedule"]["items"]]
    _falla(d, "steel_by_others sin header_source")


def test_dato_malo_frt_sin_rotulo():
    d = base()
    d["blocking_items"].append({"ref": "wall stop 111", "lf": 2.0, "material": "FRT", "source": "A00.30",
                                "label": "PROVIDE BLOCKING AT EACH WALL STOP"})
    _falla(d, "solo donde el detalle lo rotula")


def test_dispositivo_chico_sin_blocking():
    out = K.calcular(base())
    assert any("wall phone" in a for a in out["avisos"]), out["avisos"]


# ----------------------------------------------------------------------------- v62 (arbitraje #12)
def _par(id_, L, h, run=None, line=None, frm=0.0):
    w = {"id": id_, "tag": "PARAPET", "element": "parapet", "stud_size": "6\" parapet", "oc_in": 16, "rows": 1,
         "length_ft": L, "height_ft": h, "source": "11/S5.10", "line": line or id_, "from_ft": frm,
         "to_ft": round(frm + L, 4), "length_basis": "stud_cl"}
    if run:
        w["straight_run"] = run
    return w


def _solo(walls, **extra):
    d = {"constants": dict(copy.deepcopy(C), parapet_post_spacing_ft={"value": 5.0, "source": "6/S5.10"}),
         "walls": walls, "nodes": [], "trim_items": [], "trim_none_reason": "test",
         "tile_base_none_reason": "test", "frp_none_reason": "test"}
    d.update(extra)
    return d


def _bays(L, h, post=5.0, oc=16 / 12, minimo=5):
    nb = math.ceil(L / post - 1e-6)
    spb = max(minimo, 2 + max(0, math.ceil((L / nb - 0.6) / oc - 1e-6) - 1))   # v67: decisión usuario #3
    return nb * spb * h


def test_parapet_por_bay():
    """E3 (datos sintéticos): bays = ROUNDUP(L/5) por straight run; studs por bay = MAX(5, 2 + intermedios @16")
    (v68: mínimo 5 en runs de 2+ bays; un run de un bay usa la fórmula)."""
    ws = [_par("A", 40.0, 2.0), _par("B1", 30.0, 2.0, line="B"), _par("B2", 25.0, 4.5, line="B", frm=30.0),
          _par("C", 18.0, 4.0)]
    f = K.calcular(_solo(ws))["familias"]
    esperado = _bays(40.0, 2.0) + _bays(55.0, (30 * 2.0 + 25 * 4.5) / 55) + _bays(18.0, 4.0)
    assert abs(f["6\" parapet stud"] - esperado) < 0.05, (f["6\" parapet stud"], esperado)
    assert abs(esperado - (80.0 + 172.5 + 80.0)) < 0.05, esperado        # v67: bay de 4.5 -> 5 studs (antes 4)
    d = _solo([_par("C", 18.0, 4.0)])
    d["constants"]["parapet_studs_per_bay_min"] = {"value": 0, "source": "criterio distinto (prueba)"}
    f0 = K.calcular(d)["familias"]["6\" parapet stud"]
    assert abs(f0 - _bays(18.0, 4.0, minimo=0)) < 0.05 and f0 < _bays(18.0, 4.0), f0   # sin mínimo: 4 por bay
    assert abs(f["bottom track (todos)"] - sum(w["length_ft"] for w in ws)) < 0.01


def test_v66_parapet_run_por_linea():
    """#15A: la misma línea partida en el cambio de altura (dos straight_run) contaba bays por tramo y perdía studs.
    v66: tramos contiguos de una línea = UN run aunque el agente ponga straight_run distintos; un hueco los separa."""
    junto = K.calcular(_solo([_par("E1", 26.0, 2.0, "x", line="E"), _par("E2", 24.0, 4.5, "y", line="E", frm=26.0)]))
    assert abs(junto["familias"]["6\" parapet stud"] - _bays(50.0, (26 * 2.0 + 24 * 4.5) / 50)) < 0.05
    sep = K.calcular(_solo([_par("E1", 26.0, 2.0, line="E"), _par("E2", 24.0, 4.5, line="E", frm=30.0)]))
    assert abs(sep["familias"]["6\" parapet stud"] - (_bays(26.0, 2.0) + _bays(24.0, 4.5))) < 0.05
    sin = _par("X", 10.0, 2.0)
    del sin["line"]
    _falla(_solo([sin]), "parapet sin line")
    ext = _par("X", 10.0, 2.0)
    ext["length_basis"] = "outer_face"                  # #15B: largos a la cara exterior
    _falla(_solo([ext]), "length_basis")
    w = _par("X", 10.0, 2.0)
    w.pop("element")
    w["detail"] = "C/A09.21"
    _falla(_solo([w], nodes=[{"id": "a", "kind": "free", "wall": "X"}, {"id": "b", "kind": "free", "wall": "X"}]),
           "parapet fuera de element parapet")


def test_hanger_wire_lf_ref_v4():
    """Waiting 104 (ref v4): 6 carrying x 30 ft, 9 hangers c/u = 54 x drop <n> = <n> LF. #12A/#12B: 121/126 PCS."""
    d = base()
    d["ceilings"] = [{"room": "104", "system": "furring", "detail_none_reason": "sintético", "area_sf": 525.0, "span_ft": 30.0, "run_ft": 17.5,
                      "perimeter_ft": 95.0, "hanger_drop_ft": {"value": 4.5, "source": "S2.20; A04.01"},
                      "source": "A04.01"}]
    o = K.calcular(d)
    f = o["familias"]
    assert abs(f["hanger wire"] - 243.0) < 0.01, f["hanger wire"]
    # v64 (decisión usuario #4): PCS + altura por room; el LF es derivado
    hp = o["hanger_pcs"]
    assert hp["total_pcs"] == 54 and hp["por_room"][0]["altura_ft"] == 4.5 and hp["lf_derivado"] == 243.0, hp
    assert abs(f["carrying channel"] - 180.0) < 0.01 and abs(f["furring channel"] - 420.0) < 0.05, f
    del d["ceilings"][0]["hanger_drop_ft"]
    _falla(d, "hanger_drop_ft")


def test_ceiling_poligono_cuerda_media():
    """#12B 24 HR Vestibule 101: <n> x 15.77 pero área 152 (polígono). Rectángulo daba carrying 69.15."""
    d = base()
    d["ceilings"] = [{"room": "101", "system": "furring", "detail_none_reason": "sintético", "area_sf": 160.0, "span_ft": 14.0, "run_ft": 16.0,
                      "perimeter_ft": 50.0, "hanger_drop_ft": {"value": 5.375, "source": "S2.20"},
                      "source": "A04.01"}]
    f = K.calcular(d)["familias"]
    assert abs(f["carrying channel"] - 5 * 160.0 / 16.0) < 0.01, f["carrying channel"]
    assert f["carrying channel"] < 5 * 14.0 - 15


def test_soffit_no_es_furring_ni_suspendido():
    """#12A CSR soffit como furring (+<n>); #12B CSR stud_joist con carrying (+24.02)."""
    for sysm in ("furring", "stud_joist"):
        d = base()
        d["ceilings"].append({"room": "116 CSR soffit bottom", "system": sysm, "system_callout": {"detail": "9/Z9.33", "on_plan": True, "source": "sintético"}, "area_sf": 41.0, "span_ft": 12.0,
                              "run_ft": 3.42, "perimeter_ft": 30.0,
                              "hanger_drop_ft": {"value": 7.0, "source": "S2.20"}, "source": "10/A09.33", "detail": "10/A09.33"})
        _falla(d, "un soffit es framed")
    d = base()
    f0 = K.calcular(d)["familias"]
    d["ceilings"].append({"room": "116 CSR soffit bottom", "system": "framed_soffit", "system_callout": {"detail": "9/Z9.33", "on_plan": True, "source": "sintético: bubble sobre este ceiling"}, "area_sf": 41.0,
                          "span_ft": 12.0, "run_ft": 3.42, "source": "10/A09.33",
                          "drop_lines": {"value": 1, "source": "10/A09.33"}})
    _falla(copy.deepcopy(d), "drop line")                  # v65: sin el drop wall declarado
    d["walls"].append({"id": "CSR-D", "tag": "CSR", "element": "ceiling_bulkhead", "faces_none_reason": "sintético (v70): el board no es objeto de este test", "stud_size": "3-5/8\"",
                       "oc_in": 16, "rows": 1, "length_ft": 12.0, "height_ft": 7.25, "source": "10/A09.33",
                       "soffit_of": "116 CSR soffit bottom", "openings": []})
    d["nodes"] += [{"id": "cs1", "kind": "free", "wall": "CSR-D"}, {"id": "cs2", "kind": "free", "wall": "CSR-D"}]
    f0 = K.calcular(d)["familias"]
    d2 = copy.deepcopy(d)
    d2["walls"].append(dict(d["walls"][-1], id="CSR-D2"))   # #14B: segundo lado (W y E) = 2 líneas -> falla
    d2["nodes"] += [{"id": "cs3", "kind": "free", "wall": "CSR-D2"}, {"id": "cs4", "kind": "free", "wall": "CSR-D2"}]
    _falla(d2, "drop line")
    f = K.calcular(d)["familias"]
    assert f["carrying channel"] == f0["carrying channel"] and f["hanger wire"] == f0["hanger wire"]
    assert f["furring channel"] == f0["furring channel"]
    assert f["5/8\" gyp board regular (walls + ceilings)"] == f0["5/8\" gyp board regular (walls + ceilings)"]


def test_canopy_joist_12a():
    """v61.1 (#12A) integrado: canopy soffit = joists 3-5/8 + FRT plywood, sin carrying / hangers / furring."""
    d = base()
    d["ceilings"] = [{"room": "N canopy soffit", "system": "canopy_joist", "system_callout": {"detail": "9/Z9.33", "on_plan": True, "source": "sintético: bubble sobre este ceiling"}, "area_sf": 100.0, "span_ft": 25.0,
                      "run_ft": 4.0, "source": "7/A09.26"}]
    d2 = base()
    d2["ceilings"] = []
    f, f0 = K.calcular(d)["familias"], K.calcular(d2)["familias"]
    assert f["carrying channel"] == 0 and f["hanger wire"] == 0 and f["furring channel"] == 0, f
    assert abs(f["3-5/8\" stud (todos los gauges)"] - f0["3-5/8\" stud (todos los gauges)"] - 20 * 4.0) < 0.05
    assert abs(f["FRT plywood (SF)"] - f0["FRT plywood (SF)"] - 100.0) < 0.01


def test_orientacion_del_proyecto():
    """#12A 104 con span/run cruzados (furring 420 vs <n>). Con carrying_direction la orientación es fija."""
    d = base()
    d["constants"]["carrying_direction"] = {"value": "N-S", "source": "RFI-05"}
    _falla(d, "ns_ft y ew_ft")
    d["ceilings"] = [{"room": "104", "system": "furring", "detail_none_reason": "sintético", "area_sf": 525.0, "ns_ft": 30.0, "ew_ft": 17.5,
                      "perimeter_ft": 95.0, "hanger_drop_ft": {"value": 4.5, "source": "S2.20"},
                      "source": "A04.01"}]
    f = K.calcular(d)["familias"]
    assert abs(f["furring channel"] - 420.0) < 0.05 and abs(f["carrying channel"] - 180.0) < 0.01, f


def test_ceiling_perimeter_obligatorio():
    """#12B: 5 GWB ceilings sin ceiling_perimeter track (-194.3)."""
    d = base()
    del d["ceilings"][0]["perimeter_ft"]
    _falla(d, "perimeter_ft")
    d = base()
    d.setdefault("runs", []).append({"id": "CP-113", "element": "ceiling_perimeter", "orientation": "horizontal",
                                     "length_ft": 35.0, "source": "A04.01"})
    _falla(d, "lo genera canon.py")


def test_metal_trim_con_numero():
    """#12A/#12B dejaron metal trim PENDING/RFI. v62: trim_items + jamb returns x2 + transiciones x k."""
    d = base()
    del d["trim_items"]
    _falla(d, "trim_items ausente")
    d = base()
    d["walls"][0]["openings"][0].update(jamb_return=True, jamb_return_source="11/A09.27")
    d["walls"].append({"id": "TR104", "tag": "OTHER", "element": "ceiling_transition", "faces_none_reason": "sintético (v70): el board no es objeto de este test", "stud_size": "3-5/8\"",
                       "oc_in": 16, "rows": 1, "length_ft": 75.0, "height_ft": 4.5, "source": "7/A09.33", "edges": [{"edge": "W", "against": "ACT", "length_ft": 30.0, "source": "A04.01"}, {"edge": "N", "against": "ACT", "length_ft": 15.0, "source": "A04.01"}, {"edge": "E", "against": "ACT", "length_ft": 30.0, "source": "A04.01"}], 
                       "kickers": {"oc_in": 48, "length_ft": 1.5, "source": "7/A09.33",
                                   "length_printed_source": "7/A09.33 (test)"},
                       "vertical_studs": {"oc_in": 16, "height_ft": 4.5, "source": "7/A09.33", "bod_ft": {"value": 13.5, "source": "S2.20"}, "ceiling_ft": {"value": 9.0, "source": "A04.01"}}})
    d["nodes"] += [{"id": "t1", "kind": "free", "wall": "TR104"}, {"id": "t2", "kind": "free", "wall": "TR104"}]
    _falla(d, "transition_trim_per_lf")
    d["constants"]["transition_trim_per_lf"] = {"value": 2, "source": "7/A09.33"}
    o = K.calcular(d)
    # <n> + ventana 8.0 head + 2 x (8.5 - 6.5) jambs + 8.0 sill = 20 -> x 2 = 40 + <n> x 2
    assert abs(o["familias"]["metal trim (corner bead, casing, shadow molding)"] - (40.0 + 36 + 150.0)) < 0.01
    # kickers @48": ROUNDUP(75 / 4) + 1 = 20 x 1.5 = 30.0 LF a 3-5/8"
    assert any(r["familia"] == "kickers" and "30.0" in r["operacion"] for r in o["filas"]), o["filas"]


def test_storefront_en_g_rechazado():
    """#12B: office fronts modelados como storefront de 4 jambs x 2 rows dentro del G (59.7)."""
    d = base()
    d["walls"][2]["tag"] = "G"
    d["walls"][2]["openings"] = [{"ref": "office front 105", "kind": "storefront", "ro_w_ft": 7.5, "head_ft": 7.333,
                                  "source": "A11.01"}]
    d["opening_schedule"]["items"].append({"ref": "office front 105"})
    _falla(d, "storefront dentro de un wall G")


def test_opening_schedule_cerrado():
    """Header MAL 5 veces: #12A y #12B no declararon las storefront heads de line F / grid 2 (HSS de S2.20)
    ni los ductos; #12B dejó el 2.º box beam del grille. Ahora toda abertura barrida se declara una vez."""
    d = base()
    d["opening_schedule"]["items"].append({"ref": "N storefront (line F)"})
    _falla(d, "sin declarar")
    d["openings_extra"] = [{"ref": "N storefront (line F)", "kind": "storefront", "location": "exterior", "jamb_return": False,
                            "jamb_return_source": "2/A09.26",
                            "ro_w_ft": 41.6, "header": "steel_by_others",
                            "header_source": "S2.20 HSS9x5x5/8 (LLV); 2/A09.26", "source": "A09.01"}]
    f = K.calcular(d)["familias"]
    assert abs(f["header / box beam"] - 33.33) < 0.01, f       # steel by others: fuera del header LF
    d = base()
    d["opening_schedule"]["sources"] = ["A00.30", "A09.02"]
    _falla(d, "plan estructural")
    d = base()
    del d["opening_schedule"]
    _falla(d, "opening_schedule ausente")


def test_track_lines_por_wall_12b():
    """Canopy soffit: track en los dos extremos (decisión usuario #13) = fascia + wall. v70: el canopy soffit va en
    runs (en walls duplicaba los canopy joists -> ValueError)."""
    d = base()
    d["constants"]["canopy_soffit_track_lines"] = {"value": 2, "source": "decisión usuario #13"}
    cs = {"id": "CS", "tag": "OTHER", "element": "canopy_soffit", "stud_size": "3-5/8\" canopy",
          "oc_in": 16, "rows": 1, "length_ft": 20.0, "height_ft": 3.0, "openings": [],
          "source": "7/A09.26", "facade": "N", "wall_line_ft": {"value": 18.0, "source": "A04.01"}}
    mal = copy.deepcopy(d)
    mal["walls"].append(dict(cs))
    _falla(mal, "canopy_soffit en walls")
    d.setdefault("runs", []).append(dict(cs, orientation="horizontal"))
    sin = K.calcular(base())["familias"]["track de ceilings / soffits"]
    con = K.calcular(d)["familias"]["track de ceilings / soffits"]
    assert abs(con - sin - (20.0 + 18.0)) < 0.01, (sin, con)      # v66: fascia + wall, no 2 x L
    d["runs"][-1].pop("wall_line_ft")
    _falla(d, "wall_line_ft")


def test_jamb_wall_abertura_entre_walls_13a():
    """#13A: door 111 BOA muere entre el stub A1 y el wall A5; sin jamb_wall sus 4 jambs no se contaban."""
    d = base()
    d["openings_extra"] = [{"ref": "door 111", "kind": "door", "location": "interior", "ro_w_ft": 3.333, "qty": 1,
                            "with_sill": False, "source": "A00.30", "jamb_wall": "I1", "jamb_wall_source": "A02.01"}]
    d["opening_schedule"]["items"].append({"ref": "door 111"})
    _falla(copy.deepcopy(d), "sin head_ft")               # v65 (#14A): sin head no hay cripples ni track
    d["openings_extra"][0]["head_ft"] = 7.0
    b0 = K.calcular(base())["familias"]
    sin = b0["3-5/8\" stud (todos los gauges)"]
    f = K.calcular(d)["familias"]
    con = f["3-5/8\" stud (todos los gauges)"]
    # 4 jambs x <n> + cripples FLOOR(3.333/1.333) = 2 x (<n> - 7.0)
    assert abs(con - sin - (4 * 15.25 + 2 * 8.25)) < 0.01, (sin, con)
    assert abs(f["bottom track (todos)"] - b0["bottom track (todos)"] - 3.333) < 0.01
    assert abs(f["top / deflection track (todos)"] - b0["top / deflection track (todos)"] - 3.333) < 0.01
    d2 = copy.deepcopy(d)
    del d2["openings_extra"][0]["jamb_wall_source"]
    _falla(d2, "jamb_wall_source")
    d3 = copy.deepcopy(d)
    d3["openings_extra"][0]["jamb_wall"] = "NOPE"
    _falla(d3, "jamb_wall NOPE no existe")


def test_joist_dir_canopy_13b():
    """13B: canopy N (ns 4.0, ew 42.32) con carrying_direction N-S daba 4 joists x 42.32 = 169 LF (paralelos al muro);
    7/A09.26 los dibuja de muro a fascia: ROUNDUP(42.32/1.333)+1 = 33 x 4.0 = 132 LF."""
    d = base()
    d["constants"]["carrying_direction"] = {"value": "N-S", "source": "RFI-07"}
    d["ceilings"] = [{"room": "canopy soffit N", "system": "canopy_joist", "system_callout": {"detail": "9/Z9.33", "on_plan": True, "source": "sintético: bubble sobre este ceiling"}, "area_sf": 169.28, "ns_ft": 4.0, "ew_ft": 42.32,
                      "source": "3/A09.26"}]
    f0 = K.calcular(d)["familias"]
    d["ceilings"][0]["joist_dir"] = {"value": "N-S", "source": "7/A09.26"}
    f1 = K.calcular(d)["familias"]
    j0 = f0['3-5/8" stud (todos los gauges)']; j1 = f1['3-5/8" stud (todos los gauges)']
    assert abs((j0 - j1) - (4 * 42.32 - 33 * 4.0)) < 0.05, (j0, j1)
    d["ceilings"][0]["joist_dir"] = {"value": "N-S"}
    _falla(d, "joist_dir")


def test_v63_canopy_facade_glass_mat_13a():
    """#13A: fascia oeste (15/A09.27) en una facade con has_canopy false -> glass mat sin banda (-111.7 SF).
    v63: todo canopy_soffit / fascia_box declara facade y esa facade debe llevar banda."""
    d = base()
    d["facades"].append({"id": "W", "base_strip_lf": 20.0, "solid_lf": 20.0, "height_nailbase_ft": 16.75,
                         "openings_sf": 0, "has_canopy": False, "source": "A09.01"})
    d["walls"].append({"id": "FAS-W", "tag": "OTHER", "element": "fascia_box", "stud_size": "3-5/8\" canopy",
                       "oc_in": 16, "rows": 1, "length_ft": 20.0, "height_ft": 1.75, "openings": [],
                       "source": "15/A09.27", "facade": "W", "height_source": "7/A09.26"})
    d["nodes"] += [{"id": "w1", "kind": "free", "wall": "FAS-W"}, {"id": "w2", "kind": "free", "wall": "FAS-W"}]
    _falla(d, "facade W: tiene fascia_box FAS-W pero has_canopy false")
    d["facades"][-1]["has_canopy"] = True
    d["canopies"].append({"id": "C-W", "facade": "W", "band_lf": 20.0, "source": "15/A09.27"})
    g0 = K.calcular(base())["familias"]["5/8\" glass mat sheathing"]
    g1 = K.calcular(d)["familias"]["5/8\" glass mat sheathing"]
    assert abs(g1 - g0 - (20.0 * 0.5 + 20.0 * 2.0)) < 0.02, (g0, g1)
    d2 = base()
    del d2["walls"][3]["facade"]
    _falla(d2, "fascia_box sin facade")


def test_v63_canopy_soffit_track_lines_del_proyecto():
    """#13A cargó 1 línea de track en el canopy soffit y #13B 2 (default): 189.7 vs 377.6 LF."""
    d = base()
    d.setdefault("runs", []).append({"id": "CS", "tag": "OTHER", "element": "canopy_soffit", "orientation": "horizontal",
                                     "stud_size": "3-5/8\" canopy", "oc_in": 16, "rows": 1, "length_ft": 20.0,
                                     "height_ft": 3.0, "openings": [], "facade": "N", "source": "7/A09.26",
                                     "wall_line_ft": {"value": 18.0, "source": "A04.01"}})   # v70: runs, no walls
    _falla(d, "canopy_soffit_track_lines")
    d["constants"]["canopy_soffit_track_lines"] = {"value": 1, "source": "7/A09.26"}
    _falla(d, "decisión usuario #13")                  # v64: 1 línea ya no es opción
    d["constants"]["canopy_soffit_track_lines"] = {"value": 2, "source": "decisión usuario #13"}
    K.calcular(d)


def test_v63_fascia_sheathing_con_tool():
    """#13A (<n>) y #13B (<n>) sumaron el sheathing de fascia como plywood_strip a mano."""
    d = base()
    d["plywood_strips"].append({"ref": "canopy fascia ext grade FRT plywood", "lf": 30.0, "width_ft": 1.75,
                                "source": "7/A09.26", "material": "frt_5_8_ext"})
    _falla(d, "el sheathing de fascia_box lo genera canon.py")
    d2 = base()
    del d2["walls"][3]["height_source"]
    _falla(d2, "fascia_box sin height_source")


def test_v63_cement_board_obligatorio_13a():
    """#13A: cement board FALTA (canon.py no lo pedía); #13B lo sumó a mano (<n>)."""
    d = base()
    del d["tile_base"]
    _falla(d, "tile_base")
    d["tile_base_none_reason"] = "sin tile base en el finish schedule"
    _falla(copy.deepcopy(d), "sin tile_base")              # v65: el FRP usa el perímetro del tile_base
    del d["frp"]
    d["frp_none_reason"] = "sin FRP"
    assert K.calcular(d)["familias"]["cement board"] == 0.0
    assert "cement board" in K.OBLIGATORIAS


def test_v63_inventario_corre_dentro_de_canon():
    """Con plan_scale_pt_per_ft el inventario es parte de canon.py: un wall sin banda lo rechaza."""
    d = base()
    d["constants"]["plan_scale_pt_per_ft"] = {"value": 18, "source": "A02.01"}
    _falla(d, "falta band")
    out = K.calcular(base())
    assert any("SIN INVENTARIO" in a for a in out["avisos"])



def test_v64_header_por_piezas_desde_canon():
    """Decisión usuario #2: canon pasa header_schedule + pieces. Sin pieces en un box -> error; LF de línea 9.33 no."""
    d = base()
    assert abs(K.calcular(d)["familias"]["header / box beam"] - 9.33) > 9
    del d["walls"][0]["openings"][0]["pieces"]
    _falla(d, "pieces")
    d = base()
    d["walls"][2]["openings"] = [{"ref": "door 113", "kind": "door", "ro_w_ft": 3.0, "head_ft": 7.333,
                                  "source": "A00.30"}]
    d["opening_schedule"]["items"].append({"ref": "door 113"})
    o = K.calcular(d)
    assert abs(o["familias"]["header / box beam"] - (33.33 + 4.333)) < 0.02, o["familias"]["header / box beam"]
    assert abs(o["header_por_pieza"]["track"] - 4.333) < 0.01, o["header_por_pieza"]


def test_v64_ductos_y_storefront_hss_cero():
    """Decisiones usuario #12 y #16: ductos / FD sin header ni sill; storefront con HSS = 0 metal stud header."""
    d = base()
    d["opening_schedule"]["items"] += [{"ref": "FD-1"}, {"ref": "N storefront"}]
    d["openings_extra"] = [{"ref": "FD-1", "kind": "fire_damper", "ro_w_ft": 1.333, "qty": 4, "with_sill": True,
                            "source": "M01.01"},
                           {"ref": "N storefront", "kind": "storefront", "location": "exterior", "ro_w_ft": 41.6,
                            "structure": "HSS", "structure_source": "S2.20", "source": "2/A09.26",
                            "jamb_return": False, "jamb_return_source": "2/A09.26"}]
    f = K.calcular(d)["familias"]
    assert abs(f["header / box beam"] - 33.33) < 0.01 and abs(f["sill track"] - 16.67) < 0.01, f


def test_v64_kickers_con_studs_verticales():
    """Decisión usuario #7 (7/A09.33): además del kicker, los studs verticales (dashed) a estructura."""
    d = base()
    d["constants"]["transition_trim_per_lf"] = {"value": 2, "source": "7/A09.33"}
    tr = {"id": "TR104", "tag": "OTHER", "element": "ceiling_transition", "faces_none_reason": "sintético (v70): el board no es objeto de este test", "stud_size": "3-5/8\"", "oc_in": 16,
          "rows": 1, "length_ft": 75.0, "height_ft": 4.5, "source": "7/A09.33", "edges": [{"edge": "W", "against": "ACT", "length_ft": 30.0, "source": "A04.01"}, {"edge": "N", "against": "ACT", "length_ft": 15.0, "source": "A04.01"}, {"edge": "E", "against": "ACT", "length_ft": 30.0, "source": "A04.01"}], 
          "kickers": {"oc_in": 48, "length_ft": 1.5, "source": "7/A09.33", "length_printed_source": "test"}}
    d["walls"].append(tr)
    d["nodes"] += [{"id": "t1", "kind": "free", "wall": "TR104"}, {"id": "t2", "kind": "free", "wall": "TR104"}]
    _falla(d, "vertical_studs")
    tr["vertical_studs"] = {"oc_in": 16, "height_ft": 4.5, "source": "7/A09.33", "bod_ft": {"value": 13.5, "source": "S2.20"}, "ceiling_ft": {"value": 9.0, "source": "A04.01"}}
    o = K.calcular(d)
    # ROUNDUP(<n> / 1.333) + 1 = 59 x <n> = <n> (BOA +<n>)
    v = [r for r in o["filas"] if r["familia"] == "vertical studs @ transition"]
    assert len(v) == 1 and "58 studs x 4.5 = 261.0" in v[0]["operacion"], v


def test_v64_waiting_104_furring_no_joists():
    """Decisión usuario #14: suspended del RCP = furring; stud_joist solo con detalle que dibuje joists."""
    d = base()
    del d["ceilings"][1]["joist_source"]
    _falla(d, "joist_source")
    d["ceilings"][1]["system"] = "furring"
    f = K.calcular(d)["familias"]
    assert f["furring channel"] > 66.5 + 400, f["furring channel"]


# ---------------- v65 (arbitraje #14A / #14B, 17-oct-2026) ----------------

def _tr(h=4.5, **k):
    w = {"id": "TR104", "tag": "OTHER", "element": "ceiling_transition", "faces_none_reason": "sintético (v70): el board no es objeto de este test", "stud_size": "3-5/8\"", "oc_in": 16,
         "rows": 1, "length_ft": 75.0, "height_ft": h, "source": "7/A09.33", "edges": [{"edge": "W", "against": "ACT", "length_ft": 30.0, "source": "A04.01"}, {"edge": "N", "against": "ACT", "length_ft": 15.0, "source": "A04.01"}, {"edge": "E", "against": "ACT", "length_ft": 30.0, "source": "A04.01"}], 
         "kickers": dict({"oc_in": 48, "angle_deg": 45, "source": "7/A09.33"}, **k),
         "vertical_studs": {"oc_in": 16, "height_ft": 4.5, "source": "7/A09.33", "bod_ft": {"value": 13.5, "source": "S2.20"}, "ceiling_ft": {"value": 9.0, "source": "A04.01"}}}
    return w


def test_v65_transicion_sin_studs_nodos_14a_14b():
    """#14A: TR-104 de <n> ft pasaba por studs_nodos (258.12) ADEMÁS de vertical_studs (258.12) = doble.
    #14B: height_ft 1.0 inventado (59 LF fantasma). Kicker sin largo impreso = <n> / sin 45 = <n> (ref <n>)."""
    d = base()
    d["constants"]["transition_trim_per_lf"] = {"value": 2, "source": "7/A09.33"}
    s0 = K.calcular(d)["familias"]["3-5/8\" stud (todos los gauges)"]
    d["walls"].append(_tr())
    d["nodes"] += [{"id": "t1", "kind": "free", "wall": "TR104"}, {"id": "t2", "kind": "free", "wall": "TR104"}]
    o = K.calcular(d)
    s1 = o["familias"]["3-5/8\" stud (todos los gauges)"]
    esperado = 20 * 4.5 / math.sin(math.radians(45)) + 58 * 4.5      # 129.93 + <n>
    assert abs(s1 - s0 - esperado) < 0.05, (s1 - s0, esperado)          # #14A daba +258.12 más
    malo = copy.deepcopy(d)
    malo["walls"][-1]["height_ft"] = 1.0                                # #14B
    _falla(malo, "!= vertical_studs.height_ft")
    malo = copy.deepcopy(d)
    malo["walls"][-1]["kickers"]["length_ft"] = 5.5                    # largo a mano sin cota
    _falla(malo, "length_printed_source")


def test_v65_column_wrap_por_face():
    """5/A09.25: 4 faces x <n> -> 8 studs por wrap (A y B 5 con studs_nodos: 52.5 en vez de 84)."""
    d = base()
    s0 = K.calcular(d)["familias"]["3-5/8\" stud (todos los gauges)"]
    cw = {"id": "CW-1", "tag": "CANOPY-COL", "element": "column_wrap", "stud_size": "3-5/8\"", "oc_in": 16,
          "rows": 1, "length_ft": 5.0, "height_ft": 10.5, "source": "5/A09.25"}
    d["walls"].append(cw)
    d["nodes"] += [{"id": "w1", "kind": "free", "wall": "CW-1"}, {"id": "w2", "kind": "free", "wall": "CW-1"}]
    _falla(copy.deepcopy(d), "faces_ft ni studs_drawn")
    cw["faces_ft"] = [1.25, 1.25, 1.25, 1.25]
    f = K.calcular(d)["familias"]
    assert abs(f["3-5/8\" stud (todos los gauges)"] - s0 - 84.0) < 0.01
    d2 = copy.deepcopy(d)                                  # #14B: abut de un wall contra la caja (column_wrap)
    d2["nodes"] = [n for n in d2["nodes"] if n["id"] != "e"] + [{"id": "e", "kind": "abut", "wall": "I1", "into": "CW-1",
                                                                  "source": "6/A12.01"}]
    assert K.calcular(d2)["familias"]["3-5/8\" stud (todos los gauges)"] == f["3-5/8\" stud (todos los gauges)"]
    cw.pop("faces_ft")
    cw["studs_drawn"] = {"value": 10, "source": "3/A08.21"}
    f = K.calcular(d)["familias"]
    assert abs(f["3-5/8\" stud (todos los gauges)"] - s0 - 105.0) < 0.01


def test_v65_roof_step_filas_dibujadas():
    """4/A02.02 dibuja 3 filas de studs; #14A cargó 2 (RS-1, RS-2 de 2.323) = −122.3 LF."""
    d = base()
    for i, h in enumerate((2.323, 2.323)):
        d["walls"].append({"id": f"RS-{i}", "tag": "RS", "element": "roof_step", "faces_none_reason": "sintético (v70): el board no es objeto de este test", "stud_size": "3-5/8\"", "oc_in": 16,
                           "rows": 1, "length_ft": 51.73, "height_ft": h, "source": "4/A02.02"})
        d["nodes"] += [{"id": f"r{i}a", "kind": "free", "wall": f"RS-{i}"}, {"id": f"r{i}b", "kind": "free", "wall": f"RS-{i}"}]
    _falla(copy.deepcopy(d), "roof_step_rows_drawn")
    d["constants"]["roof_step_rows_drawn"] = {"value": 3, "source": "4/A02.02"}
    _falla(copy.deepcopy(d), "2 walls declarados")
    d["walls"].append(dict(d["walls"][-1], id="RS-2", height_ft=1.15))
    d["nodes"] += [{"id": "r2a", "kind": "free", "wall": "RS-2"}, {"id": "r2b", "kind": "free", "wall": "RS-2"}]
    K.calcular(d)


def test_v65_fascia_box_obligatoria_con_canopy_joist():
    """#14A no declaró fascia_box (−348.8 LF 3-5/8" de los studs de fascia)."""
    d = base()
    d["ceilings"].append({"room": "N canopy soffit", "system": "canopy_joist", "system_callout": {"detail": "9/Z9.33", "on_plan": True, "source": "sintético: bubble sobre este ceiling"}, "area_sf": 100.0, "ns_ft": 4.0,
                          "ew_ft": 25.0, "span_ft": 25.0, "run_ft": 4.0, "source": "7/A09.26", "facade": "N"})
    K.calcular(d)                                        # base tiene FAS (fascia_box, facade N)
    sin = copy.deepcopy(d)
    sin["walls"] = [w for w in sin["walls"] if w["id"] != "FAS"]
    sin["nodes"] = [n for n in sin["nodes"] if n.get("wall") != "FAS"]
    _falla(copy.deepcopy(sin), "sin fascia_box")
    run = [w for w in d["walls"] if w["id"] == "FAS"][0]
    sin["runs"] = [{k: v for k, v in run.items() if k not in ("stud_size", "oc_in", "rows", "openings")}]
    _falla(sin, "fascia_box en runs")                      # #14A: FB-* como runs = sin studs


def test_v65_box_header_as_needed_exige_vestibule_head():
    """#14B declaró el box header del vestibule pero no los studs sobre el storefront (−<n> LF)."""
    d = base()
    d["openings_extra"] = [{"ref": "vestibule S", "kind": "opening", "location": "interior", "ro_w_ft": 15.646,
                            "header_type": "BOX HEADER AS NEEDED", "header_type_source": "7/A12.10", "pieces": 4,
                            "pieces_source": "7/A12.10", "source": "1/A12.10"}]
    d["opening_schedule"]["items"].append({"ref": "vestibule S"})
    _falla(copy.deepcopy(d), "framing_wall")
    d["walls"].append({"id": "VH-S", "tag": "VH", "element": "vestibule_head", "faces_none_reason": "sintético (v70): el board no es objeto de este test", "stud_size": "3-5/8\"", "oc_in": 16,
                       "rows": 1, "length_ft": 15.646, "height_ft": 5.375, "source": "4/A12.10"})
    d["nodes"] += [{"id": "v1", "kind": "free", "wall": "VH-S"}, {"id": "v2", "kind": "free", "wall": "VH-S"}]
    d["openings_extra"][0]["framing_wall"] = "VH-S"
    K.calcular(d)


def test_v65b_header_y_sill_son_reglas():
    """Decisiones usuario #18-#22 (17-oct-2026): header_params ya no existe; GL-2 'OR STEEL' no es steel by others;
    box de 2 piezas = error; office front CONT. BOX BEAM = un run por frente (continuous_run pasa a headers.py)."""
    d = base()
    _falla(dict(copy.deepcopy(d), header_params={}), "header_params")
    _falla(dict(copy.deepcopy(d), header_params={"box_pieces": 2}), "header_params")
    d2 = copy.deepcopy(d)
    d2["walls"][0]["openings"][0]["pieces"] = 2
    _falla(d2, "#20")
    d3 = copy.deepcopy(d)
    d3["walls"][0]["openings"][0].update(header="steel_by_others", header_source="11/A09.27", or_steel=True)
    _falla(d3, "#19")
    d4 = copy.deepcopy(d)
    of = {"ref": "office front E", "wall": "OF-E", "kind": "opening", "ro_w_ft": 7.5, "qty": 4,
          "header_type": "CONT. BOX BEAM", "header_type_source": "8/A12.01", "pieces": 4,
          "pieces_source": "8/A12.01", "source": "A02.01"}
    d4["openings_extra"] = [of]
    d4["opening_schedule"]["items"].append({"ref": "office front E"})
    _falla(copy.deepcopy(d4), "#22")
    of.update(qty=1, ro_w_ft=36.5, continuous_run=True)
    f = K.calcular(d4)["familias"]
    assert abs(f["header / box beam"] - (33.33 + (36.5 + 16 / 12) * 4)) < 0.02, f["header / box beam"]


def test_v65_T_entre_G_es_abut():
    """#14A: T del G largo contra el stub del office front (que ya tiene vendor_end) = +1/row doble (<n> LF)."""
    d = base()
    d["walls"] += [{"id": "G-44", "tag": "G", "stud_size": "1-5/8\"", "oc_in": 16, "rows": 2, "length_ft": 11.5,
                    "height_ft": 15.25, "source": "A02.01"},
                   {"id": "GS-45", "tag": "G", "stud_size": "1-5/8\"", "oc_in": 16, "rows": 2, "length_ft": 3.25,
                    "height_ft": 15.25, "source": "A02.01"}]
    d["nodes"] += [{"id": "ga", "kind": "T", "branch": "G-44", "through": "GS-45"},
                   {"id": "gb", "kind": "free", "wall": "G-44"},
                   {"id": "s1", "kind": "vendor_end", "wall": "GS-45"}, {"id": "s2", "kind": "vendor_end", "wall": "GS-45"}]
    _falla(copy.deepcopy(d), "-> abut")
    d["nodes"][-4] = {"id": "ga", "kind": "abut", "wall": "G-44", "into": "GS-45", "source": "10/A12.01"}
    K.calcular(d)


def test_v65_ballistic_contorno_una_lectura():
    """E5: A1K N <n> + S <n> + SW <n> (1.74 + jog 0.61) + B2K <n> = <n> -> <n> SF.
    #14A: SW 1.16 + <n> (9.837 = 78.70); #14B: N/S 2.98 en vez de <n> (9.98 = 79.84)."""
    def k(lens):
        d = base()
        d["details"]["4/A12.01"] = {"layers_per_face": 1, "k_panel": {"panel_to_ft": 8.0},
                                    "sealant": {"bottom_faces": 2, "top_faces": 2, "source": "4/A12.01"}}
        for i, L in enumerate(lens):
            d["walls"].append({"id": f"K{i}", "tag": "A1K", "stud_size": "3-5/8\"", "oc_in": 24, "rows": 1,
                               "length_ft": L, "height_ft": 12.92, "detail": "4/A12.01", "source": "A02.01",
                               "length_source": "A02.01 vector (sintético)",
                               "faces": [{"room": "c", "board": "5/8 regular", "layers": 1, "height_ft": 12.92,
                                          "k_customer": True}]})
            d["nodes"] += [{"id": f"k{i}a", "kind": "free", "wall": f"K{i}"}, {"id": f"k{i}b", "kind": "free", "wall": f"K{i}"}]
        d["ballistic_jogs_none_reason"] = "sintético: contorno sin jogs"
        return d
    d = k([3.5, 3.5, 1.25, 0.5, 1.25])
    _falla(copy.deepcopy(d), "ballistic_contour_ft")
    d["constants"]["ballistic_contour_ft"] = {"value": 9.5, "source": "A02.01"}
    _falla(d, "!= ballistic_contour_ft")
    d = k([3.5, 3.5, 1.75, 1.25])
    d["constants"]["ballistic_contour_ft"] = {"value": 10.0, "source": "A02.01"}
    assert abs(K.calcular(d)["familias"]["ballistic panel"] - 80.0) < 0.01


def test_v65_banda_glass_mat_t_stud_b_stud():
    """#14A: banda 2.167 = T/CANOPY - B/CANOPY de la elevación; 7/A09.26 T/STUD <n> - B/STUD <n> = <n>."""
    d = base()
    d["band"] = {"height_ft": {"value": 2.167, "source": "A09.01 T/CANOPY - B/CANOPY"}}
    _falla(copy.deepcopy(d), "t_stud_ft")
    d["band"] = {"t_stud_ft": {"value": 12.75, "source": "7/A09.26"},
                 "b_stud_ft": {"value": 10.875, "source": "7/A09.26"}}
    f = K.calcular(d)["familias"]
    assert abs(f["5/8\" glass mat sheathing"] - (13.8335 + 27.667 * 1.875)) < 0.01


def test_v65_frp_bloque_obligatorio():
    """#14B FALTA FRP; #14A 357.90 (sin door 112, mop sink 2.5 ft). arb9: (<n> - <n>) x 5.0 + 2 x 2 x 4 = <n>."""
    d = base()
    del d["frp"]
    _falla(copy.deepcopy(d), "frp_none_reason")
    d["tile_base"] = [{"room": "113", "perimeter_ft": 38.0, "perimeter_basis": "gross",
                       "doors": [{"ref": "113", "ro_w_ft": 3.5}, {"ref": "112", "ro_w_ft": 3.5}],
                       "height_ft": {"value": 0.5, "source": "3/A08.01"}, "source": "1/A08.01"},
                      {"room": "114", "perimeter_ft": 34.0, "perimeter_basis": "net", "doors": [{"ref": "114", "ro_w_ft": 3.0}],
                       "gross_ft": {"value": 37.0, "source": "1/A08.01"},
                       "height_ft": {"value": 0.5, "source": "3/A08.01"}, "source": "1/A08.01"}]
    d["frp"] = {"top_ft": {"value": 5.0, "source": "A-D/A08.01"}, "rooms": ["113", "114"],
                "mop_sink": {"sides": 2, "width_ft": 2.0, "height_ft": 4.0, "source": "4/A08.01; P00.01"}}
    # perímetro NETO del tile_base (doors ya fuera, 59.10) x 5.0 + mop sink 2 x 2.0 x 4.0
    assert abs(K.calcular(d)["familias"]["FRP"] - ((31.0 + 34.0) * 5.0 + 16.0)) < 0.02
    sin = copy.deepcopy(d)
    del sin["tile_base"][0]["doors"]
    _falla(sin, "declarar doors")
    sin = copy.deepcopy(d)                                   # v68: #16A neto sin door 112 / #16B bruto sin descontar
    del sin["tile_base"][0]["perimeter_basis"]
    _falla(sin, "perimeter_basis")
    sin = copy.deepcopy(d)                                   # v68: "net" que es el bruto (#16A) = error
    sin["tile_base"][1]["perimeter_ft"] = 37.0
    _falla(sin, "net 37.0 != gross")
    sin = copy.deepcopy(d)
    del sin["tile_base"][1]["gross_ft"]
    _falla(sin, "gross_ft")


def test_v65_sealant_por_detalle():
    """5/A12.01 G: bead solo ABAJO en las dos faces (#14A lo cargó arriba: mismo LF pero otra regla); doors se
    descuentan de la corrida de abajo (55.5); un detalle sin sealant declarado falla (#14B sin sealant)."""
    d = base()
    del d["details"]["3/A12.01"]["sealant"]
    _falla(copy.deepcopy(d), "sealant {bottom_faces")
    d = base()
    d["walls"][2]["openings"] = [{"ref": "door 120", "kind": "door", "ro_w_ft": 3.333, "head_ft": 7.0,
                                  "source": "A00.30"}]
    d["opening_schedule"]["items"].append({"ref": "door 120"})
    d["sealant_items"] = [{"ref": "office bulkhead top 9/A12.01", "lf": 45.0, "faces": 2, "source": "9/A12.01"}]
    d["sealant_base_exterior"] = {"lf": 26.0, "source": "C/A09.21"}
    d["walls"].append({"id": "DB-1", "tag": "G", "element": "door_bulkhead", "stud_size": "1-5/8\"", "oc_in": 16,
                       "rows": 2, "length_ft": 7.5, "height_ft": 7.333, "detail": "3/A12.01", "source": "8/A12.01",
                       "faces": [{"room": "105", "board": "5/8 regular", "layers": 1, "height_ft": 7.333}]})
    d["nodes"] += [{"id": "db1", "kind": "free", "wall": "DB-1"}, {"id": "db2", "kind": "free", "wall": "DB-1"}]
    f = K.calcular(d)["familias"]
    # el bulkhead no hereda el bead del tipo (sus beads 8, 9/A12.01 van en sealant_items)
    assert abs(f["acoustical sealant"] - ((10.0 * 2 - 3.333 * 2) + 90.0 + 26.0)) < 0.01, f["acoustical sealant"]


def test_v65_insulation_excluida_y_level5():
    d = base()
    d["insulation_items"] = [{"ref": "batt", "sf": 100}]
    _falla(d, "EXCLUDED")
    d = base()
    d["level5_items"] = [{"ref": "WC-18 office 108", "wc_tag": "WC-18", "l_ft": 10.0, "h_ft": 9.0,
                          "base_ft": {"value": 0.5, "source": "A05.01 kn 12"}, "source": "A11.04"}]
    _falla(copy.deepcopy(d), "level5_tags")                     # v67: tags del finish schedule obligatorios
    d["constants"]["level5_tags"] = {"value": ["WC-18"], "source": "A00.40"}
    o = K.calcular(d)
    assert abs(o["familias"]["Level 5 finish"] - 85.0) < 0.01   # v67: L x (h - base)
    assert any("insulation: EXCLUDED" in a for a in o["avisos"])
    assert "EXCLUDED" in o["excluidas"]["batt insulation"]


def test_v67_accesorios_y_types_en_familias_out():
    d = base()
    o = K.calcular(d)
    import accesorios as A
    assert set(A.FAMS) <= set(o["familias"]) and set(A.FAMS) <= set(o["obligatorias"])
    assert set(o["accesorios"]["nombres_excel"]) == set(A.FAMS)
    assert "types" in o["partition_types"] and "EXT-6CFMF" in o["partition_types"]["types"]
    gh = {"id": "GH", "tag": "GR", "element": "grille_head", "faces_none_reason": "sintético (v70): el board no es objeto de este test", "stud_size": "2-1/2\"", "oc_in": 16, "rows": 1,
          "length_ft": 8.0, "height_ft": 2.0, "source": "4/A08.21", "openings": [],
          "head_build": {"head_ft": 2.0, "head_chain_in": [6, 18], "box_depth_ft": 0.5, "n_box": 2,
                         "board_in": 0.625, "source": "4/A08.21"}}
    d["walls"].append(gh)
    d["nodes"] += [{"id": "gh1", "kind": "free", "wall": "GH"}, {"id": "gh2", "kind": "free", "wall": "GH"}]
    o = K.calcular(d)
    assert o["familias"]["2-1/2\" stud"] == 0                  # grille fuera de studs_nodos (sin doble conteo)
    n = math.ceil(8.0 / (16 / 12)) + 1
    assert abs(o["familias"]["2-1/2\" CFMF coiling grille head"] - n * (2.0 - 1.0 - 0.625 / 12)) < 0.01


def test_v67_framing_screws_pcs_explicitos():
    d = _solo([_par("A", 18.0, 4.0)])
    o = K.calcular(d)
    fila = [r for r in o["filas"] if r["familia"] == "6\" parapet stud"][0]
    assert fila["pcs"] == 4 * 5                                   # 4 bays x 5 studs
    assert o["familias"]["framing screws"] == 4 * fila["pcs"], o["familias"]["framing screws"]


def test_v67_canopy_column_cadena_fos_completa():
    d = base()
    cw = {"id": "CW-1", "tag": "CANOPY-COL", "element": "column_wrap", "stud_size": "3-5/8\"", "oc_in": 16,
          "rows": 1, "length_ft": 4.0, "height_ft": 10.0, "source": "5/A09.25", "faces_ft": [1.0] * 4,
          "fos_chain": {"value": [1.0, 0.25], "source": "5/A09.25"}}
    d["walls"].append(cw)
    d["nodes"] += [{"id": "w1", "kind": "free", "wall": "CW-1"}, {"id": "w2", "kind": "free", "wall": "CW-1"}]
    _falla(copy.deepcopy(d), "cadena FOS")                      # primer eslabón solo = error
    cw.update(faces_ft=[1.25] * 4, length_ft=5.0)
    K.calcular(d)


def test_v67_canopy_wall_line_igual_a_fascia_avisa():
    d = base()
    d.setdefault("runs", []).append({"id": "CS", "element": "canopy_soffit", "orientation": "horizontal",
                                     "length_ft": 27.667, "facade": "N", "source": "7/A09.26",
                                     "wall_line_ft": {"value": 27.667, "source": "A04.01"}})
    d["constants"]["canopy_soffit_track_lines"] = {"value": 2, "source": "7/A09.26"}
    o = K.calcular(copy.deepcopy(d))
    assert any("CS: canopy_soffit wall_line_ft = length_ft" in a for a in o["avisos"]), o["avisos"]
    d["runs"][-1]["wall_line_ft"]["value"] = 25.0
    o = K.calcular(d)
    assert not any("wall_line_ft = length_ft" in a for a in o["avisos"])


def test_v67_trim_jamb_return_mismos_bordes():
    d = base()
    t0 = K.calcular(copy.deepcopy(d))["familias"]["metal trim (corner bead, casing, shadow molding)"]
    d["opening_schedule"]["items"].append({"ref": "SF-1"})
    d["openings_extra"] = [{"ref": "SF-1", "kind": "storefront", "location": "exterior", "ro_w_ft": 10.0,
                            "head_ft": 8.0, "header": "steel_by_others", "header_source": "S2.20 HSS",
                            "jamb_return": True, "jamb_return_source": "2/A09.26", "wall_jambs": 1,
                            "wall_jambs_source": "A02.01", "source": "A02.01",
                            "jambs": [{"abuts": "wall", "source": "A02.01"}, {"abuts": "pier", "source": "1/A09.25"}]}]
    o = K.calcular(d)
    t1 = o["familias"]["metal trim (corner bead, casing, shadow molding)"]
    assert abs((t1 - t0) - 2 * (10.0 + 1 * 8.0)) < 0.01, t1 - t0          # head + 1 jamb contra wall, x 2
    assert o["familias"]["gypsum board jamb return"] > 0


def test_v68_parapet_stub_de_un_bay_usa_formula():
    """v68 E3 exacta: el mínimo de 5 studs vale en los bays de un run dividido por posts (nb >= 2); un run de un
    solo bay (stub <= spacing de posts) usa 2 + ROUNDUP((L - 0.6)/oc) - 1 (números inventados)."""
    d = _solo([_par("A", 18.0, 4.0)])
    f = [r for r in K.calcular(copy.deepcopy(d))["filas"] if r["familia"] == "6\" parapet stud"][0]
    assert f["pcs"] == 4 * 5, f
    d = _solo([_par("B", 3.0, 4.0)])
    f = [r for r in K.calcular(copy.deepcopy(d))["filas"] if r["familia"] == "6\" parapet stud"][0]
    assert f["pcs"] == 2 + math.ceil((3.0 - 0.6) / (16 / 12)) - 1 == 3, f


if __name__ == "__main__":
    n = 0
    for k, f in list(globals().items()):
        if k.startswith("test_") and callable(f):
            f()
            n += 1
            print("OK", k)
    print(f"{n} tests OK")
