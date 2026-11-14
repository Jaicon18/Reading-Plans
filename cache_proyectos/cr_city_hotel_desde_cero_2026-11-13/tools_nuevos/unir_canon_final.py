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
                 "source": (f"C-H METAL/A0.06 (section: '20GA METAL \"C-H\" STUD'; STUD SCHEDULE 'C H STUD 6 6\" 20 28'') | {w['sheet']}" if size == "6" else
                            f"C-H METAL/A0.06 type CH.2 1 ('2-1/2\" 20GA metal C-H stud', type row CH.2 on A0.06) | {w['sheet']}"),
                 "op": f"ROUNDUP({L}/{w['oc_in']/12:.4f})+1 = {n} studs x {H} ft = {round(n*H,2)} LF (20 ga per C-H METAL/A0.06; {w['oc_in']}\" o.c. per A0.06 general note 6 '16\" O.C. UON'; the 24\" o.c. listed-system alternative is a review item)"})
    misc.append({"ref": f"{w['id']} J-runner", "familia": f"J-runner {size}\" (printed)", "qty": round(2 * L, 2), "unit": "LF",
                 "source": f"C-H METAL/A0.06 (head / section: '\"J\" RUNNER CHANNEL') | {w['sheet']}", "op": f"2 (top + bottom) x {L} LF = {round(2*L,2)} LF ({w.get('top_track')})"})
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
# --- RFIs cerrados por el barrido exhaustivo (frag RFIS.json): se aplican sus valores con fuente impresa ---
_rf = os.path.join(etapas, "4_canon/frag/RFIS.json")
if os.path.exists(_rf):
    canon["rfis"] = []                                    # RFIS.json manda sobre los rfis de los fragmentos de lectura
    canon["rfis_cerrados_info"] = json.load(open(_rf)).get("rfis_cerrados_info", [])
    cs = canon.get("ceilings", [])
    # RFI-02: MB-1 (A0.08) = 1" liner + 3 x 5/8 type X on 2-1/2" C-H studs @16" + J-track (A0.06 CH.2, 09 21 16.23 2.6.B/C)
    mb = [x for x in cs if "GYP-2 2-HR rated ceiling" in str(x.get("room"))]
    if mb:
        a = round(sum(float(x["area_sf"]) for x in mb), 1); p = round(sum(float(x.get("perimeter_ft") or 0) for x in mb), 1)
        canon.setdefault("ceilings_misc", []).extend(mb)
        canon["ceilings"] = cs = [x for x in cs if x not in mb]
        canon["misc_items"] += [
          {"ref": "MB-1 1in shaftliner (103/104/116)", "familia": "1\" gypsum shaftliner panel", "qty": a, "unit": "SF", "source": "A0.08 MB-1 '1\" GYP. BD. LINER' | A3.01", "op": f"MB-1 ceiling area 193.2 + 160.8 + 52.2 = {a} SF x 1 layer (RFI-02 closed)"},
          {"ref": "MB-1 C-H studs 2-1/2in @16 (103/104/116)", "familia": "C-H stud 2-1/2\" (printed)", "qty": round(a / (16 / 12), 1), "unit": "LF", "source": "C-H METAL/A0.06 CH.2 | A0.08 MB-1 | 09 21 16.23 2.6.B", "op": f"{a} SF / (16/12) ft o.c. = {round(a / (16 / 12), 1)} LF (RFI-02 closed: stud depth = nearest printed CH depth, vector cavity 3.0-3.2 in)"},
          {"ref": "MB-1 J-runner 2-1/2in perimeter (103/104/116)", "familia": "J-runner 2-1/2\" (printed)", "qty": p, "unit": "LF", "source": "C-H METAL/A0.06 'J RUNNER CHANNEL' | A0.08 MB-1", "op": f"room perimeters = {p} LF (RFI-02 closed)"}]
    # RFI-11: RS-6 'AT LEVEL-4' (A2.05) = 286 SF exterior deck (A0.02) over L3 309 + E part of 308: 2 x 5/8 type X instead of FS-1 type C
    r309 = next((x for x in cs if str(x.get("room")).startswith("L3 309") and "membrane" in str(x.get("room"))), None)
    if r309 and float(r309["area_sf"]) > 286:
        r309["area_sf"] = round(float(r309["area_sf"]) - 286.0, 1)
        r309["source"] = str(r309["source"]) + " | RFI-11 closed: 286 SF under the L4 exterior deck carry RS-6 (separate row)"
        n6 = json.loads(json.dumps(r309)); n6["room"] = "L3 309 / 308 E - RS-6 under L4 exterior deck (2 layers 5/8 type X)"
        n6.update({"area_sf": 286.0, "board": "5/8 type X", "layers": {"value": 2, "source": "A0.08 RS-6 '2 LAYERS 5/8\" TYPE X'"},
                   "assembly": {"id": "RS-6", "source": "A2.05 'RS-6 AT LEVEL-4'; A0.02 'EXTERIOR DECK 286 SF'; A0.08 RS-6"},
                   "source": "A2.05 RS-6 AT LEVEL-4; A0.02 EXTERIOR DECK 286 SF (RFI-11 closed)"})
        n6.pop("rc_end_joints", None); cs.append(n6)
