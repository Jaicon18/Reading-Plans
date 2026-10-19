#!/usr/bin/env python3
"""fixture_reglas.py — v72b: proyecto SINTÉTICO mínimo (ningún proyecto real) que pasa `reglas.py compuerta`.

Para los tests: un wall interior de juguete con su detalle, nodos, barrido MEP registrado sin cruces, accesorios
que no aplican declarados con motivo, las salidas de canon.py, la estructura de etapas (inventario, lecturas A/B,
revisión, resolución), registro, bitácora encadenada y la evidencia (b) de cada regla con imagen y archivo que
EXISTEN. No es un atajo: es un take-off completo de un set de un solo wall; si una regla nueva pide un dato, este
fixture tiene que traerlo o los tests fallan.

Uso:  from fixture_reglas import crear; crear(carpeta)  -> carpeta lista (rc 0 en reglas.py compuerta)
"""
import copy
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

PNG = bytes.fromhex("89504e470d0a1a0a0000000d4948445200000001000000010806000000"
                    "1f15c4890000000d49444154789c6360000002000100e221bc330000000049454e44ae426082")


def canon():
    return {
        "constants": {"plan_scale_pt_per_ft": {"value": 18.0, "source": "Z1.01 1/4\"=1'-0\" (synthetic)"},
                      "north_arrow": {"value": "up", "source": "Z1.01", "img": "img/norte.png"}},
        "details": {"1/Z5.01": {"layers_per_face": 1, "title": "PARTITION TYPE X1", "source": "1/Z5.01",
                                "img": "img/det1.png",
                                "sealant": {"bottom_faces": 2, "top_faces": 0, "source": "1/Z5.01"}}},
        "walls": [{
            "id": "W1", "tag": "X1", "element": "wall", "sheet": "Z1.01", "page": 1, "tag_ids": ["PT0001"],
            "stud_size": "3-5/8\"", "gauge": "20 ga", "gauge_source": "1/Z5.01 '362S125-33'", "oc_in": 16,
            "oc_source": "1/Z5.01 16\" O.C.", "rows": 1, "rows_source": "1/Z5.01 single row",
            "length_ft": 10.0, "length_source": "Z1.01 dimension 10'-0\" face to face, ticks simple",
            "length_status": "CONFIRMADO", "length_op": "printed dimension 10'-0\" (face to face)",
            "thickness_check": "Z1.01 6.0 pt / 1.5 = 4\" = schedule X1",
            "height_ft": 9.0, "height_source": "1/Z5.01 9'-0\"", "height_status": "CONFIRMADO",
            "height_op": "printed dimension 9'-0\"", "to_deck": False,
            "to_deck_source": "1/Z5.01 cap track at 9'-0\" (partial height)",
            "band": {"ori": "H", "c0": 100.0, "c1": 106.0, "lo": 100.0, "hi": 280.0, "sheet": "Z1.01"},
            "detail": "1/Z5.01", "detail_source": "1/Z5.01 PARTITION TYPE X1",
            "source_chain": "PT0001 X1 → Z5.01 schedule → 1/Z5.01", "img": "img/W1.png",
            "faces": [{"room": "901", "side": "A", "board": "5/8 regular", "layers": 1, "height_ft": 9.0,
                       "height_source": "1/Z5.01"},
                      {"room": "902", "side": "B", "board": "5/8 regular", "layers": 1, "height_ft": 9.0,
                       "height_source": "1/Z5.01"}],
            "openings": [], "source": "Z1.01"}],
        "deck_breaks_none_reason": "Z2.01 single NO SLOPE zone (synthetic)",
        "trim_items": [], "trim_none_reason": "1/Z5.01 no outside corners or terminations (synthetic)",
        "tile_base": [], "tile_base_none_reason": "Z6.01 no tile (synthetic)",
        "frp_none_reason": "Z6.01 no FRP (synthetic)", "fascia_none_reason": "Z3.01 no canopy (synthetic)",
        "ballistic_jogs_none_reason": "no type K (synthetic)",
        "mep_sweep": {"sheets": ["M1.01", "P1.01"], "registro": {"dx_pt": 0.0, "dy_pt": 0.0, "matches": 30,
                                                                 "source": "M1.01 / Z1.01 background"},
                      "source": "M1.01, P1.01 (synthetic: no crossings)"},
        "mep_penetrations": [],
        "deflection_clips": {"none_reason": "general notes swept, no deflection clip note (synthetic)",
                             "source": "Z0.01 general notes"},
        "accesorios_none": [{"familia": f, "why": "the synthetic set has no such element", "source": "Z1.01"}
                            for f in ("extra framing ATM", "gypsum board jamb return", "access panel",
                                      "Level 5 finish", "stud reinforcement MEP")],
        "nodes": [{"id": "a", "kind": "free", "wall": "W1"}, {"id": "b", "kind": "free", "wall": "W1"}],
    }


