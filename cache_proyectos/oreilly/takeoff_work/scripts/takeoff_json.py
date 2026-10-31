import json, subprocess, sys
P = "/home/user/scratchpad/run/takeoff_work/"
c = json.load(open(P + "etapas/2_lectura/takeoff_canon_AB.json"))
t = json.load(open(P + "takeoff.json"))
def fmt(o):
    A, B = o.get("A") or {}, o.get("B") or {}
    a = f"(A) Plans / specs ({A.get('source','')}): {A.get('texto','')} - delta {A.get('delta','')}"
    b = f"(B) Trade code ({B.get('cita','n/a')}): {B.get('texto','')} - delta {B.get('delta','')}"
    cc = o.get("C") or "____"
    return f"{a} | {b} | (C) Other: {cc}"
rf = []
for r in c["rfis"]:
    rf.append({"id": r["id"], "pregunta": f"{r['tema']} - where: {r.get('donde','')} - carried: {r.get('supuesto','')}",
               "delta": fmt(r.get("opciones") or {}), "opciones": r.get("opciones") or {}, "source": r.get("source", "")})
rf.append({"id": "RFI-15", "pregunta": "Gypsum board finish level not printed (no project manual in the set; A1.1 notes silent) - where: all gypsum board - carried: Level 4 (joint compound + tape quantified), no Level 5",
           "delta": "(A) Plans / specs (A1.1 interior wall & ceiling notes 3.A-3.C; A1.2 finish W-2 semi-gloss paint): nothing printed - delta 0 | (B) Trade code (GA-214 / ASTM C840: semi-gloss paint finish is recommended at Level 5): Level 5 skim coat on painted walls - delta + Level 5 SF = painted board SF | (C) Other: ____"})
for x in rf:
    if x["id"] == "RFI-15":
        x["opciones"] = {"A": {"texto": "nothing printed (A1.1 notes 3.A-3.C; A1.2 W-2 semi-gloss paint)", "source": "A1.1, A1.2", "delta": "0"},
                         "B": {"texto": "Level 5 recommended under semi-gloss paint", "cita": "GA-214 / ASTM C840", "delta": "+ Level 5 SF = painted board SF"}, "C": ""}
