"""Test BE-GK56 with the real case (Grand Kia rev3b): readerB_A-Z1-05 'same wall as A-Z1-06' parsed from the reader's text, no measurement
-> FAIL; with the reviewer's measured target A-Z1-08 'gap 0" (1/A111)' -> PASS; a measured gap > 0 (readerA_G-Z2-15, 6.9") -> FAIL
(FALTA); a target that is not a canon wall -> FAIL."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import be_gk56 as G
walls = [{"id": "A-Z1-06"}, {"id": "A-Z1-08"}, {"id": "G-Z2-19"}]
mal = {"walls": walls, "excluded_walls": [{"id": "readerB_A-Z1-05", "reason": "same wall as A-Z1-06: Merged: same straight grid-4 north leaf as A-Z1-06"}]}
assert G.fallas(mal), "target parsed from the reader's text without a measurement must FAIL"
bien = {"walls": walls, "excluded_walls": [{"id": "readerB_A-Z1-05", "reason": "same wall as A-Z1-08: Merged ...",
                                            "gap_proof": "gap 0\" (1/A111) - the reader piece lies on the drawn band of A-Z1-08"}]}
assert not G.fallas(bien), "measured target passes"
falta = {"walls": walls, "excluded_walls": [{"id": "readerA_G-Z2-15", "reason": "same wall as G-Z2-19: ...", "gap_proof": "gap 6.9\" (1/A111) - drain box"}]}
assert G.fallas(falta), "a measured gap > 0 is a FALTA"
assert G.fallas({"walls": walls, "excluded_walls": [{"id": "q", "reason": "same wall as X-Z9-99: ...", "gap_proof": "gap 0\" (1/A111)"}]}), "unknown target FAILs"
cargada = {"walls": walls, "misc_items": [{"ref": "RI-18C furring board", "qty": 18.2}], "excluded_walls": [{"id": "readerA_G-Z2-15",
           "reason": "same wall as G-Z2-19: ... its last 1.16 ft is a separate furring, loaded as RI-18C", "gap_proof": "gap 6.9\" (1/A111) - drain box"}]}
assert not G.fallas(cargada), "a measured gap > 0 whose FALTA is loaded (ref in canon) passes"
print("test_be_gk56 OK")
