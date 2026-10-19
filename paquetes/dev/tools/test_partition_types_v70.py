#!/usr/bin/env python3
"""Tests v70 de partition_types.py (E28: agrupa con particion.particion, MODO_DEFAULT "run"). Geometría inventada.
Correr: python3 test_partition_types_v70.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import particion  # noqa: E402
from partition_types import partition_types  # noqa: E402

C = {"constants": {"plan_scale_pt_per_ft": {"value": 18.0, "source": "Z2.01"}}}


def W(i, tag, ori, eje, lo, hi, el="wall", stud="3-5/8\"", rows=1):
    return {"id": i, "tag": tag, "element": el, "stud_size": stud, "rows": rows, "length_ft": round((hi - lo) / 18.0, 4),
            "band": {"sheet": "Z2.01", "ori": ori, "c0": eje - 3, "c1": eje + 3, "lo": lo, "hi": hi}}


def test_run_en_l_mismo_type_una_fila():
    c = dict(C, walls=[W("a", "P1", "H", 100, 0, 180), W("b", "P1", "V", 180, 100, 280)])
    t = partition_types(c, modo="run")                                       # v71: default "eje"; run explícito
    assert t["modo"] == "run" and particion.MODO_DEFAULT == "eje"
    r = t["types"]["P1"]
    assert r["walls"] == 1 and r["filas"][0]["wall"] == "a+b" and abs(r["lf"] - 20.0) < 1e-6, r
    assert partition_types(c, modo="tramo")["types"]["P1"]["walls"] == 2     # opción tramo: corta en la esquina


def test_t_no_encadena():
    c = dict(C, walls=[W("a", "P1", "H", 100, 0, 360), W("b", "P1", "V", 180, 103, 280)])
    assert partition_types(c)["types"]["P1"]["walls"] == 2


def test_pt4_bulkheads_un_wall_por_frente():
    g = lambda i, lo, hi: W(i, "Q", "V", 500, lo, hi, stud="1-5/8\"", rows=2)
    bh = lambda i, lo, hi: W(i, "Q", "V", 500, lo, hi, el="door_bulkhead", stud="1-5/8\"", rows=2)
    walls = [g("s1", 0, 40), bh("b1", 40, 148), g("s2", 148, 188), bh("b2", 188, 296), g("s3", 296, 336),
             bh("b3", 336, 444), bh("bx", 0, 108)]
    walls[-1]["band"].update(c0=897, c1=903)                                  # otro frente (otra línea)
    t = partition_types(dict(C, walls=walls))["types"]
    bhq = t["BULKHEAD-Q"]
    assert bhq["walls"] == 2 and abs(bhq["lf"] - 24.0) < 1e-6, bhq             # frente 1 (3 bulkheads) + frente 2
    assert sorted(f["wall"] for f in bhq["filas"]) == ["b1+b2+b3", "bx"], bhq["filas"]
    assert t["Q"]["walls"] == 3, t["Q"]                                       # los stubs no se unen con el bulkhead


def test_pt1_y_pt5_se_conservan():
    walls = [W("x1", "EXT", "V", 0, 0, 540, stud="6\""), W("x2", "EXT", "H", 540, 0, 180, stud="6\""),
             W("vh", "VEST", "H", 900, 0, 90, el="vestibule_head")]
    walls[1]["band"].update(c0=537, c1=543, lo=0, hi=180)
    r = partition_types(dict(C, walls=walls))
    assert r["types"]["EXT-6CFMF"]["walls"] == 2, r["types"]                  # v70c EJES: EXT en L = 2 walls
    assert [o["id"] for o in r["other_framing"]] == ["vh"]


def test_v70c_ejes_exterior_en_l_dos_walls_interior_uno():
    """Regla EJES: perímetro exterior en L = 2 walls (uno por fachada); interior en L = 1 wall (run)."""
    ext = [W("e1", "EXT", "H", 100, 0, 180, stud="6\""), W("e2", "EXT", "V", 180, 100, 280, stud="6\"")]
    r = partition_types(dict(C, walls=ext), modo="run")["types"]["EXT-6CFMF"]
    assert r["walls"] == 2 and abs(r["lf"] - 20.0) < 1e-6, r
    par = [dict(x, element="parapet", tag="PARAPET", stud_size="6\" parapet") for x in ext]
    assert partition_types(dict(C, walls=par), modo="run")["types"]["EXT-PARAPET"]["walls"] == 2
    loc = [dict(x, tag="P9", location="exterior") for x in ext]          # exterior por location del canon
    assert partition_types(dict(C, walls=loc), modo="run")["types"]["EXT-6CFMF"]["walls"] == 2
    inn = [W("i1", "P1", "H", 100, 0, 180), W("i2", "P1", "V", 180, 100, 280)]
    assert partition_types(dict(C, walls=inn), modo="run")["types"]["P1"]["walls"] == 1


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
    print("TODOS OK" if not fallas else f"{fallas} FALLA(S)")
    sys.exit(1 if fallas else 0)
