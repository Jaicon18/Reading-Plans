#!/usr/bin/env python3
"""Tests de studs_nodos.py con datos de un proyecto de prueba (arbitraje #10). Correr: python3 test_studs_nodos.py"""
import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import studs_nodos as S  # noqa: E402


def g_office():
    """G largo W36 + stub W43 en el office front + exterior W57 (datos sintéticos)."""
    return {
        "walls": [
            {"id": "W36", "tag": "G", "stud_size": "1-5/8\"", "length_ft": 11.5, "oc_in": 16, "rows": 2,
             "height_ft": 15.25},
            {"id": "W43", "tag": "G", "stud_size": "1-5/8\"", "length_ft": 3.5, "oc_in": 16, "rows": 2,
             "height_ft": 15.25},
            {"id": "W57", "tag": "EXT", "stud_size": "6\"", "length_ft": 47.413, "oc_in": 16, "rows": 1,
             "height_ft": 14.25},
        ],
        "nodes": [
            {"id": "N1", "kind": "T", "branch": "W36", "through": "W57"},
            {"id": "N2", "kind": "L", "walls": ["W43", "W36"]},
            {"id": "N3", "kind": "vendor_end", "wall": "W43"},
            {"id": "N4", "kind": "free", "wall": "W57"},
            {"id": "N5", "kind": "free", "wall": "W57"},
        ],
    }


def test_g_largo_22_pcs():
    out = S.contar(g_office())
    w = {r["id"]: r for r in out["walls"]}
    # arbitraje #9/#10: 11 por row (10 de campo + 1 en la T exterior)
    assert w["W36"]["pcs_full"] == 22, w["W36"]
    assert abs(w["W36"]["lf"] - 22 * 15.25) < 0.01
    # stub: (ROUNDUP(<n>/1.333)+1 = 4 + L 1) x 2 + 1 vendor_end = 11
    assert w["W43"]["pcs_full"] == 11, w["W43"]


def test_ventana_cripples():
    d = {"walls": [{"id": "E", "stud_size": "6\"", "length_ft": 24.0, "oc_in": 16, "rows": 1, "height_ft": 14.25,
                    "openings": [{"ref": "W-A", "ro_w_ft": 8.0, "head_ft": 8.5, "sill_ft": 6.5}]}],
         "nodes": [{"id": "a", "kind": "free", "wall": "E"}, {"id": "b", "kind": "free", "wall": "E"}]}
    r = S.contar(d)["walls"][0]
    # campo 18+1=19; dentro FLOOR(8/1.333)=6; +4 jambs -> 17 full; cripples 6 x (5.75 + 6.5)
    assert r["pcs_full"] == 17
    assert abs(r["lf"] - (17 * 14.25 + 6 * (14.25 - 8.5 + 6.5))) < 0.01


def test_zona_12_esquina():
    d = {"walls": [{"id": "S", "stud_size": "6\"", "length_ft": 20.0, "oc_in": 16, "rows": 1, "height_ft": 11.0,
                    "zones": [{"from_ft": 0, "to_ft": 6, "oc_in": 12}]}],
         "nodes": [{"id": "a", "kind": "free", "wall": "S"}, {"id": "b", "kind": "free", "wall": "S"}]}
    r = S.contar(d)["walls"][0]
    assert r["pcs_full"] == 1 + 6 + 11  # 6 @12" + ROUNDUP(14/1.333)=11


def _falla(d, txt):
    try:
        S.contar(d)
    except ValueError as e:
        assert txt in str(e), str(e)
        return
    raise AssertionError("debía fallar: " + txt)


def test_dato_malo_extremo_sin_nodo():
    d = g_office()
    d["nodes"] = [n for n in d["nodes"] if n["id"] != "N3"]        # se olvidó el office front del stub
    _falla(d, "exactamente 2 extremos")


def test_dato_malo_junta_contada_dos_veces():
    d = g_office()
    d["nodes"].append({"id": "N2bis", "kind": "L", "walls": ["W36", "W43"]})   # la misma esquina otra vez
    _falla(d, "exactamente 2 extremos")


def test_dato_malo_kind():
    d = copy.deepcopy(g_office())
    d["nodes"][0]["kind"] = "esquina"
    _falla(d, "desconocido")


