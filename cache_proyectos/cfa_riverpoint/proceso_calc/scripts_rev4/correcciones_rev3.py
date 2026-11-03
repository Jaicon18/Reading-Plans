"""rev3 (back-check of rev2) project fixes on the canon, after correcciones_rev2.py. Input changes only; quantities by
canon.py / accesorios.py / plantilla_excel.py (skill v81cf8). Log -> etapas/4_canon/rev3_log.json.
Use: python3 bitacora.py run scripts/correcciones_rev3.py"""
import json, os, re
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(K, "etapas", "4_canon", "takeoff_canon.json")
c = json.load(open(P))
LOG = []
log = lambda *a: LOG.append(dict(zip(("item", "rev2", "rev3", "delta", "src", "rule"), a)))
E = {e["id"]: e for e in c["existing_walls"]}
M = {m["ref"]: m for m in c["misc_items"]}
# T2: ceiling board in its own family (board key 5/8 ceiling sag-resistant)
for r in ("CLG-ENTA-B", "CLG-ENTB-B", "CLG-MEN-B", "CLG-WOM-B", "CLG-PLAY-B"):
    M[r]["familia"] = "5/8\" gyp ceiling board SAG-RESISTANT"
    M[r].pop("product", None)
log("Ceiling board row (332.06 SF)", "label '5/8\" gypsum board, regular' + product note", "row '5/8\" gypsum ceiling board, SAG-RESISTANT (ceiling type)'",
    "0 SF (label / family)", "C09250 2.1.E + 3.2.A.3 / A-909", "T2 (tool: board key 5/8 ceiling sag-resistant)")
# T1: Z size from the printed size
c["constants"]["z_furring_size"] = {"value": "2\"", "source": "A-202 WALL TYPE SCHEDULE M2.1 '2\" MTL. Z CHANNEL 2'-0\" O.C.' + A1/A-605"}
log("Z-furring row label (96 LF)", "'1-1/2\" Z-furring channel' + product note", "'2\" Z-furring channel (LF of material)'", "0 LF (label)", "A-202 M2.1, A1/A-605", "T1 (tool: printed Z size)")
# drop the notes that only explained template labels (now real labels / rows)
c["constants"]["ms_notes"] = [x for x in c["constants"]["ms_notes"]
                              if not re.search(r"PRODUCT: 2\\\"|PRODUCT: 5/8|Setting-type joint compound for the cement", x["note"])
                              and not x.get("cb_setting")]
# P1: J trim A2/A-624 on the dining face of the play-area enclosure (EX-DIN-03)
t = [x for x in c["trim_items"] if x["ref"] == "J-PLAY"][0]
l0 = t["lf"]
t["lf"] = E["EX-DIN-03"]["length_ft"]
t["source"] = (f"A2/A-624 WALL BASE AT PLAY AREA '\"J\" TRIM' on top of the 1/2\" cement board base on the DINING face of the play-area "
               f"enclosure (A1/A-624: dining side tile base / cement board; play side gyp + FRP + vinyl base) = board-only entry EX-DIN-03 "
               f"{E['EX-DIN-03']['length_ft']} LF (A-202 vector)")
log("J trim at play area wall base (A2/A-624)", f"{l0} LF (play-room perimeter)", f"{t['lf']} LF (dining face, EX-DIN-03)", f"{round(t['lf'] - l0, 2)} LF",
    "A2/A-624, A1/A-624, A-202", "P1")
# P2: MR rows cite C09250 2.2.A (not 2.1.B standard board)
n = 0
for eid in ("EX-RRM-01-GB", "EX-RRW-01-GB"):
    e = E[eid]
    for k in ("source", "height_source"):
        if isinstance(e.get(k), str) and "2.1.B" in e[k]:
            e[k] = re.sub(r"C09250[^;|]*?2\.1\.B[^;|)]*\)?", "C09250 Gypsum Board §2.2.A (water-resistant gypsum backing board) / A-909", e[k]).replace("/ A-909 / A-909", "/ A-909"); n += 1
log("MR rows spec citation (EX-RRM-01-GB, EX-RRW-01-GB)", "C09250 §2.1.B (1/2 in standard interior)", "C09250 §2.2.A water-resistant backing board", "text", "C09250 / A-909", "P2")
# P2: spec section on every Material Summary row
c["constants"]["ms_notes"] += [
    {"match": r"^Bracing", "note": "Spec: C09111 Non-load-bearing steel framing 3.2.C bracing of ceiling systems (A-909)", "source": "C09111 / A-909"},
    {"match": r"^Clip angles", "note": "Spec: C09111 2.3 framing accessories (A-909)", "source": "C09111 / A-909"},
    {"match": r"^METAL trim", "note": "Spec: C09250 2.3 trim accessories, cornerbead / LC-bead (A-909)", "source": "C09250 / A-909"},
    {"match": r"^Metal stud blocking", "note": "Spec: C09111 2.3 / A-909", "source": "C09111 / A-909"},
    {"match": r"^Sill track|^Deep-leg slotted|^Track 6|^Ceiling / soffit track", "note": "Spec: C09111 2.3 / A-909", "source": "C09111 / A-909"},
    {"match": r"^Level 5", "note": "Spec: C09250 3.5.D finish levels (A-909)", "source": "C09250 / A-909"},
    {"match": r"^Setting-type joint compound|^Alkali-resistant", "note": "Spec: C09250 2.4.B.2 / 2.4.D.2 / 3.5.E (A-909)", "source": "C09250 / A-909"},
    {"match": r"ceiling board, SAG", "note": "Spec: C09250 2.1.E Ceiling Type (sag-resistant) + 3.2.A.3 ceiling surfaces (A-909)", "source": "C09250 / A-909"},
    {"match": r"^Joint compound|^Joint tape", "note": "Spec: C09250 2.4 joint treatment materials (A-909)", "source": "C09250 / A-909"},
    {"match": r"^Extra framing|^2-1/2\" CFMF|^Additional head track|^Deflection clips", "note": "Spec: C09111 2.3 framing accessories (A-909) - none required in this project", "source": "C09111 / A-909"},
    {"match": r"^PVC trim", "note": "Spec: C09250 2.3 trim accessories (A-909) - FRP by others", "source": "C09250 / A-909"},
    {"match": r"^Power-driven fasteners and duct", "note": "Spec: C09111 2.5 / C09250 2.5 auxiliary materials (A-909) - fasteners EXCLUDED", "source": "C09111 / A-909"},
    {"match": r"^Access panel", "note": "Spec: C08306 access doors and frames (A-907) - none in our gypsum ceilings / walls", "source": "C08306 / A-907"},
    {"match": r"^Demolition", "note": "Scope: A-050 / A-052 demolition keynotes (no spec section for demolition in A-90x)", "source": "A-050"},
]
log("Spec reference on Material Summary rows (bracing, clips, trim, blocking, tracks, Level 5, mesh / setting compound)", "missing on rows 17 / 22 / 27",
    "every row cites its spec section", "text", "C09111 / C09250 / A-909", "P2")
json.dump(c, open(P, "w"), indent=1, ensure_ascii=False)
json.dump(LOG, open(os.path.join(K, "etapas", "4_canon", "rev3_log.json"), "w"), indent=1, ensure_ascii=False)
print(len(LOG), "rev3 changes")
