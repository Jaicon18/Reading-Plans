"""v140 (audit 13-nov I-1 / I-4, Xfinity rev1d, independent review R_A3): tests that REPRODUCE the two blind detectors of v81cf138.
They FAIL with v81cf138 (expected) and must PASS once the v140 fix is in. Run: python3 -I test_v140_detectores_xf.py <skill>/tools"""
import os
import sys

sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "tools"))
import chequeos_biblioteca as CB  # noqa: E402

# CB_RCP_TAGS: descriptive tags ("2x4 ACT 12'-0\" AFF", "GYP. BD. 8'-6\" AFF") on an RCP sheet must be counted (not N/A)
t = "A3.0 REFLECTED CEILING PLAN\n2x4 ACT\n12'-0\" AFF\nGYP. BD.\n8'-6\" AFF\nEXISTING\nGYP. BD.\n9'-0\" AFF"
r = CB.rcp_tags(CB.B(canon={"misc_items": []}, hojas={"A3.0": t}))
assert r[0] == "FAIL", ("CB_RCP_TAGS ciego a tags descriptivos", r)
# CB_RCP_TAGS: the RCP title split by a newline ("REFLECTED\nCEILING PLAN") must still be an RCP sheet
t2 = "A3.0 REFLECTED\nCEILING PLAN\nGYP-1"
r = CB.rcp_tags(CB.B(canon={"misc_items": []}, hojas={"A3.0": t2}))
assert r[0] == "FAIL", ("RX_HOJA_RCP con espacio literal", r)
# CB_BE_CF10: an outline spec sheet 'SPECIFICATIONS' without CSI numbers (A0.3) is a spec of the trade (not 'el set no trae specs')
a03 = ("SPECIFICATIONS\nMETALS:\nLIGHTGAGE FRAMING: METAL STUDS SHALL BE USED IN WALLS AS SHOWN ON DRAWINGS\nFINISHES: GYPSUM DRYWALL:\n"
       "GYPSUM BOARD: ASTM A36, TYPE X 5/8 FIRECODE\nJOINT COMPOUND: ASTM C 475 OF THE TYPE INDICATED.")
ms = [{"fila": 13, "material": '5/8" gypsum board, Type X', "unit": "SF", "net": 3072.97, "fuente": "N/SHEET: 2/A2.0, A0.3"}]
r = CB.be_cf10(CB.B(hojas={"A0.3": a03}, ms=ms))
assert not str(r[1][0] if r[1] else "").startswith("N/A"), ("CB_BE_CF10 no reconoce A0.3 SPECIFICATIONS", r)
print("test_v140_detectores_xf OK")
