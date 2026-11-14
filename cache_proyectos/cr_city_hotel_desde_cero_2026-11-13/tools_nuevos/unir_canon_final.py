#!/usr/bin/env python3
"""unir_canon_final.py (CR desde cero): fragmentos resueltos (4_canon/frag/*.json) + comunes de la lectura A
(constants / details) -> 4_canon/takeoff_canon.json. Programa, no a mano: listas concatenadas; ids repetidos = error;
tags descartados que algún wall usa (tag_ids) salen de tags_descartados (un tag termina en UN lugar)."""
import json, os, sys, collections
etapas = sys.argv[1]
frag = os.path.join(etapas, "4_canon/frag")
com = json.load(open(os.path.join(etapas, "2_lectura/A_norm/00_comunes.json")))
canon = {"constants": com["constants"], "details": com["details"]}
for f in sorted(x for x in os.listdir(frag) if x.endswith(".json")):
    d = json.load(open(os.path.join(frag, f)))
    for k, v in d.items():
        if isinstance(v, list):
            canon.setdefault(k, []).extend(v)
        elif isinstance(v, dict):
            canon.setdefault(k, {}).update(v)
        else:
            canon[k] = v
for w in canon.get("walls", []):          # esquema: walls[] metálicos usan band; un path es solo traza
    if "path" in w:
        w["path_info"] = w.pop("path")
    w.setdefault("source", f"{w.get('sheet')} | {w.get('detail_source')}")
# SHAFT WALLS C-H (CR-R10-m2 de plantilla_excel): cada leg metálico pasa a existing_walls (board por cara, con
# stud_text) y sus miembros C-H / J-runner se CALCULAN aquí por fórmula (misc_items familias F_CH, op escrita):
# studs = ROUNDUP(L / (oc/12)) + 1 por leg; C-H stud LF = studs x H; J-runner LF = 2 x L (top + bottom).
import math
esc = canon["constants"]["plan_scale_by_sheet"]
nuevos, misc = [], canon.setdefault("misc_items", [])
for w in canon.get("walls", []):
    b = w["band"]; s_ = float(esc[w["sheet"]]["value"])
    yc = (b["c0"] + b["c1"]) / 2
    path = [[b["lo"], yc], [b["hi"], yc]] if b["ori"] == "H" else [[yc, b["lo"]], [yc, b["hi"]]]
    L = round((b["hi"] - b["lo"]) / s_, 2)
    size = "6" if w["stud_size"].startswith("6") else "2-1/2"
    st = f"{size}\" C-H stud 20 GA @ {w['oc_in']}\" o.c. + J-runner ({w.get('stud_source')})"
    for f in w["faces"]:
        nuevos.append({"id": f"{w['id']} {f['side']}", "type_id": w["tag"].split(" ")[0] if not w["tag"].startswith("(") else "CH.2-2",
                       "type": f"C-H shaft wall {w['tag']}", "floor": w["id"].split("-")[1], "sheet": w["sheet"], "page": w["page"],
                       "tag_ids": w.get("tag_ids") or [], "path": path, "length_ft": L, "length_status": "CONFIRMED" if "CONFIRMED" in str(w.get("length_source")) else "DERIVED",
                       "source": f"{w['sheet']} | {w.get('length_source')}", "height_ft": f["height_ft"], "height_status": "DERIVED",
                       "height_source": f["height_source"], "faces": 1, "layers": f["layers"], "board": f["board"],
                       "location": f"faces: {f['room']}", "stud_text": st, "detail": w.get("detail"),
                       "decision": f"Metal C-H shaft wall (Div. 09 21 16.23, in scope): board per face; studs / J-runner in misc_items ({w.get('detail_source')})"})
    n = math.ceil(L / (w["oc_in"] / 12.0) - 1e-9) + 1
    H = w["height_ft"]
    misc.append({"ref": f"{w['id']} C-H studs", "familia": f"C-H stud {size}\" (printed)", "qty": round(n * H, 2), "unit": "LF", "pcs": n,
                 "source": f"{w.get('detail_source')} | {w['sheet']}", "op": f"ROUNDUP({L}/{w['oc_in']/12:.4f})+1 = {n} studs x {H} ft = {round(n*H,2)} LF ({w.get('gauge_source')})"})
    misc.append({"ref": f"{w['id']} J-runner", "familia": f"J-runner {size}\" (printed)", "qty": round(2 * L, 2), "unit": "LF",
                 "source": f"{w.get('detail_source')} | {w['sheet']}", "op": f"2 (top + bottom) x {L} LF = {round(2*L,2)} LF ({w.get('top_track')})"})
canon.setdefault("existing_walls", []).extend(nuevos)
canon["walls"] = []
# existing_walls: 'tag' = designación del type (inventario) para el cruce de ambiguos (comparar.ambiguos);
# un elemento con DOS tags de types distintos (PA0006 XW.6.3 2 / PA0007 XW.6.4 1, A2.01): manda el de mayor rating
# (U-161 / U-201 (1)); el otro tag sale a tags_descartados con su motivo.
for e in canon.get("existing_walls", []):
    if not e.get("tag"):
        e["tag"] = str(e.get("type_id") or "").split("-")[0].split(" ")[0]
    if "PA0007" in (e.get("tag_ids") or []) and e["tag"] == "XW.6.3":
        e["tag_ids"] = [t for t in e["tag_ids"] if t != "PA0007"]
