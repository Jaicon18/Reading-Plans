#!/usr/bin/env python3
"""build_overlay_BN.py — arma decisiones_BN.json con TODAS las decisiones del estimador de B&N, en 4 grupos.

Cómo: el script del proyecto (build_A.py) se corre con salida redirigida y con los bloques de plan check / auditoría
encendidos (REV5–REV10: no son decisiones del estimador). Los bloques de decisiones se encienden por grupos:
  base = sin decisiones;  S1 = + REV1, REV2;  S2 = + REV3, REV4;  S3 = + REV12;  S4 = + REV13 (= canon final rev13).
Cada grupo del overlay es overlay.diff(S_i, S_i+1): ops genéricas por ref / id (alta, reemplazo, baja, orden),
constants y claves de primer nivel. El takeoff.json (textos CLOSED / Scope / notas de Inputs) va en el último grupo.

Uso: build_overlay_BN.py <dir con canon_base.json, canon_S1..S4.json> <takeoff.json final> <salida decisiones_BN.json>"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import overlay  # noqa: E402

d, tk, out = sys.argv[1:4]
cs = [json.load(open(os.path.join(d, f"canon_{n}.json"))) for n in ("base", "S1", "S2", "S3", "S4")]
t = json.load(open(tk))
G = [("2026-10-24", "RFI-01 perimeter walls EXISTING / excluded; RFI-23 FRT blocking by rows; RFI-11 W.R. on all wet-room faces; "
      "RFI-27 Type X; rev1 questions: GWB ceilings Type X, restroom backing 16\"", "DECISIONES_ESTIMADOR.md (rev1 / rev2)"),
     ("2026-10-25 / 26", "Review Items RI 1-11 (W2-05 12.92, type 4 caps, curved walls 25.68, C25 x 9, door pier, board = ceiling + 6\", "
      "diagonal braces, Cafe studs to deck, WD-1 15'-0\", USG cloud, vestibule box) + RFI-14 / 16 / 17", "DECISIONES_ESTIMADOR.md (rev3 / rev4)"),
     ("2026-10-27", "34 RFI decisions (slab pins 1 row, MEP count, 2-piece door headers, FRP-1, fascia, types 3/4 one face, control joints, "
      "moment clips, corner guards, E1 12'-0\", H3a, cased opening 0, server room excluded, brace screws)", "RFI_REVISION_ESTIMADOR.json"),
     ("2026-10-28", "PVC trim per real corners / edges + division bars; Work Room FRP finished dimensions; FRP-1 below Cafe countertop",
      "rev12_pvc_trim/RFI_PVC.md")]
groups = []
for i, (fecha, que, fuente) in enumerate(G):
    groups.append({"label": f"G{i + 1}", "decision_date": fecha, "decisions": que, "source": fuente,
                   "canon": overlay.diff(cs[i], cs[i + 1])})
groups[-1]["takeoff"] = {"rfi_cierre": t.get("rfi_cierre") or {}, "inputs_notas": t.get("inputs_notas") or {},
                         "alcances": {a["id"]: {"estado": a["estado"], "nota": a["nota"]} for a in t.get("alcances") or []}}
ov = {"project": "Barnes & Noble - Colorado Springs (3173 Cinema Point)", "groups": groups}
assert overlay.aplicar_canon(cs[0], ov) == cs[4], "el overlay no reproduce el canon final"
json.dump(ov, open(out, "w"), indent=1, ensure_ascii=False)
print("decisiones_BN.json:", len(groups), "grupos; base -> final exacto")
