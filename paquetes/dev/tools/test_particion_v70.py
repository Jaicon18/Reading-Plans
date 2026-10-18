#!/usr/bin/env python3
"""Tests v70 de particion.py con un canon SINTÉTICO (ningún dato de proyecto). Correr: python3 test_particion_v70.py

- MODO_DEFAULT = "run" (decisión del estimador): un run en L de 2 segmentos = 1 wall; una T no encadena.
- door_bulkhead = BULKHEAD-<familia>: dos stubs G + un bulkhead entre ellos -> 3 grupos, nunca 1.
- "tramo" por componentes conexas: el resultado no depende del orden de los walls.
"""
import os
import random
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import particion as P  # noqa: E402

E = 18.0


def w(id_, tag, ori, eje, lo, hi, sheet="Z1.01", esp=4.0, **kw):
    d = {"id": id_, "tag": tag, "length_ft": round((hi - lo) / E, 4), "sheet": sheet,
         "band": {"ori": ori, "c0": eje - esp / 2, "c1": eje + esp / 2, "lo": lo, "hi": hi}}
    d.update(kw)
    return d


def canon(walls):
    return {"constants": {"plan_scale_pt_per_ft": {"value": E, "source": "sintético"}}, "walls": walls}


def grupos(r):
    return sorted((t, tuple(sorted(f["ids"]))) for t, d in r["types"].items() for f in d["filas"])


def test_default_es_run():
    assert P.MODO_DEFAULT == "run", P.MODO_DEFAULT
    assert P.particion(canon([w("A", "X1", "H", 100, 0, 90)]))["modo"] == "run"


def test_l_de_dos_segmentos_es_un_wall_por_default():
    c = canon([w("L1", "X1", "H", 100, 0, 180), w("L2", "X1", "V", 180, 100, 280)])
    r = P.particion(c)
    assert grupos(r) == [("X1", ("L1", "L2"))], grupos(r)
    r2 = P.particion(c, "tramo")                         # la opción tramo sigue partiendo en la esquina
    assert len(grupos(r2)) == 2, grupos(r2)


def test_t_no_encadena_por_default():
    c = canon([w("T1", "X1", "H", 100, 0, 360), w("T2", "X1", "V", 180, 102, 280)])   # T2 contra el costado de T1
    r = P.particion(c)
    assert grupos(r) == [("X1", ("T1",)), ("X1", ("T2",))], grupos(r)


def test_bulkhead_entre_dos_stubs_g():
    """G | BULKHEAD | G colineales y contiguos: 3 grupos (G, BULKHEAD-G, G) en los dos modos; nunca 1."""
    ws = [w("G-a", "G", "H", 100, 0, 90), w("BH", "G1", "H", 100, 91, 200, element="door_bulkhead"),
          w("G-b", "G", "H", 100, 201, 290)]
    for modo in P.MODOS:
        r = P.particion(canon(ws), modo)
        g = grupos(r)
        assert g == [("BULKHEAD-G", ("BH",)), ("G", ("G-a",)), ("G", ("G-b",))], (modo, g)
    # el bulkhead con el MISMO tag G que sus stubs tampoco se une (antes: 1 solo wall G)
    ws1 = [dict(x) for x in ws]
    ws1[1] = dict(ws1[1], tag="G")
    for modo in P.MODOS:
        g = grupos(P.particion(canon(ws1), modo))
        assert len(g) == 3 and ("BULKHEAD-G", ("BH",)) in g, (modo, g)
    # sin tag: la familia sale de bulkhead_of
    ws2 = [dict(x) for x in ws]
    ws2[1] = dict(ws2[1], tag=None, bulkhead_of="G1")
    assert ("BULKHEAD-G", ("BH",)) in grupos(P.particion(canon(ws2)))


def test_familia_igual_a_partition_types():
    import partition_types as PT
    for t in ("G", "G1", "A1K", "X12"):
        assert P.familia(t) == PT._familia(t), t


def test_tramo_no_depende_del_orden():
    """A-B-C colineales: A toca B y B toca C, A no toca C. La unión voraz dependía del orden."""
    base = [w("A", "X1", "H", 100, 0, 100), w("C", "X1", "H", 100, 210, 300), w("B", "X1", "H", 100, 104, 206),
            w("D", "X1", "H", 100, 400, 480), w("F", "X1", "V", 600, 0, 200), w("H", "X1", "V", 600, 205, 300)]
    ref = grupos(P.particion(canon(base), "tramo"))
    assert ("X1", ("A", "B", "C")) in ref, ref
    rnd = random.Random(7)
    for _ in range(25):
        ws = list(base)
        rnd.shuffle(ws)
        for modo in P.MODOS:
            assert grupos(P.particion(canon(ws), modo)) == grupos(P.particion(canon(base), modo)), modo


if __name__ == "__main__":
    fallas = 0
    for k, f in sorted(globals().items()):
        if k.startswith("test_") and callable(f):
            try:
                f()
                print("OK  ", k)
            except Exception as e:  # noqa: BLE001 (AttributeError con código viejo = falla)
                fallas += 1
                print("FALLA", k, e)
    print(f"{'TODOS OK' if not fallas else str(fallas) + ' FALLA(S)'}")
    sys.exit(1 if fallas else 0)
