#!/usr/bin/env python3
"""Tests de etapas.py con datos de JUGUETE fabricados aquí (ningún proyecto real). Correr: python3 test_etapas.py"""
import json
import os
import sys
import tempfile
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import etapas as T  # noqa: E402
import comparar as C  # noqa: E402

E = 18.0
FALLOS = []


def check(cond, msg):
    if not cond:
        FALLOS.append(msg)


def w(id_, tag, eje, lo, hi, tag_ids=None):
    d = {"id": id_, "tag": tag, "length_ft": round((hi - lo) / E, 4), "sheet": "Z1.01",
         "band": {"ori": "H", "c0": eje - 2, "c1": eje + 2, "lo": lo, "hi": hi}}
    if tag_ids:
        d["tag_ids"] = tag_ids
    return d


def canon(walls):
    return {"constants": {"plan_scale_pt_per_ft": {"value": E, "source": "sintético"}}, "walls": walls}


def inventario():
    tag = lambda i, t, x, y: {"id": i, "type": t, "page": 1, "sheet": "Z1.01", "center_pt": [x, y]}
    return {"sheets": [{"page": 1, "sheet": "Z1.01", "inventariable": True}],
            "partition_types": {"schedule": [{"type": "X1"}, {"type": "X2"}]},
            "ocurrencias": {"partition_tag": [tag("PT0001", "X1", 200, 110), tag("PT0002", "X2", 200, 310),
                                              tag("PT0003", "X2", 900, 900)],
                            "partition_ambiguo": [], "partition_candidato": []},
            "no_inventariables": [], "avisos": []}


def escribir(d, nombre, sub, obj):
    os.makedirs(os.path.join(d, sub), exist_ok=True)
    with open(os.path.join(d, sub, nombre), "w") as f:
        json.dump(obj, f)


def armar(d, inv, ca, cb, rev=True):
    escribir(d, "inventario.json", "1_inventario", inv)
    escribir(d, "canon_A.json", "2_lectura", ca)
    escribir(d, "canon_B.json", "2_lectura", cb)
    if rev:
        time.sleep(0.02)
        escribir(d, "revision.json", "3_revision", C.comparar(ca, cb, inv))


