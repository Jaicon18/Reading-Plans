#!/usr/bin/env python3
"""Tests de headers.py v65b (decisiones usuario #1, #2, #12, #16, #18-#22; 60.10). Datos genéricos. Correr: python3 test_headers.py"""
import json
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import headers as H  # noqa: E402


SCH = {"source": "7/S5.20", "rows": [
    {"max_span_ft": 3.333, "type": "SINGLE TRACK 18 GA", "pieces": 1, "piece": "track"},
    {"max_span_ft": 6.0, "type": "DOUBLE TRACK 18 GA", "pieces": 2, "piece": "track"},
    {"max_span_ft": 8.0, "type": "2-362CSJ20", "pieces": 2, "piece": "362CSJ20"}]}
B = 16 / 12


def caso():
    return {
        "header_schedule": SCH,
        "sill_rule": {"double_over_ft": 4.0, "source": "2/S5.20"},
        "openings": [
            {"ref": "door 101", "wall": "W1", "kind": "door", "location": "interior", "ro_w_ft": 3.333,
             "source": "A00.30"},
            {"ref": "W-A", "wall": "W9", "kind": "window", "location": "exterior", "ro_w_ft": 7.0, "qty": 5,
             "with_sill": True, "header_type": "6\" C box beam", "header_type_source": "11/A09.27",
             "pieces": 4, "pieces_source": "11/A09.27", "piece": "6\" C box", "source": "11/A09.27"},
            {"ref": "office front", "wall": "W4", "kind": "opening", "ro_w_ft": 36.5, "continuous_run": True,
             "header_type": "CONT. BOX BEAM", "run_ends": "jamb_to_jamb", "header_type_source": "9/A12.01", "pieces": 4,
             "pieces_source": "9/A12.01", "piece": "C box", "source": "A02.01"},
        ]}


def lista_sintetica():
    """Lista cerrada SINTÉTICA con todos los casos de las reglas E1, E2, E12, E16, E18-E22 (datos inventados)."""
    box = lambda src, pc: {"header_type": "BOX", "header_type_source": src, "pieces": 4, "pieces_source": src,
                           "piece": pc}
    cont = {"header_type": "CONT. BOX BEAM", "run_ends": "jamb_to_jamb", "header_type_source": "8/A12.01", "pieces": 4,
            "pieces_source": "8/A12.01", "piece": "C box", "continuous_run": True, "kind": "opening"}
    return {"header_schedule": SCH, "sill_rule": {"double_over_ft": 4.0, "source": "2/S5.20"}, "openings": [
        {"ref": "interior doors", "kind": "door", "location": "interior", "ro_w_ft": 3.0, "qty": 10,
         "source": "A00.30"},
        {"ref": "door D2", "kind": "door", "location": "interior", "ro_w_ft": 4.5, "source": "A00.30"},
        dict({"ref": "door X1", "kind": "door", "location": "exterior", "ro_w_ft": 3.0,
              "source": "14/A09.27"}, **box("14/A09.27", "C box")),
        {"ref": "ATM A", "kind": "opening", "ro_w_ft": 2.5, "with_sill": True, "source": "A08.11"},
        dict({"ref": "ATM B", "kind": "opening", "ro_w_ft": 2.5, "with_sill": True,
              "source": "5/A08.11"}, **box("6/A08.11", "C box")),
        dict({"ref": "W-A", "kind": "window", "ro_w_ft": 7.0, "qty": 5, "with_sill": True, "or_steel": True,
              "source": "11/A09.27"}, **box("11/A09.27", "6\" C box")),
        dict({"ref": "front 1", "wall": "OF-1", "ro_w_ft": 36.5, "source": "A02.01"}, **cont),
        dict({"ref": "front 2", "wall": "OF-2", "ro_w_ft": 17.0, "source": "A02.01"}, **cont),
        dict({"ref": "vestibule A", "kind": "opening", "ro_w_ft": 14.0, "source": "1/A12.10"},
             **box("4/A12.10", "C box")),
        dict({"ref": "grille G", "kind": "grille", "ro_w_ft": 12.0, "beams": 2,
              "beams_source": "4/A08.21", "source": "A08.21"}, **box("4/A08.21", "6\" CFMF box")),
        {"ref": "SF-1", "kind": "storefront", "location": "exterior", "ro_w_ft": 30.0,
         "structure": "HSS", "structure_source": "S2.20", "source": "2/A09.26"},
        {"ref": "duct 1", "kind": "duct", "ro_w_ft": 1.5, "with_sill": True, "source": "M01.01"},
        {"ref": "FD 1", "kind": "fire_damper", "ro_w_ft": 1.25, "qty": 3, "with_sill": True,
         "source": "M01.01"},
    ]}


