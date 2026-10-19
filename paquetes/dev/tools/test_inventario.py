#!/usr/bin/env python3
"""Tests de inventario.py v63 con bandas SINTÉTICAS (pt, 18 pt/ft; v73: ningún dato de un set real).
Cada test falla con el dato malo de #13A o #13B y pasa con el bueno."""
import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inventario as I  # noqa: E402

S = {"value": 18, "source": "Z1.01 1/4\" = 1'-0\""}


def W(id_, tag, ori, c0, c1, lo, hi, L=None, **kw):
    w = {"id": id_, "tag": tag, "element": kw.pop("element", "wall"), "stud_size": kw.pop("stud_size", "3-5/8\""),
         "oc_in": 16, "rows": kw.pop("rows", 1), "length_ft": L if L is not None else round((hi - lo) / 18.0, 3),
         "height_ft": kw.pop("height_ft", 15.25), "source": "Z1.01",
         "band": {"sheet": "Z1.01", "ori": ori, "c0": c0, "c1": c1, "lo": lo, "hi": hi}}
    w.update(kw)
    return w


def D(*walls, **const):
    c = {"plan_scale_pt_per_ft": S}
    c.update(const)
    return {"constants": c, "walls": list(walls)}


def _falla(d, txt):
    try:
        I.verificar(d)
    except ValueError as e:
        assert txt in str(e), str(e)
        return
    raise AssertionError("debía fallar: " + txt)


# Coordenadas SINTÉTICAS (escala 1.25 + offset sobre un caso de prueba; E24)
XJ = W("X-J", "EXT", "H", 1087.9, 1114.45, 1088.95, 1156.9, stud_size="6\"", height_ft=10.737)


def test_g4_13b_corre_sobre_el_jog():
    """#13B: el G arrancó en la cara exterior y sus primeros pies corren pegados al jog X-J."""
    _falla(D(XJ, W("X-4", "G", "H", 1075.45, 1087.0, 1088.95, 1454.35, rows=2, stud_size="1-5/8\"")),
           "corren uno junto al otro 3.78 ft")
    # bueno: el G arranca en la cara del jog; sin solape
    I.verificar(D(XJ, W("X-4", "G", "H", 1075.45, 1087.0, 1175.75, 1454.35, rows=2, stud_size="1-5/8\"")))


def test_b2k_13a_entra_al_a1k():
    """#13A: el B2K medido más largo que su banda entra al A1K que sigue en la misma línea."""
    a1k = W("K-w1", "A1K", "H", 1437.85, 1447.6, 2104.45, 2181.25, L=4.27, length_printed_ft=4.27)
    malo = W("K-w2", "B2K", "H", 1420.15, 1434.55, 2076.1, 2076.1 + 2.207 * 18, stud_size="6\"")
    _falla(D(a1k, malo), "corren uno junto al otro")
    I.verificar(D(a1k, W("K-w2", "B2K", "H", 1420.15, 1434.55, 2076.1, 2104.45, stud_size="6\"")))


def test_largo_banda_vs_canon_y_cota_manda():
    w = W("X-5", "G", "H", 1323.25, 1334.65, 1176.85, 1438.45, L=13.0)
    _falla(D(w), "banda 14.533 ft != length_ft 13.0")
    w2 = W("DB-109", "G", "V", 1446.85, 1454.35, 1098.25, 1259.5, L=9.375, length_printed_ft=9.375,
           element="door_bulkhead")
    out = I.verificar(D(w2))
    assert any("DISCREPANCIA DB-109" in a for a in out["avisos"]), out


def test_pieza_alta_apilada_13b():
    """#13B X-N1 + X-N1u en la misma huella (line F / 'Fu'): <n> LF de bottom y de top track."""
    lo = W("X-N1", "EXT", "H", 437.05, 458.8, 2056.45, 2362.6, stud_size="6\"", height_ft=10.935,
           canopy_beam={"tos_ft": 11.948, "depth_ft": 1.017, "source": "S2.20 W12x19 (CANOPY)"})
    hi = W("X-N1u", "EXT", "H", 437.05, 458.8, 2056.45, 2362.6, stud_size="6\"", height_ft=2.414)
    _falla(D(lo, hi), "canopy_beam_split")
    no = {"value": False, "source": "decisión del usuario (RFI)"}
    _falla(D(lo, hi, canopy_beam_split=no), "misma huella sin split_of")
    hi2 = dict(hi, split_of="X-N1")
    _falla(D(lo, hi2, canopy_beam_split=no), "split_of X-N1 con canopy_beam_split false")
    I.verificar(D(lo, hi2, canopy_beam_split={"value": True, "source": "decisión del usuario"}))
    out = I.verificar(D(lo, canopy_beam_split=no))
    assert out["rfi_split"][0]["bottom_track_lf"] == 17.01 and out["avisos"], out


