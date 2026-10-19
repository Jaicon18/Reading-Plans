#!/usr/bin/env python3
"""Tests sintéticos v68 de partition_types.py (R6-R11). E24: geometría inventada, sin cantidades de proyectos reales."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from partition_types import partition_types  # noqa: E402

OK = []
C = {"constants": {"plan_scale_pt_per_ft": {"value": 18.0, "source": "X2.01"}}}


def chk(n, c, m=""):
    if not c:
        raise AssertionError(f"{n}: {m}")
    OK.append(n)


def W(i, tag, L, band, el="wall", stud="3-5/8\"", rows=1, **kw):
    d = {"id": i, "tag": tag, "element": el, "stud_size": stud, "rows": rows, "length_ft": L, "band": band}
    d.update(kw)
    return d


def H(c, lo, hi, e=6):
    return {"sheet": "X2.01", "ori": "H", "c0": c - e / 2, "c1": c + e / 2, "lo": lo, "hi": hi}


def V(c, lo, hi, e=6):
    return {"sheet": "X2.01", "ori": "V", "c0": c - e / 2, "c1": c + e / 2, "lo": lo, "hi": hi}


def P(i, ln, a, L, ori=None, axis=None):
    d = {"id": i, "tag": "PARAPET", "element": "parapet", "stud_size": "6\" parapet", "length_ft": L,
         "line": ln, "from_ft": a, "to_ft": a + L}
    if ori:
        d.update(ori=ori, axis=axis)
    return d


def test_r6_parapet_straight_run_geometrico():
    # misma etiqueta de lado ("N") pero dos ejes distintos (step de 2.5 ft) = 2 walls + el step = 3
    c = dict(C, walls=[P("a", "N", 0, 12, "H", 0.0), P("s", "N", 12, 2.5, "V", 12.0), P("b", "N", 14.5, 30, "H", 2.5)])
    t = partition_types(c)["types"]["EXT-PARAPET"]
    chk("R6 step entre ejes parte el run", t["walls"] == 3 and abs(t["lf"] - 44.5) < 1e-9 and t["status"] == "OK", t)
    # cambio de altura en el mismo eje = 1 wall
    c = dict(C, walls=[P("a", "7", 0, 20, "V", 50.0), P("b", "7", 20, 10, "V", 50.1)])
    t = partition_types(c)["types"]["EXT-PARAPET"]
    chk("R6 mismo eje (<= 3\") y contiguo = 1 wall", t["walls"] == 1 and t["filas"][0]["wall"] == "a+b", t)
    c = dict(C, walls=[P("a", "W", 0, 20), P("b", "W", 20, 10)])
    r = partition_types(c)
    chk("R6 sin geometría = PENDIENTE + aviso", r["types"]["EXT-PARAPET"]["status"] == "PENDIENTE"
        and any("R6" in a for a in r["avisos"]), r["avisos"])


def test_r7_bulkhead_familia():
    walls = [W("q", "Q", 10, H(100, 0, 180), stud="1-5/8\"", rows=2),
             W("q1", "Q1", 3, V(500, 120, 168), stud="1-5/8\"", rows=2)]
    walls += [W("b1", "Q", 6, V(300, 0, 108), el="door_bulkhead", stud="1-5/8\"", rows=2),
              W("b2", "Q1", 6, V(500, 0, 108), el="door_bulkhead", stud="1-5/8\"", rows=2),
              W("b3", "Q1", 6, V(500, 180, 288), el="door_bulkhead", stud="1-5/8\"", rows=2)]
    t = partition_types(dict(C, walls=walls))["types"]
    chk("R7 BULKHEAD por familia (Q1 -> Q), un wall por frente", "BULKHEAD-Q1" not in t and
        t["BULKHEAD-Q"]["walls"] == 2 and abs(t["BULKHEAD-Q"]["lf"] - 18) < 1e-9, t.get("BULKHEAD-Q"))


def test_r8_chase_una_cara_un_wall():
    ch = W("ch", "K1", 7, H(100, 0, 126, e=20), el="chase", rows=2,
           faces=[{"room": "R1", "layers": 1, "height_ft": 9}, {"room": "R2", "layers": 1, "height_ft": 9}])
    bo = {"caras": [{"wall": "ch", "sf": 100.0}]}
    t = partition_types(dict(C, walls=[ch]), bo)["types"]["K1"]
    chk("R8 chase de 2 caras = 2 walls", t["walls"] == 2 and abs(t["lf"] - 14) < 1e-9, t)
    chk("R8 board repartido por cara", all(abs(f["board_sf"] - 50.0) < 1e-9 for f in t["filas"]), t["filas"])


def test_r9_column_wrap_caras_con_board():
    box = {"sheet": "X2.01", "ori": "BOX", "c0": 0, "c1": 30, "lo": 0, "hi": 30}
    cw = W("cw", "K1", 8.0, box, el="column_wrap",
           faces=[{"room": "R1", "height_ft": 9, "length_ft": 1.5}, {"room": "R2", "height_ft": 9, "length_ft": 2.0},
                  {"room": "EXTERIOR", "height_ft": 0, "length_ft": 4.5}])
    t = partition_types(dict(C, walls=[cw]))["types"]["K1"]
    chk("R9 LF = caras con board", abs(t["lf"] - 3.5) < 1e-9 and t["status"] == "OK", t)
    cc = W("cc", "CANOPY COL", 6.0, box, el="column_wrap", location="exterior",
           fos_chain={"value": [1.5], "source": "9/X9.01 1'-6\" overall"})
    t = partition_types(dict(C, walls=[cc]))["types"]["CANOPY-COL"]
    chk("R9 fos_chain sin FOS = PENDIENTE", t["status"] == "PENDIENTE", t)
    cc["fos_chain"] = {"value": [1.25, 0.25], "source": "9/X9.01 1'-3\" FOS + 3\" FOS"}
    t = partition_types(dict(C, walls=[cc]))["types"]["CANOPY-COL"]
    chk("R9 fos_chain con FOS = OK", t["status"] == "OK", t)


def test_r10_return_suma():
    walls = [W("a", "K2", 10, H(100, 0, 180)), W("r1", "K2", 0.6, V(0, 100, 111)), W("r2", "K2", 0.6, V(180, 100, 111))]
    t = partition_types(dict(C, walls=walls))["types"]["K2"]
    chk("R10 returns suman al wall, 1 wall", t["walls"] == 1 and abs(t["lf"] - 11.2) < 1e-9
        and t["filas"][0]["wall"] == "a+r1+r2", t)


def test_r11_aviso_solape():
    walls = [W("x", "K3", 2, H(100, 91, 127)), W("y", "K4", 10, V(94, 0, 180, e=6))]
    r = partition_types(dict(C, walls=walls))
    chk("R11 extremo pasado de la cara del perpendicular = aviso", any("R11" in a and a.startswith("x ") for a in r["avisos"]),
        r["avisos"])
    walls = [W("x", "K3", 2, H(100, 97, 133)), W("y", "K4", 10, V(94, 0, 180, e=6))]
    r = partition_types(dict(C, walls=walls))
    chk("R11 extremo en la cara = sin aviso", not any("R11" in a for a in r["avisos"]), r["avisos"])


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"):
            f()
    print(f"test_partition_types_v68: {len(OK)} checks OK")