def test_lista_cerrada_por_piezas():
    """E2/E20/E21/E22: cada abertura (R.O. + 1'-4") x piezas; box = 4; un run por frente; HSS / ducto / FD = 0."""
    out = H.calcular(lista_sintetica())
    esp = ((3.0 + B) * 1 * 10 + (4.5 + B) * 2 + (3.0 + B) * 4 + (2.5 + B) * 1 + (2.5 + B) * 4 + (7.0 + B) * 4 * 5
           + (36.5 + B) * 4 + (17.0 + B) * 4 + (14.0 + B) * 4 + (12.0 + B) * 4 * 2)
    assert abs(out["totales_lf"]["header"] - esp) < 0.05, (out["totales_lf"], esp)
    esp_sill = (2.5 + B) * 1 + (2.5 + B) * 1 + (7.0 + B) * 2 * 5
    assert abs(out["totales_lf"]["sill track"] - esp_sill) < 0.05, out["totales_lf"]
    r = {x["ref"]: x for x in out["renglones"]}
    assert r["interior doors"]["pieces"] == 1 and r["door D2"]["pieces"] == 2
    assert r["door X1"]["pieces"] == 4 and r["ATM B"]["pieces"] == 4 and r["ATM A"]["pieces"] == 1
    assert r["SF-1"]["estado"] == "STEEL_BY_OTHERS" and r["SF-1"]["header_lf"] == 0
    assert r["duct 1"]["estado"] == "NOT_FRAMED" and r["FD 1"]["sill_lf"] == 0
    assert abs(out["por_pieza"]["track"] - ((3.0 + B) * 10 + (4.5 + B) * 2 + (2.5 + B))) < 0.05, out["por_pieza"]


def test_lf_por_piezas():
    out = H.calcular(caso())
    esperado = (3.333 + B) * 1 + 5 * (7.0 + B) * 4 + (36.5 + B) * 4
    assert abs(out["totales_lf"]["header"] - esperado) < 0.02, out["totales_lf"]
    assert abs(out["totales_lf"]["sill track"] - 5 * (7.0 + B) * 2) < 0.02       # 2/S5.20 > 4'-0" -> 2


def test_tipo_y_piezas_del_schedule():
    d = caso()
    d["openings"].append({"ref": "door D2", "wall": "W2", "kind": "door", "ro_w_ft": 4.5, "source": "A00.30"})
    r = {x["ref"]: x for x in H.calcular(d)["renglones"]}
    assert r["door 101"]["header_type"] == "SINGLE TRACK 18 GA" and r["door 101"]["pieces"] == 1
    assert r["door D2"]["header_type"] == "DOUBLE TRACK 18 GA" and abs(r["door D2"]["header_lf"] - (4.5 + B) * 2) < 0.01
    assert "CONT. BOX BEAM" in r["office front"]["description"]
    assert abs(r["office front"]["header_lf"] - (36.5 + B) * 4) < 0.01    # (run + 1'-4") x 4 piezas, un run


def test_schedule_sin_piezas_falla():
    d = caso()
    d["header_schedule"] = {"source": "7/S5.20", "rows": [{"max_span_ft": 4.0, "type": "SINGLE TRACK"}]}
    _falla(d, "pieces")


def test_box_sin_piezas_falla():
    d = caso()
    del d["openings"][2]["pieces"]
    _falla(d, "pieces")
    d = caso()
    del d["openings"][2]["pieces_source"]
    _falla(d, "pieces")


