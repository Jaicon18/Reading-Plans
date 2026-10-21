#!/usr/bin/env python3
"""test_v77.py — decisiones del usuario D1-D6 (D1 corregida en v77b), R77.10 y compuertas R76.7 a-e. Cada caso falla con el dato
malo y pasa con el bueno. Datos SINTÉTICOS (walls / rooms 9xx, hojas Z / X, coordenadas inventadas)."""
import copy
import json
import os
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
F, N = [], [0]


def caso(nombre):
    def d(fn):
        N[0] += 1
        try:
            fn()
            print("OK  ", nombre)
        except Exception as e:                       # noqa: BLE001
            print("FALLA", nombre, type(e).__name__, e)
            F.append(nombre)
        return fn
    return d


def falla(fn, *a, texto=""):
    try:
        fn(*a)
    except ValueError as e:
        assert texto in str(e), e
        return
    raise AssertionError("no falló")


def _atm_canon():
    import test_canon as T
    d = T.base()
    w = [x for x in d["walls"] if x["id"] == "I1"][0]
    w["to_deck"] = True
    w["openings"] = [{"ref": "ATM 9", "kind": "atm", "ro_w_ft": 2.25, "head_ft": 5.0, "sill_ft": 2.5,
                      "with_sill": True, "source": "1/X8.11", "jamb_return": False, "jamb_return_source": "1/X8.11",
                      "substrate_none_reason": "1/X8.11 sintético",
                      "atm_recess": {"source": "1/X8.11", "drawn": "WU ATM (sintético)"}}]
    d["opening_schedule"]["items"].append({"ref": "ATM 9"})
    return d


# ------------------------------------------------------------------------------------------------------ D1
@caso("D1 v77b: la partición interior del walk-up ATM completa (studs + 2 runners) = extra framing; sigue en su type")
def _():
    import canon as K
    d = _atm_canon()
    sin = copy.deepcopy(d)
    sin["walls"][2]["openings"][0].pop("atm_recess")
    sin["walls"][2]["openings"][0]["atm_recess_none_reason"] = "1/X8.11 sintético: solo R.O."
    td = tempfile.mkdtemp()
    f0, out = K.calcular(sin)["familias"], K.calcular(copy.deepcopy(d), td)
    f1 = out["familias"]
    atm = f1["extra framing ATM"]
    for k in ('3-5/8" stud (todos los gauges)', "bottom track (todos)", "top / deflection track (todos)"):
        assert abs(f0[k] - f1[k]) < 0.01, (k, f0[k], f1[k])            # nada se resta (convención del estimador)
    st = {x["id"]: x for x in json.load(open(os.path.join(td, "studs_out.json")))["walls"]}
    assert atm > 2 * 10.0 + 100, atm                                     # studs piso a deck + 2 runners de 10 ft
    assert abs(atm - (st["I1"]["lf"] + 20.0)) < 0.02, (atm, st["I1"]["lf"])
    rf = [r for r in out.get("rfis_accesorios") or [] if r.get("familia") == "extra framing ATM"]
    assert rf and rf[0]["delta"] < 0, rf                                 # RFI: contarla una sola vez


@caso("D1 v77b: atm_recess en wall exterior (drive-up) = error; sin to_deck = error; fórmula vieja = error; 2 ATM")
def _():
    import canon as K
    import chequeos_v72 as C72
    d = _atm_canon()
    d["walls"][2]["location"] = "exterior"
    falla(K.calcular, d, texto="exterior")
    assert any("exterior" in x for x in C72.r72_7(d))
    d = _atm_canon()
    d["walls"][2]["openings"][0]["location"] = "exterior"
    falla(K.calcular, d, texto="exterior")
    d = _atm_canon()
    d["walls"][2].pop("to_deck")
    falla(K.calcular, d, texto="to_deck")
    d = _atm_canon()
    d["walls"][2]["openings"][0]["atm_recess"].update(width_ft=4.0, sistered_h_ft=6.0, furring_rows=3)
    falla(K.calcular, d, texto="D1")
    d = _atm_canon()
    d["walls"][2]["openings"][0]["atm_recess"].pop("drawn")
    falla(K.calcular, d, texto="drawn")
    d = _atm_canon()
    d["extra_framing"] = [{"ref": "ATM 9", "kind": "atm_recess", "lf": 30.0, "source": "1/X8.11"}]
    falla(K.calcular, d, texto="D1")
    d = _atm_canon()                                                    # drive-up en la exterior: none_reason, pasa
    d["walls"][0]["openings"].append({"ref": "ATM 11", "kind": "atm", "location": "exterior", "ro_w_ft": 2.0,
                                      "head_ft": 5.0, "sill_ft": 2.5, "with_sill": True, "source": "6/X8.11",
                                      "jamb_return": False, "jamb_return_source": "6/X8.11",
                                      "substrate_none_reason": "6/X8.11 sintético",
                                      "atm_recess_none_reason": "6/X8.11 sintético: drive-up en la wall exterior"})
    d["opening_schedule"]["items"].append({"ref": "ATM 11"})
    K.calcular(d)
    d = _atm_canon()
    o2 = dict(d["walls"][2]["openings"][0], ref="ATM 10")
    d["walls"][2]["openings"].append(o2)
    d["opening_schedule"]["items"].append({"ref": "ATM 10"})
    out = K.calcular(d)
    mov = d["_atm_wall"]
    assert [m["lf"] > 0 for m in mov] == [True, False], mov          # la wall una sola vez
    assert abs(out["familias"]["extra framing ATM"] - mov[0]["lf"]) < 0.01


