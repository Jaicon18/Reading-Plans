"""Decision 9 (C09250 2.4.B.2 / 2.4.D.2 / 3.5.E, A-909): cement board joints = alkali-resistant mesh tape + setting-type
compound. Driver = the cement board NET computed by canon.py (familias_out.json 'cement board'); yields = the Inputs
yields of joint tape (0.37 LF/SF) and joint compound (0.072 lb/SF). Writes misc_items MESH-CB (family
'alkali-resistant mesh tape (printed)') and the setting-compound quantity as a Material Summary note (no LB family for
it in the fixed template). Use: python3 bitacora.py run scripts/malla_cb.py"""
import json, os
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C4 = os.path.join(K, "etapas", "4_canon")
P = os.path.join(C4, "takeoff_canon.json")
c = json.load(open(P))
fo = json.load(open(os.path.join(C4, "out", "familias_out.json")))
cb = round(float(fo["familias"]["cement board"]), 2)
q = round(cb * 0.37, 2)
lb = round(cb * 0.072, 2)
c["misc_items"] = [m for m in c["misc_items"] if m["ref"] != "MESH-CB"]
c["misc_items"].append({"ref": "MESH-CB", "familia": "alkali-resistant mesh tape (printed)", "qty": q, "unit": "LF",
    "source": "C09250 2.4.B.2 (tape for tile backing panels as recommended by the manufacturer) + 2.4.D.2 + 3.5.E / A-909; DUROCK cement board (2.2.B) joints",
    "op": f"Inputs joint tape yield 0.37 LF/SF x {cb} SF of 1/2\" cement board (Material Summary cement board row) = {q} LF"})
n = [x for x in c["constants"].get("ms_notes", []) if not x.get("cb_setting")]
n.append({"match": r"mesh tape", "note": f"Setting-type joint compound for the cement board joints: Inputs yield 0.072 lb/SF x {cb} SF = {lb} lb (C09250 2.4.D.2 / 3.5.E; no LB row for it in the fixed template)",
          "source": "C09250 2.4.D.2 / A-909", "cb_setting": True})
c["constants"]["ms_notes"] = n
json.dump(c, open(P, "w"), indent=1, ensure_ascii=False)
print("mesh tape", q, "LF; setting compound", lb, "lb; cement board", cb)
