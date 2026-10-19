#!/usr/bin/env python3
"""test_v73.py — reglas v73 (arbitraje #21). Cada caso falla con el dato malo y pasa con el bueno. Datos SINTÉTICOS."""
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


def K(id_, lo, hi, c0, c1, L, **kw):
    w = {"id": id_, "tag": "X1K", "element": "wall", "tag_ids": ["PT9"], "length_ft": L, "length_status": "DERIVADO",
         "band": {"ori": "H", "c0": c0, "c1": c1, "lo": lo, "hi": hi, "sheet": "Z1.01"}, "sheet": "Z1.01"}
    w.update(kw)
    return w


@caso("R73.1 cota impresa junto al tramo manda sobre el vector (sin dim_scan = falla)")
def _():
    import chequeos_v73 as C
    c = {"walls": [K("K1", 0, 54, 0, 8, 3.0)]}
    assert any("sin dim_scan" in x for x in C.r73_1(c))
    c["walls"][0]["dim_scan"] = {"found": [{"text": "3' - 5\"", "value_ft": 3.4167}], "source": "cotas_banda.py"}
    assert any("!= cota impresa" in x for x in C.r73_1(c))
    c["walls"][0].update(length_ft=3.417, length_status="CONFIRMADO")
    assert C.r73_1(c) == []
    c["walls"][0].update(length_ft=3.0, length_status="DERIVADO")
    c["walls"][0]["dim_scan"]["no_aplica"] = "la cota mide el hueco interior del cuarto, Z1.01"
    assert C.r73_1(c) == []


@caso("R73.2 dos walls K paralelos del mismo contorno no se solapan; jog sin band = falla; jog sobre wall = falla")
def _():
    import chequeos_v73 as C
    a, b = K("KA", 0, 60, 0, 10, 3.333), K("KB", 50, 110, 14, 22, 3.333)
    c = {"walls": [a, b], "ballistic_jogs": [{"ref": "j", "length_ft": 0.2}]}
    f = C.r73_2(c)
    assert any("KA y KB" in x for x in f) and any("sin band" in x for x in f), f
    b["band"]["lo"] = 60
    c["ballistic_jogs"][0]["band"] = {"ori": "V", "c0": 56, "c1": 60, "lo": 5, "hi": 18}
    assert any("se solapan" in x for x in C.r73_2(c))
    c["ballistic_jogs"][0]["band"].update(lo=10, hi=14)
    assert C.r73_2(c) == [], C.r73_2(c)


@caso("R73.5 MEP: solo ductos de mep.cruces en la familia; manual / pipe / FD a RFI (accesorios y compuerta)")
def _():
    import accesorios as A
    import chequeos_v73 as C
    d = {"walls": [{"id": "W1", "rows": 1}, {"id": "W2", "rows": 2}],
         "mep_sweep": {"sheets": ["P1.01", "M1.01"], "source": "mep.registro", "registro": {
             "dx_pt": 0, "dy_pt": 0, "matches": 40, "source": "mep.registro"}},
         "mep_penetrations": [
             {"ref": "d1", "wall": "W2", "width_in": 8, "xy": [1, 1], "method": "mep.cruces", "kind": "duct", "source": "M1.01"},
             {"ref": "d2", "wall": "W1", "width_in": 20, "xy": [2, 2], "method": "manual", "kind": "duct", "source": "M1.01"},
             {"ref": "p1", "wall": "W1", "dia_in": 2, "xy": [3, 3], "method": "mep.cruces", "kind": "pipe", "source": "P1.01"},
             {"ref": "FD 12x12", "wall": "W1", "width_in": 12, "xy": [4, 4], "method": "manual", "kind": "fire_damper",
              "source": "M1.01"}]}
    o = A.Out()
    A.stud_reinforcement(d, None, o)
    assert o.fam[A.F_REINF] == 2, o.filas
    temas = " | ".join(r["tema"] for r in o.rfis)
    assert "read by hand" in temas and "pipes over 1 in" in temas, temas
    e, _ = C.esperado_mep(d)
    assert e == 2
    assert C.r73_5(d, {"familias": {A.F_REINF: 2.0}}) == []
    assert C.r73_5(d, {"familias": {A.F_REINF: 6.0}})