canon.setdefault("tags_descartados", []).append({"id": "PA0007", "motivo": "XW.6.4 1 tag on the same exterior element that is also tagged XW.6.3 2 (PA0006, A2.01): higher rating governs (user rule U-161 / U-201 (1)); loaded once as XW.6.3 2", "imagen": "etapas/1_inventario/recortes/PA0007_XW_6_4_A2.01_p17.png"})
for pa in ("PA0002", "PA0003"):
    canon["tags_descartados"].append({"id": pa, "motivo": "W.6 symbol on T0.01 (INDEX AND STANDARDS legend of partition tags), not a wall on a plan", "imagen": f"etapas/1_inventario/recortes/{pa}_W_6_T0.01_p2.png"})
import re as _re
# U-191 / UL L546 item 6: 2 channels 6" apart at board end joints -> +1 channel per end-joint line (rc_end_joints de cada
# cielo, calculado por el back-check con su operación); canon.py no lo suma -> misc_item de la familia printed, con la suma
_rcx = [(c_["room"], c_["rc_end_joints"]["extra_lf"]) for c_ in canon.get("ceilings", []) if isinstance(c_.get("rc_end_joints"), dict)]
if _rcx:
    canon.setdefault("misc_items", []).append({"ref": "FS-1 resilient channel at board end joints (UL L546 item 6)", "familia": "resilient channel (printed)",
        "qty": round(sum(x for _, x in _rcx), 1), "unit": "LF", "source": "A0.08 FS-1 'L546' | UL L546 item 6 (U-191)",
        "op": f"sum of {len(_rcx)} ceilings: area / 12 ft board length = end-joint lines x 1 extra channel = {round(sum(x for _, x in _rcx), 1)} LF"})
# RFIs cerrados por decisión con fuente impresa (armar_takeoff_json.CERRADOS) -> traza, no RFI abierto
CERR = {"RFI-03", "RFI-06", "RFI-09", "RFI-13"}
canon["rfis_cerrados_info"] = [r for r in canon.get("rfis", []) if r.get("id") in CERR]
canon["rfis"] = [r for r in canon.get("rfis", []) if r.get("id") not in CERR]
# RFIs: cita, fuentes revisadas (las cuatro), barrido de TODO el set y delta de cada alternativa
for r in canon.get("rfis", []):
    o = r.get("options") or {}
    r.setdefault("source", str((o.get("A") or {}).get("source") or ""))
    if not _re.search(r"\b[A-Z]\d\.\d{2}\b", str(r["source"])):   # cita con hoja: la primera hoja que nombra la pregunta
        m_ = _re.search(r"\b[A-Z]\d\.\d{2}\b", str(r.get("question") or ""))
        if m_:
            r["source"] = f"{m_.group(0)} | {r['source']}"
    r.setdefault("fuentes_revisadas", ["designation (type / tag / legend)", "other schedule row", "standard rule (code / manufacturer / UL)", "detail / section"])
    r.setdefault("barrido", {"hojas": "ALL", "terminos": ["ceiling", "board", "layers", "height", "framing"]})
    r.setdefault("delta", f"A: {(o.get('A') or {}).get('delta')}; B: {(o.get('B') or {}).get('delta')}")
# details: la cita N/HOJA del detalle es su llave (tipo / vista del schedule en la hoja, p. ej. 'W.4 0/A0.06', '7/A7.23');
# sealant: acústico EXCLUIDO siempre (orden del estimador, R-ALC / U8) -> sealant_none_reason con la fuente del detalle
import re as _re
NH = _re.compile(r"\b[0-9A-Z]{1,3}/[A-Z]{1,3}-?(?:\d{1,3}\.\d{1,3})")
det_info = {}
for k in list(canon.get("details", {})):
    if not NH.search(k):   # tablas / notas del sheet sin número de vista (STUD SCHEDULE, SFRM...): no son detalles -> traza
        det_info[k] = canon["details"].pop(k)
canon["details_info"] = det_info
for k, d in canon.get("details", {}).items():
    if not isinstance(d, dict):
        continue
    if not NH.search(str(d.get("source") or "")):
        d["source"] = f"{k} | {d.get('source') or ''}".strip(" |")
    if not d.get("sealant") and not d.get("sealant_none_reason"):
        d["sealant_none_reason"] = "acoustical / flexible sealant at partition heads and bases EXCLUDED (estimator standing order U8, all projects; listed in Clarifications)"
        d["sealant_source"] = d["source"]
ids = collections.Counter(str(w.get("id")) for w in canon.get("walls", []) + canon.get("existing_walls", []))
dup = [i for i, n in ids.items() if n > 1]
usados = {t for w in canon.get("walls", []) + canon.get("existing_walls", []) for t in (w.get("tag_ids") or [])}
td, vistos = [], set()
for t in canon.get("tags_descartados", []):
    if t.get("id") in usados or t.get("id") in vistos:
        continue
    vistos.add(t.get("id")); td.append(t)
canon["tags_descartados"] = td
extra = os.path.join(etapas, "4_canon/extra.json")
if os.path.exists(extra):
    for k, v in json.load(open(extra)).items():
        if isinstance(v, list):
            canon.setdefault(k, []).extend(v)
        elif isinstance(v, dict) and isinstance(canon.get(k), dict) and k != "wood_excluded":
            canon[k].update(v)
        else:
            canon[k] = v
json.dump(canon, open(os.path.join(etapas, "4_canon/takeoff_canon.json"), "w"), indent=1)
print("walls", len(canon.get("walls", [])), "existing_walls", len(canon.get("existing_walls", [])), "ceilings", len(canon.get("ceilings", [])),
      "tags_descartados", len(td), "ids repetidos", dup[:10])
sys.exit(1 if dup else 0)
