#!/usr/bin/env python3
"""Tests v70 de accesorios.py con datos SINTÉTICOS (números inventados). Correr: python3 test_accesorios_v70.py

- sill_return false + sill_return_source N/HOJA: el jamb return (y su trim) omite el borde del sill; el double
  sill track (headers.py) no cambia. sill_return false sin source -> ValueError.
- atm_recess.*_status = CRITERIO aceptado con rfi; sin rfi -> ValueError.
"""
import copy
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import accesorios as A  # noqa: E402
import canon as K  # noqa: E402
from test_canon import base  # noqa: E402
from test_accesorios import canon_base, fam_base, STUDS  # noqa: E402

F_JR = "gypsum board jamb return"
F_TRIM = "metal trim (corner bead, casing, shadow molding)"


def _err(c, txt):
    try:
        A.calcular(fam_base(), c, STUDS)
    except ValueError as e:
        assert txt in str(e), e
        return
    raise AssertionError("debía fallar: " + txt)


def test_sill_return_false_omite_borde_del_sill():
    c = canon_base()
    win = c["walls"][0]["openings"][0]                      # ventana 6.0 x head 7.0 / sill 3.0, with_sill
    o0 = A.calcular(fam_base(), copy.deepcopy(c), STUDS)["familias"][F_JR]
    win.update(sill_return=False, sill_return_source="10/X9.27")
    o1 = A.calcular(fam_base(), c, STUDS)["familias"][F_JR]
    assert abs((o0 - o1) - 6.0 * 0.5) < 0.011, (o0, o1)     # solo el borde inferior (R.O.) x ancho del return
    assert A._edge(win) == 6.0 + 2 * 7.0 - 2 * 3.0, A._edge(win)


def test_sill_return_false_sin_source():
    c = canon_base()
    c["walls"][0]["openings"][0]["sill_return"] = False
    c["walls"][0]["openings"][0].pop("sill_return_source", None)    # v75: la base ya declara el sill (R75.3)
    _err(copy.deepcopy(c), "sill_return_source")
    c["walls"][0]["openings"][0]["sill_return_source"] = "según detalle"           # sin N/HOJA
    _err(c, "sill_return_source")


def test_canon_sill_track_igual_return_y_trim_sin_sill():
    d0 = base()
    f0 = K.calcular(copy.deepcopy(d0))["familias"]
    d1 = copy.deepcopy(d0)
    op = d1["walls"][0]["openings"][0]
    assert op["with_sill"] and op["ro_w_ft"] > 4.0           # sill track doble (2 piezas)
    op.update(sill_return=False, sill_return_source="10/Z9.27")
    f1 = K.calcular(d1)["familias"]
    assert abs(f1["sill track"] - f0["sill track"]) < 1e-9, (f0["sill track"], f1["sill track"])
    assert abs(f0[F_JR] - f1[F_JR] - op["ro_w_ft"] * 0.5) < 0.011, (f0[F_JR], f1[F_JR])
    assert f1[F_TRIM] < f0[F_TRIM] - 1.0, (f0[F_TRIM], f1[F_TRIM])
    import headers as H                                     # headers.py: 2 piezas con y sin sill_return
    o = {"ref": "w", "kind": "window", "location": "exterior", "ro_w_ft": 6.0, "qty": 1, "with_sill": True,
         "source": "Z9.02", "header_type": "DOUBLE TRACK", "header_type_source": "7/Z5.20", "pieces": 2,
         "pieces_source": "7/Z5.20", "sill_return": False, "sill_return_source": "10/Z9.27"}
    a = H.calcular({"openings": [dict(o)]})["totales_lf"]["sill track"]
    o.pop("sill_return")
    b = H.calcular({"openings": [o]})["totales_lf"]["sill track"]
    assert a == b and abs(a - 2 * (6.0 + 16 / 12)) < 0.05, (a, b)        # 2 piezas x (R.O. + 1'-4")


