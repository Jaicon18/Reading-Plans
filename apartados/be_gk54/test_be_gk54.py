"""Test BE-GK54 with the real case M-A111-29 (Grand Kia rev3a): A-Z1-20 excluded as 'same single wall as A1-Z1-08' while A111 draws a
second leaf (1503.8-1507.6) 2 in. from A1-Z1-08 (1509.0-1512.8) -> FAIL; with the leaf carried (no RED) or a gap_proof -> PASS."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import be_gk54 as G

canon = {"walls": [{"id": "A1-Z1-08", "band": {"ori": "V", "c0": 1509.0, "c1": 1512.8, "lo": 1124.0, "hi": 1163.8, "sheet": "A111"}}],
         "excluded_walls": [{"id": "A-Z1-20", "reason": "same single wall as A1-Z1-08 behind the drinking fountain / WOMEN 120 vanity"}]}
red = [{"hoja": "A111", "tipo": "muro", "id": "M-A111-29", "x": "1014.3", "y": "1505.7", "largo_ft": "3.48", "estado": "ROJO"},
       {"hoja": "A111", "tipo": "muro", "id": "M-A111-29b", "x": "1145.0", "y": "1505.7", "largo_ft": "4.0", "estado": "ROJO"}]
# the coverage CSV of rev3a gives the red in rotated plan coordinates of the band's 'along' / 'cross' axes: along = y, cross = x for ori V
red_v = [{"hoja": "A111", "tipo": "muro", "id": "M-A111-29", "x": "1505.7", "y": "1145.0", "largo_ft": "4.0", "estado": "ROJO"}]
# the real rev3a row is in rendered (rotated 270) page points: (1014.3, 1505.7) -> unrotated (1505.7, 2160 - 1014.3 = 1145.7)
real = [{"hoja": "A111", "tipo": "muro", "id": "M-A111-29", "x": "1014.3", "y": "1505.7", "largo_ft": "3.48", "estado": "ROJO"}]
rot270 = lambda h, x, y: (y, 2160.0 - x)
assert G.fallas(canon, real, to_canon=rot270), "the real rev3a red (rotated coordinates) must FAIL"
assert G.fallas(canon, red_v), "the hidden second leaf must FAIL"
assert not G.fallas(canon, [dict(red_v[0], estado="CUBIERTO")]), "once the leaf is carried, PASS"
canon2 = {**canon, "excluded_walls": [dict(canon["excluded_walls"][0], gap_proof="1/A150 shows one wall, no gap")]}
assert not G.fallas(canon2, red_v), "an exclusion with printed gap proof passes"
assert not G.fallas({**canon, "excluded_walls": [{"id": "Q", "reason": "existing CMU"}]}, red_v), "other exclusions are not checked"
print("test_be_gk54 OK")