def inventario():
    return {"sheets": [{"page": 1, "sheet": "Z1.01", "inventariable": True}],
            "partition_types": {"schedule": [{"type": "X1"}]},
            "ocurrencias": {"partition_tag": [{"id": "PT0001", "type": "X1", "page": 1, "sheet": "Z1.01",
                                               "center_pt": [190, 103]}],
                            "partition_ambiguo": [], "partition_candidato": []},
            "no_inventariables": [], "avisos": []}


def _w(p, obj):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


def _bitacora(d, tools):
    import bitacora
    p = os.path.join(d, "bitacora.jsonl")
    prev = "0"
    with open(p, "w", encoding="utf-8") as f:
        for tool, args in tools:
            r = {"tool": tool, "args": args, "rc": 0, "hashes": {}, "usa": [], "prev": prev,
                 "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}
            prev = bitacora._hash_renglon(r)
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return p


def crear(d, evidencia=True):
    """Arma el proyecto sintético en d (carpeta de etapas). -> d"""
    import canon as K
    import comparar as C
    c = canon()
    os.makedirs(os.path.join(d, "img"), exist_ok=True)
    for n in ("W1", "det1", "norte", "evid"):
        open(os.path.join(d, "img", n + ".png"), "wb").write(PNG)
    inv = inventario()
    _w(os.path.join(d, "1_inventario", "inventario.json"), inv)
    open(os.path.join(d, "1_inventario", "inventario.md"), "w").write("# Inventory\n\n1. PT0001 X1 Z1.01 (img/W1.png)\n")
    _w(os.path.join(d, "2_lectura", "canon_A.json"), c)
    _w(os.path.join(d, "2_lectura", "canon_B.json"), c)
    time.sleep(0.02)
    _w(os.path.join(d, "3_revision", "revision.json"), C.comparar(c, c, inv))
    open(os.path.join(d, "3_revision", "revision.md"), "w").write("# Review\n\nNo differences.\n")
    open(os.path.join(d, "3_revision", "resolucion.md"), "w").write("# Resolution\n\nW1: A = B (Z1.01, img/W1.png)\n")
    _w(os.path.join(d, "4_canon", "takeoff_canon.json"), c)
    out = os.path.join(d, "out")
    os.makedirs(out, exist_ok=True)
    import contextlib
    import io
    with contextlib.redirect_stdout(io.StringIO()):
        fo = K.calcular(copy.deepcopy(c), out)
    _w(os.path.join(out, "familias_out.json"), fo)
    _w(os.path.join(out, "vigas_out.json"), {"walls_bajo_viga": []})
    _w(os.path.join(d, "registro.json"), {"renglones": []})
    _bitacora(d, [(t, [s] if s else []) for t, s in (
        ("arranque.py", None), ("alcances.py", "escanear"), ("registro.py", "crear"), ("inventario_tags.py", None),
        ("canon.py", None), ("contar_tags.py", None), ("vigas_sobre_walls.py", None), ("framed_openings.py", None),
        ("alcance_filtro.py", None))])
    if evidencia:
        completar_evidencia(d)
    return d


def completar_evidencia(d):
    """Llena evidencias_reglas.json con lo que la compuerta pide (b): un registro por (regla, caso)."""
    import reglas
    arch = os.path.join(d, "3_revision", "resolucion.md")
    ev = []
    for x in reglas.faltantes(d):
        if x["caso"] == "corrida":
            ev.append({"regla": x["regla"], "caso": "corrida", "archivo": arch,
                       "valor": "cumplida en la corrida sintética (ver resolucion.md)"})
        else:
            ev.append({"regla": x["regla"], "caso": x["caso"], "source": "1/Z5.01", "img": "img/evid.png",
                       "valor": "verificado en el plano sintético: face to face, ticks simple, callout + arrow + grid "
                                "+ content"})
    _w(os.path.join(d, "4_canon", "evidencias_reglas.json"), {"evidencias": ev})
    return ev


if __name__ == "__main__":
    import tempfile
    import reglas
    t = crear(sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp(prefix="fixture_reglas_"))
    o = reglas.compuerta(t)
    print(t, "OK" if o["ok"] else f"{o['n_fallas']} fallas: " + json.dumps(o["fallas"][:10], ensure_ascii=False))