def test_ductos_fd_no_se_enmarcan():
    """Decisión usuario #12: ni el duct > stud bay lleva header/sill."""
    d = caso()
    d["openings"].append({"ref": "duct 24x12", "wall": "W2", "kind": "duct", "ro_w_ft": 2.0,
                          "with_sill": True, "source": "M01.01"})
    d["openings"].append({"ref": "FD-1", "wall": "W2", "kind": "fire_damper", "ro_w_ft": 1.2, "qty": 4,
                          "with_sill": True, "source": "M01.01"})
    base = H.calcular(caso())["totales_lf"]
    out = H.calcular(d)
    assert out["totales_lf"] == base
    assert {x["estado"] for x in out["renglones"] if x["kind"] in ("duct", "fire_damper")} == {"NOT_FRAMED"}


def test_borde_cabe_en_modulo():
    d = caso()
    d["openings"].append({"ref": "louver", "wall": "W2", "kind": "opening", "ro_w_ft": 14.375 / 12,
                          "with_sill": True, "source": "A08.01"})
    r = {x["ref"]: x for x in H.calcular(d)["renglones"]}
    assert r["louver"]["estado"] == "FITS_MODULE" and r["louver"]["header_lf"] == 0
    d["openings"][-1]["ro_w_ft"] = 14.5 / 12
    r = {x["ref"]: x for x in H.calcular(d)["renglones"]}
    assert r["louver"]["estado"] == "HEADER"


def test_span_fuera_de_schedule_sin_piezas_falla():
    d = caso()
    d["openings"][0]["ro_w_ft"] = 12.0
    _falla(d, "sin fila en el header schedule")


def _falla(d, txt):
    try:
        H.calcular(d)
    except ValueError as e:
        assert txt in str(e), str(e)
        return
    raise AssertionError("debía fallar: " + txt)


def test_dato_malo_members_multiplica():
    d = caso()
    d["openings"][2]["members"] = 2
    _falla(d, "pieces_source")


def test_dato_malo_recessed_accessory():
    d = caso()
    d["openings"].append({"ref": "FEC", "wall": "W3", "kind": "recessed_accessory", "ro_w_ft": 2.0,
                          "source": "A10.01"})
    _falla(d, "no es header")


def test_dato_malo_sin_source():
    d = caso()
    del d["openings"][0]["source"]
    _falla(d, "falta 'source'")


def test_dato_malo_source_sin_hoja():
    d = caso()
    d["openings"][0]["source"] = "plano"
    _falla(d, "forma N/HOJA")


def test_dato_malo_abertura_duplicada():
    d = caso()
    d["openings"].append(dict(d["openings"][0]))
    _falla(d, "repetida")


def test_dato_malo_ro_cero_y_qty():
    d = caso()
    d["openings"][0]["ro_w_ft"] = 0
    _falla(d, "> 0")
    d = caso()
    d["openings"][0]["qty"] = 1.5
    _falla(d, "entero")


def test_dato_malo_header_type_sin_fuente():
    d = caso()
    del d["openings"][2]["header_type_source"]
    _falla(d, "header_type")


def _falla(d, txt):
    try:
        H.calcular(d)
    except ValueError as e:
        assert txt in str(e), str(e)
        return
    raise AssertionError("debía fallar: " + txt)


def test_dato_malo_12_recessed_como_opening():
    """#12A FEC-2 recess 3.0 ft y #12B TA-13 hand dryer 1.425 ft entraron como kind 'opening' (+4.33, +5.52)."""
    for ref, ro in (("FEC-2 recess", 3.0), ("TA-13 hand dryer recess Men 113", 1.425)):
        d = {"openings": [{"ref": ref, "wall": "B", "kind": "opening", "ro_w_ft": ro, "source": "A08.01"}]}
        _falla(d, "recessed accessory")


