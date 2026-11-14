#!/usr/bin/env python3
"""armar_takeoff_json.py (CR desde cero): takeoff.json para plantilla_excel desde el canon (RFIs, review items, alcances).
Las cantidades NO se escriben aquí: salen de familias_out.json (--familias)."""
import json, sys
et = sys.argv[1]; out = sys.argv[2]
c = json.load(open(f"{et}/4_canon/takeoff_canon.json"))
CERRADOS = {  # decisiones con fuente impresa (U-162: planos primero; R-ALC-10: el plano manda sobre la spec)
 "RFI-03": "CLOSED - estimator decision (option A, drawings govern, R-ALC-10): A0.06 GN 10 '5/8\" GYPSUM BOARD AT ALL OTHER LOCATIONS' -> GYP-1 = 5/8\" regular. Spec 09 29 00 2.3.B lists 1/2\" ceiling board; delta = same SF, lighter board.",
 "RFI-06": "CLOSED - drawings govern (U-162): 7/A7.23 and 5/A7.31 draw WOOD blocking -> board only, framing Div. 06 excluded. Delta if metal: + soffit framing LF.",
 "RFI-09": "CLOSED - drawings govern (U-162): A0.06 FURRED INSULATION FI.2 detail = 5/8\" type X over min. R-11.4 rigid insulation adhesive-applied to masonry, no furring member drawn -> board only.",
 "RFI-13": "CLOSED - drawings + code (U-162): GYP-1 legend 'GYPSUM BOARD ON METAL SUSPENSION SYSTEM' + spec 09 22 16 2.2.F grid suspension -> USG drywall suspension system, mains 48\" o.c., cross tees 16\" o.c. (manufacturer standard), loaded.",
}
rfis, revisar = [], []
for r in c.get("rfis", []) + c.get("rfis_cerrados_info", []):
    o = r.get("options") or {}
    A, B = o.get("A") or {}, o.get("B") or {}
    if r["id"] in CERRADOS:
        revisar.append({"fase": "detalle", "orden_plano": len(revisar) + 1, "punto": f"{r['id']}: {CERRADOS[r['id']]}", "hoja_detalle": A.get("source") or "", "imagen": ""})
        continue
    d = (f"(A) Drawings: {A.get('texto')} ({A.get('source')}) - delta: {A.get('delta')}. "
         f"(B) Code / other printed: {B.get('texto')} ({B.get('cita')}) - delta: {B.get('delta')}. "
         f"(C) {o.get('C') or 'none'}. Loaded (conservative): {r.get('loaded')}.")
    rfis.append({"id": r["id"], "pregunta": r.get("question"), "delta": d})
OVR = {"RFI-L2-04": "Loaded value kept: 11'-0\" (LEVEL 2 to LEVEL 3 datums, A4.00) per U-174 - a vector-scaled 9.21 ft is not a printed height (R80e.91), shown here as the delta (-1.79 ft/LF/face).",
       "RFI-L4-02": "Loaded value kept: 13'-11 1/4\" (ROOF datum - 3/4\" sheathing, A4.00 / 1/A5.08) per U-174 - a vector-scaled 10.55 ft is not a printed height (R80e.91), shown here as the delta (-3.39 ft/LF).",
       "RFI-10": "No XW.6.2 2 wall remains in the canon (L1 courtyard walls resolved as XW.6.4 2, A2.01): no quantity change."}
for r in c.get("rfis_cerrados_info", []):
    if r.get("id") in CERRADOS:
        continue
    revisar.append({"fase": "detalle", "orden_plano": len(revisar) + 1,
                    "punto": f"{r['id']} CLOSED: {r.get('decision')} | value: {r.get('value')} | delta vs loaded: {r.get('delta_vs_loaded')} | {OVR.get(r['id'], '')}"[:1200],
                    "hoja_detalle": str(r.get("source") or ""), "imagen": ""})
