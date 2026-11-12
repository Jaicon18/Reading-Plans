"""Test BE-GK55 with the real case R17-F1 (Grand Kia rev3b): A-Z1-13 unchanged, new F-Z1-21 across the kn 51 infill -> false T = FAIL;
with corner_skip or with both ids explained in CAMBIOS -> PASS; a new node between two NEW walls is not checked."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import be_gk55 as G
a13 = {"id": "A-Z1-13", "band": {"ori": "H", "c0": 1327.4, "c1": 1331.2, "lo": 1275.0, "hi": 1388.2, "sheet": "A111"}}
f21 = {"id": "F-Z1-21", "band": {"ori": "V", "c0": 1395.4, "c1": 1396.4, "lo": 1326.6, "hi": 1362.6, "sheet": "A111"}}
prev = {"walls": [a13], "nodes": [{"kind": "free", "wall": "A-Z1-13"}]}
new = {"walls": [a13, f21], "nodes": [{"kind": "T", "branch": "A-Z1-13", "through": "F-Z1-21"}]}
assert G.fallas(prev, new, "F-Z1-21 + F-Z1-22 (nuevos): keynote 52 patch"), "false T on an unchanged wall must FAIL"
new_skip = {"walls": [a13, dict(f21, corner_skip_info={"A-Z1-13": "kn 51 infill between (A111)"})], "nodes": new["nodes"]}
assert not G.fallas(prev, new_skip, ""), "declared non-meeting pair passes"
assert not G.fallas(prev, new, "A-Z1-13 / F-Z1-21: corner checked on A111"), "explained in CAMBIOS passes"
f22 = {"id": "F-Z1-22", "band": {"ori": "V", "c0": 1395.4, "c1": 1396.4, "lo": 1370.9, "hi": 1374.6, "sheet": "A111"}}
assert not G.fallas(prev, {"walls": [a13, f21, f22], "nodes": [{"kind": "split", "walls": ["F-Z1-21", "F-Z1-22"]}]}, ""), "new-new node not checked"
print("test_be_gk55 OK")
