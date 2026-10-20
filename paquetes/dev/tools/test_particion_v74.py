#!/usr/bin/env python3
"""test_particion_v74.py — reglas R74.1–R74.6 de particion.py (modo "eje") y su paso por partition_types.py.

Datos 100 % inventados: types P / Q / R / QB (sin relación con ningún set), hoja Z1.01, ids X* / Y*, escala
18 pt/ft. Cada caso arma la geometría mínima que dispara la regla y la que NO la dispara.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import particion as P          # noqa: E402
import partition_types as PT   # noqa: E402

FALLAS = []


def caso(nombre):
    def deco(fn):
        try:
            fn()
            print("OK  ", nombre)
        except AssertionError as e:
            FALLAS.append(nombre)
            print("FALLA", nombre, e)
        return fn
    return deco


def H(wid, tag, y0, y1, x0, x1, tags=("T1",), **kw):
    d = {"id": wid, "tag": tag, "element": "wall", "sheet": "Z1.01", "length_ft": round((x1 - x0) / 18.0, 3),
         "tag_ids": list(tags), "band": {"ori": "H", "c0": y0, "c1": y1, "lo": x0, "hi": x1}}
    d.update(kw)
    return d


def V(wid, tag, x0, x1, y0, y1, tags=("T1",), **kw):
    d = {"id": wid, "tag": tag, "element": "wall", "sheet": "Z1.01", "length_ft": round((y1 - y0) / 18.0, 3),
         "tag_ids": list(tags), "band": {"ori": "V", "c0": x0, "c1": x1, "lo": y0, "hi": y1}}
    d.update(kw)
    return d


def canon(ws):
    return {"constants": {"plan_scale_pt_per_ft": {"value": 18.0}}, "walls": ws}


def frente():
    """Frente de oficinas inventado: línea V con returns Q (con tag, 9 pt) y bulkheads entre ellos; un remate sin
    tag de 9 pt tipado P por la nota general (P mide 7 pt) en la punta norte; un stub P de 6" de 9 pt en la punta
    sur; los walls P con tag miden 7 pt."""
    return [
        V("X1", "P", 300, 309, 0, 36, tags=()),                           # remate sin tag, espesor de Q
        {"id": "XB1", "tag": "Q", "element": "door_bulkhead", "sheet": "Z1.01", "length_ft": 7.5, "tag_ids": [],
         "band": {"ori": "V", "c0": 300, "c1": 309, "lo": 36, "hi": 171}},
        V("X2", "Q", 300, 309, 171, 225, tags=("T2",)),                   # return con tag
        {"id": "XB2", "tag": "Q", "element": "door_bulkhead", "sheet": "Z1.01", "length_ft": 7.5, "tag_ids": [],
         "band": {"ori": "V", "c0": 300, "c1": 309, "lo": 225, "hi": 360}},
        V("X3", "P", 300, 309, 360, 366, tags=()),                        # stub sin tag, espesor de Q
        H("X4", "Q", 171, 180, 309, 500, tags=("T3",)),                   # wall Q que llega en T al frente
        H("X5", "P", 600, 607, 0, 250, tags=("T4",)),                     # walls P con tag (7 pt)
        V("X6", "P", 700, 707, 400, 600, tags=("T5",)),
    ]


@caso("R74.1 remate sin tag con espesor de otro type en su línea toma ese type (no el de la nota general)")
def _():
    r = P.particion(canon(frente()), "eje")
    assert r["retipados"].get("X1") == "Q", r["retipados"]
    assert r["retipados"].get("X3") == "Q", r["retipados"]
    assert "X1" in [i for f in r["types"]["Q"]["filas"] for i in f["ids"]], r["types"]["Q"]
    assert r["types"]["P"]["walls"] == 2, r["types"]["P"]


@caso("R74.1 no retipa: espesor igual al de su type, o sin walls con tag de otro type en su línea")
def _():
    ws = frente()
    ws[0]["band"].update(c0=300, c1=307)                                   # el remate mide 7 pt = P
    r = P.particion(canon(ws), "eje")
    assert "X1" not in r["retipados"], r["retipados"]
    ws = [V("Y1", "P", 300, 309, 0, 36, tags=()), H("Y2", "P", 600, 607, 0, 250, tags=("T4",)),
          V("Y3", "Q", 800, 809, 0, 90, tags=("T2",))]                     # Q con tag existe pero en OTRA línea
    r = P.particion(canon(ws), "eje")
    assert r["retipados"] == {}, r["retipados"]


@caso("R74.2 stub sin tag <= 6\" que no toca un wall con tag de su type: ni wall ni LF del type (va a stubs)")
def _():
    r = P.particion(canon(frente()), "eje")
    q = r["types"]["Q"]
    assert [s["ids"] for s in q.get("stubs") or []] == [["X3"]], q
    assert q["walls"] == 3, q                                              # X1 (remate) + X2 + X4
    assert abs(q["lf"] - (2.0 + 3.0 + 10.611)) < 0.01, q


@caso("R74.2 un stub que SÍ toca por el extremo a un wall con tag de su type es su return (se suma)")
def _():
    ws = [H("Y1", "Q", 0, 9, 0, 180, tags=("T1",)), V("Y2", "Q", 171, 180, 9, 15, tags=())]
    r = P.particion(canon(ws), "eje")
    q = r["types"]["Q"]
    assert q["walls"] == 1 and abs(q["lf"] - 10.333) < 0.01, q
    assert not q.get("stubs"), q


def alcove(tipo_u="P"):
    """Línea R (con tag) partida por un nicho en U sin tag que abre entre sus dos tramos."""
    return [V("Y1", "R", 100, 110, 0, 200, tags=("T1",)), V("Y2", "R", 100, 110, 290, 500, tags=("T2",)),
            H("Y3", tipo_u, 196, 203, 60, 100, tags=()), V("Y4", tipo_u, 53, 60, 196, 294, tags=()),
            H("Y5", tipo_u, 287, 294, 60, 100, tags=()), H("Y6", tipo_u, 600, 607, 0, 200, tags=("T3",))]


@caso("R74.3 grupo sin tag que cierra el hueco entre dos tramos colineales de otro type = nicho (no es wall)")
def _():
    r = P.particion(canon(alcove()), "eje")
    p = r["types"]["P"]
    assert p["walls"] == 1, p                                              # solo Y6
    assert [a["ids"] for a in p.get("anexos") or []] == [["Y3", "Y4", "Y5"]] or \
        sorted(p["anexos"][0]["ids"]) == ["Y3", "Y4", "Y5"], p
    assert sorted(p["anexos"][0]["abre_en"]) == ["Y1", "Y2"], p


@caso("R74.3 protección: U sin tag que no abre en otra línea sigue siendo UN wall")
def _():
    ws = [w for w in alcove() if w["id"] not in ("Y1", "Y2")]
    r = P.particion(canon(ws), "eje")
    assert r["types"]["P"]["walls"] == 2, r["types"]["P"]


@caso("R74.4 bulkheads colineales con returns de otro type en los huecos = UN wall por frente")
def _():
    r = P.particion(canon(frente()), "eje")
    b = r["types"]["BULKHEAD-Q"]
    assert b["walls"] == 1 and abs(b["lf"] - 15.0) < 0.01, b


@caso("R74.4 dos bulkheads colineales con hueco LARGO y vacío entre ellos = dos walls")
def _():
    ws = [{"id": f"XB{k}", "tag": "Q", "element": "door_bulkhead", "sheet": "Z1.01", "length_ft": 7.5,
           "tag_ids": [], "band": {"ori": "V", "c0": 300, "c1": 309, "lo": lo, "hi": lo + 135}}
          for k, lo in ((1, 0), (2, 400))]
    r = P.particion(canon(ws), "eje")
    assert r["types"]["BULKHEAD-Q"]["walls"] == 2, r["types"]["BULKHEAD-Q"]
    for w in ws:
        w["stud_size"] = "1-5/8\""
    ws.append(V("Y9", "Q", 900, 909, 0, 90, tags=("T2",), stud_size="1-5/8\""))
    assert PT.partition_types(canon(ws))["types"]["BULKHEAD-Q"]["walls"] == 2


@caso("R74.5 box sin tag con la huella de un box con tag = el mismo elemento (no cuenta)")
def _():
    box = {"ori": "BOX", "c0": 10, "c1": 50, "lo": 10, "hi": 40}
    ws = [{"id": "Y1", "tag": "R", "element": "pier", "sheet": "Z1.01", "length_ft": 3.0, "tag_ids": ["T9"],
           "band": dict(box)},
          {"id": "Y2", "tag": "EXT", "element": "pier", "sheet": "Z1.01", "length_ft": 3.1, "tag_ids": [],
           "band": dict(box), "stud_size": "6\"", "location": "exterior"}]
    r = P.particion(canon(ws), "eje")
    assert r["duplicados"] == {"Y2": "Y1"}, r["duplicados"]
    assert "EXT-6CFMF" not in r["types"] and r["types"]["R"]["walls"] == 1, r["types"]


@caso("R74.6 EXT con stud conocido -> EXT-<stud>CFMF; dos lecturas EXT / EXT-6CFMF dan un solo type")
def _():
    ws = [H("Y1", "EXT", 0, 9, 0, 360, tags=(), stud_size="6\"", location="exterior"),
          V("Y2", "EXT-6CFMF", 0, 9, 400, 700, tags=(), stud_size="6\"", location="exterior")]
    r = P.particion(canon(ws), "eje")
    assert list(r["types"]) == ["EXT-6CFMF"] and r["types"]["EXT-6CFMF"]["walls"] == 2, r["types"]


@caso("partition_types (ruta del Excel) da lo mismo que particion: types, walls, LF; stub y nicho en other_framing")
def _():
    ws = frente() + [w for w in alcove() if not w["id"].startswith("Y6")]
    for w in ws:
        w.setdefault("stud_size", "3-5/8\"")
    c = canon(ws)
    a = P.particion(c, "eje")
    b = PT.partition_types(c)
    for t in ("P", "Q", "R", "BULKHEAD-Q"):
        assert a["types"][t]["walls"] == b["types"][t]["walls"], (t, a["types"][t], b["types"][t])
        assert abs(a["types"][t]["lf"] - b["types"][t]["lf"]) < 0.01, (t, a["types"][t]["lf"], b["types"][t]["lf"])
    els = {o["element"] for o in b["other_framing"]}
    assert {"stub", "alcove"} <= els, els


@caso("las reglas no dependen del orden de los walls en el canon")
def _():
    ws = frente() + alcove()
    a = P.particion(canon(ws), "eje")
    b = P.particion(canon(list(reversed(ws))), "eje")
    ka = {t: (d["walls"], d["lf"]) for t, d in a["types"].items()}
    kb = {t: (d["walls"], d["lf"]) for t, d in b["types"].items()}
    assert ka == kb, (ka, kb)


if __name__ == "__main__":
    print(f"{'OK' if not FALLAS else 'FALLAS'}: {len(FALLAS)} falla(s)")
    sys.exit(1 if FALLAS else 0)
