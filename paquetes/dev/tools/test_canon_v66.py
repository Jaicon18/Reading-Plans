#!/usr/bin/env python3
"""Tests de canon.py v66 (arbitraje #15A / #15B, 2026-10-17). Datos SINTÉTICOS (E24: ningún valor de un proyecto
de examen). Cada test de 'dato malo' reproduce la falla de una prueba.
Correr: python3 test_canon_v66.py"""
import copy
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import canon as K  # noqa: E402
import test_canon as T  # noqa: E402


def test_ballistic_jogs_sin_walls_fantasma():
    """#15A modeló dos jogs del contorno ballistic como walls A1K de <n> ft: studs y dos faces de 5/8" de más.
    v66: ballistic_jogs suma ballistic + 3/8" + las faces de 5/8" que diga el detalle, sin studs."""
    d = T.base()
    d["details"]["4/A12.01"] = {"layers_per_face": 1, "k_panel": {"panel_to_ft": 8.0},
                                "sealant": {"bottom_faces": 2, "top_faces": 2, "source": "4/A12.01"}}
    d["walls"].append({"id": "K1", "tag": "A1K", "stud_size": "3-5/8\"", "oc_in": 24, "rows": 1, "length_ft": 3.5,
                       "height_ft": 12.0, "detail": "4/A12.01", "source": "A02.01",
                       "length_source": "A02.01 vector (sintético)",
                       "faces": [{"room": "c", "board": "5/8 regular", "layers": 1, "height_ft": 12.0,
                                  "k_customer": True}]})
    d["nodes"] += [{"id": "k1a", "kind": "free", "wall": "K1"}, {"id": "k1b", "kind": "free", "wall": "K1"}]
    d["constants"]["ballistic_contour_ft"] = {"value": 3.5, "source": "A02.01"}
    d["ballistic_jogs"] = []
    f0 = K.calcular(copy.deepcopy(d))["familias"]
    d["ballistic_jogs"] = [{"ref": "jog SW", "length_ft": 0.5, "height_ft": 12.0, "detail": "4/A12.01",
                            "faces_5_8": 1, "source": "A02.01"}]
    T._falla(copy.deepcopy(d), "!= ballistic_contour_ft")        # el jog entra en el contorno
    d["constants"]["ballistic_contour_ft"] = {"value": 4.0, "source": "A02.01"}
    f1 = K.calcular(copy.deepcopy(d))["familias"]
    assert abs(f1["ballistic panel"] - f0["ballistic panel"] - 0.5 * 8.0) < 0.01
    assert abs(f1["3/8\" gyp board"] - f0["3/8\" gyp board"] - 0.5 * 4.0) < 0.01
    assert abs(f1[K.F_GYP] - f0[K.F_GYP] - 0.5 * 12.0) < 0.01
    assert f1[K.F_36] == f0[K.F_36]                                 # sin studs
    malo = copy.deepcopy(d)
    del malo["ballistic_jogs"][0]["faces_5_8"]
    T._falla(malo, "faces_5_8")
    malo = copy.deepcopy(d)
    malo["ballistic_jogs"][0]["detail"] = "3/A12.01"
    T._falla(malo, "k_panel")


def test_column_wrap_por_partes():
    """#15A cargó el pier entero en 6"; #15B entero en 3-5/8". Si el detalle dibuja dos sistemas (L interior
    3-5/8" METAL FRAMING + L exterior 6" CFMF), cada parte va a su familia con los studs dibujados."""
    d = T.base()
    s0 = K.calcular(copy.deepcopy(d))["familias"]
    pier = {"id": "PIER-X", "tag": "PIER", "element": "column_wrap", "stud_size": "mixed", "oc_in": 16, "rows": 1,
            "length_ft": 6.0, "height_ft": 14.0, "source": "2/A09.25",
            "parts": [{"stud_size": "3-5/8\"", "studs_drawn": {"value": 4, "source": "2/A09.25"}},
                      {"stud_size": "6\"", "studs_drawn": {"value": 3, "source": "2/A09.25"}}]}
    d["walls"].append(pier)
    f = K.calcular(copy.deepcopy(d))["familias"]
    assert abs(f[K.F_36] - s0[K.F_36] - 4 * 14.0) < 0.01
    assert abs(f["6\" stud (todos los gauges)"] - s0["6\" stud (todos los gauges)"] - 3 * 14.0) < 0.01
    malo = copy.deepcopy(d)
    malo["walls"][-1]["parts"][1]["studs_drawn"] = {"value": 3}
    T._falla(malo, "studs_drawn {value, source}")
    malo = copy.deepcopy(d)
    malo["walls"][-1]["faces_ft"] = [1.5, 1.5, 1.5, 1.5]
    T._falla(malo, "parts excluye")


