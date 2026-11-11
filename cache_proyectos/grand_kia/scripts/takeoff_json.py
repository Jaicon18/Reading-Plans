"""Grand Kia - <W>/takeoff.json (formato plantilla_excel.py) desde el canon resuelto, proceso/proyecto_datos.json,
4_canon/rfis_final.json y el escaneo de alcances. SOLO TEXTO: toda cantidad del Excel sale de familias_out.json por
plantilla_excel. Uso: python3 bitacora.py run scripts/takeoff_json.py <tools_dir>"""
import json, os, sys
sys.path.insert(0, sys.argv[1])
import plantilla_excel
K = '/root/gk/work'
C4 = os.path.join(K, "etapas", "4_canon")
c = json.load(open(os.path.join(C4, "takeoff_canon.json")))
pd = json.load(open(os.path.join(K, "proceso", "proyecto_datos.json")))["proyecto_datos"]
RF = json.load(open(os.path.join(C4, "rfis_final.json"))) if os.path.exists(os.path.join(C4, "rfis_final.json")) else {"rfis": [], "review_items": []}
EXTRA = json.load(open(os.path.join(C4, "alcance_notas.json"))) if os.path.exists(os.path.join(C4, "alcance_notas.json")) else {}


def fmt(o):
    A, B = o.get("A") or {}, o.get("B") or {}
    C = o.get("C") or "____"
    return (f"(A) Drawings ({A.get('source', '')}): {A.get('texto', '')} - delta {A.get('delta', '')} | "
            f"(B) Code ({B.get('cita', 'n/a')}): {B.get('texto', '')} - delta {B.get('delta', '')} | (C) Other: {C or '____'}")


def _fig(v):
    if isinstance(v, dict):
        return "; ".join(f"({k}) {_fig(x)}" for k, x in v.items())
    if isinstance(v, list):
        return "; ".join(_fig(x) for x in v)
    return str(v)


rfis, cierre = [], {}
for r in RF["rfis"]:
    st = str(r.get("status", "open")).lower()
    if st != "open":
        res = r.get("resolved") or {}
        cierre[r["id"]] = {"pregunta": f"{r.get('question', r.get('topic', ''))} - {st.upper()} [{res.get('source', r.get('source', ''))}]: {res.get('answer', '')}",
                           "delta": r.get("delta_applied") or "0 (closed by the drawings / code / standing rule)"}
        continue
    o = r.get("opciones") or {}
    b0 = r.get("barrido") or {}
    r["barrido"] = dict(b0, hojas="ALL", terminos=b0.get("terminos") or b0.get("terms") or [],
                        grep=b0.get("swept_txt") or "full text of the set searched (OCR layer A000-A560 + S/M/P/E text + spec book)")
    sw = (r.get("barrido") or {}).get("swept_txt") or ""
    rfis.append({"id": r["id"], "pregunta": f"{r['question']} - carried: {r.get('loaded', '')} (conservative value loaded). {sw}"[:3000],
                 "delta": fmt(o), "opciones": o, "source": r.get("source", ""), "barrido": r.get("barrido", {}),
                 "img": r.get("img")})
import re as _re
NH = _re.compile(r"\b[0-9A-Z]{1,3}/[A-Z]{1,2}-?\d{3}[A-Z]?\b")
WID = _re.compile(r"\b([A-H]1?)-Z\d-\d{2}\b")
revisar = []
for i, x in enumerate(RF.get("review_items") or []):
    if not isinstance(x, dict):
        continue
    txt = f"{x.get('item', '')}: {_fig(x.get('figures', ''))}; delta {_fig(x.get('delta', ''))}; decision: {_fig(x.get('decision', 'value loaded as described'))}"
    blob = " ".join(str(x.get(k) or "") for k in ("sheet", "item", "figures", "decision"))
    m_nh, m_w = NH.search(blob), WID.search(blob)
    it = {"punto": txt, "imagen": os.path.basename(str(x.get("img") or ""))}
    if m_w:          # a review item about a wall goes with its type on the floor plan (U10)
        it.update(fase="floor_plan", type=m_w.group(1), hoja_detalle=x.get("sheet") or "A111")
    elif m_nh:
        it.update(fase="detalle", orden_plano=i + 1, hoja_detalle=m_nh.group(0))
    else:
        it.update(fase="floor_plan", type="GENERAL", hoja_detalle=x.get("sheet") or "A111")
    revisar.append(it)
