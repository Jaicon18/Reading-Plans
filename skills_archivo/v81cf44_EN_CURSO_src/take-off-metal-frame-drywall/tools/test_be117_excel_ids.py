#!/usr/bin/env python3
"""test_be117_excel_ids.py — BE-117 d/e/f (coordinator 3-nov, CFA River Point rev4): every markup finds its ID and its
sheets in the Excel row. (d) a Material Summary row cites the bare sheets of its items' sources not covered by an
N/SHEET (gyp ceiling row lacked A-221); (e) Level 5 op = "<ref> <SF> SF = L x (h - base)" (before the ref read as the
LF); (f) the 1/2" regular board row breaks down per face / ceilings[].id like the other boards (before: op text only).
Synthetic; fails with v81cf10 trazabilidad / accesorios."""
import json, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import accesorios as A
import trazabilidad as T
# (e)
o = A.Out()
A.level5({"level5_items": [{"ref": "L5-X", "wc_tag": "WC-1", "l_ft": 10.0, "h_ft": 10.0, "source": "A-211 note",
                            "base_ft": {"value": 0.5, "source": "A-211 base"}}],
          "constants": {"level5_tags": {"value": ["WC-1"], "source": "A-211"}}}, o)
op = [r for r in o.filas if r["familia"] == A.F_L5][0]["operacion"]
assert op.startswith("L5-X 95.0 SF = 10.0 x (10.0 - base 0.5)"), op
# (d) + (f)
d = tempfile.mkdtemp()
FS = "5/8\" gyp ceiling board SAG-RESISTANT"
json.dump({"familias": {"1/2\" gyp board": 100.0, FS: 40.0}, "partition_types": {"types": {}}, "accesorios": {},
           "filas": [{"familia": FS, "ref": "CLG-1-B", "valor": 40.0, "source": "A-221 gyp ceiling hatch; framing per C3/S-241", "operacion": "x"}]},
          open(os.path.join(d, "familias_out.json"), "w"))
json.dump({"caras": [{"wall": "W1", "room": "R", "board": "1/2 regular", "sf": 60.0}]}, open(os.path.join(d, "board_out.json"), "w"))
for n, v in (("studs_out.json", {"walls": []}), ("corridas_out.json", {"renglones": []})):
    json.dump(v, open(os.path.join(d, n), "w"))
cp = os.path.join(d, "canon.json")
json.dump({"walls": [], "ceilings": [{"id": "SOF-1", "room": "Soffit R", "board": "1/2 regular", "area_sf": 40.0,
                                      "detail": "C4/A-624", "system": "framed_soffit"}],
           "misc_items": [{"ref": "CLG-1-B", "familia": FS, "qty": 40.0, "unit": "SF",
                           "source": "A-221 gyp ceiling hatch; framing per C3/S-241", "op": "x"}]}, open(cp, "w"))
out = T.aplicar({"materials": [{"material": "1/2\" gypsum board regular", "unit": "SF", "net": 100.0, "familia": "1/2\" gyp board", "source": "x"},
                               {"material": "5/8\" gypsum ceiling board, SAG-RESISTANT", "unit": "SF", "net": 40.0, "familia": FS, "source": "x"}],
                 "walls": []}, d, cp)
c0, c1 = out["materials"][0]["cita"], out["materials"][1]["cita"]
assert "SOF-1 40" in c0 and "W1 60" in c0 and "C4/A-624" in c0, c0
assert "C3/S-241" in c1 and "A-221" in c1.split("|")[0], c1
print("test_be117_excel_ids OK")
