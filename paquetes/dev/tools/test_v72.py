#!/usr/bin/env python3
"""test_v72.py — un test por cada cambio v72 (arbitraje #20). Datos sintéticos, ningún valor de proyecto.

Correr: python3 test_v72.py   (rc 0 = todo OK). Cada test falla con las tools v71 (salvo los marcados "protección").
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
FALLOS = []
OK = []


def caso(nombre):
    def deco(fn):
        try:
            fn()
            OK.append(nombre)
        except AssertionError as e:
            FALLOS.append(f"{nombre}: {e}")
        except Exception as e:                       # noqa: BLE001 — un crash es una falla del test
            FALLOS.append(f"{nombre}: {type(e).__name__}: {e}")
        return fn
    return deco


def H(wid, tag, y0, y1, x0, x1, L, tags=("PT1",), **kw):
    w = {"id": wid, "tag": tag, "element": "wall", "sheet": "A1.01", "length_ft": L, "tag_ids": list(tags),
         "band": {"ori": "H", "c0": y0, "c1": y1, "lo": x0, "hi": x1}}
    w.update(kw)
    return w


def V(wid, tag, x0, x1, y0, y1, L, tags=("PT1",), **kw):
    w = {"id": wid, "tag": tag, "element": "wall", "sheet": "A1.01", "length_ft": L, "tag_ids": list(tags),
         "band": {"ori": "V", "c0": x0, "c1": x1, "lo": y0, "hi": y1}}
    w.update(kw)
    return w


def canon(walls, **kw):
    c = {"constants": {"plan_scale_pt_per_ft": {"value": 18, "source": "A1.01 scale"}}, "walls": walls}
    c.update(kw)
    return c


# ---------------- chequeos_v72 ----------------
@caso("R72.1 segmento sin tag de un type K = falla")
def _():
    import chequeos_v72 as C
    c = canon([H("K1", "A1K", 0, 8, 0, 54, 3.0, hatch_extent={"value_ft": 3.0, "source": "A1.01 vector", "img": "x.png"}),
               V("K1r", "A1K", 54, 62, 0, 14, 0.78, tags=())])
    f = C.revisar(c)["fallas"]
    assert any("K1r" in x and "R72.1" in x for x in f), f


@caso("R72.1 wall K sin hatch_extent o con largo distinto al hatch = falla; igual = OK")
def _():
    import chequeos_v72 as C
    sin = C.revisar(canon([H("K1", "B2K", 0, 8, 0, 54, 1.77)]))["fallas"]
    assert any("hatch_extent" in x for x in sin), sin
    mal = C.revisar(canon([H("K1", "B2K", 0, 8, 0, 54, 1.77, hatch_extent={"value_ft": 1.5, "source": "A1.01 vector",
                                                                            "img": "x.png"})]))["fallas"]
    assert any("!= hatch_extent" in x for x in mal), mal
    ok = C.revisar(canon([H("K1", "B2K", 0, 8, 0, 54, 1.5, hatch_extent={"value_ft": 1.5, "source": "A1.01 vector",
                                                                          "img": "x.png"})]))["fallas"]
    assert not ok, ok


@caso("R72.2 diagonal = promedio de las dos caras; sin caras = falla")
def _():
    import chequeos_v72 as C
    w = {"id": "D1", "tag": "F", "element": "wall", "length_ft": 10.0, "tag_ids": ["PT9"],
         "band": {"ori": "D", "p0": [0, 0], "p1": [180, 0]}}
    f = C.revisar(canon([w]))["fallas"]
    assert any("faces_top" in x for x in f), f
    w["band"].update(faces_top=[[0, 0], [171, 0]], faces_bottom=[[0, 8], [189, 8]])     # 9.5 y 10.5 -> 10.0
    assert not C.revisar(canon([w]))["fallas"]
    w["length_ft"] = 9.5                                                               # la cara corta: falla
    assert any("promedio" in x for x in C.revisar(canon([w]))["fallas"])


def _pier():
    ext = {"id": "PX", "tag": "EXT", "element": "pier", "sheet": "A1.01", "length_ft": 3.0, "tag_ids": [],
           "location": "exterior", "stud_size": "6\"", "band": {"ori": "BOX", "c0": 100, "c1": 140, "lo": 10, "hi": 40}}
    inte = {"id": "PC", "tag": "C1", "element": "pier", "sheet": "A1.01", "length_ft": 3.2, "tag_ids": ["PT5"],
            "stud_size": "3-5/8\"", "band": {"ori": "BOX", "c0": 101, "c1": 139, "lo": 9, "hi": 41}}
    return ext, inte


@caso("R72.3 parte sin tag de un box: sin part_of = falla; partition_types no la cuenta como wall")
def _():
    import chequeos_v72 as C
    import partition_types as PTY
    ext, inte = _pier()
    fac = H("E1", "EXT", 0, 8, 0, 360, 20.0, tags=(), location="exterior", stud_size="6\"")
    c = canon([fac, ext, inte])
    assert any("R72.3" in x and "PX" in x for x in C.revisar(c)["fallas"])
    ext["part_of"] = "PC"
    assert not [x for x in C.revisar(c)["fallas"] if "R72.3" in x]
    r = PTY.partition_types(c)
    assert r["types"]["EXT-6CFMF"]["walls"] == 1, r["types"]["EXT-6CFMF"]
    assert any(o["id"] == "PX" and o["element"] == "pier_part" for o in r["other_framing"]), r["other_framing"]


@caso("R72.4 vigas_sobre_walls manda: override 'estricto' o sin imagen = falla")
def _():
    import chequeos_v72 as C
    c = canon([V("G1", "G", 0, 9, 0, 54, 3.0)])
    vig = {"walls_bajo_viga": [{"wall": "G1", "profile": "W14X30", "beam_axis_pt": 10.5}]}
    assert any("R72.4" in x for x in C.revisar(c, vig)["fallas"])
    c["walls"][0]["beam_override"] = {"motivo": "eje fuera de la band (lectura estricta)", "source": "1/S2.01",
                                      "img": "x.png"}
    assert any("estricta" in x for x in C.revisar(c, vig)["fallas"])
    c["walls"][0].pop("beam_override")
    c["walls"][0]["stops_under_beam"] = {"value": True, "source": "S2.01"}
    assert not C.revisar(c, vig)["fallas"]


@caso("R72.5 MEP: sin method/xy = falla; FD del schedule y del barrido del mismo tamaño = falla")
def _():
    import chequeos_v72 as C
    c = canon([], mep_penetrations=[{"ref": "FD 14x14", "wall": "W1", "width_in": 14, "xy": [1, 2],
                                     "method": "mep.cruces"},
                                    {"ref": "duct 8in", "wall": "W1", "dia_in": 8}],
              opening_schedule={"items": [{"ref": "FD-1 14x14 room", "kind": "fire_damper"}]})
    f = C.revisar(c)["fallas"]
    assert any("duct 8in" in x and "method" in x for x in f), f
    assert any("contado dos veces" in x for x in f), f


@caso("R72.6 face side con letra de brújula = falla")
def _():
    import chequeos_v72 as C
    w = H("W1", "A1", 0, 8, 0, 90, 5.0, faces=[{"side": "N", "length_ft": 5.0}])
    assert any("R72.6" in x for x in C.revisar(canon([w]))["fallas"])
    w["faces"][0]["side"] = "A"
    assert not C.revisar(canon([w]))["fallas"]


@caso("R72.6 board_caras: face END con largo suma board y no entra en Σ(side); sin length_source = error")
def _():
    import board_caras as BC
    fn = [getattr(BC, n) for n in dir(BC) if n in ("calcular", "board", "caras")]
    fn = fn[0] if fn else None
    assert fn is not None, "board_caras sin función de cálculo"
    d = {"details": {"1/A1.01": {"layers_per_face": 1}},
         "walls": [{"id": "W1", "detail": "1/A1.01", "length_printed_ft": 10.0,
                    "faces": [{"room": "R1", "board": "5/8 regular", "layers": 1, "height_ft": 10.0, "side": "A",
                               "length_ft": 10.0, "length_source": "A1.01"},
                              {"room": "R1", "board": "5/8 regular", "layers": 1, "height_ft": 10.0, "side": "END",
                               "length_ft": 0.667, "length_source": "A1.01 return"}]}]}
    r = fn(d)
    assert abs(r["totales_sf"]["5/8 regular"] - 106.67) < 0.01, r["totales_sf"]
    d["walls"][0]["faces"][1].pop("length_source")
    try:
        fn(d)
        raise AssertionError("END sin length_source debía fallar")
    except ValueError:
        pass


# ---------------- particion (R72.7) ----------------
@caso("R72.7 stub sin tag <= 6\" no es wall propio; se suma al wall con tag más cercano")
def _():
    import particion
    ws = [V("G1", "G", 0, 9, 0, 54, 3.0, tags=("PT1",)),
          {"id": "BH", "tag": "G", "element": "door_bulkhead", "sheet": "A1.01", "length_ft": 7.5, "tag_ids": [],
           "band": {"ori": "V", "c0": 0, "c1": 9, "lo": 54, "hi": 189}},
          V("G5", "G", 0, 9, 189, 195, 0.333, tags=()),
          H("G8", "G", 195, 204, 40, 220, 10.0, tags=("PT2",))]
    r = particion.particion(canon(ws), "eje")
    g = r["types"]["G"]
    assert g["walls"] == 2, g
    assert abs(g["lf"] - 13.333) < 0.01, g


@caso("protección: grupo sin tag de más de 6\" sigue siendo UN wall (alcove)")
def _():
    import particion
    ws = [H("A", "A1", 0, 8, 0, 180, 10.0, tags=("PT1",)),
          V("u1", "A1", 400, 408, 0, 36, 2.0, tags=()), H("u2", "A1", 36, 44, 400, 460, 3.33, tags=()),
          V("u3", "A1", 452, 460, 0, 36, 2.0, tags=())]
    r = particion.particion(canon(ws), "eje")
    assert r["types"]["A1"]["walls"] == 2, r["types"]["A1"]


# ---------------- accesorios ----------------
def _acc():
    import accesorios
    return accesorios, accesorios.Out()


@caso("R72.8 expansion anchors: solo walls exteriores; column wrap a pins; parte de box a RFI")
def _():
    A, o = _acc()
    ext, inte = _pier()
    ext["part_of"] = "PC"
    col = {"id": "COL", "tag": "CANOPY-COL", "element": "column_wrap", "location": "exterior", "length_ft": 6.0,
           "tag_ids": [], "band": {"ori": "BOX", "c0": 500, "c1": 520, "lo": 500, "hi": 520}}
    fac = H("E1", "EXT-6CFMF", 0, 8, 0, 360, 20.0, tags=(), location="exterior")
    data = canon([fac, ext, inte, col])
    A.pins_anchors(data, o)
    assert abs(o.fam[A.F_ANCH] - 20.0 / (8 / 12)) < 0.01, o.fam[A.F_ANCH]
    assert abs(o.fam[A.F_PINS] - (3.2 + 6.0)) < 0.01, o.fam[A.F_PINS]
    assert any(r["familia"] == A.F_ANCH and abs(r["delta"] - 4.5) < 0.01 for r in o.rfis), o.rfis


def _mep_data(**kw):
    d = canon([H("W1", "B", 0, 8, 0, 200, 10.0), H("G1", "G", 50, 59, 0, 200, 10.0, rows=2)],
              mep_sweep={"sheets": ["P1.01", "M1.01"], "source": "mep.registro in this run",
                         "registro": {"dx_pt": 1.0, "dy_pt": 2.0, "matches": 40, "source": "mep.registro"}})
    d.update(kw)
    return d


@caso("R72.5 FD de openings_extra y del barrido con el mismo tamaño se cuenta UNA vez")
def _():
    A, o = _acc()
    d = _mep_data(openings_extra=[{"ref": "FD-1 R-2 14x14 room", "kind": "fire_damper", "width_in": 14, "wall": "W1"}],
                  mep_penetrations=[{"ref": "FD R-2 14x14", "wall": "W1", "width_in": 14, "xy": [10, 4],
                                     "source": "6/S5.01; M1.01"}])
    A.stud_reinforcement(d, None, o)
    assert o.fam[A.F_REINF] == 1, o.filas


@caso("R72.9 plates por fila de studs (double row = 2) con RFI de la alternativa")
def _():
    A, o = _acc()
    d = _mep_data(mep_penetrations=[{"ref": "duct 8x10", "wall": "G1", "width_in": 8, "xy": [10, 54],
                                     "source": "6/S5.01; M1.01"}])
    A.stud_reinforcement(d, None, o)
    assert o.fam[A.F_REINF] == 2, o.filas
    assert any(r["familia"] == A.F_REINF and r["delta"] == -1 for r in o.rfis), o.rfis


def _frp(ic):
    return canon([], frp={"top_ft": {"value": 5.0, "source": "A/A8.01"}, "rooms": ["1"]},
                 tile_base=[{"room": "1", "perimeter_ft": 30.0, "perimeter_basis": "net", "doors": [],
                             "inside_corners": ic}])


@caso("R72.10 FRP: > 4 vértices sin jogs = falla de compuerta; notch < 6\" no lleva inside corner trim (RFI)")
def _():
    import chequeos_v72 as C
    sin = _frp({"value": 7, "vertices": 10, "outside_corners": 3, "source": "1/A8.01"})
    assert any("R72.10" in x for x in C.revisar(sin)["fallas"])
    A, o = _acc()
    ic = {"value": 7, "vertices": 10, "outside_corners": 3, "source": "1/A8.01",
          "jogs": [{"kind": "notch", "depth_in": 2.5, "source": "1/A8.01 vector"},
                   {"kind": "step", "depth_in": 12, "source": "1/A8.01 vector"}]}
    A.pvc_trim(_frp(ic), o)
    assert abs(o.fam[A.F_PVC] - (60.0 + 5 * 5.0)) < 0.01, o.filas
    assert any(r["familia"] == A.F_PVC and abs(r["delta"] - 10.0) < 0.01 for r in o.rfis), o.rfis


@caso("R72.11 ATM recess con dato CRITERIO sin alternativas = falla de compuerta; con alternativas = RFI con delta")
def _():
    A, o = _acc()
    ar = {"width_ft": 2.2, "width_status": "CONFIRMADO", "width_source": "5/A8.11", "sistered_h_ft": 6.0,
          "sistered_h_status": "CRITERIO", "sistered_h_source": "6/A8.11", "furring_rows": 0,
          "furring_rows_status": "CRITERIO", "furring_rows_source": "6/A8.11", "rfi": "RFI-1", "source": "6/A8.11"}
    d = canon([H("W1", "EXT", 0, 8, 0, 200, 10.0, oc_in=16, openings=[{"ref": "ATM-1", "kind": "atm",
                                                                      "atm_recess": ar}])])
    import chequeos_v72 as C
    assert any("R72.11" in x for x in C.revisar(d)["fallas"])
    A.extra_framing(d, o)
    assert any("R72.11" in x for x in o.avisos), o.avisos
    A, o = _acc()
    ar["alternativas"] = [{"label": "sistered to the deck", "sistered_h_ft": 12.0}]
    assert not [x for x in C.revisar(d)["fallas"] if "R72.11" in x]
    A.extra_framing(d, o)
    assert any(r["familia"] == A.F_XATM and abs(r["delta"] - 18.0) < 0.01 for r in o.rfis), o.rfis


# ---------------- plantilla_excel (R71.8b) ----------------
@caso("R71.8b fusionar respeta renglones por tamaño y exige que sumen la familia")
def _():
    import plantilla_excel as PEX
    fo = {"familias": {"bottom track (todos)": 100.0},
          "accesorios": {"familias": {}, "estado": {}, "unidades": {}, "waste": {}, "filas": [], "avisos": [],
                         "rfis": [], "nombres_excel": {}, "excluidas": []}}
    import copy
    d = copy.deepcopy(PEX.EJEMPLO)
    d["materials"] = [
        {"material": "Bottom track 6\"", "unit": "LF", "net": 60.0, "source": "familias_out.json 'bottom track (todos)'"},
        {"material": "Bottom track 3-5/8\"", "unit": "LF", "net": 40.0, "source": "familias_out.json 'bottom track (todos)'"}]
    out = PEX.fusionar(copy.deepcopy(d), fo)
    nets = sorted(m["net"] for m in out["materials"] if str(m["material"]).startswith("Bottom track"))
    assert nets == [40.0, 60.0], nets
    d["materials"][1]["net"] = 100.0
    try:
        PEX.fusionar(d, fo)
        raise AssertionError("dos renglones que suman 160 contra la familia 100 debían fallar")
    except ValueError as e:
        assert "repartida" in str(e) or "R71.8b" in str(e), e


@caso("R71.8b verificar: Σ renglones por tamaño != familia de familias_out = error")
def _():
    import openpyxl
    import plantilla_excel as PEX
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Partition Takeoff"
    ws.append(["x"]); ws.append(["x"]); ws.append(["x"])
    ws.append(["Partition / Scope", "Wall #", "Length (LF)", "Height (FT)", "Layers", "Stud Size"])
    ws.append(["A1 #1", "1", 10, 10, 2, "3-5/8\""])
    ws.append(["G #2", "2", 10, 10, 4, "1-5/8\""])
    ms = wb.create_sheet("Material Summary")
    ms.append(["t"]); ms.append(["t"]); ms.append(["Material", "Unit", "Net"])
    for n in ("Bottom track 3-5/8\"", "Bottom track 1-5/8\"", "Bottom track other"):
        ms.append([n, "LF", 500.0])
    for n in ("Top / deflection track 3-5/8\"", "Top / deflection track 1-5/8\""):
        ms.append([n, "LF", 250.0])
    assert not [e for e in PEX.verificar_r71_track(wb) if "R71.8b" in e]      # sin familia: no adivina
    err = PEX.verificar_r71_track(wb, {"bottom track": 500.0, "top / deflection track": 500.0})
    assert any("Σ bottom track" in e for e in err), err


# ---------------- etapas unir (P-02) ----------------
@caso("P-02 unir: 18 vs 18.0 con fuentes distintas = OK (fuentes unidas); 18 vs 19 = error; metadatos por fragmento")
def _():
    import etapas
    with tempfile.TemporaryDirectory() as t:
        json.dump({"fragment": "A1", "constants": {"plan_scale_pt_per_ft": {"value": 18, "source": "A1.01 scale"}},
                   "walls": []}, open(os.path.join(t, "a.json"), "w"))
        json.dump({"fragment": "A2", "constants": {"plan_scale_pt_per_ft": {"value": 18.0, "source": "1/A1.01 bar"}},
                   "walls": []}, open(os.path.join(t, "b.json"), "w"))
        c, err = etapas.unir(t)
        assert not err, err
        assert "|" in c["constants"]["plan_scale_pt_per_ft"]["source"], c["constants"]
        assert isinstance(c["fragment"], dict), c["fragment"]
        json.dump({"constants": {"plan_scale_pt_per_ft": {"value": 19, "source": "x"}}, "walls": []},
                  open(os.path.join(t, "c.json"), "w"))
        c, err = etapas.unir(t)
        assert err, "18 vs 19 debía ser error"


if __name__ == "__main__":
    for x in OK:
        print("OK  ", x)
    for x in FALLOS:
        print("FALLA", x)
    print(f"{len(OK)} OK, {len(FALLOS)} falla(s)")
    sys.exit(1 if FALLOS else 0)