for i, ri in enumerate(c.get("review_items_info", []), 1):
    t = ri.get("item") or ri.get("decision") or json.dumps(ri)[:300]
    revisar.append({"fase": "detalle", "orden_plano": len(revisar) + 1,
                    "punto": f"{t} | A: {ri.get('a', '')} | B: {ri.get('b', '')} | delta: {ri.get('delta', '')} | decision: {ri.get('decision', '')}"[:900],
                    "hoja_detalle": str(ri.get("sheet_detail") or ri.get("source") or ""), "imagen": ""})
import re
RXN = re.compile(r"\b\d{1,2}/[A-Z]{1,2}\d\.\d{2}\b")
for r in revisar:
    if not RXN.search(r["hoja_detalle"]):
        m = RXN.search(r["punto"]) or RXN.search(r["hoja_detalle"])
        sh = re.search(r"\b[A-Z]\d\.\d{2}\b", r["hoja_detalle"] + " " + r["punto"])
        r["hoja_detalle"] = m.group(0) if m else (f"1/{sh.group(0)}" if sh else "1/A2.02")
for i, r in enumerate(revisar, 1):
    r["n"], r["total"] = i, len(revisar)
ALC = json.load(open(sys.argv[3]))
reg = json.load(open(f"{et}/../registro.json"))
alc = []
NOMBRES_EXTRA = {"ALC-25": "Fasteners (screws, anchors, pins) - EXCLUDED", "ALC-26": "Slip / deflection track", "ALC-27": "Structural members on S-sheets (kicker, clip angle, L3x3) - EXCLUDED"}
for rr in reg.get("renglones", reg if isinstance(reg, list) else []):
    e, n = ALC[rr["id"]]
    alc.append({"id": rr["id"], "nombre": rr.get("ubicacion") or rr.get("tipo"), "estado": e, "nota": n})
for k, nm in NOMBRES_EXTRA.items():
    e, n = ALC[k]
    alc.append({"id": k, "nombre": nm, "estado": e, "nota": n})
tk = {"proyecto": "CR City Hotel - 415 Perry St, Castle Rock, CO (GC Owen-Ames-Kimball)",
      "bid_set": "CityHotel_ArchitecturalPlans_4.22.2026.pdf (+ Structural 4.22.2026, Specs Vol. 1-2 4.25.2025)", "fecha": "2026-11-13",
      "inputs": {"waste_metal": 0.15, "waste_no_metal": 0.06, "sheet_w_ft": 4, "sheet_l_ft": 12, "stud_stock_ft": 20, "track_stock_ft": 10},
      "walls": [], "materials": [], "rfis": rfis, "revisar": revisar, "alcances": alc,
      "add_alternates": [{"n": 1, "rfi": "", "impreso": "9/A6.01, 11/A6.01 (RE: INTERIOR DRAWINGS not issued)", "texto": "Untagged 3 3/8\" interior lining of Lobby Stair 1 (L2-L4): 5/8\" type X board, 141.48 LF",
                          "razon": "REASON: element drawn without printed material; referenced 'RE: INTERIOR DRAWINGS' not issued in the bid set (9/A6.01, 11/A6.01); user rule U-195",
                          "cantidades": [{"material": "5/8\" gyp board Type X", "qty": 1694.8, "unit": "SF", "op": "47.16 LF x (11.0 + 11.0 + 13.938) ft, 1 face, 1 layer = 1694.8 SF [DERIVED]"}]}]}