# COORDINACIÓN 11-nov: A520 missing, A111 / A112 scale proof, and every A/B height resolution (U-176 control 1) in Review Items
_a520 = json.load(open(os.path.join(K, "etapas", "A520_FALTANTE.json")))
revisar.append({"punto": "Sheet A520 is NOT in the set (page 41 repeats A521; sheet index A000 lists it). " + str(len(_a520["bubbles"])) +
                " details are called to it (" + str(_a520["occurrences"]) + " bubble occurrences): " + "; ".join(f"{b['detail']} from {', '.join(b['called_from'])}" for b in _a520["bubbles"]) +
                ". Searched: Crossland set (identical md5), Brinkman ADD #1 (spec book only), BuildingConnected files. Parapet / roof-edge framing taken from wall sections A310-A312, building sections A300 / A301, S121 / S122 / S403 and spec 05 40 00; no quantity depends on A520 alone.",
                "fase": "floor_plan", "type": "GENERAL", "hoja_detalle": "A310", "imagen": "RI_A520_missing_p41_repeats_A521.png"})
revisar.append({"punto": "Plan scale: A111 / A112 scale bars read 1/4\" = 1'-0\" but every printed dimension measures 1/8\" = 1'-0\" (9 pt/ft): e.g. B-Z2-02 string 7'-8 1/2\" spans 882.0 to 951.6 pt = 69.6 pt (69.6 / 9 = 7.73 ft vs printed 7.71 ft; at 1/4\" it would read 3.87 ft); F-Z3-03 string 8'-0\" (window F) = 72 pt (72 / 9 = 8.00 ft). Quantities and the Bluebeam /Measure of A111 / A112 use 1/8\".",
                "fase": "floor_plan", "type": "GENERAL", "hoja_detalle": "A111", "imagen": "RI_A111_scale_label.png"})
_ar = os.path.join(K, "alturas", "FINAL", "ALTURAS_AB_RESOLUCION.csv")
if os.path.isfile(_ar):
    import csv as _csv
    for r in _csv.DictReader(open(_ar, encoding="utf-8-sig")):
        m_w = WID.search(r["Wall ID"])
        revisar.append({"punto": f"Height {r['Wall ID']} (two blind readings disagreed, U-176): {r['Resolution']}",
                        "imagen": os.path.basename(r.get("Image") or ""),
                        **({"fase": "floor_plan", "type": m_w.group(1), "hoja_detalle": "A111"} if m_w else
                           {"fase": "floor_plan", "type": "GENERAL", "hoja_detalle": "A108" if "DEMO" in r["Wall ID"] else "A131"})})
