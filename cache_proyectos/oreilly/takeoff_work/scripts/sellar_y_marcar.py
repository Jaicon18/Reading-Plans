"""Sella cada wall del canon con closer.py y marca la evidencia por type con planmark.py (corrida O'Reilly Evans #1).

Uso: python3 bitacora.py run scripts/sellar_y_marcar.py <tools_dir> <bidset_SIN_MARKUPS.pdf>
Sale: etapas/4_canon/out/cierres/<wall>.json (sellado), etapas/4_canon/out/cierres_resumen.json,
      etapas/7_imagenes/planmark/<sheet>_type_<t>.png
"""
import json, os, sys
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, sys.argv[1])
PDF = sys.argv[2]
os.environ.setdefault("TAKEOFF_CONTROL_JOINT_MOTIVO", (
    "Gypsum board control joints are printed only on the S42 walls (2/A4.2 reveal located on 14/A4.1): carried as trim "
    "items (DRMF-625-75 reveal); no other control joint is labeled on A1.1, A4.1 or A4.2."))
import closer
from closer import Val, Wall, CierreRechazado
import planmark

C = json.load(open(K + "/etapas/4_canon/takeoff_canon.json"))
S = {w["id"]: w for w in json.load(open(K + "/etapas/4_canon/out/studs_out.json"))["walls"]}
R = {r["id"][2:]: r for r in json.load(open(K + "/etapas/4_canon/out/corridas_out.json"))["renglones"] if r["id"].startswith("W:")}
B = {}
for c in json.load(open(K + "/etapas/4_canon/out/board_out.json"))["caras"]:
    B.setdefault(c["wall"], []).append(c)

OUT = K + "/etapas/4_canon/out/cierres"
os.makedirs(OUT, exist_ok=True)
EXCL = {
    "INSULATION": "EXCLUDED: batt insulation not in scope (estimator criterion: no insulation); sound batt of S43 / S61 (A1.1) in Scope Checklist",
    "SEALANT": "EXCLUDED: acoustical sealant excluded in all projects (estimator standing order, U8)",
    "BLOCKING": "EXCLUDED here: FRT blocking is carried as project blocking_items (6/A4.2, A4.1, 8/A3.2, 10/A4.2 - RFI-10), not per wall",
    "PATCH": "NOT APPLICABLE: new building, no existing walls (A1.1)",
    "CLIPS": "EXCLUDED: no bracing clip called on the A1.1 wall types or 5/A4.2-7/A4.2; deflection at the roof per A1.1 note 2.C (track)",
}
BYID = {w["id"]: w for w in C["walls"]}


def tag_de(w):
    """Tag del wall; un return sin tag (part_of) toma el type del wall con tag del que es parte."""
    return w.get("tag") or (BYID.get(w.get("part_of")) or {}).get("tag") or ""


