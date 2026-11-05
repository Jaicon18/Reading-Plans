"""Assembles cfa_final/FINAL_FOR_REVIEW_rev10 from the rev10 chain outputs only (copy, no edit): markups PDF and one PNG per
marked sheet (named <SHEET>_..., auditoria_entrega). The Excel (+ its .sello.json) is written there directly by
plantilla_excel.py armar. Docs are written by scripts/docs_rev10.py. Use: python3 bitacora.py run scripts/armar_entrega_rev10.py"""
import os, shutil, glob
K = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.dirname(K)
F = os.path.join(S, "cfa_final", "FINAL_FOR_REVIEW_rev10")
for d in ("Take-off", "Planos marcados", "proceso"):
    os.makedirs(os.path.join(F, d), exist_ok=True)
for p in glob.glob(os.path.join(F, "Planos marcados", "*")):
    os.remove(p)                                       # only files this script wrote in a previous run of rev10
E = os.path.join(K, "etapas")
cp = lambda a, b: (shutil.copy2(a, b), print("copied", os.path.relpath(b, F)))
cp(os.path.join(E, "6_markups", "markups_rev10.pdf"), os.path.join(F, "Planos marcados", "CFA2284_RiverPoint_Markups_Bluebeam_rev10.pdf"))
for p in sorted(glob.glob(os.path.join(E, "7_imagenes", "*_marked_by_type_rev10.png"))):
    sh = os.path.basename(p).split("_")[0]
    cp(p, os.path.join(F, "Planos marcados", f"{sh}_CFA2284_RiverPoint_marked_by_type_rev10.png"))
for p in glob.glob(os.path.join(F, "Take-off", "*")):
    if not os.path.basename(p).startswith("CFA2284_RiverPoint_Takeoff_FINAL_rev10.xlsx"):
        raise SystemExit(f"unexpected file in Take-off: {p}")
# rev10 RFI sweep evidence + independent schedule reading (cited in Pending Items / RFI_PENDIENTES / fichas.json)
R5 = os.path.join(F, "proceso", "rfi5")
os.makedirs(R5, exist_ok=True)
for p in glob.glob(os.path.join(R5, "*")):
    os.remove(p)
for p in sorted(glob.glob(os.path.join(K, "rfi5", "*.png")) + glob.glob(os.path.join(K, "rfi5", "contextos_*.md"))
                + [os.path.join(K, "rfi5", "terminos.json"), os.path.join(K, "fichas.json"), os.path.join(K, "fichas_lectura", "sched_all.png")]):
    cp(p, os.path.join(R5, os.path.basename(p)))
# rev10 (U-118): the circled images cited by Review Items (proceso/review_img) and by the open RFIs (proceso/rfi_img)
import json
tk = json.load(open(os.path.join(K, "takeoff.json")))
idx = {}
for r_, _, fs in os.walk(E):
    for f in fs:
        if f.lower().endswith(".png"):
            idx.setdefault(f, os.path.join(r_, f))
for sub, refs in (("review_img", [x.get("imagen") for x in tk.get("revisar") or []]),
                  ("rfi_img", [x.get("img") for x in tk.get("rfis") or []])):
    D = os.path.join(F, "proceso", sub)
    os.makedirs(D, exist_ok=True)
    for p in glob.glob(os.path.join(D, "*")):
        os.remove(p)
    for ref in refs:
        n = os.path.basename(str(ref or ""))
        if not n or n not in idx:
            raise SystemExit(f"{sub}: image {ref} not found in etapas/")
        cp(idx[n], os.path.join(D, n))
# rev10: circled crop of every bubble view read (U-113 / U-137) + the readings
B = os.path.join(F, "proceso", "bubbles_img")
os.makedirs(B, exist_ok=True)
for p in glob.glob(os.path.join(B, "*")):
    os.remove(p)
for p in sorted(glob.glob(os.path.join(E, "8_burbujas", "img_rev7", "*.png"))):
    cp(p, os.path.join(B, os.path.basename(p)))
cp(os.path.join(E, "8_burbujas", "ALL.json"), os.path.join(F, "proceso", "BUBBLE_READINGS_rev10.json"))
cp(os.path.join(K, "callouts_no_aplican.json"), os.path.join(F, "proceso", "callouts_not_applicable_rev10.json"))