@caso("R73.9 RFIs de accesorios en inglés: verificar no los rechaza")
def _():
    import accesorios as A
    import plantilla_excel as PE
    d = {"walls": [{"id": "W2", "rows": 2}],
         "mep_sweep": {"sheets": ["P1.01", "M1.01"], "source": "mep.registro", "registro": {
             "dx_pt": 0, "dy_pt": 0, "matches": 40, "source": "mep.registro"}},
         "mep_penetrations": [
             {"ref": "d1", "wall": "W2", "width_in": 8, "xy": [1, 1], "method": "mep.cruces", "kind": "duct", "source": "M1.01"},
             {"ref": "d2", "wall": "W2", "width_in": 8, "xy": [2, 1], "method": "manual", "kind": "duct", "source": "M1.01"}]}
    o = A.Out()
    A.stud_reinforcement(d, None, o)
    malos = [r["tema"] for r in o.rfis if PE.es_texto_es(PE.en(r["familia"] + ": " + r["tema"]))]
    malos += [r.get("alternativa") for r in o.rfis if PE.es_texto_es(PE.en(str(r.get("alternativa") or "")))]
    assert not malos, malos


@caso("R73.6 deflection clips: sin bloque = falla; nota + slip track = 0 + RFI con studs de walls a estructura")
def _():
    import accesorios as A
    import chequeos_v73 as C
    assert C.r73_6({})
    d = {"walls": [{"id": "W1", "to_deck": True}, {"id": "W2"}],
         "deflection_clips": {"note_source": "Z1.10 note 2", "slip_track_source": "1/Z5.01"}}
    o = A.Out()
    A.deflection_clips(d, {"walls": [{"id": "W1", "pcs_full": 9}, {"id": "W2", "pcs_full": 5}]}, o)
    assert o.fam[A.F_CLIPS] == 0 and o.rfis[0]["delta"] == 9, (o.fam, o.rfis)
    del d["deflection_clips"]["slip_track_source"]
    o = A.Out()
    A.deflection_clips(d, {"walls": [{"id": "W1", "pcs_full": 9}]}, o)
    assert o.fam[A.F_CLIPS] == 9
    assert C.r73_6(d) == []


@caso("R73.7 segmento sin tag con espesor de otro type no entra al type por defecto")
def _():
    import chequeos_v73 as C
    c = {"partition_schedule": [{"type": "X1", "thickness_in": 4.875}, {"type": "X7", "thickness_in": 6.125}],
         "walls": [{"id": "U1", "tag": "X1", "tag_ids": [], "default_type_source": "Z1.01 note A",
                    "thickness_check": "Z1.01 measured 9.2 pt / 1.5 = 6.13 in vs schedule X1"}]}
    f = C.r73_7(c)
    assert f and "X7" in f[0], f
    c["walls"][0]["default_type_rfi"] = {"alternativas": ["X1", "X7"], "source": "Z1.01"}
    assert C.r73_7(c) == []


@caso("R73.8 la operación escrita cuadra (cadena tipeada distinta de su suma = falla)")
def _():
    import chequeos_v73 as C
    c = {"walls": [{"id": "W1", "length_ft": 5.0, "length_op": "1.5 + 2.25 + 1.0 = 5.0"}]}
    assert C.r73_8(c)
    c["walls"][0]["length_op"] = "(140.0 - 50.0) / 18 = 90.0 / 18 = 5.0"
    assert C.r73_8(c) == [], C.r73_8(c)
    c["walls"][0].update(length_op="10.0 - 4.0 = 6.0 - 1.0 = 5.0")
    assert C.r73_8(c) == []