res, rech = [], []
for n, w in enumerate([w for w in C["walls"] if w["element"] == "wall"], 1):
    wid, det = w["id"], w["detail"]
    try:
        x = Wall(n, tag_de(w), f"{wid} - {w.get('location') or w.get('source', '')} ({w['sheet']})")
        L = Val(w["length_ft"], "DERIVADO", fuente=w["sheet"], operacion=(w.get("length_op") or w.get("length_source", "")) + f" ({det})")
        hst = w.get("height_status") or "DERIVADO"
        H = Val(w["height_ft"], "CONFIRMADO" if hst == "CONFIRMADO" else "DERIVADO", fuente=w["height_source"],
                operacion=w.get("height_op") or ("height per " + w["height_source"]))
        x.base(L, H, w["oc_in"], C["constants"].get("bracing_oc_in", 48))
        for f in w.get("faces") or []:
            x.cara(f["room"], Val(f["height_ft"], "DERIVADO", operacion=f["height_source"] + f" ({det})"),
                   f["board"], f.get("layers", 1))
        if not w.get("faces"):
            x.cara("no board face", Val(0, "DERIVADO", operacion=w.get("faces_none_reason", "no faces") + f" ({det})"),
                   "none", 1)
        for o in w.get("openings") or []:
            x.abertura("puerta" if o["kind"] == "door" else "hueco", o["ref"], o["ro_w_ft"], o["head_ft"],
                       head=o.get("head_source") or o.get("source", ""))
        s, r = S[wid], R[wid]
        x.partida("STUD", Val(s["pcs_full"] + s["cripples"], "DERIVADO", operacion=s["operacion"] + f" ({det})"), "pcs")
        for lado, k in (("TRACK_BOTTOM", "bottom_track"), ("TRACK_TOP", "top_track")):
            if w.get(k) is False:      # Z-furring (RFI-16) / deep-leg track in its own row (3/S5.1, 4/S5.1)
                x.excluir(lado, "EXCLUDED here: " + w["track_note_info"] + " (" + w["track_source"] + ")")
            else:
                x.partida(lado, Val(r["bottom_lf" if k == "bottom_track" else "top_lf"], "DERIVADO", operacion=r["operacion"] + f" ({det})"), "LF")
        if r["bracing_lf"]:
            x.partida("BRACING", Val(r["bracing_lf"], "DERIVADO", operacion=r["operacion"] + f" ({det})"), "LF")
        else:
            x.excluir("BRACING", f"EXCLUDED: 0 bracing rows for this height per {r['operacion']}")
        if w.get("openings"):
            x.excluir("HEADER", "EXCLUDED here: headers are carried by headers.py from the A5.1 / A5.2 schedules "
                                "(Header / metal stud box beam row); CMU openings by the mason - RFI-13")
        else:
            x.excluir("HEADER", "EXCLUDED: wall has no opening on " + w["sheet"])
        caras = B.get(wid, [])
        for c in caras:
            x.partida("BOARD:" + c["room"], Val(c["sf"], "DERIVADO", operacion=c["operacion"] + f" ({det})"), "SF")
        if not caras:
            x.excluir("BOARD", "EXCLUDED: " + (w.get("faces_none_reason") or "no board on this wall") + f" ({det})")
        for k, v in EXCL.items():
            x.excluir(k, v)
        d = x.emit(os.path.join(OUT, wid.replace("/", "_") + ".json"))
        res.append({"wall": wid, "tag": tag_de(w), "sello": d["sello"]})
    except CierreRechazado as e:
        rech.append({"wall": wid, "error": str(e)})

json.dump({"sellados": res, "rechazados": rech}, open(K + "/etapas/4_canon/out/cierres_resumen.json", "w"),
          ensure_ascii=False, indent=1)
print(f"closer: {len(res)} walls sellados, {len(rech)} rechazados")
for r in rech:
    print("RECHAZADO", r["error"][:600])

# ---- planmark: evidencia por sheet y type ----
PAG = {"A1.1": 37}


def banda(b):
    """BOX del canon (c0..c1 = x, lo..hi = y, build_A column wraps) -> BOX de planmark (x0, y0, x1, y1)."""
    if b["ori"] != "BOX":
        return b
    return {"ori": "BOX", "x0": b["c0"], "x1": b["c1"], "y0": b["lo"], "y1": b["hi"], "sheet": b["sheet"]}
IMG = K + "/etapas/7_imagenes/planmark"
os.makedirs(IMG, exist_ok=True)
fallas = 0
for sh, pg in PAG.items():
    hoja = planmark.Hoja(PDF, pg, dpi=100)
    tipos = sorted({tag_de(w) for w in C["walls"] if w["sheet"] == sh and w.get("band")})
    for t in tipos:
        items = [{"id": w["id"], "band": banda(w["band"]), "lf": w["length_ft"], "tagged": bool(w.get("tag_ids")),
                  "dashed": w.get("element") == "soffit_side"}
                 for w in C["walls"] if w["sheet"] == sh and tag_de(w) == t and w.get("band")]
        try:
            hoja.overview(items, f"{sh} type {t}", os.path.join(IMG, f"{sh}_type_{t}.png"))
        except Exception as e:
            fallas += 1
            print("PLANMARK", sh, t, type(e).__name__, str(e)[:300])
print(f"planmark: {fallas} falla(s)")
sys.exit(1 if rech or fallas else 0)
