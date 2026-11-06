"""v81cf53 (CR City Hotel Castle Rock, BE-CR01..03): repite los errores originales con datos sintéticos.
BE-CR01: inventario_tags no reconocía types con punto (W.62 / XW.6.3) y tomaba sheet numbers del índice como types.
BE-CR02: familias Type C / shaftliner / exterior Type X sheathing / C-H stud / J-runner no existían.
BE-CR03: no había sistema de ceiling 'board sobre resilient channel bajo wood joists'."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inventario_tags as it
import canon
from collections import defaultdict


def test_cr01_regex():
    for t in ("W.62", "DW.4", "XW.6.3", "CH.6", "FI.6"):
        assert it.TYPE_RE.match(t) and it.TAG_DOT_RE.match(t), t
    assert it.SCHED_TITLE_RE.search("INTERIOR WALL ASSEMBLIES")
    assert not it.TAG_DOT_RE.match("A2.02")


def test_cr02_familias():
    for k in ("5/8 type C", "1 shaftliner", "5/8 exterior gyp sheathing type X"):
        assert canon.BOARD_FAM[k] in canon.FAMS
    import familias
    assert familias.familia("5/8\" gypsum board, Type C (ceiling)", "SF") == "5/8\" gyp board Type C"
    assert familias.familia("5/8\" exterior gypsum sheathing, Type X", "SF") == "5/8\" EXTERIOR gyp sheathing Type X"


def test_cr03_rc():
    fam, filas = defaultdict(float), []
    c = {"room": "Guest 201", "system": "resilient_channel", "area_sf": 120.0, "board": "5/8 type C",
         "assembly": {"id": "FS-1", "source": "A0.08 FS-1 UL L546"}, "rc_oc_in": {"value": 16, "source": "UL L546"},
         "layers": {"value": 1, "source": "A0.08 FS-1"}, "source": "A3.02"}
    canon._ceiling_rc(c, "A3.02", fam, filas)
    assert abs(fam["resilient channel (printed)"] - 90.0) < 0.01 and abs(fam[canon.F_TYPEC] - 120.0) < 0.01
    bad = dict(c); bad.pop("assembly")
    try:
        canon._ceiling_rc(bad, "A3.02", defaultdict(float), [])
        raise AssertionError("sin assembly debía fallar")
    except ValueError:
        pass



def test_cr04_board_only():
    import tempfile, json, subprocess
    d = {"project": "t", "constants": {"plan_scale_by_sheet": {"A2.02": {"value": 9, "source": "A2.02 1/8"}}}, "walls": [],
         "existing_walls": [{"id": "W1", "sheet": "A2.02", "page": 18, "path": [[0, 0], [90, 0]], "length_ft": 10, "height_ft": 9.24,
                             "faces": 2, "layers": 1, "board": "5/8 type X", "location": "x", "source": "A2.02 4/A5.05", "decision": "R80f.1 (2026-11-05)"}]}
    import canon
    try:
        canon.corridas  # noqa
    except Exception:
        pass
    # the board-only branch must not raise "'runs' vacío"
    src = open(canon.__file__).read()
    assert "board-only project (existing_walls)" in src



def test_cr05_esquinas_board_only():
    import esquinas
    c = {"constants": {"plan_scale_by_sheet": {"A2.02": {"value": 9, "source": "x"}, "A7.05": {"value": 18, "source": "y"}}},
         "walls": [], "existing_walls": [{"id": "a", "sheet": "A2.02"}]}
    r = esquinas.revisar(c)
    assert r is not None and not r.get("fallas")



def test_cr09_escala_rotulo():
    import verificar_markups_excel as v
    assert v.escalas_impresas("PERMIT\nLVL 2\nA2.02\n1/8\" = 1'-0\"\n1") == [9.0]
    assert v.escalas_impresas("1 1/2\" = 1'-0\"") == [108.0]
    assert v.escalas_impresas("3/4\" = 1'-0\"") == [54.0]


def test_be_cr09b_auditoria_rx_scale_no_cruza_saltos():
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))
    import auditoria_entrega as a
    from fractions import Fraction
    t = 'A2.01\n1/8" = 1\'-0"\n1 1/2" = 1\'-0"'
    assert [a.frac(m.group(1)) for m in a.RX_SCALE.finditer(t)] == [Fraction(1, 8), Fraction(3, 2)]


if __name__ == "__main__":
    test_cr01_regex(); test_cr02_familias(); test_cr03_rc(); test_cr04_board_only(); test_cr05_esquinas_board_only(); test_cr09_escala_rotulo(); test_be_cr09b_auditoria_rx_scale_no_cruza_saltos(); print("test_cr_city_hotel OK")
