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


if __name__ == "__main__":
    test_cr01_regex(); test_cr02_familias(); test_cr03_rc(); print("test_cr_city_hotel OK")