@caso("cotas_banda: lee cotas pies-pulgadas y encuentra la cota paralela junto a la banda (PDF sintético)")
def _():
    import pymupdf as fitz
    import cotas_banda as CB
    assert CB.valor_ft("3' - 5\"") == round(3 + 5 / 12, 4) and CB.valor_ft("5'-6 1/2\"") == round(5 + 6.5 / 12, 4)
    assert CB.valor_ft("4\"") == round(4 / 12, 4) and CB.valor_ft("TYP.") is None
    d = tempfile.mkdtemp()
    p = os.path.join(d, "z.pdf")
    doc = fitz.open()
    pg = doc.new_page(width=600, height=400)
    pg.insert_text((120, 150), "3' - 5\"", fontsize=8)
    pg.insert_text((400, 300), "9' - 0\"", fontsize=8)
    doc.save(p)
    r = CB.dim_scan(p, 1, {"ori": "H", "c0": 160, "c1": 168, "lo": 100, "hi": 161.5})
    assert [x["value_ft"] for x in r["found"]] == [round(3 + 5 / 12, 4)], r


@caso("R73.3 track por elemento: parapet / heads / tamaño; Σ = familia (resto a 'other')")
def _():
    import canon
    data = {"walls": [{"id": "A", "stud_size": "6\""}, {"id": "B", "stud_size": "3-5/8\""}]}
    co = {"renglones": [{"id": "W:A", "element": "wall", "bottom_lf": 10.0, "top_lf": 10.0},
                        {"id": "W:B", "element": "wall", "bottom_lf": 5.0, "top_lf": 5.0},
                        {"id": "W:P", "element": "parapet", "bottom_lf": 20.0, "top_lf": 20.0},
                        {"id": "W:R", "element": "roof_step", "bottom_lf": 7.0, "top_lf": 7.0}]}
    fam = {"bottom track (todos)": 45.0, "top / deflection track (todos)": 42.0}
    t = canon.track_by_element(data, co, fam)
    assert t["bottom"]['Bottom track 6"'] == 10.0 and t["bottom"]["Parapet bottom track"] == 20.0
    assert abs(sum(t["bottom"].values()) - 45.0) < 0.01 and any("other" in k for k in t["bottom"])
    assert abs(sum(t["top"].values()) - 42.0) < 0.01


@caso("R73.3 nombres de la plantilla: renglón que cita su familia toma el nombre de la plantilla")
def _():
    import plantilla_excel as PE
    fo = {"nombres_contexto": {"ballistic_th": '3/8"', "bracing_oc_in": 48}}
    assert PE.nombre_plantilla("ballistic panel", fo) == 'Ballistic panel 3/8" UL752'
    assert PE.nombre_plantilla("bracing C.R. channel", fo) == 'Bracing 1-1/2" C.R. channel @ 48" O.C.'
    assert PE.nombre_plantilla("familia que no existe", fo) is None


@caso("R73.3 plywood_strips sin uso = falla de compuerta; con uso, renglón de la plantilla por uso")
def _():
    import canon
    import chequeos_v73 as C
    c = {"plywood_strips": [{"ref": "p1"}]}
    assert C.r73_3(c)
    c["plywood_strips"][0]["uso"] = "pier"
    assert C.r73_3(c) == []
    canon.PLY.clear()
    canon.PLY_USO.clear()
    fam = {canon.F_PLY: 0.0}
    canon._ply(fam, "frt_3_4", 10.0, canon._uso_strip({"ref": "s1", "uso": "pier"}))
    canon._ply(fam, "frt_5_8", 5.0, canon._uso_strip({"ref": "s2", "source": "5/8 FRT plywood bonded to polyiso"}))
    assert canon.PLY_USO == {'3/4" FRT plywood at storefront piers': 10.0,
                             'Exterior sheathing 5/8" FRT plywood bonded to polyiso (nailbase)': 5.0}, canon.PLY_USO


@caso("calificador: rango min == max manda sobre la ref; _partition_types y modo consistencia")
def _():
    import eval_takeoff as E
    assert E.grade_rango(10.0, 10.0, 10.1, 0.02, 0.10)[0].startswith("IGUAL")
    assert E.grade_rango(10.0, 10.0, 11.5, 0.02, 0.10)[0].startswith("MAL")


print(f"test_v73: {N[0] - len(F)} OK, {len(F)} falla(s)")
sys.exit(1 if F else 0)
