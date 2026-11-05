"""rev2 (back-check rev1 of HFT Loveland, BACKCHECK_rev1.md): printed data the back-check found uncarried or mis-ruled,
written into the canon as DATA with its N/SHEET (no quantity typed here: canon.py computes every number; the RFI-05
deltas are computed by canon.braces_to_structure itself with the alternative of each option).
 F1  braces_to_structure: A1.1 wall legend note 1 "ALL WALLS BRACED TO STRUCTURE ABOVE @ 4'-0\" O.C. MAX" + 2/A4.1 lateral
     bracing (metal stud brace, Trade Ready Spazzer 9200 spacing bar); brace length not printed -> conservative LOADED =
     printed B.O. structure of the bay (A1.2 chart, Sales high point +-16'-9\") minus the top of the lowest board; RFI-05.
 F3  vestibule bulkhead carried as typed rows (partition_row) -> its slip top track (3/A5.3) goes to the slip family.
 F4  constants.bracing_min_height_ft = A4.1 wall type note 7 ("partitions higher than 12'-0\"").
 F6  constants.partition_row_rule = one Partition Takeoff row per wall id (= the markups).
 O1  header misc sources: the T162-54 track clip is a member of 9/A5.3, not a sheet; no D1.0 citation on headers.
Use: python3 bitacora.py run scripts/rev2_canon.py <tools_dir>"""
import json, os, sys
sys.path.insert(0, sys.argv[1])
import canon as CN
K = os.environ.get("K") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(K, "etapas", "4_canon", "takeoff_canon.json")
c = json.load(open(P))
cs = c.setdefault("constants", {})
cs["bracing_min_height_ft"] = {"value": 12, "source": "A4.1 wall type note 7 'AT PARTITIONS HIGHER THAN 12'-0\" ... 1-1/2\" 16 GA C.R. CHANNELS AT 8'-0\" O.C. VERT.'"}
cs["type_order"] = {"value": [p["type"] for p in c.get("partition_schedule") or []] + ["BULKHEAD-VH", "RE"],
                    "source": "A4.1 wall type schedule order A-E, then the vestibule bulkhead (1/A5.3) and the receiving enclosure (S2.1)"}
cs["partition_row_rule"] = {"value": "wall_id", "source": "A1.1 / A4.0 wall ids: one Partition Takeoff row per wall, the same ids as the markups"}
c["braces_to_structure"] = {
    "spacing_in": {"value": 48, "source": "A1.1 wall legend note 1 'ALL WALLS BRACED TO STRUCTURE ABOVE @ 4'-0\" O.C. MAX.' (2/A4.1 prints 5'-0\" O.C. max: the stricter A1.1 spacing loaded)"},
    "structure_ft": {"value": 16.75, "source": "A1.2 clearance heights chart: SALES B.O. structure +-16'-9\" (high point of the bays of these walls, conservative; Sales Replenishment +-15'-9 1/2\")"},
    "brace": {"product": "6\" x 20 GA metal stud brace (stud of type A, A/A4.1)", "source": "2/A4.1 LATERAL BRACING @ FREE-STANDING WALLS"},
    "bar": {"product": "Trade Ready Spazzer 9200 spacing bar", "source": "2/A4.1"},
    "length_rule_info": "brace length not printed: loaded = B.O. structure - top of the lowest board of the wall (full vertical distance, conservative); RFI-05",
    "rfi": "RFI-05"}
pn = cs.setdefault("product_names", {})
pn[CN.F_BRACE_ST] = {"value": "Metal stud brace to structure, 6\" x 20 GA stud @ 4'-0\" O.C. (LF of material)", "source": "A1.1 note 1, 2/A4.1, A/A4.1"}
pn[CN.F_BAR_ST] = {"value": "Trade Ready Spazzer 9200 spacing bar at the brace line (LF)", "source": "2/A4.1"}
for w in c["walls"]:
    if w.get("element") == "vestibule_head":
        w["partition_row"] = "vestibule bulkhead carried as its own typed row (1/A5.3), inside the grand total"
M = {m["ref"]: m for m in c.get("misc_items") or []}
if "BXH-02-CLIP" in M:
    M["BXH-02-CLIP"]["source"] = "9/A5.3 box header attachment: track clips jamb to jamb (member printed in 9/A5.3)"