@caso("R77.10 el largo del wall corre a través de la door hasta la esquina: R.O. fuera del band = falla")
def _():
    import chequeos_v77 as C77
    d = {"constants": {"plan_scale_pt_per_ft": 18.0},
         "walls": [{"id": "W9", "band": {"sheet": "Z2.01", "ori": "H", "p0": [100.0, 50.0], "p1": [280.0, 50.0]},
                    "openings": [{"ref": "door 9A", "kind": "door", "ro_w_ft": 3.3333, "xy_pt": [310.0, 50.0]}]}]}
    assert C77.r77_10(d) and "R77.10" in C77.r77_10(d)[0]               # wall cortado en la jamb: door afuera
    d["walls"][0]["band"]["p1"] = [340.0, 50.0]                         # largo hasta la esquina, door adentro
    assert C77.r77_10(d) == []
    d["walls"][0]["openings"][0].pop("xy_pt")
    assert C77.r77_10(d) == []


# ------------------------------------------------------------------------------------------------------ D2
def _cont(ref, ro, c, wall="OF-1", j0=0.0):
    return {"ref": ref, "wall": wall, "kind": "opening", "ro_w_ft": ro, "qty": 1, "continuous_run": True,
            "header_type": "CONT. BOX BEAM", "header_type_source": "8/Z12.01", "pieces": 4,
            "pieces_source": "8/Z12.01", "source": "Z2.01", "run_ends": "jamb_to_jamb",
            "front_line": {"sheet": "Z2.01", "ori": "V", "c_pt": c, "jambs_pt": [j0, j0 + ro * 18.0],
                           "scale_pt_per_ft": 18.0, "source": "Z2.01"}}


@caso("D2 CONT. BOX BEAM: un run por frente de la primera a la última jamb + 1'-4\" x 4; por abertura = error")
def _():
    import headers as H
    B = 16 / 12
    t = H.calcular({"openings": [_cont("F-E", 40.0, 900.0), _cont("F-W", 18.5, 500.0, wall="OF-2")]})
    assert abs(t["totales_lf"]["header"] - ((40.0 + B) * 4 + (18.5 + B) * 4)) < 0.02, t["totales_lf"]
    # malo: una "línea" por oficina sobre el mismo frente (walls distintos, misma línea)
    malas = [_cont(f"OF-{i}", 7.5, 900.0, wall=f"DB-{i}", j0=150.0 * i) for i in range(4)]
    falla(H.calcular, {"openings": malas}, texto="misma línea")
    falla(H.calcular, {"openings": [dict(_cont("F", 40.0, 900.0), front_line=None)]}, texto="front_line")
    falla(H.calcular, {"openings": [dict(_cont("F", 40.0, 900.0), ro_w_ft=42.0)]}, texto="primera a última jamb")
    falla(H.calcular, {"openings": [dict(_cont("F", 40.0, 900.0), run_ends="wall_to_wall")]}, texto="D2")


@caso("D2 header schedule: piezas = rótulo impreso (SINGLE 1, DOUBLE 2, '2-...' 2)")
def _():
    import headers as H
    sch = {"source": "7/Z5.20", "rows": [{"max_span_ft": 3.333, "type": "SINGLE TRACK 18 GA", "pieces": 1},
                                          {"max_span_ft": 6.0, "type": "DOUBLE TRACK 18 GA", "pieces": 2},
                                          {"max_span_ft": 8.0, "type": "2-362CSJ20", "pieces": 2}]}
    op = {"ref": "d1", "kind": "door", "ro_w_ft": 3.333, "source": "Z0.30"}
    H.calcular({"header_schedule": sch, "openings": [op]})
    mal = copy.deepcopy(sch)
    mal["rows"][2]["pieces"] = 1
    falla(H.calcular, {"header_schedule": mal, "openings": [op]}, texto="D2")
    mal = copy.deepcopy(sch)
    mal["rows"][0]["pieces"] = 2
    falla(H.calcular, {"header_schedule": mal, "openings": [op]}, texto="D2")