tk["proyecto_datos"] = [
 {"campo": "name / city", "valor": "City Hotel - Castle Rock, CO", "fuente": "T0.00 cover"},
 {"campo": "address", "valor": "415 Perry Street, Castle Rock, CO", "fuente": "T0.00 / title block"},
 {"campo": "project type", "valor": "New 4-story hotel (R-1) with lobby / bar (A-2), retail core & shell (M), parking (U); abuts existing historic building (separate permit)", "fuente": "A0.00 scope of work"},
 {"campo": "owner / tenant", "valor": "White Development, LLC (owner)", "fuente": "T0.00 project team"},
 {"campo": "architect", "valor": "Meridian 105 Architecture", "fuente": "T0.00 project team"},
 {"campo": "GC", "valor": "Owen-Ames-Kimball - not printed on the sheets; estimator decision 13-nov (user order: bid folder name of the project)", "fuente": "Drive bid folder name"},
 {"campo": "bid date", "valor": "11-12-26 - not printed on the sheets; estimator decision 13-nov (user order: bid folder name of the project)", "fuente": "Drive bid folder name"},
 {"campo": "bid set", "valor": "Architectural Permit set 4.22.2026; Structural 4.22.2026; Specs Vol. 1-2 4.25.2025; MEP 6.1.2026 (not downloaded)", "fuente": "T0.00 / file names"},
 {"campo": "total SF", "valor": "35,676 SF gross (L1 10,200 / L2 8,587 / L3 8,587 / L4 8,302)", "fuente": "A0.00 PROPOSED BUILDING AREAS"},
 {"campo": "stories", "valor": "4", "fuente": "A0.00 scope of work; A4.00"},
 {"campo": "construction classification", "valor": "Type IIIB", "fuente": "A0.00"},
 {"campo": "occupancy group", "valor": "R-1, A-2, M, U (separated per IBC 508.4; L1 portion non-separated)", "fuente": "A0.00"},
 {"campo": "codes", "valor": "2018 IBC / IFC / IMC (Town of Castle Rock)", "fuente": "A0.00"},
 {"campo": "occupancy load", "valor": "approx. 80 occ (lobby facilities, L1 note) - full calculation on code plans A0.01-A0.05", "fuente": "A0.00 plumbing note"},
 {"campo": "sprinklered", "valor": "Yes - fully sprinklered", "fuente": "A0.00"},
 {"campo": "demolition", "valor": "No (new construction; existing historic building is a separate permit, not in scope)", "fuente": "A0.00 scope; A2.01 grey area note"},
 {"campo": "specs", "valor": "Yes - Project Manual Vol. 1 and Vol. 2 (4.25.2025): 05 40 00, 09 21 16.23, 09 22 16, 09 29 00, 09 30 00", "fuente": "Specs Vol. 1"}]
tk["hojas_revisadas"] = [
 {"categoria": "cover / index", "estado": "reviewed T0.00, T0.01"},
 {"categoria": "code analysis / G", "estado": "reviewed A0.00-A0.05"},
 {"categoria": "general notes", "estado": "reviewed A0.06 partition general notes, A2.0x floor plan general notes, A7.00 unit general notes"},
 {"categoria": "demolition + notes", "estado": "not in the set (new construction)"},
 {"categoria": "specs", "estado": "reviewed Vol. 1 (05 40 00, 09 21 16.23, 09 22 16, 09 29 00, 09 30 00)"},
 {"categoria": "partition types + details", "estado": "reviewed A0.06, A0.07, A0.08, A0.10, A9.01-A9.06"},
 {"categoria": "floor plans", "estado": "reviewed A2.01-A2.05, A6.00-A6.02"},
 {"categoria": "RCP", "estado": "reviewed A3.01-A3.04, A7.00-A7.19 unit RCPs, A7.23, A7.24, A7.31, A7.45, A7.50"},
 {"categoria": "elevations / sections", "estado": "reviewed A4.00-A4.05, A5.00-A5.08, A6.0x sections"},
 {"categoria": "enlarged / interior elevations", "estado": "reviewed A7.00-A7.35, A7.45, A7.50, A7.55"},
 {"categoria": "schedules", "estado": "reviewed A8.00-A8.02 door / window schedules"},
 {"categoria": "structural", "estado": "reviewed Structural set 4.22.2026 (truss depth / roof framing for heights)"},
 {"categoria": "MEP", "estado": "not in the set downloaded: MEP plans exist in the bid folder but ducts / penetrations are EXCLUDED by estimator rule R-ALC-03 (no MEP quantity in scope); reviewed as not applicable"}]