def test_grille_dos_box_beams():
    """4/A08.21: DOS 6\" CFMF BOX BEAM de 4 piezas c/u (#20) -> 2 x 4 x (R.O. + 1'-4")."""
    malo = {"openings": [{"ref": "grille G", "wall": "GH-1", "kind": "opening", "ro_w_ft": 12.0,
                          "source": "1/A08.21"}]}
    _falla(malo, "kind 'grille'")
    sin = {"openings": [{"ref": "grille G", "kind": "grille", "ro_w_ft": 12.0, "source": "1/A08.21"}]}
    _falla(sin, "beams")
    ok = {"openings": [{"ref": "grille G", "kind": "grille", "ro_w_ft": 12.0, "beams": 2,
                        "beams_source": "4/A08.21", "source": "1/A08.21", "header_type": "6\" CFMF BOX BEAM",
                        "header_type_source": "4/A08.21", "pieces": 4, "pieces_source": "4/A08.21"}]}
    assert abs(H.calcular(ok)["totales_lf"]["header"] - 2 * 4 * (12.0 + B)) < 0.01


def test_storefront_exterior_hss_cero():
    """Decisión usuario #16: storefront con HSS lintel (S2.20) = steel by others, 0 metal stud header."""
    d = {"openings": [{"ref": "SF-1", "kind": "storefront", "location": "exterior", "ro_w_ft": 30.0,
                       "source": "A09.01"}]}
    _falla(d, "structure_source")
    d["openings"][0]["structure_source"] = "S2.20"
    _falla(d, "structure debe ser")
    d["openings"][0]["structure"] = "HSS"
    out = H.calcular(d)
    assert out["totales_lf"]["header"] == 0 and out["renglones"][0]["estado"] == "STEEL_BY_OTHERS"
    d["openings"][0].update(structure="none", header_type="BOX", header_type_source="9/A12.01", pieces=4,
                            pieces_source="9/A12.01")
    assert H.calcular(d)["totales_lf"]["header"] > 0


def test_cli_rc():
    with tempfile.TemporaryDirectory() as t:
        bueno, malo, sal = (os.path.join(t, x) for x in ("b.json", "m.json", "s.json"))
        json.dump(caso(), open(bueno, "w"))
        d = caso()
        d["openings"][2]["members"] = 2
        json.dump(d, open(malo, "w"))
        p = subprocess.run([sys.executable, os.path.join(AQUI, "headers.py"), bueno, sal], capture_output=True)
        assert p.returncode == 0 and json.load(open(sal))["totales_lf"]["header"] > 0
        p = subprocess.run([sys.executable, os.path.join(AQUI, "headers.py"), malo, sal], capture_output=True,
                           text=True)
        assert p.returncode != 0 and "ERROR headers.py" in p.stderr, p.stderr



def _gl2(**kw):
    o = {"ref": "W-A", "wall": "W9", "kind": "window", "ro_w_ft": 7.0, "qty": 5, "with_sill": True,
         "header_type": "METAL STUD BOX BEAM OR STEEL FRAMING AS REQUIRED", "header_type_source": "11/A09.27",
         "pieces": 4, "pieces_source": "11/A09.27", "source": "11/A09.27"}
    o.update(kw)
    return o


def test_v65b_18_sill_double_es_regla():
    """#18: DOUBLE sill track > 4'-0" aunque la entrada no traiga sill_rule y sin bajarla."""
    t = H.calcular({"openings": [_gl2()]})["totales_lf"]
    assert abs(t["sill track"] - 5 * (7.0 + B) * 2) < 0.02, t                       # 2 piezas, no 1
    _falla({"openings": [_gl2(sill_pieces=1, sill_pieces_source="2/S5.20")]}, "#18")
    _falla(dict(caso(), header_params={"sill_double_track": False}), "header_params")
    t = H.calcular({"openings": [_gl2(ro_w_ft=3.5)]})["totales_lf"]                 # <= 4'-0" -> 1 pieza
    assert abs(t["sill track"] - 5 * (3.5 + B)) < 0.02, t


def test_v65b_19_gl2_metal_box_no_steel():
    """#19: 'METAL STUD BOX BEAM OR STEEL FRAMING AS REQUIRED' (11/A09.27) = metal stud box beam (v65: steel = 0)."""
    _falla({"openings": [_gl2(structure="steel", structure_source="11/A09.27")]}, "#19")
    _falla({"openings": [_gl2(header_type="BOX", or_steel=True, structure="HSS", structure_source="S2.20")]}, "#19")
    _falla(dict(caso(), header_params={"gl2_header": "steel"}), "header_params")
    assert abs(H.calcular({"openings": [_gl2()]})["totales_lf"]["header"] - 5 * 4 * (7.0 + B)) < 0.02