hojas = [
    {"categoria": "cover / index / code", "estado": "reviewed", "hojas": "A000 cover (sheet index 129 sheets, project description, code information, building code analysis III-B sprinklered, area by occupancy 41,287 SF), A001 project information, A002 / A003 code plans (rated walls)"},
    {"categoria": "general notes", "estado": "reviewed", "hojas": "A111 / A112 general notes 1-2 and keynotes 1-60, A113 keynotes 1-7, A550 general notes 1-5 and keynotes 1-15, A131 RCP notes / keynotes, S001 general structural notes"},
    {"categoria": "demolition + notes", "estado": "reviewed", "hojas": "A108 demolition ground floor plan + keynotes 1-56, A109 demolition second floor plan"},
    {"categoria": "specs", "estado": "reviewed", "hojas": "Project Specifications (spec book, ADD #1 identical): 01 10 00, 02 41 19, 05 40 00 Cold-Formed Metal Framing, 06 10 00, 06 16 00 Sheathing, 07 21 00, 07 92 00, 09 29 00 Gypsum Board (no non-structural metal framing section in the book)"},
    {"categoria": "partition types + details", "estado": "reviewed", "hojas": "A550 wall construction types A-K (A/A1 ... H/H1, J/K CMU), A551 2-hour rated CMU wall UL U906, A540 interior details (7 control joints, 8 brace, 10 floor, 13 deflection track, 14 / 23 / 24 / 28 ceiling details)"},
    {"categoria": "floor plans", "estado": "reviewed", "hojas": "A110 overall ground floor, A111 / A112 partial ground floor plans (tags, dimensions; scale bar reads 1/4\" but dimensions measure 1/8\"), A113 second floor, A150 enlarged restrooms"},
    {"categoria": "RCP", "estado": "reviewed", "hojas": "A130 overall RCP, A131 / A132 partial RCP (ceiling tags PGB / ACT / exposed, heights, keynotes, legend), A133 second floor RCP"},
    {"categoria": "elevations / sections", "estado": "reviewed", "hojas": "A200 / A201 exterior elevations, A300 / A301 building sections (heights measured at printed scale: no deck elevations printed), A310-A312 wall sections"},
    {"categoria": "enlarged / interior elevations", "estado": "reviewed", "hojas": "A150 enlarged restroom plans, A210 / A211 interior elevations, A220 / A221 window frame elevations, A230 / A231 casework elevations"},
    {"categoria": "schedules", "estado": "reviewed", "hojas": "A400 door schedule, A401 hardware, A140 interior finish schedule / legend (Level 5 at WC-1), A141-A143 finish plans"},
    {"categoria": "structural", "estado": "reviewed", "hojas": "S001 general notes (CFS mils table), S111-S122 foundation / framing plans, S201-S204 typical details, S301-S302, S401-S403 framing details (CFS 362S162-33, 600S162-43, 1000S162-43)"},
    {"categoria": "MEP", "estado": "reviewed", "hojas": "M101-M301, P100-P501, E001-ES301 swept for wall penetrations / access panels (ducts EXCLUDED by standing order)"},
]
reg = json.load(open(os.path.join(K, "registro.json")))
NOMB = {r["id"]: r.get("ubicacion") for r in reg["renglones"]}
alc = EXTRA.get("alc") or []
alcances = [{"id": i, "nombre": NOMB.get(i, i), "estado": e, "nota": x} for i, e, x in alc]
for k, (n, x) in enumerate(EXTRA.get("extra") or [], 1):
    alcances.append({"id": f"ALC-E{k:02d}", "nombre": n,
                     "estado": "CUANTIFICADO" if x.startswith(("QUANTIFIED", "INCLUDED")) else "NO APLICA", "nota": x})
