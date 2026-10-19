#!/usr/bin/env python3
"""Tests v70 de etapas.py (unir + compuerta) y comparar.py con datos de JUGUETE (ningún proyecto real).
Correr: python3 test_etapas_v70.py

unir: (a) lista vs dict = ERROR sin crash; (b) notes distintas -> {fragmento: texto} + aviso, otro escalar distinto
= ERROR con los dos fragmentos; (c) convención de band (caras > 2 ft, largo ±3 % / 1 ft, banda traspuesta);
(d) page 0-based contra el inventario (unir y comparar); (e) refs de openings contra la lista de aberturas.
compuerta: un candidato (PC####, tag fuera del schedule) que ninguna lectura toma y sin alerta -> FALLA.
"""
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


def w(id_, tag, eje, lo, hi, **kw):
    d = {"id": id_, "tag": tag, "length_ft": round((hi - lo) / E, 4), "sheet": "Z1.01", "page": 2,
         "band": {"ori": "H", "c0": eje - 2, "c1": eje + 2, "lo": lo, "hi": hi}}
    d.update(kw)
    return d


def canon(walls, **kw):
    d = {"constants": {"plan_scale_pt_per_ft": {"value": E, "source": "sintético"}}, "walls": walls}
    d.update(kw)
    return d


def inventario(cand=()):
    tag = lambda i, t, x, y: {"id": i, "type": t, "page": 2, "sheet": "Z1.01", "center_pt": [x, y]}
    return {"sheets": [{"page": 1, "sheet": "Z0.01"}, {"page": 2, "sheet": "Z1.01", "inventariable": True}],
            "partition_types": {"schedule": [{"type": "X1"}]},
            "ocurrencias": {"partition_tag": [tag("PT0001", "X1", 200, 110)], "partition_ambiguo": [],
                            "partition_candidato": [dict(tag(i, None, x, y), text=t) for i, t, x, y in cand]},
            "no_inventariables": [], "avisos": []}


def frags(d, *objs):
    os.makedirs(d, exist_ok=True)
    for k, o in enumerate(objs):
        with open(os.path.join(d, f"f{k + 1}.json"), "w") as f:
            json.dump(o, f)
    return d


def unir(*objs, inv=None):
    with tempfile.TemporaryDirectory() as d:
        frags(os.path.join(d, "x"), *objs)
        ruta = None
        if inv is not None:
            ruta = os.path.join(d, "inv.json")
            json.dump(inv, open(ruta, "w"))
        av = []
        c, err = T.unir(os.path.join(d, "x"), ruta, av)
        rc = T.main(["etapas.py", "unir", os.path.join(d, "x"), os.path.join(d, "o.json")]
                    + (["--inventario", ruta] if ruta else []))
        return c, err, av, rc


def test_a_lista_vs_dict_sin_crash():
    c, err, _, rc = unir(canon([w("A1", "X1", 100, 0, 180)], evidence=["img1.png"]),
                         canon([w("A2", "X1", 300, 0, 180)], evidence={"img": "img2.png"}))
    assert any(x.startswith("evidence: list in f1.json, dict in f2.json") for x in err), err
    assert rc == 1


def test_b_notes_por_fragmento_y_escalar_distinto():
    c, err, av, rc = unir(canon([w("A1", "X1", 100, 0, 180)], notes="hoja 1"),
                          canon([w("A2", "X1", 300, 0, 180)], notes="hoja 2"))
    assert err == [] and rc == 0, err
    assert c["notes"] == {"f1.json": "hoja 1", "f2.json": "hoja 2"}, c["notes"]
    assert any("notes" in x for x in av), av
    c, err, _, rc = unir(canon([w("A1", "X1", 100, 0, 180)], prefix="A"), canon([w("A2", "X1", 300, 0, 180)], prefix="B"))
    assert any("prefix" in x and "f1.json" in x and "f2.json" in x for x in err) and rc == 1, err