def test_mr_solo_detras_de_toilet_y_lavatory_13b():
    """F/A08.01 'MOISTURE RESISTANT GYPSUM BOARD BEHIND TOILET AND LAVATORY': los dos van en el chase C1
    (A08.01 enlarged plan). El nicho del corridor (W-r) es el drinking fountain: sin MR."""
    c1 = W("W-p", "C1", "H", 1740.4, 1752.0, 1176.85, 1402.45,
           faces=[{"room": "914", "board": "5/8 MR", "layers": 1, "height_ft": 12.918}],
           adjacent_to="W-q", adjacent_source="A12.01 C1 chase (2 rows)")
    c2 = W("W-q", "C1", "H", 1752.0, 1764.7, 1176.85, 1402.45,
           faces=[{"room": "913", "board": "5/8 MR", "layers": 1, "height_ft": 12.896}])
    fx = [{"ref": "WC 914", "kind": "water_closet", "wall": "W-p", "room": "914", "source": "A08.01"},
          {"ref": "LAV 914", "kind": "lavatory", "wall": "W-p", "room": "914", "source": "A08.01"},
          {"ref": "WC 913", "kind": "water_closet", "wall": "W-q", "room": "913", "source": "A08.01"},
          {"ref": "LAV 913", "kind": "lavatory", "wall": "W-q", "room": "913", "source": "A08.01"}]
    d = D(c1, c2)
    d["wet_fixtures"] = fx
    I.verificar(d)
    nicho = W("W-r", "C1", "V", 1411.6, 1454.35, 1706.95, 1798.6,
              faces=[{"room": "911", "board": "5/8 MR", "layers": 1, "height_ft": 12.949}])
    d2 = copy.deepcopy(d)
    d2["walls"].append(nicho)
    _falla(d2, "faces MR sin fixture detrás")
    d2["wet_fixtures"].append({"ref": "EWC", "kind": "drinking_fountain", "wall": "W-r", "room": "911",
                               "source": "Z1.01"})
    _falla(d2, "un drinking fountain NO")
    d3 = copy.deepcopy(d)
    d3["walls"][1]["faces"][0]["board"] = "5/8 regular"
    _falla(d3, "fixtures sin face MR")


def test_chase_doble_necesita_adjacent_to():
    c1 = W("W-p", "C1", "H", 1740.4, 1752.0, 1176.85, 1402.45)
    c2 = W("W-q", "C1", "H", 1752.0, 1764.7, 1176.85, 1402.45)
    _falla(D(c1, c2), "corren uno junto al otro 12.53 ft")
    _falla(D(dict(c1, adjacent_to="W-q"), c2), "adjacent_to sin adjacent_source")


def test_purlin_por_flute_13b():
    """Flute H: purlin en walls H; #13B puso purlin a los door bulkheads (V)."""
    fl = {"value": "H", "source": "S2.20 deck entre joists; 10/A09.33"}
    g = W("X-5", "G", "H", 1323.25, 1334.65, 1176.85, 1438.45, purlin=True)
    db = W("DB-109", "G", "V", 1446.85, 1454.35, 1098.25, 1259.5, L=9.375, length_printed_ft=9.375,
           element="door_bulkhead", purlin=True)
    _falla(D(g, db, deck_flute_dir=fl), "DB-109(V: purlin no)")
    I.verificar(D(g, dict(db, purlin=False), deck_flute_dir=fl))
    _falla(D(dict(g, purlin=False), deck_flute_dir=fl), "X-5(H: purlin sí)")
    # exterior bajo perimeter beam: no llega a deck
    x = W("X-S1a", "EXT", "H", 2153.8, 2175.55, 1156.9, 1943.25, stud_size="6\"", to_deck=False)
    I.verificar(D(x, deck_flute_dir=fl))


def test_roof_step_una_purlin_por_run_13b():
    rs = [{"id": f"RS-{i}", "element": "roof_step", "stud_size": "3-5/8\"", "length_ft": 50.0, "height_ft": h,
           "straight_run": "B", "purlin": p, "source": "4/A02.02"} for i, h, p in ((1, 3.3, False), (2, 3.49, True),
                                                                                    (3, 1.18, True))]
    _falla(D(*rs, deck_flute_dir={"value": "H", "source": "S2.20"}), "una pieza (59.1)")
    rs[2]["purlin"] = False
    I.verificar(D(*rs, deck_flute_dir={"value": "H", "source": "S2.20"}))


def test_altura_por_zona_13b():
    """Y2-2a/b cayeron al HI (<n>) estando bajo el low roof sur."""
    z = {"value": {"HI": {"stud_h_ft": 15.25, "source": "S2.20"},
                   "LOW-S": {"stud_h_ft": 12.75, "source": "S2.20 B.O.D. 13'-0 5/8\" a 12'-6 3/8\""}},
         "source": "S2.20"}
    w = W("Y2-2a", "B2", "V", 1440.85, 1454.35, 1582.45, 1706.95, stud_size="6\"", zone="LOW-S")
    _falla(D(w, deck_zones=z), "!= zona LOW-S")
    I.verificar(D(dict(w, height_ft=12.75), deck_zones=z))


def test_sin_escala_o_sin_banda():
    _falla({"constants": {}, "walls": []}, "plan_scale_pt_per_ft")
    w = W("W-s", "A1", "H", 1246.3, 1255.45, 1566.85, 1936.3)
    del w["band"]
    _falla(D(w), "falta band")


def test_banda_diagonal_14b():
    # diagonal sintética a 30 deg: eje p0-p1 = 360 pt / 18 = 20.0 ft; un largo distinto falla  [ciego-ok]
    f = W("QD-91", "F", "H", 0, 1, 0, 1, L=20.0)
    f["band"] = {"sheet": "Z1.01", "ori": "D", "p0": [100.0, 100.0], "p1": [411.769, 280.0]}
    assert I.verificar(D(f))["ok"]
    malo = copy.deepcopy(f); malo["length_ft"] = 21.2
    _falla(D(malo), "banda D")
    sin = copy.deepcopy(f); del sin["band"]["p1"]
    _falla(D(sin), "p0 [x,y]")


if __name__ == "__main__":
    n = 0
    for k, f in list(globals().items()):
        if k.startswith("test_") and callable(f):
            f()
            n += 1
            print("OK", k)
    print(f"{n} tests OK")