rf.sort(key=lambda x: int(x["id"].split("-")[1]))
t["rfis"] = rf
Q = lambda s: s
al = [
 ("ALC-01", "Interior partition framing (studs + tracks)", "CUANTIFICADO", "Types S24, S41, S42, S43, S61 (A1.1 wall types; 5/A4.2, 6/A4.2, 7/A4.2): 3-5/8\" and 6\" 20 ga studs and tracks in Material Summary; S21 / S24 Z-furring in its own row."),
 ("ALC-02", "Exterior wall framing (CFMF)", "CUANTIFICADO", "Entry piers + head wall over storefront A (8\" 800S162-54 + 6\" 600S162-54 @ 16\", 1/A3.1, 2/A3.1, 3/S5.3), south stucco panel 600S162-43 (1/A3.4), vestibule heads 600S162-54 (3/A3.1, S4.1 key note 3, RFI-05)."),
 ("ALC-03", "Parapet framing", "NO APLICA", "Parapets are CMU to T.O. masonry with PEMB coping (A2.1, A3.1-A3.2); the CFMF above storefront A up to T.O. metal stud 120'-8\" (2/A3.1) is counted in the exterior head wall (ALC-02)."),
 ("ALC-04", "Top / deflection and bottom track", "CUANTIFICADO", "Bottom and top / deflection track by stud size (A1.1 note 2.C deflection channels at walls to roof structure; 3/S5.1, 4/S5.1); heads row for the vestibule heads."),
 ("ALC-05", "Headers, sills and jambs at openings", "CUANTIFICADO", "Header / box beam and additional head track by headers.py from the door / window schedules (A5.1, A5.2); CMU openings by mason (RFI-13)."),
 ("ALC-06", "Bracing / bridging", "CUANTIFICADO", "Horizontal stud bridging @ 4'-0\" O.C. vertical (A1.1 note 2.F) as C.R. channel rows; S42 header kickers / struts (1/S5.1, 2/S5.1, 5/S5.1, RFI-09); diagonal flat strap (note 2.B) in RFI-12."),
 ("ALC-07", "Gypsum board on walls (layers per type)", "CUANTIFICADO", "5/8\" Type X on every type (A1.1 wall types S21-S61); faces to the hard-lid ceiling or to the purlin (RFI-01, RFI-02)."),
 ("ALC-08", "Moisture / abuse / special board at wet areas", "CUANTIFICADO", "5/8\" Type X moisture resistant at restrooms 103 / 104 walls and ceilings (A1.1 note 3.B, A1.2, 1A/A4.1)."),
 ("ALC-09", "Exterior gypsum / glass mat sheathing", "CUANTIFICADO", "5/8\" glass mat sheathing at the entry piers (1/A3.1 key 19) and the south stucco panel (1/A3.4); head wall over storefront A takes FRT plywood (2/A3.1 key 34)."),
 ("ALC-10", "FRT plywood sheathing / substrate", "CUANTIFICADO", "5/8\" exterior FRT plywood sheathing on the head wall face and storefront head soffit (2/A3.1, 3/A3.1 key 34) + 5/8\" FRT plywood backing 8'-0\" to 10'-0\" at the S41 box-outs (key note 5, 4/A4.2)."),
 ("ALC-11", "Gypsum board ceilings", "CUANTIFICADO", "C-3 gypsum hard-lid ceilings: office 102 + vestibule 100A (Type X) and restrooms 103 / 104 (Type X W.R.) (A1.2, 7/A4.2, 3/A3.1); top-side board in RFI-05."),
 ("ALC-12", "Ceiling suspension (furring / carrying channel / hangers)", "NO APLICA", "No suspended gypsum ceiling: hard lids are framed with 6\" joists @ 24\" (7/A4.2, 3/A3.1, counted in the 6\" stud row); C-1 ACT in Parts A is by the ACT trade (A1.2, 9/A4.2)."),
 ("ALC-13", "Soffits and bulkheads (framing + board)", "NO APLICA", "NO APLICA: no soffit or bulkhead drawn on A1.1, A1.2 or A3.1-A4.2; the S42 suspended header walls (6/A4.2) are rows of type S42 (ALC-01) and the vestibule 100A hard lid with its joists (3/A3.1) is in ALC-11 / 6\" stud row."),
 ("ALC-14", "Canopy / marquee framing and sheathing", "NO APLICA", "No canopy or marquee framing on A2.1 / A3.x: the stucco cornice (A2.1 key 5) is plaster on the CMU parapet; sign backing in RFI-10."),
 ("ALC-15", "Column furring / wraps", "NO APLICA", "PEMB columns: key note 1 concealed in the walls with 24 ga sheet metal cover by others (1/A4.2 key 16), key note 2 exposed painted (A1.1): no gypsum column wraps."),
 ("ALC-16", "Blocking (FRT wood / metal) for millwork", "CUANTIFICADO", "FRT 2x nailers at the S42 header walls (6/A4.2 keys 10-11) and at T.O. metal stud (8/A3.2, 2/A3.1 key 11), toilet accessories (A4.1 note 1), water heater, fire extinguishers (10/A4.2); quantities in RFI-10."),
 ("ALC-17", "Framed openings (MEP, access panels, diffusers)", "RFI", "MEP and electrical sheets excluded by the estimator (2026-10-31): no framed openings or penetrations counted - RFI-08."),
 ("ALC-18", "Trim: corner bead, casing bead, control joints, reveals", "CUANTIFICADO", "Corner bead at the hard-lid tops (7/A4.2), DRMF reveals at the S42 control joints (2/A4.2, 14/A4.1); J-mold / header corner bead in RFI-11."),
 ("ALC-19", "Acoustical sealant / sound attenuation (EXCLUDED: estimator standing order)", "NO APLICA", "EXCLUDED in all projects (estimator standing order); sound batt (S43, S61) is insulation, EXCLUDED."),
 ("ALC-20", "FRP / cement board / tile backer", "RFI", "No FRP or cement board called; restrooms W-4 sanitary wall and ceiling panel system (A1.2) is a finish item - RFI-07."),
 ("ALC-21", "Shaft walls / area separation walls", "NO APLICA", "No shaft walls or area separation walls in the set (A1.1 wall types S21-S61 only)."),
 ("ALC-22", "Rated assemblies (UL designs) and their board type", "NO APLICA", "No UL design called on A1.1 wall types; Type X board is specified by type (A1.1)."),
 ("ALC-23", "Special panels (ballistic, lead-lined, abuse)", "NO APLICA", "No ballistic, lead-lined or abuse panels on A1.1 / A1.2."),
 ("ALC-24", "Finish level (Level 4 / Level 5)", "RFI", "Finish level not printed (no project manual in the set): Level 4 carried (compound + tape), Level 5 in RFI-15."),
]
t["alcances"] = [{"id": i, "nombre": n, "estado": e, "nota": x} for i, n, e, x in al]
t["revisar"] = []
json.dump(t, open(P + "takeoff.json", "w"), indent=1, ensure_ascii=False)
# registro marks (registro.py, never by hand)
S = "/tmp/skill80t/take-off-metal-frame-drywall/tools/"
env = dict(__import__("os").environ, BITACORA=P + "bitacora.jsonl")
for i, n, e, x in ([] if "--sin-registro" in sys.argv else al):
    if e == "RFI":
        rfi = [w for w in x.replace("(", " ").replace(")", " ").replace(".", " ").split() if w.startswith("RFI-")][0]
        args = ["marcar", P + "registro.json", i, "pendiente_rfi", f"{rfi} {x}"]
    else:
        args = ["marcar", P + "registro.json", i, "verificado", f"{e}: {x}"]
    p = subprocess.run([sys.executable, S + "bitacora.py", "run", S + "registro.py", *args], cwd=P, env=env, capture_output=True, text=True)
    print(i, p.returncode, (p.stdout + p.stderr).strip().splitlines()[-1][:100])