def test_c_banda_traspuesta_y_fuera_de_convencion():
    bueno = w("A1", "X1", 100, 0, 180)
    tras = w("A2", "X1", 300, 0, 180)
    tras["band"] = {"ori": "H", "c0": 0, "c1": 180, "lo": 298, "hi": 302}        # c0/c1 = extensión
    _, err, _, rc = unir(canon([bueno]), canon([tras]))
    assert any("A2" in x and "banda traspuesta" in x for x in err) and rc == 1, err
    assert not any("A1" in x for x in err), err
    ancho = w("A3", "X1", 500, 0, 180)
    ancho["band"].update(c0=480, c1=530)                                         # 2.8 ft entre caras
    largo = w("A4", "X1", 700, 0, 180, length_ft=14.0)                           # banda 10 ft vs 14 ft
    ok = w("A5", "X1", 900, 0, 180, length_ft=11.5, band_length_ok_reason="cota impresa 11'-6\" (length_source)")
    soffit = w("S1", "X1", 1100, 0, 180, element="soffit_side")
    soffit["band"].update(c0=1080, c1=1140)                                      # soffit ancho: no aplica caras
    _, err, _, rc = unir(canon([ancho, largo, ok, soffit]))
    assert any("A3" in x and "c1 - c0" in x for x in err), err
    assert any("A4" in x and "hi - lo" in x for x in err), err
    assert not any("A5" in x or "S1" in x for x in err), err
    assert rc == 1


def test_c_escala_del_canon():
    c = canon([w("A1", "X1", 100, 0, 180, length_ft=20.0)])                      # 180 pt a 9 pt/ft = 20 ft
    c["constants"]["plan_scale_pt_per_ft"]["value"] = 9.0
    _, err, _, _ = unir(c)
    assert err == [], err


def test_d_page_0_based():
    inv = inventario()
    _, err, _, rc = unir(canon([w("A1", "X1", 100, 0, 180, page=1)]), inv=inv)
    assert any("A1" in x and "page 0-based" in x for x in err) and rc == 1, err
    _, err, _, rc = unir(canon([w("A1", "X1", 100, 0, 180, page=2)]), inv=inv)
    assert err == [] and rc == 0, err
    # inventario en <carpeta>/../1_inventario/inventario.json (sin --inventario)
    with tempfile.TemporaryDirectory() as d:
        frags(os.path.join(d, "2_lectura"), canon([w("A1", "X1", 100, 0, 180, page=1)]))
        os.makedirs(os.path.join(d, "1_inventario"))
        json.dump(inv, open(os.path.join(d, "1_inventario", "inventario.json"), "w"))
        _, err = T.unir(os.path.join(d, "2_lectura"))
        assert any("page 0-based" in x for x in err), err


def test_d_comparar_rechaza_page_0_based():
    inv = inventario()
    a = canon([w("A1", "X1", 100, 100, 460, tag_ids=["PT0001"])])
    b = canon([w("B1", "X1", 100, 100, 460, page=1)])
    try:
        C.comparar(a, b, inv)
        raise AssertionError("comparar aceptó page 0-based")
    except ValueError as e:
        assert "page 0-based" in str(e) and "B1" in str(e), e
    with tempfile.TemporaryDirectory() as d:
        for n, o in (("a.json", a), ("b.json", b), ("i.json", inv)):
            json.dump(o, open(os.path.join(d, n), "w"))
        rc = C.main(["comparar.py"] + [os.path.join(d, n) for n in ("a.json", "b.json", "i.json")] +
                    [os.path.join(d, "rev")])
        assert rc != 0


def test_e_refs_de_openings():
    sched = {"source": "sintético", "items": [{"ref": "D-1"}, {"ref": "D-2"}]}
    a = w("A1", "X1", 100, 0, 180, openings=[{"ref": "D-1", "ro_w_ft": 3, "head_ft": 7}])
    b = w("A2", "X1", 300, 0, 180, openings=[{"ref": "door 1 (otro nombre)", "ro_w_ft": 3, "head_ft": 7}])
    _, err, _, rc = unir(canon([a], opening_schedule=sched), canon([b], openings_extra=[{"ref": "D-9"}]))
    m = [x for x in err if x.startswith("openings:")]
    assert m and "door 1 (otro nombre)" in m[0] and "D-9" in m[0] and "Etapa 2a" in m[0] and rc == 1, err
    _, err, _, rc = unir(canon([a], opening_list=["D-1", "D-2"]))
    assert err == [] and rc == 0, err