def _atm(c, status, rfi=None):
    ar = {"width_ft": 4.0, "width_source": "X2.01 vector", "width_status": "CONFIRMADO", "sistered_h_ft": 6.0,
          "sistered_h_source": "6/X8.11", "sistered_h_status": "CONFIRMADO", "furring_rows": 3,
          "furring_rows_source": "6/X8.11 (criterio: filas no dibujadas)", "furring_rows_status": status,
          "source": "6/X8.11"}
    if rfi:
        ar["rfi"] = rfi
    c["walls"][0]["openings"].append({"ref": "ATM 9", "kind": "window", "ro_w_ft": 2.0, "head_ft": 5.0,
                                      "sill_ft": 3.0, "jamb_return": True, "substrate_none_reason": "sintético (v76 R76.4)", "jamb_return_source": "6/X8.11", "jamb_return_label": "GYPSUM BOARD JAMB RETURN",
                                      "atm_recess": ar})
    return c


def test_atm_recess_criterio_con_rfi():
    o = A.calcular(fam_base(), _atm(canon_base(), "CRITERIO", "RFI-X-1"), STUDS)
    assert o["estado"]["extra framing ATM"] == "CRITERIO", o["estado"]["extra framing ATM"]
    assert any(r["familia"] == "extra framing ATM" for r in o["rfis"])
    _err(_atm(canon_base(), "CRITERIO"), "rfi")
    _err(_atm(canon_base(), "SUPUESTO", "RFI-X-1"), "CRITERIO")


def _gh(chain, src="4/X8.21", **kw):
    c = canon_base()
    gh = [w for w in c["walls"] if w["id"] == "GH"][0]
    gh["head_build"] = dict({"head_ft": sum(chain) / 12.0, "head_chain_in": chain, "box_depth_ft": 0.5, "n_box": 2,
                             "board_in": 0.625, "source": src}, **kw)
    return c


def test_r70_9_cadena_del_head():
    _err(_gh([30], "4/X8.21: studs in the 2'-6\" zone; 1'-0\" zone above by vendor"), "R70.9")
    _err(_gh([30], head_chain_source="4/X8.21 chain of two dims"), "R70.9")
    o = A.calcular(fam_base(), _gh([12, 18], "4/X8.21: 1'-0\" + 1'-6\" chain"), STUDS)
    n = 7                                                     # ROUNDUP(8.0 / 1.333) + 1
    sl = 30 / 12.0 - 2 * 0.5 - 0.625 / 12.0                   # Σ cadena − n_box x box − board
    f = [k for k in o["familias"] if "2-1/2" in k][0]
    assert abs(o["familias"][f] - n * sl) < 0.011, (o["familias"][f], n * sl)
    A.calcular(fam_base(), _gh([24], "4/X8.21 head 2'-0\""), STUDS)    # una cota sola y sin cadena: aceptado


def test_storefront_cripples_fuera_de_pins_y_anchors():
    c = canon_base()
    inte0, ext0 = A.track_slab(c)
    c["walls"].append({"id": "SC", "tag": "EXT", "element": "storefront_cripples", "stud_size": "6\"", "oc_in": 16,
                       "rows": 1, "length_ft": 25.0, "height_ft": 3.0, "location": "exterior"})
    inte1, ext1 = A.track_slab(c)
    assert inte1 == inte0 and ext1 == ext0, (ext0, ext1)
    assert "SC" not in [x[0] for x in inte1 + ext1]


if __name__ == "__main__":
    fallas = 0
    for k, f in sorted(globals().items()):
        if k.startswith("test_") and callable(f):
            try:
                f()
                print("OK  ", k)
            except Exception as e:  # noqa: BLE001
                fallas += 1
                print("FALLA", k, type(e).__name__, str(e)[:300])
    print(f"{'TODOS OK' if not fallas else str(fallas) + ' FALLA(S)'}")
    sys.exit(1 if fallas else 0)