def test_dato_malo_abertura_ancha():
    d = g_office()
    d["walls"][1]["openings"] = [{"ref": "x", "ro_w_ft": 4.0, "head_ft": 7.0}]
    _falla(d, "más ancha")


def _par_split(kind_corte):
    d = {"walls": [{"id": "X5-1a", "stud_size": "6\"", "length_ft": 11.948, "oc_in": 16, "rows": 1, "height_ft": 15.25},
                   {"id": "X5-1b", "stud_size": "6\"", "length_ft": 3.759, "oc_in": 16, "rows": 1, "height_ft": 13.0}],
         "nodes": [{"id": "a", "kind": "free", "wall": "X5-1a"}, {"id": "b", "kind": "free", "wall": "X5-1b"}]}
    if kind_corte == "split":
        d["nodes"].append({"id": "c", "kind": "split", "walls": ["X5-1a", "X5-1b"], "why": "grid B"})
    else:   # dato malo de #11B: el corte declarado como dos extremos libres
        d["nodes"] += [{"id": "c1", "kind": "free", "wall": "X5-1a"}, {"id": "c2", "kind": "free", "wall": "X5-1b"}]
    return d


def test_split_no_duplica_stud_del_corte():
    bien = {r["id"]: r for r in S.contar(_par_split("split"))["walls"]}
    mal = {r["id"]: r for r in S.contar(_par_split("free"))["walls"]}
    # un wall continuo de 15.707 ft tendría ROUNDUP(15.707/1.333)+1 = 13 studs; partido: 10 + 4 = 14 con 'free'  [ciego-ok]
    assert bien["X5-1a"]["pcs_full"] + bien["X5-1b"]["pcs_full"] == 13, bien
    assert mal["X5-1a"]["pcs_full"] + mal["X5-1b"]["pcs_full"] == 14, mal


def test_split_entre_tipos_distintos_falla():
    d = _par_split("split")
    d["walls"][1]["oc_in"] = 24
    _falla(d, "no es el mismo wall partido")


def test_abut_office_front_g_22():
    """G largo que muere contra el stub entre dos vendor frames (10/A12.01): abut, no T."""
    d = {"walls": [
            {"id": "G8", "stud_size": "1-5/8\"", "length_ft": 11.5, "oc_in": 16, "rows": 2, "height_ft": 15.25},
            {"id": "G6", "stud_size": "1-5/8\"", "length_ft": 3.256, "oc_in": 16, "rows": 2, "height_ft": 15.25},
            {"id": "E1", "stud_size": "6\"", "length_ft": 50.385, "oc_in": 16, "rows": 1, "height_ft": 14.25}],
         "nodes": [{"id": "t", "kind": "T", "branch": "G8", "through": "E1"},
                   {"id": "ab", "kind": "abut", "wall": "G8", "into": "G6", "source": "10/A12.01"},
                   {"id": "v1", "kind": "vendor_end", "wall": "G6"}, {"id": "v2", "kind": "vendor_end", "wall": "G6"},
                   {"id": "f1", "kind": "free", "wall": "E1"}, {"id": "f2", "kind": "free", "wall": "E1"}]}
    w = {r["id"]: r for r in S.contar(d)["walls"]}
    assert w["G8"]["pcs_full"] == 22, w["G8"]          # #11A/#11B daban 24 (T en las dos puntas)
    d["nodes"][1] = {"id": "ab", "kind": "T", "branch": "G8", "through": "G6"}
    assert {r["id"]: r for r in S.contar(d)["walls"]}["G8"]["pcs_full"] == 24


def test_abut_sin_source_falla():
    d = _par_split("split")
    d["nodes"] = [{"id": "a", "kind": "free", "wall": "X5-1a"}, {"id": "b", "kind": "free", "wall": "X5-1b"},
                  {"id": "c", "kind": "abut", "wall": "X5-1a", "into": "X5-1b"},
                  {"id": "d", "kind": "free", "wall": "X5-1b"}]
    _falla(d, "abut exige source")


if __name__ == "__main__":
    n = 0
    for k, f in list(globals().items()):
        if k.startswith("test_") and callable(f):
            f()
            n += 1
            print("OK", k)
    print(f"{n} tests OK")
