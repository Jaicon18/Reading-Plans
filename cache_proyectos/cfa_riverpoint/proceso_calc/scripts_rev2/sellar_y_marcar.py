"""Seals every metal wall of the reconciled canon with closer.py and marks the evidence per sheet / type with
planmark.py (CFA #2284 River Point). Numbers come from canon.py outputs (studs_out / corridas_out / board_out);
this script only hands them to the closer gate.

Use: python3 bitacora.py run scripts/sellar_y_marcar.py <tools_dir> <clean.pdf>
Out: etapas/4_canon/out/cierres/<wall>.json, etapas/4_canon/out/cierres_resumen.json,
     etapas/7_imagenes/planmark/<sheet>_type_<t>.png
"""
import json, os, sys
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, sys.argv[1])
PDF = sys.argv[2]
os.environ.setdefault("TAKEOFF_CONTROL_JOINT_MOTIVO", (
    "No gypsum board control joint is printed or detailed for our scope (A-202 wall notes, A-221 RCP, A-60x/A-62x "
    "elevations, C09250 / A-909 swept); runs of metal-framed board are < 30 ft (longest M2.1 14'-2\"): none quantified."))
import closer
from closer import Val, Wall, CierreRechazado
import planmark

C4 = os.path.join(K, "etapas", "4_canon")
C = json.load(open(os.path.join(C4, "takeoff_canon.json")))
S = {w["id"]: w for w in json.load(open(os.path.join(C4, "out", "studs_out.json")))["walls"]}
R = {r["id"][2:]: r for r in json.load(open(os.path.join(C4, "out", "corridas_out.json")))["renglones"] if r["id"].startswith("W:")}
B = {}
for c in json.load(open(os.path.join(C4, "out", "board_out.json")))["caras"]:
    B.setdefault(c["wall"], []).append(c)
OUT = os.path.join(C4, "out", "cierres")
os.makedirs(OUT, exist_ok=True)
EXCL = {
    "INSULATION": "EXCLUDED: insulation not in scope (estimator standing order); mineral wool A1/A-605, batts B.1-B.5/A-202 by others",
    "SEALANT": "EXCLUDED: acoustical sealant excluded in all projects (estimator standing order, U8)",
    "PATCH": "EXCLUDED here: board on existing walls is carried as board-only entries (existing_walls), not per metal wall",
    "CLIPS": "EXCLUDED: " + C["deflection_clips"]["none_reason"] + " (" + C["deflection_clips"]["source"] + ")",
}
BLK = {}
for b in C.get("blocking_items") or []:
    BLK.setdefault(b["wall"], []).append(b)

res, rech = [], []
for n, w in enumerate([w for w in C["walls"] if w.get("element", "wall") == "wall"], 1):
    wid, det = w["id"], w["detail"]
    try:
        x = Wall(n, w.get("tag") or "", f"{wid} - {w.get('location', '')} ({w['sheet']})")
        L = Val(w["length_ft"], "DERIVADO", fuente=w["sheet"], operacion=(w.get("length_op") or w.get("length_source", "")) + f" ({det})")
        H = Val(w["height_ft"], "DERIVADO", fuente=w["height_source"], operacion=w.get("height_op") or ("height per " + w["height_source"]))
        x.base(L, H, w["oc_in"], 48)
        for f in w.get("faces") or []:
            x.cara(f["room"], Val(f["height_ft"], "DERIVADO", operacion=f["height_source"] + f" ({det})"), f["board"], f.get("layers", 1))
        s, r = S[wid], R[wid]
        x.partida("STUD", Val(s["pcs_full"] + s["cripples"], "DERIVADO", operacion=s["operacion"] + f" ({det})"), "pcs")
        for lado, k in (("TRACK_BOTTOM", "bottom_track"), ("TRACK_TOP", "top_track")):
            if w.get(k) is False:
                x.excluir(lado, "EXCLUDED here: " + (w.get("track_source_info") or "no runner drawn") + " (" + w["track_source"] + ")")
            else:
                x.partida(lado, Val(r["bottom_lf" if k == "bottom_track" else "top_lf"], "DERIVADO", operacion=r["operacion"] + f" ({det})"), "LF")
        if r["bracing_lf"]:
            x.partida("BRACING", Val(r["bracing_lf"], "DERIVADO", operacion=r["operacion"] + f" ({det})"), "LF")
        else:
            x.excluir("BRACING", f"EXCLUDED: 0 bracing rows for this height per {r['operacion']}")
        x.excluir("HEADER", "EXCLUDED: wall has no opening on " + w["sheet"] + " (canon openings [])")
        bl = BLK.get(wid)
        if bl:
            x.partida("BLOCKING", Val(round(sum(b["lf"] * b["rows"] for b in bl), 2), "DERIVADO",
                                      operacion=" + ".join(f"{b['ref']} {b['lf']} x {b['rows']} row(s) ({b['source'][:60]})" for b in bl)), "LF")
        else:
            x.excluir("BLOCKING", "EXCLUDED: no blocking printed on this wall (A-202 F.1 wood blocking is Div. 06; blocking_items of the canon)")
        caras = B.get(wid, [])
        for c in caras:
            x.partida("BOARD:" + c["room"], Val(c["sf"], "DERIVADO", operacion=c["operacion"] + f" ({det})"), "SF")
        if not caras:
            x.excluir("BOARD", "EXCLUDED: no board face on this wall (" + det + ")")
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

# ---- planmark: evidence per sheet and type (walls[] with a band) ----
PAG = {"A-202": 13, "A-221": 15}
IMG = os.path.join(K, "etapas", "7_imagenes", "planmark")
os.makedirs(IMG, exist_ok=True)
fallas = 0
for sh, pg in PAG.items():
    hoja = planmark.Hoja(PDF, pg, dpi=100)
    tipos = sorted({w.get("tag") for w in C["walls"] if w["band"].get("sheet") == sh})
    for t in tipos:
        items = [{"id": w["id"], "band": w["band"], "lf": w["length_ft"], "tagged": bool(w.get("tag_ids")),
                  "dashed": w.get("element") == "soffit_side"}
                 for w in C["walls"] if w["band"].get("sheet") == sh and w.get("tag") == t]
        try:
            r = hoja.overview(items, f"CFA #2284 River Point - {sh} - type {t} (evidence)", os.path.join(IMG, f"{sh}_type_{t.replace('.', '_')}.png"))
            print("planmark", sh, t, r["tinta"])
        except Exception as e:
            fallas += 1
            print("PLANMARK", sh, t, type(e).__name__, str(e)[:300])
print(f"planmark: {fallas} failure(s)")
sys.exit(1 if rech or fallas else 0)
