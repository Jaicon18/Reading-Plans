#!/usr/bin/env python3
"""Tests v71 (arbitraje #19) con datos SINTÉTICOS (ningún dato de proyecto). Correr: python3 test_v71.py

Uno por cambio; cada uno falla con las tools v70c:
  particion "eje" (default)       test_eje_*            partition_types tag_ids    test_pt_eje_tag_ids
  Layers ponderado                test_layers_*         mep.py sin offsets (E24)   test_mep_*
  chequeos_v71 (R71.1/2/3/5)      test_chq_*            headers R71.10 / R71.11    test_hdr_*
  plantilla R71.8 track/tamaño    test_track_excel_*    track_por_tamano.py        test_track_desglose
  vigas_sobre_walls P4            test_vigas_*          etapas compuerta v71       test_etapas_llama_v71
  accesorios PAFs por run / chase test_paf_*, test_chase_*   framed_openings _src  test_framed_openings_*
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

E = 18.0


def w(id_, tag, ori, eje, lo, hi, esp=6.0, tags=None, **kw):
    d = {"id": id_, "tag": tag, "length_ft": round((hi - lo) / E, 4), "sheet": "Z1.01",
         "band": {"ori": ori, "c0": eje - esp / 2, "c1": eje + esp / 2, "lo": lo, "hi": hi}}
    if tags is not None:
        d["tag_ids"] = tags
    d.update(kw)
    return d


def canon(walls, **kw):
    d = {"constants": {"plan_scale_pt_per_ft": {"value": E, "source": "sintético"}}, "walls": walls}
    d.update(kw)
    return d


def grupos(r, t=None):
    return sorted(tuple(sorted(f["ids"])) for k, d in r["types"].items() if t in (None, k) for f in d["filas"])


# ------------------------------------------------------------------ particion "eje"
def test_eje_es_default():
    import particion as P
    assert P.MODO_DEFAULT == "eje" and "run" in P.MODOS and "tramo" in P.MODOS


def test_eje_esquina_entre_dos_tags_corta():
    """L entre dos segmentos CON tag = 2 walls (el estimador corta en la esquina; run daba 1)."""
    import particion as P
    c = canon([w("a", "X1", "H", 100, 0, 180, tags=["T1"]), w("b", "X1", "V", 177, 103, 280, tags=["T2"])])
    assert grupos(P.particion(c)) == [("a",), ("b",)], grupos(P.particion(c))


def test_eje_return_sin_tag_se_suma():
    """Return corto SIN tag en el extremo de un wall con tag = parte de ese wall (no wall propio)."""
    import particion as P
    c = canon([w("a", "X1", "H", 100, 0, 180, tags=["T1"]), w("r", "X1", "V", 177, 103, 110)])
    r = P.particion(c)
    assert grupos(r) == [("a", "r")], grupos(r)
    assert r["types"]["X1"]["filas"][0]["sin_tag_sumado"] == ["r"]


def test_eje_grupo_sin_tag_es_un_wall():
    """U sin ningún tag (alcove) dentro de un type que sí trae tags = 1 wall (criterio "run continuo")."""
    import particion as P
    c = canon([w("t", "X1", "H", 900, 0, 300, tags=["T1"]),
               w("u1", "X1", "H", 100, 0, 60), w("u2", "X1", "V", 3, 103, 200), w("u3", "X1", "H", 200, 0, 60)])
    g = grupos(P.particion(c))
    assert ("u1", "u2", "u3") in g and ("t",) in g and len(g) == 2, g


def test_eje_dos_tags_misma_linea_un_wall():
    """Dos tags sobre la misma línea recta, segmentos contiguos (partidos por un wall que cruza) = 1 wall."""
    import particion as P
    c = canon([w("a", "X1", "H", 100, 0, 100, tags=["T1"]), w("b", "X1", "H", 100, 100, 250, tags=["T2"])])
    assert grupos(P.particion(c)) == [("a", "b")]


def test_eje_hueco_vacio_corta_y_hueco_con_ro_une():
    """Hueco colineal vacío (alcove / pasillo) corta; hueco con el R.O. de uno de los walls (xy dentro) une."""
    import particion as P
    a = w("a", "X1", "H", 100, 0, 100, tags=["T1"])
    b = w("b", "X1", "H", 100, 160, 250, tags=["T2"])
    assert len(grupos(P.particion(canon([a, b])))) == 2
    a2 = dict(a, openings=[{"ref": "D1", "kind": "door", "xy_pt": [130.0, 100.0]}])
    r = P.particion(canon([a2, b]))
    assert grupos(r) == [("a", "b")], grupos(r)
    assert any("R70.3" in x for x in r["avisos"])


def test_eje_t_no_encadena_y_bulkhead_corta():
    import particion as P
    c = canon([w("t1", "X1", "H", 100, 0, 360, tags=["T1"]), w("t2", "X1", "V", 180, 103, 280, tags=["T2"])])
    assert len(grupos(P.particion(c))) == 2
    ws = [w("g1", "G", "V", 50, 0, 90, tags=["T1"]), w("bh", "G", "V", 50, 90, 200, element="door_bulkhead"),
          w("g2", "G", "V", 50, 200, 290, tags=["T2"])]
    r = P.particion(canon(ws))
    assert grupos(r, "G") == [("g1",), ("g2",)] and grupos(r, "BULKHEAD-G") == [("bh",)], grupos(r)


def test_eje_exterior_un_wall_por_eje():
    import particion as P
    c = canon([w("e1", "EXT-6CFMF", "H", 100, 0, 180), w("e2", "EXT-6CFMF", "V", 177, 103, 280),
               w("e3", "EXT-6CFMF", "H", 100, 180, 300)])
    assert grupos(P.particion(c)) == [("e1", "e3"), ("e2",)], grupos(P.particion(c))


def test_eje_pier_exterior_no_vuelve_exterior_al_type():
    """Un pier interior marcado exterior en el mismo type no hace que el type corte como exterior."""
    import particion as P
    pier = {"id": "p", "tag": "X1", "length_ft": 3.0, "sheet": "Z1.01", "element": "pier", "exterior": True,
            "band": {"ori": "BOX", "c0": 0, "c1": 30, "lo": 0, "hi": 40}, "tag_ids": ["T9"]}
    c = canon([w("a", "X1", "H", 100, 0, 180, tags=["T1"]), w("r", "X1", "V", 177, 103, 110), pier])
    assert ("a", "r") in grupos(P.particion(c)), grupos(P.particion(c))


def test_eje_sin_tags_corta_esquinas_y_suma_jogs():
    import particion as P
    c = canon([w("a", "X1", "H", 100, 0, 180), w("b", "X1", "V", 177, 103, 280), w("j", "X1", "V", 3, 103, 110)])
    r = P.particion(c)
    assert grupos(r) == [("a", "j"), ("b",)], grupos(r)
    assert any("tag_ids" in x for x in r["avisos"])


def test_pt_eje_tag_ids():
    """partition_types pasa tag_ids a particion: L con dos tags = 2 filas (v70c las unía en 1)."""
    import partition_types as PT
    ws = [dict(w("a", "X1", "H", 100, 0, 180, tags=["T1"]), stud_size="3-5/8\"", height_ft=10),
          dict(w("b", "X1", "V", 177, 103, 280, tags=["T2"]), stud_size="3-5/8\"", height_ft=10)]
    r = PT.partition_types(canon(ws))
    assert r["types"]["X1"]["walls"] == 2, r["types"]["X1"]


# ------------------------------------------------------------------ Layers
def test_layers_ponderado_por_largo_de_face():
    """Cara A 10 ft 1 layer + cara B partida 4 + 6 ft 1 layer c/u = 2.00 (v70c: 3)."""
    import partition_types as PT
    x = dict(w("a", "X1", "H", 100, 0, 180, tags=["T1"]), stud_size="3-5/8\"", height_ft=10,
             faces=[{"room": "1", "layers": 1, "length_ft": 10.0, "height_ft": 9},
                    {"room": "2", "layers": 1, "length_ft": 4.0, "height_ft": 9},
                    {"room": "3", "layers": 1, "length_ft": 6.0, "height_ft": 9}])
    f = PT.partition_types(canon([x]))["types"]["X1"]["filas"][0]
    assert f["layers"] == 2.0, f["layers"]


def test_layers_faces_sin_largo_mismo_side_cuentan_una_vez():
    import partition_types as PT
    x = dict(w("a", "X1", "H", 100, 0, 180, tags=["T1"]), stud_size="3-5/8\"", height_ft=10,
             faces=[{"room": "1", "layers": 2, "side": "A"}, {"room": "2", "layers": 2, "side": "A"},
                    {"room": "3", "layers": 1, "side": "B"}, {"room": "4", "layers": 1, "height_ft": 0}])
    assert PT.partition_types(canon([x]))["types"]["X1"]["filas"][0]["layers"] == 3.0


# ------------------------------------------------------------------ mep.py (E24)
def test_mep_sin_offsets_de_proyecto():
    src = open(os.path.join(AQUI, "mep.py"), encoding="utf-8").read()
    import re
    assert "OFF = {" not in src and not re.search(r"'dx':\s*-?\d{2,}\.\d", src), "offsets fijos en mep.py"
    assert not re.search(r"\bARQ\s*=\s*\d", src), "página arquitectónica fija en mep.py"


def test_mep_exige_arq():
    import mep
    try:
        mep._arq(None)
    except ValueError as e:
        assert "arq" in str(e)
    else:
        raise AssertionError("mep._arq(None) debía fallar")


# ------------------------------------------------------------------ chequeos_v71
def test_chq_r71_1_flecha_norte():
    import chequeos_v71 as Q
    c = canon([], facades=[{"id": "N"}])
    assert any("R71.1" in x for x in Q.revisar(c)["fallas"])
    c["constants"]["north_arrow"] = {"value": "up", "source": "Z1.01 north arrow", "img": "img/n.png"}
    assert not Q.revisar(c)["fallas"], Q.revisar(c)["fallas"]


def test_chq_r71_2_box_doble():
    import chequeos_v71 as Q
    bx = {"ori": "BOX", "c0": 0, "c1": 30, "lo": 0, "hi": 40}
    c = canon([{"id": "p1", "tag": "C9", "element": "pier", "band": dict(bx), "sheet": "Z1.01"},
               {"id": "p2", "tag": "EXT", "element": "pier", "band": dict(bx), "sheet": "Z1.01"}])
    assert any("R71.2" in x for x in Q.revisar(c)["fallas"])
    c["walls"][1]["band"] = {"ori": "BOX", "c0": 100, "c1": 130, "lo": 0, "hi": 40}
    assert not Q.revisar(c)["fallas"]


def test_chq_r71_3_bulkhead_y_r71_5():
    import chequeos_v71 as Q
    c = canon([w("bh", "G", "V", 50, 0, 135, element="door_bulkhead")],
              sealant_items=[{"ref": "bulkhead top sealant", "lf": 20.0}],
              tags_descartados=[{"id": "PT1", "motivo": "measured by other task"}])
    f = Q.revisar(c)["fallas"]
    assert any("R71.3" in x for x in f) and any("R71.5" in x for x in f), f
    c["sealant_items"][0]["lf"] = 7.5
    c["tags_descartados"][0]["motivo"] = "legend sample, not a wall tag"
    assert not Q.revisar(c)["fallas"], Q.revisar(c)["fallas"]


def test_etapas_llama_v71():
    src = open(os.path.join(AQUI, "etapas.py"), encoding="utf-8").read()
    assert "chequeos_v71" in src


# ------------------------------------------------------------------ headers
def _hdr(**kw):
    o = {"ref": "F1", "wall": "W1", "kind": "opening", "ro_w_ft": 30.0, "continuous_run": True, "qty": 1,
         "header_type": "CONT. BOX BEAM", "header_type_source": "9/Z5.01", "pieces": 4,
         "pieces_source": "9/Z5.01", "piece": "C box", "source": "Z1.01"}
    o.update(kw)
    return {"openings": [o]}


def test_hdr_r71_11_cont_run_ends():
    import headers as H
    try:
        H.calcular(_hdr())
    except ValueError as e:
        assert "run_ends" in str(e)
    else:
        raise AssertionError("CONT. BOX BEAM sin run_ends debía fallar")
    H.calcular(_hdr(run_ends="jamb_to_jamb", run_ends_source="9/Z5.01"))


def test_hdr_r71_10_assumed():
    import headers as H
    d = _hdr(header_type="BOX HEADER (NOT PRINTED - ASSUMED)", continuous_run=False)
    d["openings"][0].pop("continuous_run")
    try:
        H.calcular(d)
    except ValueError as e:
        assert "R71.10" in str(e)
    else:
        raise AssertionError("header ASSUMED debía fallar")


# ------------------------------------------------------------------ track por tamaño
def _wb(tams, filas_ms):
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Partition Takeoff"
    ws.append(["title"])
    ws.append(["note"])
    ws.append(["Partition / Scope", "Wall #", "Length (LF)", "Height (FT)", "Layers", "Stud Size"])
    for t in tams:
        ws.append(["X", 1, 10, 10, 2, t])
    ms = wb.create_sheet("Material Summary")
    ms.append(["t"])
    ms.append(["n"])
    ms.append(["Material", "Unit", "Net"])
    for f in filas_ms:
        ms.append([f, "LF", 10])
    return wb


def test_track_excel_r71_8():
    import plantilla_excel as PE
    malo = _wb(['6"', '3-5/8"'], ["Bottom track (all sizes)", "Top / deflection track (all sizes)"])
    assert len(PE.verificar_r71_track(malo)) == 2
    bueno = _wb(['6"', '3-5/8"'], ['Bottom track 6"', 'Bottom track 3-5/8"', 'Top / deflection track 6"',
                                   'Top / deflection track 3-5/8"'])
    assert PE.verificar_r71_track(bueno) == []
    assert PE.verificar_r71_track(_wb(['6"'], ["Bottom track (all sizes)"])) == []


def test_track_desglose():
    import track_por_tamano as T
    c = canon([dict(w("a", "X1", "H", 100, 0, 180), stud_size='3-5/8"'),
               dict(w("b", "X2", "H", 300, 0, 90), stud_size='6"', gauge="600S162-54", rows=1),
               dict(w("c", "G", "H", 500, 0, 90), stud_size='1-5/8"', rows=2)])
    r = T.desglose(c, 40.0)
    assert r["por_tamano"] == {'3-5/8"': 10.0, '6" 54 mil': 5.0, '1-5/8"': 10.0} and r["other"] == 15.0, r
    assert T.desglose(c, 20.0)["fallas"]


# ------------------------------------------------------------------ vigas_sobre_walls P4
def test_vigas_dos_paralelas_rotulo_distinto_pide_decision():
    import vigas_sobre_walls as V
    wall = w("a", "X1", "H", 100, 0, 360)
    v1 = {"p0": (0, 100), "p1": (400, 100), "lw": 2.0, "perfil": {"profile": "W12X19", "depth_ft": 1.017}}
    v2 = {"p0": (0, 109), "p1": (400, 109), "lw": 2.0, "perfil": {"profile": "W16X26", "depth_ft": 1.308}}
    r = V.cruzar([v1, v2], [wall])
    assert r and r[0]["profile"] is None and len(r[0]["candidatas"]) == 2, r
    r = V.cruzar([v1], [wall])
    assert r[0]["profile"] == "W12X19"


def test_vigas_rotulo_un_solo_dueno():
    import vigas_sobre_walls as V
    v1 = {"p0": (0, 100), "p1": (400, 100)}
    v2 = {"p0": (0, 109), "p1": (400, 109)}
    rot = [("W16X26", 200, 115)]                         # más cerca de v2
    assert V.perfil(v1, rot, otras=[v1, v2]) is None
    assert V.perfil(v2, rot, otras=[v1, v2])["profile"] == "W16X26"


# ------------------------------------------------------------------ accesorios / framed_openings
def test_paf_por_run():
    """Dos walls de parapet del mismo run: ROUNDUP sobre la suma (A7), no por wall."""
    import accesorios as A
    par = [dict(w("p1", "EXT-PARAPET", "V", 50, 0, 18 * 23.4), element="parapet"),
           dict(w("p2", "EXT-PARAPET", "V", 50, 18 * 23.4, 18 * 47.9), element="parapet")]
    runs = A._runs_parapet(par)
    assert len(runs) == 1 and abs(runs[0][1] - 47.9) < 1e-6, runs
    par2 = [dict(x, run="R1") for x in par]
    for x in par2:
        x.pop("band")
    assert len(A._runs_parapet(par2)) == 1


def test_chase_sobre_losa():
    import accesorios as A
    assert "chase" in A.ON_SLAB and "chase" not in A.NOT_ON_SLAB


def test_framed_openings_src_texto_tras_hoja():
    import framed_openings as F
    assert F._src("Z4.01 ceiling plan; spacing not printed - criterion", "x")
    try:
        F._src("spacing not printed; Z4.01", "x")
    except ValueError:
        pass
    else:
        raise AssertionError("la primera parte debe citar N/HOJA")


if __name__ == "__main__":
    fallas = 0
    for k, f in sorted(globals().items()):
        if k.startswith("test_") and callable(f):
            try:
                f()
                print("OK   ", k)
            except Exception as e:  # noqa: BLE001
                fallas += 1
                print("FALLA", k, type(e).__name__, str(e)[:300])
    print("TODOS OK" if not fallas else f"{fallas} FALLA(S)")
    sys.exit(1 if fallas else 0)
