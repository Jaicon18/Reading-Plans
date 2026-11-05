"""Seals every metal wall / vestibule-head element of the canon with closer.py and marks the evidence per sheet / type
with planmark.py (HFT Loveland). Numbers come from canon.py outputs (studs_out / corridas_out / board_out); this script
only hands them to the closer gate.
Use: python3 bitacora.py run scripts/sellar_y_marcar.py <tools_dir> <clean.pdf>
Out: etapas/4_canon/out/cierres/<wall>.json, out/cierres_resumen.json, etapas/7_imagenes/planmark/<sheet>_type_<t>.png"""
import json, os, sys
K = os.environ.get("K") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, sys.argv[1])
PDF = sys.argv[2]
C4 = os.path.join(K, "etapas", "4_canon")
C = json.load(open(os.path.join(C4, "takeoff_canon.json")))
cj = [m for m in C.get("misc_items") or [] if m.get("familia") == "control joint"]
os.environ.setdefault("TAKEOFF_CONTROL_JOINT_MOTIVO", (
    "Control joints carried as their own items (" + ", ".join(f"{m['ref']} {m['source']}" for m in cj) + ")" if cj else
    "No gypsum board control joint printed for our scope"))
import closer
from closer import Val, Wall, CierreRechazado
import planmark

S = {w["id"]: w for w in json.load(open(os.path.join(C4, "out", "studs_out.json")))["walls"]}
R = {r["id"][2:]: r for r in json.load(open(os.path.join(C4, "out", "corridas_out.json")))["renglones"] if r["id"].startswith("W:")}
B = {}
for c in json.load(open(os.path.join(C4, "out", "board_out.json")))["caras"]:
    B.setdefault(c["wall"], []).append(c)
OUT = os.path.join(C4, "out", "cierres")
os.makedirs(OUT, exist_ok=True)
dc = C.get("deflection_clips") or {}
EXCL = {
    "INSULATION": "EXCLUDED: insulation not in scope (estimator standing order); batts of 1/A500 wall types by others",
    "SEALANT": "EXCLUDED: acoustical sealant excluded in all projects (estimator standing order)",
    "CLIPS": "EXCLUDED: " + (dc.get("none_reason") or dc.get("note_source") or "no deflection clip printed")
             + " (" + (dc.get("source") or dc.get("slip_track_source") or "4/A500") + ")",
}
BLK = {}
for b in C.get("blocking_items") or []:
    BLK.setdefault(b["wall"], []).append(b)

