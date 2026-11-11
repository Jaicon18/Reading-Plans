"""Closes every 'pendiente' row of registro.json with `registro.py marcar` (through bitacora.py run), Xfinity - Interquest:
 - ALC-01..24: from the Scope Checklist notes of takeoff.json (ALC-19 'EXCLUDED: ...', estimator standing order);
 - walls: closer seal (etapas/4_canon/out/cierres_resumen.json) + markup /NM + detail;
 - other canon elements (door 101, SOF-01, DEMO, braces, blocking, trims): canon source + operation + markup / Excel row;
 - RCP rooms: the EXCLUDED markup on A3.0 with its printed reason (rcp_cuartos.json).
Never edits registro.json by hand.  Use: python3 bitacora.py run scripts/registro_marcar.py <tools_dir>"""
import json, os, subprocess, sys
K = os.environ.get("K") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = sys.argv[1]
td = json.load(open(os.path.join(K, "takeoff.json")))
reg = json.load(open(os.path.join(K, "registro.json")))
c = json.load(open(os.path.join(K, "etapas/4_canon/takeoff_canon.json")))
sel = {s["wall"]: s["sello"] for s in json.load(open(os.path.join(K, "etapas/4_canon/out/cierres_resumen.json")))["sellados"]}
cu = {f"RCP-{r['sheet']}-{r['room'].replace(' ', '_')}": r for r in json.load(open(os.path.join(K, "etapas/6_markups/rcp_cuartos.json")))["rooms"]}
X = "XF_Takeoff_FINAL_" + os.environ.get("REV", "rev1") + ".xlsx"
nota = {}
for a in td["alcances"]:
    if a["id"].startswith("ALC-E"):
        continue
    if a["id"] == "ALC-19":
        nota[a["id"]] = "EXCLUDED: acoustical sealant excluded in all projects (estimator standing order); " + a["nota"]
    elif a["estado"] == "NO APLICA":
        nota[a["id"]] = "NO APLICA: " + a["nota"]
    else:
        nota[a["id"]] = "CUANTIFICADO: " + a["nota"]
for w in c["walls"]:
    if w["id"] in sel:
        nota[w["id"]] = (f"CUANTIFICADO: closer seal {sel[w['id']]} (etapas/4_canon/out/cierres/{w['id']}.json); {w['length_ft']} LF x "
                         f"{w['height_ft']} ft, {w.get('detail')}; markup TO-{w['id']} on {w['sheet']}; Partition Takeoff row {w['id']} ({X})")
for o in c["opening_schedule"]["items"]:
    nota[o["ref"]] = f"CUANTIFICADO: {o['ref']} R.O. {o['ro_w_ft']} ft in {o['wall']}, head per 7/A2.0 (header row of {X}); {o['ro_status']}"
sh = c["soffit_header_info"]
nota[sh["ref"]] = (f"CUANTIFICADO: SOF-01-TRACK / STUDS / BOARD + CB-SOF-01 (canon misc_items, RFI-02 closed); {sh['area_op']}; "
                   f"markup TO-SOF-01-BOARD on A3.0; image {os.path.basename(sh['img'])}")
for m in c["misc_items"]:
    if m["ref"].startswith(("DEMO", "BRACE")):
        nota[m["ref"]] = f"CUANTIFICADO: {m['op']} ({m['source']}); Material Summary of {X}" + (
            f"; markup DEMO-{m['ref']} on A1.0" if m["ref"].startswith("DEMO") else "")
for b in c["blocking_items"]:
    nota[b["ref"]] = f"CUANTIFICADO: {b['op']} = {b['lf']} LF ({b['source']}); Material Summary of {X}"
for t in c["trim_items"]:
    nota[t["ref"]] = f"CUANTIFICADO: {t['op']} = {t['lf']} LF ({t['source']}); Material Summary of {X}"
for k, r in cu.items():
    nota[k] = f"NO APLICA: EXCLUDED - {r['reason']} ({r['nhoja']}); grey outline + red text EXCLUDED markup on {r['sheet']}"
rc = 0
for r in reg["renglones"]:
    if r["estado"] != "pendiente":
        continue
    if r["id"] not in nota:
        print(r["id"], "NO EVIDENCE - left pending")
        rc = 1
        continue
    p = subprocess.run([sys.executable, os.path.join(T, "bitacora.py"), "run", os.path.join(T, "registro.py"), "marcar",
                        os.path.join(K, "registro.json"), r["id"], "verificado", nota[r["id"]]], cwd=K, capture_output=True, text=True)
    print(r["id"], p.returncode, ((p.stdout + p.stderr).strip().splitlines() or [""])[0][:120])
    rc |= p.returncode
sys.exit(rc)