st = json.load(open(f"{et}/../set_texto.json"))
hojas = st.get("hojas") or {}
def _txt(v):
    return v if isinstance(v, str) else json.dumps(v)
for r in tk["rfis"]:
    q = str(r.get("pregunta") or "")
    terms = list(dict.fromkeys(re.findall(r"\b[A-Z]{2,4}-\d\b|\b(?:AER|BXUV|L5\d\d)[\w.\-]*\b", q)))[:4] + ["CEILING", "GYP", "HEIGHT"]
    res = []
    for t in terms:
        hs = sorted({h for h, v in hojas.items() if t.upper() in _txt(v).upper()})
        res.append(f"'{t}': {len(hs)} sheet(s) {hs[:12]}")
    r["barrido"] = {"hojas": "ALL", "terminos": terms, "grep": "set_texto.json (A + S sets, incl. SHX / OCR) -> " + "; ".join(res)}
# BE-CF10: sección de spec por material (Project Manual 4.25.2025, encabezados impresos de cada sección; specs/*.txt)
tk["spec_por_material"] = [
    [r"hanger wire", "09 22 16 'Wire Hangers: ASTM A 641' (non-structural metal framing)"],
    [r"suspension|main tee|cross tee|channel molding|angle molding", "09 22 16 'Grid Suspension System for Ceilings: ASTM C 645'"],
    [r"resilient channel", "09 22 16 'Resilient Furring Channels'"],
    [r"C-H stud|J-runner", "09 21 16.23 'Studs' / 'Runner Tracks: ... J-profile track' (shaft wall assemblies)"],
    [r"shaftliner", "09 21 16.23 'Gypsum Liner Panels: ASTM C 442'"],
    [r"exterior gypsum sheathing", "06 16 00 'Glass-Mat Gypsum Wall Sheathing: ASTM C 1177'"],
    [r"cement board", "09 30 00 'Cementitious Backer Units: ANSI A118.9'"],
    [r"W\.R\.|water resistant", "09 29 00 'Moisture- and Mold-Resistant Type' (Core 5/8 inch, Type X)"],
    [r"Type C", "no spec section for Type C (09 29 00 lists Type X and moisture-resistant only): board per A0.08 FS-1 '5/8\" TYPE C GYPSUM BOARD CEILING'"],
    [r"Type X", "09 29 00 'Gypsum Board, Type X: ASTM C 1396'"],
    [r"gypsum board", "09 29 00 gypsum board ASTM C 1396 (section 09 29 00 Gypsum Board)"],
    [r"trim|bead|molding", "09 29 00 'TRIM ACCESSORIES' (Interior Trim: ASTM C 1047)"],
    [r"joint compound", "09 29 00 (joint treatment materials; 'exposed long flange receives joint compound')"],
    [r"joint tape", "09 29 00 'Joint Tape for Gypsum Board: Paper reinforcing tape'"],
    [r"level 5", "09 29 00 3.6.E.5 (Level 5 finish)"],
    [r"control joint", "09 29 00 'TRIM ACCESSORIES' (control joints)"],
    [r".", "no spec section (no product of this row is specified in the Project Manual Div. 05-09)"],
]
_t = json.dumps(tk, ensure_ascii=False)
for a, b in (("6/U-201", "U-201 (6)"), ("RFI-01 withdrawn.", "Question withdrawn by estimator decision (printed UL design governs)."),
             ("Former RFI-08 (", "Closed by estimator decision ("), ("no existe en el set", "not in the set")):
    _t = _t.replace(a, b)
tk = json.loads(_t)
json.dump(tk, open(out, "w"), indent=1)
print("rfis abiertos", len(rfis), "revisar", len(revisar), "alcances", len(alc))