res, rech = [], []
for n, w in enumerate([w for w in C["walls"] if w["id"] in S], 1):
    wid, det = w["id"], w.get("detail") or w.get("source")
    try:
        x = Wall(n, w.get("tag") or "", f"{wid} - {w.get('location', '')} ({w['sheet']})")
        L = Val(w["length_ft"], "DERIVADO", fuente=w["sheet"], operacion=(w.get("length_op") or w.get("length_source", "")) + f" ({det})")
        H = Val(w["height_ft"], "DERIVADO", fuente=w["height_source"], operacion=w.get("height_op") or ("height per " + w["height_source"]))
        x.base(L, H, w["oc_in"], 48)
        for f in w.get("faces") or []:
            x.cara(f["room"], Val(f["height_ft"], "DERIVADO", operacion=f["height_source"] + f" ({det})"), f["board"], f.get("layers", 1))
        if not w.get("faces"):       # structural CFS wall without gypsum: its face is declared with board EXCLUDED
            x.cara("both faces (no gypsum board)", Val(w["height_ft"], "DERIVADO", operacion=str(w.get("faces_none_reason") or det)[:200]),
                   "NONE - " + str(w.get("faces_none_reason") or "no gypsum board")[:80], 1)
        s, r = S[wid], R[wid]
        x.partida("STUD", Val(s["pcs_full"] + s["cripples"], "DERIVADO", operacion=s["operacion"] + f" ({det})"), "pcs")
        for lado, k in (("TRACK_BOTTOM", "bottom_track"), ("TRACK_TOP", "top_track")):
            v = r["bottom_lf" if k == "bottom_track" else "top_lf"]
            if w.get(k) is False or not v:
                x.excluir(lado, "EXCLUDED here: " + (w.get("track_source") or "no runner drawn") + f" ({det})")
            else:
                x.partida(lado, Val(v, "DERIVADO", operacion=r["operacion"] + f" ({det})"), "LF")
        if r["bracing_lf"]:
            x.partida("BRACING", Val(r["bracing_lf"], "DERIVADO", operacion=r["operacion"] + f" ({det})"), "LF")
        else:
            x.excluir("BRACING", f"EXCLUDED: 0 bracing rows per {r['operacion']}")
        if w.get("openings"):
            x.excluir("HEADER", "carried by headers.py through canon.py (header / box beam row): " +
                      ", ".join(f"{o['ref']} {o.get('header_source') or o.get('header') or ''}"[:80] for o in w["openings"]))
        else:
            x.excluir("HEADER", "EXCLUDED: wall has no opening on " + w["sheet"] + " (canon openings [])")
        bl = BLK.get(wid)
        if bl:
            x.partida("BLOCKING", Val(round(sum(b["lf"] * b.get("rows", 1) for b in bl), 2), "DERIVADO",
                                      operacion=" + ".join(f"{b['ref']} {b['lf']} ({b['source'][:60]})" for b in bl)), "LF")
        else:
            x.excluir("BLOCKING", "EXCLUDED: " + (C.get("blocking_none_reason") or "no metal blocking printed")[:200])
        caras = B.get(wid, [])
        for c in caras:
            x.partida("BOARD:" + c["room"], Val(c["sf"], "DERIVADO", operacion=c["operacion"] + f" ({det})"), "SF")
        if not caras:
            x.excluir("BOARD", "EXCLUDED: no gypsum board face on this wall: " + str(w.get("faces_none_reason") or det)[:200])
        x.excluir("PATCH", "EXCLUDED: no patching of existing board in this wall (new construction)")
        for k, v in EXCL.items():
            x.excluir(k, v)
        d = x.emit(os.path.join(OUT, wid.replace("/", "_") + ".json"))
        res.append({"wall": wid, "tag": w.get("tag"), "sello": d["sello"]})
    except CierreRechazado as e:
        rech.append({"wall": wid, "error": str(e)})

json.dump({"sellados": res, "rechazados": rech}, open(os.path.join(C4, "out", "cierres_resumen.json"), "w"), ensure_ascii=False, indent=1)
print(f"closer: {len(res)} walls sealed, {len(rech)} rejected")
for r in rech:
    print("REJECTED", r["wall"], r["error"][:800])

sm = json.load(open(os.path.join(K, "etapas", "SHEET_MAP.json")))
PAG = {v: int(k) for k, v in sm.items()}
IMG = os.path.join(K, "etapas", "7_imagenes", "planmark")
os.makedirs(IMG, exist_ok=True)
fallas = 0
for sh in sorted({w["band"]["sheet"] for w in C["walls"] if w.get("band")}):
    hoja = planmark.Hoja(PDF, PAG[sh], dpi=100)
    for t in sorted({w.get("tag") for w in C["walls"] if w["band"].get("sheet") == sh}):
        items = [{"id": w["id"], "band": w["band"], "lf": w["length_ft"], "tagged": bool(w.get("tag_ids")),
                  "dashed": w.get("element") != "wall"}
                 for w in C["walls"] if w["band"].get("sheet") == sh and w.get("tag") == t]
        try:
            r = hoja.overview(items, f"Consumer Cellular - Centennial, CO - {sh} - type {t} (evidence)",
                              os.path.join(IMG, f"{sh}_type_{t.replace('.', '_')}.png"))
            print("planmark", sh, t, r["tinta"])
        except Exception as e:
            fallas += 1
            print("PLANMARK", sh, t, type(e).__name__, str(e)[:300])
print(f"planmark: {fallas} failure(s)")
sys.exit(1 if rech or fallas else 0)
