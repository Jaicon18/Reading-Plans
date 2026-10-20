#!/usr/bin/env python3
"""Tests sintéticos de accesorios.py (E24: sin cantidades de ningún proyecto real; números inventados)."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import accesorios as A  # noqa: E402

OK = []


def chk(nombre, cond, msg=""):
    if not cond:
        raise AssertionError(f"{nombre}: {msg}")
    OK.append(nombre)


def canon_base():
    return {
        "constants": {"plan_scale_pt_per_ft": {"value": 18.0, "source": "X1.01"}},
        "walls": [
            {"id": "W1", "tag": "P1", "element": "wall", "stud_size": "3-5/8\"", "oc_in": 16, "rows": 1,
             "length_ft": 20.0, "height_ft": 10.0,
             "openings": [{"ref": "win 1", "kind": "window", "ro_w_ft": 6.0, "head_ft": 7.0, "sill_ft": 3.0,
                           "with_sill": True, "jamb_return": True, "substrate_none_reason": "sintético (v76 R76.4)", "jamb_return_source": "9/X9.01", "jamb_return_label": "GYPSUM BOARD JAMB RETURN",
                           "sill_return": True, "sill_return_source": "9/X9.01", "sill_return_label": "GYPSUM BOARD RETURN"},
                          {"ref": "door 1", "kind": "door", "ro_w_ft": 3.0, "head_ft": 7.0, "sill_ft": 0}]},
            {"id": "W2", "tag": "P2", "element": "wall", "stud_size": "1-5/8\"", "oc_in": 16, "rows": 2,
             "length_ft": 10.0, "height_ft": 10.0, "openings": []},
            {"id": "X1", "tag": "EXT", "element": "wall", "stud_size": "6\"", "oc_in": 16, "rows": 1,
             "length_ft": 30.0, "height_ft": 12.0, "openings": []},
            {"id": "BH", "tag": "P2", "element": "door_bulkhead", "stud_size": "1-5/8\"", "rows": 2,
             "length_ft": 8.0, "height_ft": 2.0},
            {"id": "PA1", "tag": "PAR", "element": "parapet", "stud_size": "6\" parapet", "length_ft": 10.5,
             "height_ft": 3.0, "ori": "H", "axis": 0.0},
            {"id": "PA2", "tag": "PAR", "element": "parapet", "stud_size": "6\" parapet", "length_ft": 4.0,
             "height_ft": 3.0, "ori": "V", "axis": 10.5},
            {"id": "GH", "tag": "GR", "element": "grille_head", "stud_size": "2-1/2\"", "oc_in": 16, "rows": 1,
             "length_ft": 8.0, "height_ft": 2.0,
             "head_build": {"head_ft": 2.0, "head_chain_in": [6, 18], "box_depth_ft": 0.5, "n_box": 2,
                            "board_in": 0.625, "source": "4/X8.21"}},
        ],
        "openings_extra": [
            {"ref": "FD 10x10", "kind": "fire_damper", "ro_w_ft": 10 / 12, "qty": 2, "source": "M1.01"},
            {"ref": "box run", "kind": "opening", "ro_w_ft": 12.0, "qty": 1, "continuous_run": True},
            {"ref": "sf 1", "kind": "storefront", "ro_w_ft": 10.0, "head_ft": 8.0, "structure": "HSS",
             "jamb_return": True, "substrate_none_reason": "sintético (v76 R76.4)", "jamb_return_source": "2/X9.26", "jamb_return_label": "GYPSUM BOARD JAMB RETURN", "wall_jambs": 1,
             "wall_jambs_source": "X2.01", "jambs": [{"abuts": "wall", "source": "X2.01"},
                                                     {"abuts": "pier", "source": "1/X9.25"}]},
        ],
        "frp": {"top_ft": {"value": 4.0, "source": "A/X8.01"}, "rooms": ["R1"],
                "mop_sink": {"sides": 2, "width_ft": 2.0, "height_ft": 3.0, "source": "5/X8.01"}},
        "tile_base": [{"room": "R1", "perimeter_ft": 25.0, "height_ft": {"value": 0.5, "source": "X8.01"},
                       "doors": [{"ref": "d", "ro_w_ft": 3.0}], "source": "X2.01"}],
        "level5_items": [{"ref": "WC-9 wall", "wc_tag": "WC-9", "l_ft": 10.0, "h_ft": 9.0,
                          "base_ft": {"value": 0.5, "source": "X5.01 kn 3"}, "source": "X0.40"}],
        "access_panels": [{"ref": "AP 1", "qty": 1, "source": "X4.01 kn 2", "size": "2'x2'"}],
        "mep_sweep": {"sheets": ["P1.01", "M1.01"], "source": "P1.01; M1.01",
                      "registro": {"dx_pt": 10.0, "dy_pt": -4.0, "matches": 30, "source": "registro2 X2.01"}},
    }


def fam_base():
    return {"familias": {"5/8\" gyp board regular (walls + ceilings)": 900.0, "5/8\" gyp MOISTURE RESISTANT": 60.0,
                         "3/8\" gyp board": 40.0, "5/8\" EXTERIOR gyp sheathing": 500.0},
            "filas": [{"familia": "6\" parapet stud", "operacion": "L 10 -> ... = 12 x H ponderada 3.0 = 36"},
                      {"familia": "3-5/8\" stud (todos los gauges)", "ref": "COL",
                       "operacion": "column_wrap Σ (...) = 8 studs x 10 x 1 = 80 LF"},
                      {"familia": "ceilings", "operacion": "= 99 studs"}]}


STUDS = {"walls": [{"id": "W1", "pcs_full": 18, "cripples": 4}, {"id": "W2", "pcs_full": 18, "cripples": 0}]}


def test_yields_board():
    o = A.calcular(fam_base(), canon_base(), STUDS)
    f = o["familias"]
    chk("board driver sin exterior", abs(f["drywall screws"] - 1.2 * 1000) < 0.011, f["drywall screws"])
    chk("compound", abs(f["joint compound"] - 72.0) < 0.011)
    chk("tape", abs(f["joint tape"] - 370.0) < 0.011)


def test_yield_override():
    c = canon_base()
    c["constants"]["drywall_screws_per_sf"] = {"value": 1.0, "source": "proveedor"}
    o = A.calcular(fam_base(), c, STUDS)
    chk("override yield", abs(o["familias"]["drywall screws"] - 1000.0) < 0.011)
    c["constants"]["joint_tape_lf_per_sf"] = {"value": 0.3}
    try:
        A.calcular(fam_base(), c, STUDS)
        chk("override sin source = error", False)
    except ValueError:
        chk("override sin source = error", True)


def test_head_track():
    o = A.calcular(fam_base(), canon_base(), STUDS)
    chk("solo la ventana > 4'-0\"", abs(o["familias"]["additional head track"] - (6.0 + 2 * 8 / 12)) < 0.011,
        o["familias"]["additional head track"])
    r = [x for x in o["rfis"] if x["familia"] == "additional head track"]
    chk("box run al RFI con delta", r and abs(r[0]["delta"] - round(12 + 16 / 12, 2)) < 0.01, r)


def test_reinforcement_y_sleeves():
    o = A.calcular(fam_base(), canon_base(), STUDS)
    # v73 (R73.5): un FD de openings_extra (fuera del barrido mep.cruces) no entra en la familia: RFI con su delta
    chk("FD fuera de mep.cruces = 0 en la familia + RFI", o["familias"]["stud reinforcement MEP"] == 0 and any(
        r["familia"] == "stud reinforcement MEP" and r["delta"] == 2 for r in o["rfis"]), o["rfis"])
    # PAFs: ROUNDUP(10.5)=11 + ROUNDUP(4)=4 + 2 sleeves
    chk("PAFs por run + sleeves", o["familias"]["PAFs and duct sleeves"] == 17, o["familias"]["PAFs and duct sleeves"])
    c = canon_base()
    c["openings_extra"] = [x for x in c["openings_extra"] if x["kind"] != "fire_damper"]
    o = A.calcular(fam_base(), c, STUDS)
    chk("barrido sin penetraciones = 0 DERIVADO", o["estado"]["stud reinforcement MEP"] == "DERIVADO"
        and o["familias"]["stud reinforcement MEP"] == 0)
    c = canon_base()
    del c["mep_sweep"]
    o = A.calcular(fam_base(), c, STUDS)
    chk("v67 sin mep_sweep = PENDIENTE aunque haya FD", o["estado"]["stud reinforcement MEP"] == "PENDIENTE")
    c = canon_base()
    c["mep_sweep"]["sheets"] = ["M1.01"]
    _err("v67 mep_sweep sin hoja P = error", c, "P*")


def _err(nombre, c, frase, studs=STUDS):
    try:
        A.calcular(fam_base(), c, studs)
        chk(nombre, False, "no falló")
    except ValueError as e:
        chk(nombre, frase in str(e), str(e))


def test_v67_reinforcement_pipes():
    c = canon_base()
    c["mep_penetrations"] = [{"ref": "pipe chico", "wall": "W1", "dia_in": 1.0, "qty": 3, "source": "P1.01",
                              "method": "mep.cruces", "kind": "pipe"},
                             {"ref": "pipe 3", "wall": "W1", "dia_in": 3.0, "qty": 2, "source": "P1.01",
                              "method": "mep.cruces", "kind": "pipe"},
                             {"ref": "duct 2 studs", "wall": "W2", "width_in": 10, "qty": 1, "source": "M1.01",
                              "method": "mep.cruces", "kind": "duct",
                              "studs_cut": {"value": 2, "source": "M1.01 (cruza un stud de cada row)"}}]
    o = A.calcular(fam_base(), c, STUDS)
    # v73 (R73.5): solo ductos de mep.cruces en la familia; pipe > 1" a RFI (+2); FD de openings_extra a RFI
    chk("pipe <= 1in sin plate; pipe 3in a RFI; studs_cut declarado", o["familias"]["stud reinforcement MEP"]
        == 2, o["familias"]["stud reinforcement MEP"])
    chk("RFI de pipes > 1in con delta 2", any("pipes over 1 in" in r["tema"] and r["delta"] == 2 for r in o["rfis"]),
        o["rfis"])


def test_reinforcement_ancho():
    c = canon_base()
    c["mep_penetrations"] = [{"ref": "duct wide", "wall": "W1", "width_in": 30, "qty": 1, "source": "M1.01",
                              "method": "mep.cruces", "kind": "duct"}]
    o = A.calcular(fam_base(), c, STUDS)
    chk("ducto de 30\" @16\" corta 2 studs", o["familias"]["stud reinforcement MEP"] == 2)
    c["mep_penetrations"][0]["method"] = "manual"
    o = A.calcular(fam_base(), c, STUDS)
    chk("v73 cruce manual = 0 en la familia + RFI", o["familias"]["stud reinforcement MEP"] == 0 and any(
        "read by hand" in r["tema"] and r["delta"] == 2 for r in o["rfis"]), o["rfis"])


def test_grille():
    o = A.calcular(fam_base(), canon_base(), STUDS)
    n = math.ceil(8.0 / (16 / 12)) + 1
    sl = 2.0 - 2 * 0.5 - 0.625 / 12
    chk("grille: entre box beams menos board", abs(o["familias"]["2-1/2\" CFMF coiling grille head"] - n * sl) < 0.011)
    c = canon_base()
    del c["walls"][6]["head_build"]
    o = A.calcular(fam_base(), c, STUDS)
    chk("v67 grille sin head_build = PENDIENTE (nunca height_ft)",
        o["estado"]["2-1/2\" CFMF coiling grille head"] == "PENDIENTE"
        and o["familias"]["2-1/2\" CFMF coiling grille head"] == 0)
    c["accesorios_rfi"] = [{"familia": "2-1/2\" CFMF coiling grille head", "motivo": "head sin cota",
                            "delta": "+/- 1 ft por stud", "source": "4/X8.21"}]
    o = A.calcular(fam_base(), c, STUDS)
    chk("accesorios_rfi: PENDIENTE -> RFI con delta", o["estado"]["2-1/2\" CFMF coiling grille head"] == "RFI")


def test_jamb_return():
    o = A.calcular(fam_base(), canon_base(), STUDS)
    win = 6.0 + 2 * 7.0 - 2 * 3.0 + 6.0
    sf = 10.0 + 1 * 8.0
    chk("jamb return ventana + head storefront + 1 jamb", abs(o["familias"]["gypsum board jamb return"] -
                                                            (win + sf) * 0.5) < 0.011)


def test_v67_jamb_return_declarado():
    c = canon_base()
    c["walls"][2]["openings"] = [{"ref": "ext door", "kind": "door", "ro_w_ft": 3.0, "head_ft": 7.0}]
    _err("abertura exterior sin jamb_return declarado = error", c, "ext door")
    c["walls"][2]["openings"][0].update(jamb_return=False, jamb_return_source="3/X9.25")
    o = A.calcular(fam_base(), c, STUDS)
    chk("false con source no suma", abs(o["familias"]["gypsum board jamb return"] -
                                        (6.0 + 2 * 7.0 - 2 * 3.0 + 6.0 + 18.0) * 0.5) < 0.011)
    c = canon_base()
    del c["openings_extra"][2]["jambs"]
    _err("v68 storefront con wall_jambs sin jambs por jamb = error", c, "jambs")
    c = canon_base()
    del c["openings_extra"][2]["head_ft"]
    _err("storefront con wall_jambs > 0 sin head_ft = error claro", c, "head_ft")
    c["openings_extra"][2]["wall_jambs"] = 0
    c["openings_extra"][2]["jambs"][0]["abuts"] = "frame"
    o = A.calcular(fam_base(), c, STUDS)
    chk("wall_jambs 0 no necesita head_ft", o["familias"]["gypsum board jamb return"] > 0)


def test_pvc():
    o = A.calcular(fam_base(), canon_base(), STUDS)
    room = 2 * 25.0 + 4 * 4.0 + 2 * 1 * 4.0
    mop = 1 * 3.0 + 2 * 2.0 + 2 * 3.0
    chk("PVC trim", abs(o["familias"]["PVC trim at FRP"] - (room + mop)) < 0.011, o["familias"]["PVC trim at FRP"])
    c = canon_base()
    c["tile_base"][0]["inside_corners"] = {"value": 6, "vertices": 8, "outside_corners": 2, "source": "X2.01"}
    o = A.calcular(fam_base(), c, STUDS)
    chk("inside corners declarados", abs(o["familias"]["PVC trim at FRP"] - (room + 2 * 4.0 + mop)) < 0.011)
    # v68: cuarto con un notch = 6 vértices = 5 inside + 1 outside; 6 inside o 4 inside con 6 vértices = error
    for bad in ({"value": 6, "vertices": 6, "outside_corners": 0, "source": "X2.01"},
                {"value": 4, "vertices": 6, "outside_corners": 2, "source": "X2.01"},
                {"value": 5, "source": "X2.01"}):
        c = canon_base()
        c["tile_base"][0]["inside_corners"] = bad
        try:
            A.calcular(fam_base(), c, STUDS)
            chk(f"inside corners {bad} rechazado", False)
        except ValueError as e:
            chk(f"inside corners {bad['value']} rechazado", "vertices" in str(e) or "inside" in str(e), e)
    c = canon_base()
    c["tile_base"][0]["inside_corners"] = {"value": 5, "vertices": 6, "outside_corners": 1, "source": "X2.01"}
    o = A.calcular(fam_base(), c, STUDS)
    chk("notch: 5 inside", abs(o["familias"]["PVC trim at FRP"] - (room + 1 * 4.0 + mop)) < 0.011)
    # v68: perimeter_basis gross -> el edge trim usa el perímetro neto de doors (igual que el FRP)
    c = canon_base()
    t0 = c["tile_base"][0]
    t0["perimeter_basis"] = "gross"
    t0["doors"] = [{"ref": "D1", "ro_w_ft": 3.0}] * max(1, len(t0.get("doors") or []))
    nd = len(t0["doors"])
    o = A.calcular(fam_base(), c, STUDS)
    chk("PVC edge con perímetro neto", abs(o["familias"]["PVC trim at FRP"] - (room - 2 * 3.0 * nd + mop)) < 0.011,
        o["familias"]["PVC trim at FRP"])


def test_pins_anchors():
    o = A.calcular(fam_base(), canon_base(), STUDS)
    chk("pins: interior x rows, sin bulkhead/parapet/grille", abs(o["familias"]["slab pins"] - (20 + 2 * 10)) < 0.011,
        o["familias"]["slab pins"])
    chk("anchors exterior @8\"", abs(o["familias"]["expansion anchors"] - 30 * 1.5) < 0.011)


def test_framing_screws():
    fb = fam_base()
    fb["filas"].append({"familia": "6\" stud (todos los gauges)", "ref": "jambs", "pcs": 5, "operacion": "x"})
    o = A.calcular(fb, canon_base(), STUDS)
    chk("v67 pcs explícito de canon", o["familias"]["framing screws"] == 4 * 65, o["familias"]["framing screws"])
    o = A.calcular(fam_base(), canon_base(), STUDS)
    chk("4 x (studs_nodos 40 + parapet 12 + column wrap 8), sin joists", o["familias"]["framing screws"] == 4 * 60,
        o["familias"]["framing screws"])


def test_level5_y_ap():
    c = canon_base()
    c["constants"]["level5_tags"] = {"value": ["WC-9", "WC-7"], "source": "X0.40"}
    o = A.calcular(fam_base(), c, STUDS)
    chk("level 5 neto de base", abs(o["familias"]["Level 5 finish"] - 10 * 8.5) < 0.011)
    chk("tag faltante = PENDIENTE", o["estado"]["Level 5 finish"] == "PENDIENTE" and
        any("WC-7" in a for a in o["avisos"]))
    chk("access panel", o["familias"]["access panel"] == 1)
    c = canon_base()
    c["constants"]["level5_tags"] = {"value": ["WC-1"], "source": "X0.40"}
    c["level5_items"][0]["wc_tag"] = "WC-10"
    o = A.calcular(fam_base(), c, STUDS)
    chk("v67 tag exacto: WC-10 no cubre WC-1", o["estado"]["Level 5 finish"] == "PENDIENTE")
    c = canon_base()
    del c["level5_items"][0]["base_ft"]
    _err("v67 Level 5 sin base_ft = error", c, "base_ft")
    c = canon_base()
    c["level5_items"] = []
    c["constants"]["level5_tags"] = {"value": [], "source": "X0.40 sin LEVEL 5"}
    o = A.calcular(fam_base(), c, STUDS)
    chk("v67 schedule sin LEVEL 5 = 0 DERIVADO", o["estado"]["Level 5 finish"] == "DERIVADO")


def test_extra_framing():
    o = A.calcular(fam_base(), canon_base(), STUDS)
    chk("extra framing sin datos = PENDIENTE", o["estado"]["extra framing ATM"] == "PENDIENTE")
    c = canon_base()
    c["accesorios_none"] = [{"familia": "extra framing ATM", "why": "sin ATM ni extra framing en el set",
                             "source": "X2.01; X8.11"}]
    o = A.calcular(fam_base(), c, STUDS)
    chk("v67 accesorios_none = 0 DERIVADO con motivo", o["estado"]["extra framing ATM"] == "DERIVADO")
    c = canon_base()
    c["walls"][0]["openings"][0]["atm_recess"] = {"width_ft": 4.0, "sistered_h_ft": 6.0, "furring_rows": 3,
                                                   "source": "6/X8.11"}
    _err("atm recess sin width_source = error", c, "width_source")
    c["walls"][0]["openings"][0]["atm_recess"]["width_source"] = "X2.01"
    c["walls"][0]["openings"][0]["atm_recess"].update({"width_status": "CONFIRMADO", "sistered_h_status": "CONFIRMADO", "sistered_h_source": "6/X8.11",
         "furring_rows_status": "CONFIRMADO", "furring_rows_source": "6/X8.11"})
    o = A.calcular(fam_base(), c, STUDS)
    chk("atm recess", abs(o["familias"]["extra framing ATM"] - ((3 + 1) * 6.0 + 3 * 4.0)) < 0.011)


def test_v67_atm_obligatorio():
    c = canon_base()
    c["walls"][0]["openings"].append({"ref": "ATM drive-up", "kind": "window", "ro_w_ft": 3.0, "head_ft": 6.0,
                                      "sill_ft": 3.0, "jamb_return": True, "substrate_none_reason": "sintético (v76 R76.4)", "jamb_return_source": "6/X8.11", "jamb_return_label": "GYPSUM BOARD JAMB RETURN"})
    _err("ATM sin atm_recess = error", c, "ATM")
    c["walls"][0]["openings"][-1]["atm_recess"] = {"width_ft": 3.0, "sistered_h_ft": 6.0, "furring_rows": 2,
                                                   "source": "X8.11", "width_source": "X2.01"}
    _err("atm_recess sin N/HOJA = error", c, "N/HOJA")
    c["walls"][0]["openings"][-1]["atm_recess"]["source"] = "6/X8.11"
    c["walls"][0]["openings"][-1]["atm_recess"].update({"width_status": "CONFIRMADO", "sistered_h_status": "CONFIRMADO", "sistered_h_source": "6/X8.11",
         "furring_rows_status": "CONFIRMADO", "furring_rows_source": "6/X8.11"})
    o = A.calcular(fam_base(), c, STUDS)
    chk("ATM con recess = DERIVADO", o["estado"]["extra framing ATM"] == "DERIVADO")


def test_nombres_y_unidades():
    o = A.calcular(fam_base(), canon_base(), STUDS)
    chk("16 familias (v73: deflection clips)", len(o["familias"]) == 16)
    chk("toda fila con source", all(r["source"] for r in o["filas"]))
    n = o["nombres_excel"]
    chk("v67 un renglón de Material Summary por familia", set(n) == set(o["familias"]))
    chk("grille con N/HOJA", "(4/X8.21)" in n["2-1/2\" CFMF coiling grille head"], n)
    chk("access panel con medida", n["access panel"] == "Access panel 2'x2'", n["access panel"])
    chk("insulation EXCLUDED", "EXCLUDED" in o["excluidas"]["batt insulation"])



def test_v68_registro_y_visual():
    c = canon_base()
    del c["mep_sweep"]["registro"]
    o = A.calcular(fam_base(), c, STUDS)
    chk("v68 sin registro = PENDIENTE", o["estado"]["stud reinforcement MEP"] == "PENDIENTE")
    c = canon_base()
    c["mep_sweep"]["registro"]["matches"] = 12
    o = A.calcular(fam_base(), c, STUDS)
    chk("v68 registro < 25 = PENDIENTE", o["estado"]["stud reinforcement MEP"] == "PENDIENTE")
    c = canon_base()
    c["mep_sweep"]["source"] = "P1.01 lectura visual"
    _err("v68 barrido visual = error", c, "visual")
    c = canon_base()
    c["mep_penetrations"] = [{"ref": "duct a", "wall": "W1", "width_in": 10, "qty": 1, "source": "M1.01 (visual)"}]
    _err("v68 penetración visual = error", c, "visual")
    c = canon_base()
    c["mep_penetrations"] = [{"ref": "duct a", "wall": "W1", "width_in": 10, "xy": [100, 200], "source": "M1.01"},
                             {"ref": "duct a bis", "wall": "W1", "width_in": 10, "xy": [100, 200], "source": "M1.01"}]
    _err("v68 misma penetración dos veces = error", c, "repetida")
    c["mep_penetrations"] = [{"ref": "pipe in cavity", "wall": "W2", "dia_in": 3.0, "in_cavity": True,
                              "in_cavity_source": "5/X12.01", "source": "P1.01"}]
    o = A.calcular(fam_base(), c, STUDS)
    chk("v68 pipe dentro de la cavidad = 0", o["familias"]["stud reinforcement MEP"] == 0)


def test_v68_grille_cadena():
    c = canon_base()
    c["walls"][6]["head_build"]["head_chain_in"] = [18]
    _err("v68 head_ft != suma de la cadena = error", c, "suma")
    del c["walls"][6]["head_build"]["head_chain_in"]
    _err("v68 head_build sin cadena = error", c, "head_chain_in")
    c["walls"][6]["head_build"].update(head_chain_in=[18], head_ft=1.5)
    o = A.calcular(fam_base(), c, STUDS)
    chk("v68 cadena de un eslabón da menos (la cadena completa manda)",
        o["familias"]["2-1/2\" CFMF coiling grille head"] < A.calcular(fam_base(), canon_base(), STUDS)[
            "familias"]["2-1/2\" CFMF coiling grille head"])


def test_v68_jambs_por_jamb():
    c = canon_base()
    c["openings_extra"][2]["jambs"][1]["abuts"] = "wall"
    _err("v68 wall_jambs != jambs contra wall = error", c, "!=")
    c["openings_extra"][2]["wall_jambs"] = 2
    o = A.calcular(fam_base(), c, STUDS)
    win = 6.0 + 2 * 7.0 - 2 * 3.0 + 6.0
    chk("v68 dos jambs contra wall", abs(o["familias"]["gypsum board jamb return"] - (win + 10 + 16) * 0.5) < 0.011)
    c["openings_extra"][2]["jambs"][1]["source"] = "X2.01 wall/pier"
    _err("v68 fuente 'wall/pier' = error", c, "wall/pier")


def test_v68_access_panel_sin_doble_conteo():
    fo = {"items": [{"tag": "AP 1", "category": "access_panel", "qty": 1, "source": "X4.01"}]}
    o = A.calcular(fam_base(), canon_base(), STUDS, fo)
    chk("v68 canon + fo del mismo panel = 1", o["familias"]["access panel"] == 1, o["familias"]["access panel"])
    c = canon_base()
    del c["access_panels"]
    o = A.calcular(fam_base(), c, STUDS, fo)
    chk("v68 sin canon cuenta fo_in", o["familias"]["access panel"] == 1)


def test_v68_atm_estados_y_e12():
    c = canon_base()
    c["walls"][0]["openings"].append({"ref": "ATM 2", "kind": "window", "ro_w_ft": 2.0, "head_ft": 5.0,
                                      "sill_ft": 3.0, "jamb_return": True, "substrate_none_reason": "sintético (v76 R76.4)", "jamb_return_source": "6/X8.11", "jamb_return_label": "GYPSUM BOARD JAMB RETURN",
                                      "atm_recess": {"width_ft": 4.0, "width_source": "X2.01 vector",
                                                     "width_status": "DERIVADO", "sistered_h_ft": 6.0,
                                                     "sistered_h_source": "6/X8.11", "sistered_h_status": "CONFIRMADO",
                                                     "furring_rows": 3, "furring_rows_source": "6/X8.11",
                                                     "furring_rows_status": "DERIVADO", "source": "6/X8.11"}})
    o = A.calcular(fam_base(), c, STUDS)
    chk("v68 ATM con dato DERIVADO = CRITERIO + RFI", o["estado"]["extra framing ATM"] == "CRITERIO" and
        any(r["familia"] == "extra framing ATM" for r in o["rfis"]))
    del c["walls"][0]["openings"][-1]["atm_recess"]["width_status"]
    _err("v68 ATM sin width_status = error", c, "width_status")
    c = canon_base()
    c["extra_framing"] = [{"ref": "duct 8x10 framing", "kind": "mep", "lf": 6.0, "source": "M1.01"}]
    _err("v68 extra framing de ducto = error (E12)", c, "E12")


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"):
            f()
    print(f"test_accesorios: {len(OK)} checks OK")