def main():
    A = canon([w("A1", "X1", 100, 100, 460, ["PT0001"]), w("A2", "X2", 300, 100, 460)])
    B = canon([w("B1", "X1", 100, 100, 460), w("B2", "X2", 300, 100, 460)])

    # 1. carpeta vacía: falla por los cuatro archivos; estado pide la etapa 1
    with tempfile.TemporaryDirectory() as d:
        f, _ = T.estructura(d)
        check(len(f) == 4 and all(x.startswith("falta") for x in f), f"1 vacía: {f}")
        _, sig = T.estado(d)
        check(sig.startswith("ETAPA 1"), f"1 estado: {sig}")

    # 2. todo en disco: PT0003 sin wall en A ni B -> comparar lo alerta -> PASA (la alerta queda a la vista)
    with tempfile.TemporaryDirectory() as d:
        armar(d, inventario(), A, B)
        f, av = T.estructura(d)
        check(f == [], f"2 debería pasar: {f}")
        fc, _ = T.compuerta(d)
        check(any(x.startswith("reglas:") for x in fc), f"2 v72b: sin canon conciliado reglas.py falla: {fc}")
        check(any("tag_ids" in x for x in av), f"2 aviso tag_ids: {av}")
        check(any("alertas 1" in x for x in av), f"2 aviso alertas: {av}")
        _, sig = T.estado(d)
        check(sig.startswith("ETAPA 3→4"), f"2 estado: {sig}")
        check(T.main(["etapas.py", "compuerta", d]) == 1, "2 rc (v72b: reglas.py sin canon)")

    # 3. revisión manipulada: se borra la alerta de PT0003 -> FALLA "sin wall y sin alerta"
    with tempfile.TemporaryDirectory() as d:
        armar(d, inventario(), A, B)
        p = os.path.join(d, "3_revision", "revision.json")
        rev = json.load(open(p))
        rev["alertas"] = [x for x in rev["alertas"] if x.get("kind") != "tag sin wall"]
        json.dump(rev, open(p, "w"))
        f, _ = T.compuerta(d)
        check(any("PT0003" in x and "sin alerta" in x for x in f), f"3: {f}")
        check(T.main(["etapas.py", "compuerta", d]) == 1, "3 rc")

    # 4. inventario con un tag nuevo que la revisión no cubre -> FALLA (revisión de otro inventario / vencida)
    with tempfile.TemporaryDirectory() as d:
        armar(d, inventario(), A, B)
        inv = inventario()
        inv["ocurrencias"]["partition_tag"].append({"id": "PT0004", "type": "X1", "page": 1, "sheet": "Z1.01",
                                                    "center_pt": [50, 50]})
        time.sleep(0.02)
        escribir(d, "inventario.json", "1_inventario", inv)
        f, _ = T.compuerta(d)
        check(any("PT0004" in x for x in f), f"4 cobertura: {f}")
        check(any("vencida" in x for x in f), f"4 vencida: {f}")

    # 5. lectura B rehecha después de la revisión -> FALLA vencida
    with tempfile.TemporaryDirectory() as d:
        armar(d, inventario(), A, B)
        time.sleep(0.02)
        escribir(d, "canon_B.json", "2_lectura", B)
        f, _ = T.compuerta(d)
        check(any("vencida" in x and "canon_B" in x for x in f), f"5: {f}")

    # 6. recorte no verificado en el inventario -> FALLA
    with tempfile.TemporaryDirectory() as d:
        inv = inventario()
        inv["avisos"] = ["PNG NO VERIFICADO: recortes/PT0001.png"]
        armar(d, inv, A, B)
        f, _ = T.compuerta(d)
        check(any("PNG NO VERIFICADO" in x for x in f), f"6: {f}")

    # 7. JSON roto -> FALLA; layout plano aceptado
    with tempfile.TemporaryDirectory() as d:
        for n, o in (("inventario.json", inventario()), ("canon_A.json", A), ("canon_B.json", B)):
            json.dump(o, open(os.path.join(d, n), "w"))
        time.sleep(0.02)
        open(os.path.join(d, "revision.json"), "w").write("{roto")
        f, _ = T.estructura(d)
        check(len(f) == 1 and "no es JSON válido" in f[0], f"7: {f}")
        json.dump(C.comparar(A, B, inventario()), open(os.path.join(d, "revision.json"), "w"))
        f, _ = T.estructura(d)
        check(f == [], f"7 plano: {f}")

    # 9. v72b: proyecto sintético completo (fixture_reglas) -> la compuerta corre reglas.py y PASA
    with tempfile.TemporaryDirectory() as d:
        import fixture_reglas
        fixture_reglas.crear(d)
        f, _ = T.compuerta(d)
        check(f == [], f"9 fixture: {f}")
        check(os.path.isfile(os.path.join(d, "reglas_out.json")), "9 reglas_out.json")

    # 8. un tag sin wall en una lectura pero con wall en la otra -> no falla (queda como ítem de revisión)
    with tempfile.TemporaryDirectory() as d:
        B2 = canon([w("B1", "X1", 100, 100, 460), w("B2", "X2", 300, 100, 460), w("B3", "X2", 900, 850, 950)])
        armar(d, inventario(), A, B2)
        f, av = T.estructura(d)
        check(f == [], f"8: {f}")
        check(any("solo_B 1" in x for x in av), f"8 aviso: {av}")

    # 9. unir: fragmentos por hoja -> un canon; id repetido y escala distinta = error
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "A"))
        f1 = canon([w("A1", "X1", 100, 100, 460)])
        f2 = canon([w("A2", "X2", 300, 100, 460)])
        json.dump(f1, open(os.path.join(d, "A", "Z1.01.json"), "w"))
        json.dump(f2, open(os.path.join(d, "A", "Z1.02.json"), "w"))
        out = os.path.join(d, "canon_A.json")
        check(T.main(["etapas.py", "unir", os.path.join(d, "A"), out]) == 0, "9 rc unir")
        c = json.load(open(out))
        check([x["id"] for x in c["walls"]] == ["A1", "A2"], f"9 walls: {c['walls']}")
        check(c["constants"]["plan_scale_pt_per_ft"]["value"] == E, "9 constants")
        f3 = canon([w("A1", "X1", 500, 100, 460)])
        f3["constants"]["plan_scale_pt_per_ft"]["value"] = 9.0
        json.dump(f3, open(os.path.join(d, "A", "Z1.03.json"), "w"))
        _, err = T.unir(os.path.join(d, "A"))
        check(any("repetido" in x for x in err) and any("plan_scale_pt_per_ft" in x for x in err), f"9 errores: {err}")
        check(T.main(["etapas.py", "unir", os.path.join(d, "A"), out]) == 1, "9 rc error")

    if FALLOS:
        for x in FALLOS:
            print("FALLO:", x)
        print(f"test_etapas: {len(FALLOS)} fallo(s)")
        return 1
    print("test_etapas: 9 tests OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