def test_v65b_20_box_cuatro_piezas():
    """#20: todo box beam / box header = 4 piezas (2 C + 2 track); 2 piezas (v64/v65 default) = error."""
    _falla({"openings": [_gl2(pieces=2)]}, "#20")
    for ref, src, ro in (("door X1", "14/A09.27", 3.0), ("ATM B", "6/A08.11", 2.5),
                         ("vestibule A", "4/A12.10", 5.75)):
        o = {"ref": ref, "kind": "opening", "ro_w_ft": ro, "source": src, "header_type": "BOX HEADER",
             "header_type_source": src, "pieces": 2, "pieces_source": src}
        _falla({"openings": [o]}, "#20")
        o["pieces"] = 4
        assert abs(H.calcular({"openings": [o]})["totales_lf"]["header"] - (ro + B) * 4) < 0.02
    _falla(dict(caso(), header_params={"box_pieces": 2}), "header_params")


def test_v65b_21_door_double_track():
    """#21: door con R.O. <= 6'-0" (fila DOUBLE TRACK de 7/S5.20) = 2 piezas; no se baja a 1."""
    d = {"header_schedule": SCH, "openings": [{"ref": "door D2", "kind": "door", "location": "interior",
                                               "ro_w_ft": 4.5, "source": "A00.30"}]}
    r = H.calcular(d)["renglones"][0]
    assert r["pieces"] == 2 and abs(r["header_lf"] - (4.5 + B) * 2) < 0.01, r
    d["openings"][0].update(header_type="SINGLE TRACK (9/S5.20 > 4'-0\")", header_type_source="9/S5.20",
                            pieces=1, pieces_source="9/S5.20")
    _falla(d, "#21")
    _falla(dict(caso(), header_params={"pieces_override": {"door D2": 1}}), "header_params")


def test_v65b_22_office_front_un_run_continuo():
    """#22: CONT. BOX BEAM = UN run por frente (no uno por abertura); dos frentes = dos runs."""
    of = {"ref": "office fronts", "wall": "OF-E", "kind": "opening", "ro_w_ft": 7.0, "qty": 5,
          "header_type": "CONT. BOX BEAM", "run_ends": "jamb_to_jamb", "header_type_source": "8/A12.01", "pieces": 4,
          "pieces_source": "8/A12.01", "source": "A02.01"}
    _falla({"openings": [of]}, "#22")                                             # por abertura
    run = dict(of, ref="office front E", qty=1, ro_w_ft=36.5, continuous_run=True)
    _falla({"openings": [run, dict(run, ref="office front E2")]}, "#22")           # dos runs en la misma línea
    _falla({"openings": [dict(run, wall="")]}, "wall")
    w = dict(run, ref="office front W", wall="OF-W", ro_w_ft=17.0)
    t = H.calcular({"openings": [run, w]})["totales_lf"]["header"]
    assert abs(t - ((36.5 + B) * 4 + (17.0 + B) * 4)) < 0.02, t          # un run por frente
    _falla({"openings": [dict(_gl2(), continuous_run=True)]}, "continuous_run")
    _falla(dict(caso(), header_params={"office_front_header": "per_opening"}), "header_params")



def test_v68_kind_atm_igual_a_window():
    """v68 (#16B): el protocolo nombra la abertura ATM con kind "atm"; headers.py la rechazaba."""
    def d(kind):
        c = caso()
        c["openings"] = [{"ref": "ATM X", "wall": "W1", "kind": kind, "ro_w_ft": 2.5, "with_sill": True,
                          "source": "5/X8.11"}]
        return c
    ra, rw = H.calcular(d("atm")), H.calcular(d("window"))
    assert ra["totales_lf"] == rw["totales_lf"] and ra["totales_lf"]["sill track"] > 0, ra["totales_lf"]
    assert ra["renglones"][0]["kind"] == "atm"


if __name__ == "__main__":
    n = 0
    for k, f in list(globals().items()):
        if k.startswith("test_") and callable(f):
            f()
            n += 1
            print("OK", k)
    print(f"{n} tests OK")