# U-159: Elec 421 (L4, 3/A7.50) sin renglón: closet 7'-8" (impreso, 3/A7.50) x 1.41 ft (vector, inner faces x 1034.8-1060.2 pt / 18 pt/ft)
# = 10.8 SF; mismo sistema que 417 / 418 (RFI-05 cerrado: techo L4 a 8'-11 1/4")
_r418 = next((x for x in canon.get("ceilings", []) if str(x.get("room")).startswith("L4 Men 418")), None)
if _r418 and not any("421" in str(x.get("room")) for x in canon["ceilings"]):
    e421 = json.loads(json.dumps(_r418)); e421.pop("rc_end_joints", None)
    e421.update({"room": "L4 Elec 421 - ceiling at bottom of roof assembly (untagged)", "sheet": "A7.50", "page": 76, "area_sf": 10.8,
                 "perimeter_ft": round(2 * (7.667 + 1.41), 2), "area_status": "DERIVED",
                 "source": "3/A7.50 ELEC 421: 7'-8\" printed x 1.41 ft vector inner faces (25.4 pt / 18 pt/ft) = 10.8 SF; RFI-05 closed (L4 at 8'-11 1/4\", 1/A5.06)",
                 "polygon": [[1034.8, 1137.0], [1060.2, 1137.0], [1060.2, 1275.0], [1034.8, 1275.0]], "hatch_check_cause": "untagged closet on 3/A7.50 (no RCP hatch for L4 enlarged rooms)"})
    canon["ceilings"].append(e421)
# área del cielo = polígono medido en el RCP (rcp_polys.json, el mismo que mide Bluebeam): Excel = markups (U-153 / BE-149);
# el área del back-check queda como area_backcheck_info y la diferencia > 5 % va a review_items
_pp = os.path.join(etapas, "6_markups/rcp_polys.json")
if os.path.exists(_pp):
    _po = {q["room"]: q for q in json.load(open(_pp)) if q.get("kind") == "ceiling"}
    for x in canon.get("ceilings", []):
        q = _po.get(x["room"])
        if q and q.get("area_poly_sf"):
            a0, a1 = float(x["area_sf"]), round(float(q["area_poly_sf"]), 2)
            if abs(a1 - a0) > 0.005:
                x["area_backcheck_info"] = a0; x["area_sf"] = a1; x["area_status"] = "DERIVED"
                x["source"] = f"{x.get('source')} | area = RCP polygon {q['sheet']} {a1} SF (vector, shoelace / scale^2)"
                if isinstance(x.get("rc_end_joints"), dict) and a0:
                    x["rc_end_joints"]["extra_lf"] = round(x["rc_end_joints"]["extra_lf"] * a1 / a0, 1)
                if abs(a1 - a0) / a0 > 0.05:
                    canon.setdefault("review_items_info", []).append({"item": f"ceiling area {x['room']}", "sheet_detail": q["sheet"],
                        "a": f"back-check {a0} SF", "b": f"RCP polygon {a1} SF", "delta": f"{round(a1 - a0, 1)} SF ({round(100 * (a1 - a0) / a0, 1)} %)",
                        "decision": f"loaded the RCP polygon on {q['sheet']} (what Bluebeam measures); verify the enlarged views A7.23 / A7.24 for corridors"})
# U-191 / UL L546 item 6: 2 channels 6" apart at board end joints -> +1 channel per end-joint line (rc_end_joints de cada
# cielo, calculado por el back-check con su operación); canon.py no lo suma -> misc_item de la familia printed, con la suma
_rcx = [(c_["room"], c_["rc_end_joints"]["extra_lf"]) for c_ in canon.get("ceilings", []) if isinstance(c_.get("rc_end_joints"), dict)]
if _rcx:
    canon.setdefault("misc_items", []).append({"ref": "FS-1 resilient channel at board end joints (UL L546 item 6)", "familia": "resilient channel (printed)",
        "qty": round(sum(x for _, x in _rcx), 1), "unit": "LF", "source": "A0.08 FS-1 'L546' | UL L546 item 6 (U-191)",
        "op": f"sum of {len(_rcx)} ceilings: area / 12 ft board length = end-joint lines x 1 extra channel = {round(sum(x for _, x in _rcx), 1)} LF"})
# R80f.16: cielo sin hatch en el RCP general = causa impresa (membrana rated apilada sobre ACT / GYP-1 no se dibuja con hatch;
# cielos L1 sin tag con su sección; toilets 112/113 con el tag en el pasillo 2/A7.50)
CAUSA_HATCH = [(r"FS-1 above|rated membrane", "stacked rated membrane FS-1 above the hung ceiling: A0.08 FS-1 'LEVEL 2,3,4 THROUGHOUT' / A7.00 GN 1 - drawn on sections (A5.0x), never hatched on the RCP"),
               (r"Bar 107", "untagged on A3.01 / A7.31: extent from sections 3/A5.04, 5/A5.04 'SUSPENDED GYP CEILING' (RFI-07 closed)"),
               (r"Toilet 11[23]", "GYP-1 9'-0\" tag printed in the passage between the toilets on 2/A7.50 (no hatch on A3.01)"),
               (r"Lobby", "lobby GYP-1 field / coffers drawn on 2/A7.31 and 5/A7.31, not hatched on A3.01")]
for c_ in canon.get("ceilings", []):
    if str(c_.get("level") or c_.get("room", "")[:2]) == "L1" or str(c_.get("room", "")).startswith("L1"):
        for rx, why in CAUSA_HATCH:
            if _re.search(rx, str(c_.get("room"))):
                c_.setdefault("hatch_check_cause", why); break
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