# ------------------------------------------------------------------------------------------------------ D5
@caso("D5 sill track: > 4'-0\" x 2, <= 4'-0\" x 1, solo con sill; door con sill = error")
def _():
    import headers as H
    B = 16 / 12
    ops = [{"ref": "w1", "kind": "window", "ro_w_ft": 8.0, "with_sill": True, "source": "Z9.27",
            "header_type": "BOX", "header_type_source": "11/Z9.27", "pieces": 4, "pieces_source": "11/Z9.27"},
           {"ref": "a1", "kind": "atm", "ro_w_ft": 2.25, "with_sill": True, "source": "4/Z8.11"},
           {"ref": "o1", "kind": "opening", "ro_w_ft": 6.0, "source": "Z2.01"}]
    sch = {"source": "7/Z5.20", "rows": [{"max_span_ft": 3.333, "type": "SINGLE TRACK", "pieces": 1},
                                          {"max_span_ft": 6.0, "type": "DOUBLE TRACK", "pieces": 2}]}
    t = H.calcular({"header_schedule": sch, "openings": ops})["totales_lf"]["sill track"]
    assert abs(t - ((8.0 + B) * 2 + (2.25 + B) * 1)) < 0.02, t
    falla(H.calcular, {"openings": [{"ref": "d", "kind": "door", "ro_w_ft": 3.333, "with_sill": True,
                                     "source": "Z0.30"}]}, texto="D5")


# ------------------------------------------------------------------------------------------------------ D3 / D4
def _strip(**kw):
    s = {"ref": "PIER-A-1", "uso": "pier", "material": "frt_3_4", "label": "3/4\" FRT PLYWOOD", "source": "1/Z9.25",
         "width_pt": 81.0, "scale_pt_per_ft": 108.0, "scale_check": {"printed_in": 0.75, "measured_pt": 6.75},
         "width_ft": 0.75, "jambs": 1, "height_ft": 8.5, "height_source": "Z9.01 T/GLAZING", "lf": 8.5,
         "plies": 1, "layers_drawn": 2, "rfi": "RFI-PLY (sintético): +1 ply"}
    s.update(kw)
    return s


@caso("D4 strip de pier: ancho por vector con escala verificada, jambs x alto impreso, plies del rótulo + RFI")
def _():
    import chequeos_v77 as C77
    ok = {"plywood_strips": [_strip()], "walls": [{"id": "PR", "element": "pier", "jamb_strips": ["PIER-A-1"]}]}
    assert not C77.r77_4(ok), C77.r77_4(ok)
    for mal, txt in ((dict(width_ft=0.333), "width_pt"), (dict(scale_check={"printed_in": 0.75, "measured_pt": 9.0}),
                                                          "scale_check"),
                     (dict(label="AWB ON 5/8\" FRT PLYWOOD BONDED TO POLYISO"), "cara"),
                     (dict(lf=17.0), "jambs"), (dict(rfi=""), "rfi")):
        d = copy.deepcopy(ok)
        d["plywood_strips"][0].update(mal)
        assert any(txt in x for x in C77.r77_4(d)), (txt, C77.r77_4(d))
    d = copy.deepcopy(ok)
    d["plywood_strips"][0].pop("width_pt")
    assert any("vector" in x for x in C77.r77_4(d))
    d = copy.deepcopy(ok)
    d["walls"][0].pop("jamb_strips")
    assert any("jamb_strips" in x for x in C77.r77_4(d))
    d["walls"][0]["jamb_strips_none_reason"] = "3/Z8.21: pier de grille sin storefront"
    assert not C77.r77_4(d)


# ------------------------------------------------------------------------------------------------------ D6
@caso("D6 borde de transición: el ceiling no suma track de perímetro en ese borde (canon resta edge_of)")
def _():
    import chequeos_v76 as C
    d = {"ceilings": [{"room": "905", "system": "furring", "area_sf": 100.0, "perimeter_ft": 40.0}],
         "walls": [{"id": "T-1", "element": "ceiling_transition", "length_ft": 10.0, "edge_of": ["905"]}]}
    assert C.bordes_transicion(d, ("furring", "stud_joist")) == {"905": 10.0}


