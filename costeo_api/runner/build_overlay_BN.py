#!/usr/bin/env python3
"""build_overlay_BN.py — arma decisiones_BN.json (34 RFI + PVC/FRP, decisiones del estimador 2026-10-27 / 28)
desde el canon y el takeoff.json finales de B&N (rev13). Se corre una vez; el runner solo lee el JSON."""
import json
import sys

K = sys.argv[1] if len(sys.argv) > 1 else "cache_proyectos/barnes_noble/takeoff_work"
c = json.load(open(K + "/etapas/4_canon/takeoff_canon.json"))
t = json.load(open(K + "/takeoff.json"))
MISC = ["FRP-TYPES-3-4", "FRP-1-CAFE-WORKROOM", "FRP-1-JANITOR", "FRP-1-CAFE-BELOW-COUNTER", "CLOUD-FASCIA-GWB",
        "CONTROL-JOINTS-T2", "MOMENT-CLIPS-T3-T4", "HUS-EZ-T3-T4", "SCREWS-10-16-MOMENT-CLIPS", "CORNER-GUARDS-METAL-72",
        "CORNER-GUARD-STAINLESS-48", "SCREWS-8-BRACE-ENDS"]
STRIPS = ["TYPE-3-A-FRT", "TYPE-4-A-FRT", "C-H3a-A-FRT"]
mi = {m["ref"]: m for m in c["misc_items"]}
st = {s["ref"]: s for s in c["plywood_strips"]}
walls = [w for w in c["walls"] if w.get("tag") in ("3", "4") or w["id"] in ("C-E1-S", "C-E1-P.2", "C-E1-B", "C-H3a")]
ov = {
    "project": "Barnes & Noble - Colorado Springs (3173 Cinema Point)",
    "decision_date": "2026-10-27 / 2026-10-28",
    "source": "cache_proyectos/barnes_noble/RFI_REVISION_ESTIMADOR.json (34 RFI) + rev12_pvc_trim/RFI_PVC.md (PVC / FRP)",
    "canon": {
        "constants": {k: c["constants"][k] for k in ("slab_pin_spacing_ft", "addl_head_track_min_ro_ft", "addl_head_track_pieces")},
        "top": {k: c[k] for k in ("mep_estimator_count", "pvc_trim_items", "acc_nombres", "frp_none_reason", "markup_label")},
        "upsert": {"misc_items": [mi[r] for r in MISC], "plywood_strips": [st[r] for r in STRIPS]},
        "remove": {"plywood_strips": ["SERVER-ROOM-BACKBOARD"], "blocking_items": ["BLK-CASED-OPENING"]},
        "walls": [{"id": w["id"], "faces": w["faces"]} for w in walls],
    },
    "takeoff": {
        "rfi_cierre": t["rfi_cierre"],
        "inputs_notas": {"slab_pin_spacing_ft": t["inputs_notas"]["slab_pin_spacing_ft"]},
        "alcances": {a["id"]: {"estado": a["estado"], "nota": a["nota"]} for a in t["alcances"]
                     if a["id"] in ("ALC-10", "ALC-16", "ALC-17", "ALC-18", "ALC-20")},
    },
}
json.dump(ov, open(sys.argv[2] if len(sys.argv) > 2 else "costeo_api/runner/decisiones_BN.json", "w"), indent=1, ensure_ascii=False)
print("decisiones_BN.json:", len(MISC), "misc,", len(STRIPS), "strips,", len(walls), "walls,", len(t["rfi_cierre"]), "RFI cerrados")