td = {
    "proyecto": "Grand Kia Auto Dealership - 2040 W 104th Avenue, Thornton (Denver), CO 80234 (Brinkman Construction)",
    "bid_set": "Grand Kia - Current Drawing Set (John Mahoney Architect project 2412, issue 7/23/26), 112 pages; Project Specifications + ADD #1 (11/03/2026); identical sets from Brinkman and Crossland",
    "fecha": "2026-11-10",
    "inputs": {"waste_metal": 0.15, "waste_no_metal": 0.06, "sheet_w_ft": 4, "sheet_l_ft": 12, "stud_stock_ft": 20,
               "track_stock_ft": 10, "plan_scale_pt_per_ft": 9.0, "bod_ft": 24.9},
    "inputs_notas": {"bod_ft": "No deck elevation printed: heights per wall measured on A300 / A301 / A310-A312 at the printed scale (see Partition Takeoff); 24.9 ft = showroom roof (A300 B-B) shown for reference only.",
                     "plan_scale_pt_per_ft": "A111 / A112 dimensions measure 1/8\" = 1'-0\" (9 pt/ft) although the scale bar reads 1/4\"; A113 3/32\" (6.75 pt/ft); A150 1/2\" (36 pt/ft).",
                     "drywall_screws_per_sf": "YIELD; fasteners EXCLUDED (estimator standing order U-053)."},
    "type_order": ["A", "A1", "B", "B1", "C", "C1", "D", "D1", "E", "E1", "F", "F1", "G", "G1", "H", "H1"],
    "walls": [], "materials": [],
    # BE-CF10: spec section / article of every material, read from the project spec book (specs/*.txt, ADD #1 = same book)
    "spec_por_material": [
        [r"glass mat|DensShield|tile backer", "09 29 00 2.3 Tile Backing Panels (glass-mat, ASTM C 1178)"],
        [r"EXTERIOR gyp|sheathing", "06 16 00 2.5 Wall Sheathing (Glass-Mat Gypsum Wall Sheathing, ASTM C 1177)"],
        [r"gypsum board|gyp board|Type X", "09 29 00 2.1 Interior Gypsum Board"],
        [r"control joint|corner bead|casing|trim|J mold|edge trim|bead|reveal", "09 29 00 2.4 Trim Accessories"],
        [r"compound|tape", "09 29 00 2.5 Joint Treatment Materials"],
        [r"Level 5", "09 29 00 3.6.D Gypsum Board Finish Levels (Level 5 per A140 general note 1)"],
        [r"main tee|cross tee|angle molding|hanger|grid", "no spec section (gypsum ceiling suspension not in the spec book; 24/A540 and IBC 808 / ASTM C 636 per RFI-25)"],
        [r"stud|track|runner|header|box beam|bridging|brace|channel|clip|blocking|joist|slip|deflection", "05 40 00 2.2 Exterior and Interior Non-Load-Bearing Wall Framing / 2.3 Framing Accessories"],
        [r"demolition", "02 41 19 Selective Demolition (Div. 02; no spec section in Div. 05 / 09)"],
        [r".", "no spec section"],
    ],
    "rfis": rfis, "rfi_cierre": cierre, "revisar": plantilla_excel.ordenar_revisar(revisar), "alcances": alcances,
    "proyecto_datos": pd, "hojas_revisadas": hojas, "barrido_no_dibujado": EXTRA.get("barrido") or [],
}
# visible text in English, no internal file / program words (R80e.84) and no raw dicts
def _fig(v):
    if isinstance(v, dict):
        return "; ".join(f"({k}) {_fig(x)}" for k, x in v.items())
    if isinstance(v, list):
        return "; ".join(_fig(x) for x in v)
    return str(v)
REPL = [(r"\bcanon(?:ical)?\b", "take-off"), (r"\bCanon\b", "Take-off"), (r"comparacion_sets\.json", "program comparison of the two GC sets"),
        (r"\b[\w/.-]+\.(?:json|py|md)\b", "audit file"), (r"\bsin\b", "without"), (r"\bcon\b", "with")]
def limpiar(o):
    if isinstance(o, dict):
        return {k: limpiar(v) for k, v in o.items()}
    if isinstance(o, list):
        return [limpiar(v) for v in o]
    if isinstance(o, str) and not o.startswith("/"):
        o = _re.sub(r"\by\s*(=|~)?\s*(?=\d)", "vert. coord. ", o)     # plot coordinate 'y 1319' / 'y=1319' (not the Spanish 'y')
        o = _re.sub(r"(?i)\bconflicting\b", "differing", o); o = _re.sub(r"(?i)\bconflicts?\b", "mismatch", o)   # drawing-vs-drawing readings, not plan-vs-spec (R-ALC-10 notes keep their own wording)
        o = _re.sub(r"\bbuild_canon\b", "the take-off program", o)
        o = _re.sub(r"\bgauge_by_wall\b", "gauge per wall", o)
        o = _re.sub(r"see RFI-01 resolved\.bands", "see RFI-01 (gauge per wall height band)", o)
        for a, b in REPL:
            o = _re.sub(a, b, o, flags=_re.I if a.startswith("\\bcanon") else 0)
        return o
    return o
for it in td["revisar"]:
    it["punto"] = it["punto"]
td = limpiar(td)
json.dump(td, open(os.path.join(K, "takeoff.json"), "w"), indent=1, ensure_ascii=False)
print("rfis open", len(rfis), "closed", len(cierre), "revisar", len(revisar), "alcances", len(alcances))