if "BXH-02" in M:
    M["BXH-02"]["source"] = "8/A5.3 + 9/A5.3 BOX HEADER (A3.1 keynote 612) 'BRAKE METAL SECTION OVER 6\" 16 GA. METAL BOX-HEADER' at the new +-12'-0 1/2\" opening"
# F2: estimator-facing texts (no internal process words in the cells / markups)
import re
for w in c["walls"]:
    if "hat channel" in str(w.get("stud_size") or "").lower():
        w["stud_size"] = '1-1/2" metal hat channel'
        for k in ("stud_source", "gauge_source"):
            if w.get(k):
                w[k] = re.sub(r"\s*\(schema has no hat-channel family[^)]*\)", "", w[k])
for m in c.get("misc_items") or []:
    if m.get("familia") == "FRP":
        m["op"] = str(m["op"]).replace("; scope decided by calculator", "; FRP carried per A1.3 finish schedule (G.C. scope)").replace("scope decided by calculator", "FRP carried per A1.3 finish schedule (G.C. scope)")
if c.get("frp_none_reason"):
    c["frp_none_reason"] = ("FRP WC-1 (A1.3 finish schedule 'FIBER REINFORCED PLASTIC (FRP) TO CEILING', RR 107 / 108 + 1/A4.1 mop alcove) "
                            "carried in its own FRP panels row (G.C. scope per A1.3); PVC trim is part of the FRP install (A1.3 WC-1 remarks)")
for x in c.get("accesorios_none") or []:
    if x.get("familia") == "PVC trim at FRP":
        x["why"] = "PVC trim molding is part of the FRP install (A1.3 WC-1 remarks 'PROVIDE PVC TRIM MOLDING'), carried with the FRP panels row"
# RFI-05 with the deltas computed by the tool function (loaded vs each alternative)
base = CN.braces_to_structure(c)
alt_a = CN.braces_to_structure(c, length_factor=0.7071)
alt_b = CN.braces_to_structure(c, spacing_in=60)
lf0 = round(sum(x["brace_lf"] for x in base), 2)
pc0 = sum(x["pcs"] for x in base)
da = round(sum(x["brace_lf"] for x in alt_a) - lf0, 2)
db_lf = round(sum(x["brace_lf"] for x in alt_b) - lf0, 2)
db_pc = sum(x["pcs"] for x in alt_b) - pc0
sm = json.load(open(os.path.join(K, "etapas", "SHEET_MAP.json")))
c["rfis"] = [r for r in c.get("rfis") or [] if r.get("id") != "RFI-05"]
c["rfis"].append({
    "id": "RFI-05",
    "question": ("Walls braced to structure (A1.1 wall legend note 1 'ALL WALLS BRACED TO STRUCTURE ABOVE @ 4'-0\" O.C. MAX', "
                 "2/A4.1 lateral bracing at free-standing walls: metal stud brace + Trade Ready Spazzer 9200 spacing bar at the "
                 "mid-point between the end of the board and the structure): the brace length and member are not printed. "
                 f"Loaded {pc0} braces of 6\" x 20 GA stud @ 4'-0\" O.C. on the walls with unsheathed studs above the board, each "
                 "as long as the full height from the top of the board to the printed B.O. structure +-16'-9\" (A1.2)."),
    "loaded": f"LOADED {pc0} braces, {lf0} LF of 6\" x 20 GA stud + Spazzer bar along each braced wall",
    "fuentes_revisadas": [sm[k] for k in sorted(sm, key=int)],
    "options": {
        "A": {"texto": "Drawings: brace at about 45 deg from the mid-point between the top of the board and the structure (2/A4.1 geometry)",
              "source": "2/A4.1", "delta": f"{da} LF of brace stud (same {pc0} braces)"},
        "B": {"texto": "Code / detail spacing: 5'-0\" O.C. max of 2/A4.1 instead of the 4'-0\" of A1.1 note 1",
              "cita": "2/A4.1 note (5'-0\" O.C. max); ASTM C754 bracing of studs to structure", "delta": f"{db_pc} braces, {db_lf} LF of brace stud"},
        "C": ""},
    "source": "A1.1 / 2/A4.1"})
json.dump(c, open(P, "w"), indent=1, ensure_ascii=False)
print(f"rev2 data written: {len(base)} braced walls, {pc0} braces, {lf0} LF loaded; RFI-05 delta A {da} LF, B {db_pc} pcs / {db_lf} LF")