def _con_parapet(d):
    d["constants"]["parapet_post_spacing_ft"] = {"value": 5.0, "source": "6/S5.10"}
    d["walls"].append(dict(T._par("PX", 27.667, 2.0, line="PX"), facade="N"))
    return d


def test_nailbase_sube_a_t_stud_del_parapet():
    """E25 (#15B): la nailbase de la facade se cortó en el stud top del wall; la sección la lleva hasta el coping
    (T/STUD del parapet). Una facade con parapet declara parapet_t_stud_ft + nailbase_top/bottom_ft."""
    d = _con_parapet(T.base())
    T._falla(copy.deepcopy(d), "parapet_t_stud_ft")
    f = d["facades"][0]
    f.update(parapet_t_stud_ft={"value": 17.25, "source": "C/A09.21"},
             nailbase_top_ft={"value": 15.0, "source": "C/A09.21"},
             nailbase_bottom_ft={"value": 0.5, "source": "5/A09.26"}, height_nailbase_ft=14.5)
    T._falla(copy.deepcopy(d), "nailbase sigue en la cara exterior del parapet")
    f.update(nailbase_top_ft={"value": 17.25, "source": "C/A09.21"})
    T._falla(copy.deepcopy(d), "height_nailbase_ft")             # altura que no cuadra con top - bottom
    f["height_nailbase_ft"] = 16.75
    K.calcular(copy.deepcopy(d))
    sin_fac = copy.deepcopy(d)
    del sin_fac["walls"][-1]["facade"]
    T._falla(sin_fac, "parapet sin facade")
    alt = _con_parapet(T.base())                                  # alternativa: tira de la cara del parapet
    alt["plywood_strips"].append({"ref": "parapet outer face N", "lf": 27.667, "width_ft": 3.0,
                                  "parapet_face_of": "N", "source": "C/A09.21",
                                  "material": "nailbase_5_8_polyiso"})
    K.calcular(alt)


def test_purlin_en_transicion_paralela_al_flute():
    """#15A ADV-B H7: la transición (track a deck, paralela al flute) quedaba sin purlin porque su elemento no estaba
    en la lista. v66: ceiling_transition y ceiling_bulkhead entran en PURLIN_ELEMS (10/A09.33)."""
    import inventario
    assert "ceiling_transition" in inventario.PURLIN_ELEMS and "ceiling_bulkhead" in inventario.PURLIN_ELEMS


def test_canopy_soffit_wall_line_corridas():
    """#15B: canopy_soffit L x 2 (las dos líneas a largo de fascia) <n> LF. v66: fascia + wall medidas aparte."""
    import corridas as C
    base = {"bracing": {"spacing_in": 48, "source": "F/1/S5.20"}, "section_details": [], "ceiling_details": [],
            "runs": [{"id": "CS", "element": "canopy_soffit", "orientation": "horizontal", "length_ft": 40.0,
                      "source": "7/A09.26", "wall_line_ft": {"value": 34.0, "source": "A04.01"}}]}
    o = C.calcular(copy.deepcopy(base))
    assert abs(o["totales_lf"]["track de ceilings / soffits"] - 74.0) < 0.01, o["totales_lf"]
    del base["runs"][0]["wall_line_ft"]
    try:
        C.calcular(base)
    except ValueError as e:
        assert "wall_line_ft" in str(e)
    else:
        raise AssertionError("canopy_soffit sin wall_line_ft debía fallar")


if __name__ == "__main__":
    n = 0
    for k, f in list(globals().items()):
        if k.startswith("test_") and callable(f) and f.__module__ == __name__:
            f()
            n += 1
            print("OK", k)
    print(f"{n} tests OK")