def test_compuerta_candidato_sin_wall_y_sin_alerta():
    inv = inventario(cand=[("PC0001", "Y7", 600, 600)])
    a = canon([w("A1", "X1", 100, 100, 460, tag_ids=["PT0001"])])
    b = canon([w("B1", "X1", 100, 100, 460)])
    with tempfile.TemporaryDirectory() as d:
        for nombre, sub, o in (("inventario.json", "1_inventario", inv), ("canon_A.json", "2_lectura", a),
                               ("canon_B.json", "2_lectura", b)):
            os.makedirs(os.path.join(d, sub), exist_ok=True)
            json.dump(o, open(os.path.join(d, sub, nombre), "w"))
        time.sleep(0.02)
        rev = C.comparar(a, b, inv)
        assert any(c["tag"] == "PC0001" for c in rev["cobertura_tags"]), "candidato fuera del cruce"
        assert any(x["kind"] == "tag sin wall" and x["tag"]["id"] == "PC0001" for x in rev["alertas"])
        os.makedirs(os.path.join(d, "3_revision"))
        p = os.path.join(d, "3_revision", "revision.json")
        json.dump(rev, open(p, "w"))
        f, _ = T.estructura(d)
        assert f == [], f                                   # con su alerta: pasa (queda a la vista)
        f, _ = T.compuerta(d)                               # v72b: sin canon conciliado reglas.py no da OK
        assert any(x.startswith("reglas:") for x in f), f
        rev["alertas"] = [x for x in rev["alertas"] if (x.get("tag") or {}).get("id") != "PC0001"]
        json.dump(rev, open(p, "w"))
        f, _ = T.compuerta(d)
        assert any("PC0001" in x and "sin alerta" in x for x in f), f
        # revisión vieja que no cubre el candidato -> también falla
        rev["cobertura_tags"] = [c for c in rev["cobertura_tags"] if c["tag"] != "PC0001"]
        json.dump(rev, open(p, "w"))
        f, _ = T.compuerta(d)
        assert any("PC0001" in x for x in f), f


def test_compuerta_corre_esquinas_sobre_el_canon_final():
    inv = inventario()
    a = canon([w("A1", "X1", 100, 100, 460, tag_ids=["PT0001"])])
    b = canon([w("B1", "X1", 100, 100, 460)])
    banda = lambda ori, c0, c1, lo, hi: {"sheet": "Z1.01", "ori": ori, "c0": c0, "c1": c1, "lo": lo, "hi": hi}
    h = {"id": "H1", "tag": "X1", "element": "wall", "length_ft": 193 / E, "band": banda("H", 100, 107, 100, 293)}
    v = {"id": "V1", "tag": "X1", "element": "wall", "length_ft": 293 / E, "band": banda("V", 293, 300, 107, 400)}
    with tempfile.TemporaryDirectory() as d:
        for nombre, sub, o in (("inventario.json", "1_inventario", inv), ("canon_A.json", "2_lectura", a),
                               ("canon_B.json", "2_lectura", b)):
            os.makedirs(os.path.join(d, sub), exist_ok=True)
            json.dump(o, open(os.path.join(d, sub, nombre), "w"))
        time.sleep(0.02)
        os.makedirs(os.path.join(d, "3_revision"))
        json.dump(C.comparar(a, b, inv), open(os.path.join(d, "3_revision", "revision.json"), "w"))
        f, _ = T.estructura(d)
        assert f == [], f                                        # sin canon final: no se revisan esquinas
        os.makedirs(os.path.join(d, "4_canon"))
        p = os.path.join(d, "4_canon", "takeoff_canon.json")
        json.dump(canon([h, v]), open(p, "w"))                   # esquina sin dueño (R70.2)
        f, _ = T.compuerta(d)
        assert any(x.startswith("esquinas:") and "sin dueño" in x for x in f), f
        assert T.main(["etapas.py", "compuerta", d]) == 1
        v["band"]["lo"] = 100                                    # V cubre el cuadrado: un dueño
        json.dump(canon([h, v]), open(p, "w"))
        f, _ = T.compuerta(d)
        assert not [x for x in f if x.startswith("esquinas:")], f


if __name__ == "__main__":
    fallas = 0
    for k, f in sorted(globals().items()):
        if k.startswith("test_") and callable(f):
            try:
                f()
                print("OK  ", k)
            except Exception as e:  # noqa: BLE001 (crash con código viejo = falla)
                fallas += 1
                print("FALLA", k, type(e).__name__, e)
    print(f"{'TODOS OK' if not fallas else str(fallas) + ' FALLA(S)'}")
    sys.exit(1 if fallas else 0)