# ------------------------------------------------------------------------------------------------------ R77.7
@caso("R77.7 ceiling suspendido sin carrying_direction del proyecto = error")
def _():
    import canon as K
    import test_canon as T
    d = T.base()
    del d["constants"]["carrying_direction"]
    falla(K.calcular, d, texto="R77.7")


# ------------------------------------------------------------------------------------------------------ R76.7
@caso("R76.7 a: A_BLOCKING reconoce el rótulo 'F.R.T.' con puntos")
def _():
    import reglas as R
    assert R.RX_FRT_ROTULO.search("2X F.R.T. BLOCKING") and R.RX_FRT_ROTULO.search("FRT WOOD")
    assert not R.RX_FRT_ROTULO.search("2X WOOD BLOCKING")

    class Ctx:
        canon = {"blocking_items": [{"ref": "b1", "lf": 10, "material": "FRT", "label": "2X F.R.T. BLOCKING"}]}
    assert not R.a_blocking(Ctx())
    Ctx.canon["blocking_items"][0]["label"] = "2X WOOD BLOCKING"
    assert R.a_blocking(Ctx())


@caso("R76.7 b: el detector de español ignora rutas, archivos, ids y coordenadas")
def _():
    import plantilla_excel as P
    for t in ("img /home/user/x/el_detalle_muro.png", "A-W2-PT0031 y 974.8 (A02.01)", "x 841.44 y 454.44-840.72",
              "EL. 15'-4 1/2\" B.O.D.", "see EL-12 and ATM-DU"):
        assert not P.es_texto_es(t), (t, P.es_texto_es(t))
    assert P.es_texto_es("la cara del muro sur")


@caso("R76.7 c: vigas_sobre_walls no cruza bands de otra hoja")
def _():
    import vigas_sobre_walls as V
    vig = [{"p0": (100.0, 500.0), "p1": (400.0, 500.0), "lw": 2.5, "perfil": {"profile": "W12X19"}}]
    ws = [{"id": "A", "band": {"sheet": "Z2.01", "ori": "H", "c0": 498, "c1": 502, "lo": 120, "hi": 380}},
          {"id": "B", "band": {"sheet": "Z2.02", "ori": "H", "c0": 498, "c1": 502, "lo": 120, "hi": 380}}]
    assert {x["wall"] for x in V.cruzar(vig, ws, hoja="Z2.01")} == {"A"}
    assert {x["wall"] for x in V.cruzar(vig, ws)} == {"A", "B"}


@caso("R76.7 d: bitácora con lock y realpath (symlink = mismo archivo; anotaciones concurrentes sin romper cadena)")
def _():
    import importlib
    import threading
    tmp = tempfile.mkdtemp()
    os.environ["BITACORA"] = os.path.join(tmp, "bit.jsonl")
    import bitacora as B
    importlib.reload(B)
    f = os.path.join(tmp, "x.json")
    open(f, "w").write("{}")
    ln = os.path.join(tmp, "ln.json")
    os.symlink(f, ln)
    ths = [threading.Thread(target=B.anotar, args=({"tool": f"t{i}", "hashes": {B._ruta(ln): B.sha(f)}},))
           for i in range(8)]
    [t.start() for t in ths]
    [t.join() for t in ths]
    rows = B.leer()
    assert len(rows) == 8 and B.cadena_ok(rows) == 0, B.cadena_ok(rows)
    assert B._vigente(rows[0], ln) and B._vigente(rows[0], f)
    del os.environ["BITACORA"]
    importlib.reload(B)


@caso("R76.7 e: inventario_tags / alcances leen la copia limpia (sin /Annots)")
def _():
    import pymupdf
    import copia_limpia as CL
    tmp = tempfile.mkdtemp()
    p = os.path.join(tmp, "set.pdf")
    doc = pymupdf.open()
    pg = doc.new_page()
    pg.insert_text((72, 72), "PARTITION TYPE Z1")
    pg.add_text_annot((100, 100), "markup de otro estimador")
    doc.save(p)
    doc.close()
    limpio, n = CL.copia_limpia(p)
    assert limpio.endswith("_SIN_MARKUPS.pdf") and n >= 1
    d2 = pymupdf.open(limpio)
    assert not list(d2[0].annots() or [])
    assert CL.copia_limpia(limpio) == (limpio, None)
    src = open(os.path.join(AQUI, "inventario_tags.py")).read() + open(os.path.join(AQUI, "alcances.py")).read()
    assert src.count("copia_limpia.copia_limpia(pdf)") == 2


if __name__ == "__main__":
    print(f"{N[0] - len(F)} OK, {len(F)} falla(s)")
    sys.exit(1 if F else 0)
