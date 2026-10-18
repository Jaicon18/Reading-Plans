#!/usr/bin/env python3
"""Tests sintéticos de partition_types.py (E24: geometría inventada, sin cantidades de proyectos reales)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from partition_types import partition_types  # noqa: E402

OK = []


def chk(n, c, m=""):
    if not c:
        raise AssertionError(f"{n}: {m}")
    OK.append(n)


def W(i, tag, L, band, el="wall", stud="3-5/8\"", rows=1, **kw):
    d = {"id": i, "tag": tag, "element": el, "stud_size": stud, "rows": rows, "length_ft": L, "band": band}
    d.update(kw)
    return d


def H(c, lo, hi):          # banda: ori H, centro c (espesor 6 pt), extensión lo..hi (pt; escala 18 pt/ft)
    return {"sheet": "X2.01", "ori": "H", "c0": c - 3, "c1": c + 3, "lo": lo, "hi": hi}


def V(c, lo, hi):
    return {"sheet": "X2.01", "ori": "V", "c0": c - 3, "c1": c + 3, "lo": lo, "hi": hi}


C = {"constants": {"plan_scale_pt_per_ft": {"value": 18.0, "source": "X2.01"}}}


def test_colineales_contiguos_un_wall():
    # un tramo recto partido por zona de altura = 1 wall; otro paralelo lejos = otro wall
    c = dict(C, walls=[W("a", "P1", 10, H(100, 0, 180)), W("b", "P1", 5, H(100, 180, 270)),
                       W("c", "P1", 5, H(400, 0, 90))])
    r = partition_types(c)["types"]["P1"]
    chk("split por altura = 1 wall", r["walls"] == 2 and abs(r["lf"] - 20) < 1e-9, r)


def test_colineal_no_contiguo():
    c = dict(C, walls=[W("a", "P1", 5, H(100, 0, 90)), W("b", "P1", 5, H(100, 200, 290))])
    chk("colineal con hueco = 2 walls", partition_types(c)["types"]["P1"]["walls"] == 2)


def test_jog():
    c = dict(C, walls=[W("a", "P2", 8, V(50, 0, 144)), W("j", "P2", 0.5, H(144, 50, 59)),
                       W("b", "P2", 8, V(59, 144, 288))])
    r = partition_types(c, modo="tramo")["types"]["P2"]
    # v68 R10: el jog no es wall aparte pero su LF suma al wall vecino (modo "tramo")
    chk("jog <= 1 ft: no es wall, su LF suma", r["walls"] == 2 and len(r["jogs"]) == 1 and abs(r["lf"] - 16.5) < 1e-9, r)
    # v70 (E28, modo "run" por default): a + jog + b es UN run continuo con quiebres = 1 wall
    r = partition_types(c)["types"]["P2"]
    chk("v70 run: jog dentro del run", r["walls"] == 1 and abs(r["lf"] - 16.5) < 1e-9, r)
    c = dict(C, walls=[W("j", "P3", 0.5, H(10, 0, 9))])
    chk("si es el único de su type, cuenta", partition_types(c)["types"]["P3"]["walls"] == 1)


def test_v67_fila_para_la_hoja():
    c = dict(C, walls=[W("a", "P2", 8, V(50, 0, 144), height_ft=10.0, detail="1/X12.01", length_printed_ft=8,
                         faces=[{"room": "R1", "layers": 1}, {"room": "R2", "layers": 1}]),
                       W("j", "P2", 0.5, H(144, 50, 59), height_ft=10.0, detail="1/X12.01"),
                       W("b", "P2", 4, V(50, 144, 216), height_ft=13.0, detail="1/X12.01")])
    bo = {"caras": [{"wall": "a", "sf": 100.0}, {"wall": "b", "sf": 50.0}, {"wall": "j", "sf": 5.0}]}
    r = partition_types(c, bo, modo="tramo")["types"]["P2"]      # v70: el jog en la Location es del modo tramo
    f = r["filas"][0]
    chk("R2 unido: un renglón, ids con +", r["walls"] == 1 and f["wall"] == "a+b+j", r)
    chk("altura ponderada por largo", abs(f["height_ft"] - (8 * 10 + 4 * 13 + 0.5 * 10) / 12.5) < 1e-3, f)
    chk("board por wall de board_out", abs(f["board_sf"] - 155.0) < 1e-6, f)
    chk("jog en la Location del vecino", "incl. jog j" in f["location"] and "R1 / R2" in f["location"], f)
    chk("status DERIVADO si un tramo no tiene cota", f["status"] == "DERIVADO" and f["source"] == "1/X12.01", f)


def test_v67_parapet_un_wall_por_run():
    P = lambda i, ln, a, L: {"id": i, "tag": "PARAPET", "element": "parapet", "stud_size": "6\" parapet",
                             "length_ft": L, "line": ln, "from_ft": a, "to_ft": a + L}
    c = dict(C, walls=[P("p1", "E", 0, 20), P("p2", "E", 20, 10), P("p3", "E", 40, 5), P("p4", "N", 0, 8)])
    t = partition_types(c)["types"]["EXT-PARAPET"]
    chk("contiguos de una line = 1 wall; hueco o línea distinta = otro", t["walls"] == 3 and abs(t["lf"] - 43) < 1e-9
        and t["filas"][0]["wall"] == "p1+p2", t)
    chk("v68 R6: sin ori + axis el run sale PENDIENTE", t["status"] == "PENDIENTE", t)


def test_nombres_no_partition():
    c = dict(C, walls=[W("x1", "EXT", 30, V(0, 0, 540), stud="6\""),
                       W("x2", "EXT", 10, V(0, 540, 720), stud="6\""),
                       W("p1", "PARAPET", 40, None, el="parapet", stud="6\" parapet"),
                       W("cw", "CANOPY COL", 4, {"sheet": "X2.01", "ori": "BOX", "c0": 0, "c1": 18, "lo": 0,
                                                 "hi": 18}, el="column_wrap"),
                       W("vh", "VEST", 6, None, el="vestibule_head"),
                       W("rs", "RS", 20, None, el="roof_step"),
                       W("tr", "TRANS", 20, None, el="ceiling_transition")])
    r = partition_types(c)
    t = r["types"]
    chk("EXT-6CFMF un wall por línea", t["EXT-6CFMF"]["walls"] == 1 and abs(t["EXT-6CFMF"]["lf"] - 40) < 1e-9, t)
    chk("EXT-PARAPET", "EXT-PARAPET" in t)
    chk("CANOPY-COL normalizado", "CANOPY-COL" in t)
    chk("otros fuera de types", {o["element"] for o in r["other_framing"]} ==
        {"vestibule_head", "roof_step", "ceiling_transition"})


def test_bulkhead_run():
    walls = [W("g1", "Q", 10, H(100, 0, 180), stud="1-5/8\"", rows=2),
             W("g2", "Q", 10, H(300, 0, 180), stud="1-5/8\"", rows=2)]
    walls += [W(f"b{i}", "BULK", 6, V(500, i * 150, i * 150 + 108), el="door_bulkhead", stud="1-5/8\"", rows=2)
              for i in range(3)]
    walls += [W("bw", "BULK", 6, V(900, 0, 108), el="door_bulkhead", stud="1-5/8\"", rows=2)]
    t = partition_types(dict(C, walls=walls))["types"]
    chk("bulkheads colineales = 1 run por frente", t["BULKHEAD-Q"]["walls"] == 2 and
        abs(t["BULKHEAD-Q"]["lf"] - 24) < 1e-9, t.get("BULKHEAD-Q"))


def test_pier_tag_manda():
    c = dict(C, walls=[W("pr", "P9", 9, {"sheet": "X2.01", "ori": "BOX", "c0": 0, "c1": 40, "lo": 0, "hi": 30},
                         el="pier")])
    chk("pier con tag interior = su tag", "P9" in partition_types(c)["types"])


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"):
            f()
    print(f"test_partition_types: {len(OK)} checks OK")
