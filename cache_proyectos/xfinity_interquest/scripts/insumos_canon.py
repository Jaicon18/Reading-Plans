"""Inputs of framed_openings.py and alcance_filtro.py written FROM the canon / canon.py outputs (no quantity typed here).
  fo    -> etapas/4_canon/fo_in.json: the closed list of framed-opening items of our GWB surfaces = canon access_panels /
           framed_openings_items (none in this set: A2.0 access panels are in ACT; ducts EXCLUDED by standing order),
           wall stud-bay module, and the M / E sweep (canon mep_sweep sheets + E sheets of the set) when a GWB ceiling exists.
  alcance -> etapas/4_canon/alcance_in.json: one row per furring-like member (walls of the vertical-furring family
           from out/studs_out.json, misc_items whose family / description says furring / hat channel / channel), with
           substrate_of = drywall + its N/SHEET (the wall type detail) so alcance_filtro.py classifies it by rule.
Use: python3 bitacora.py run scripts/insumos_canon.py fo|alcance"""
import json, os, re, sys
K = os.environ.get("K") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C4 = os.path.join(K, "etapas", "4_canon")
c = json.load(open(os.path.join(C4, "takeoff_canon.json")))
sm = json.load(open(os.path.join(K, "etapas", "SHEET_MAP.json")))
modo = sys.argv[1]
if modo == "fo":
    items = list(c.get("framed_openings_items") or [])
    for ap in c.get("access_panels") or []:
        items.append(ap)
    fo = {"modules": {"wall_stud_bay_in": 14.375}, "items": items,
          "source_info": "canon access_panels / framed_openings_items; ducts / air devices EXCLUDED (estimator standing order)"}
    if not items:
        an = next((x for x in c.get("accesorios_none") or [] if x.get("familia") == "access panel"), {})
        fo["items_none_reason"] = ("no framed opening in our GWB surfaces: " + (an.get("why") or "no access panel printed in gypsum")
                                   + f" ({an.get('source') or 'A2.0'}); ducts / air devices crossing walls EXCLUDED by estimator standing order "
                                   f"(M / P sheets {', '.join((c.get('mep_sweep') or {}).get('sheets') or [])})")
    if c.get("ceilings"):
        ms = list((c.get("mep_sweep") or {}).get("sheets") or [])
        es = [v for v in sm.values() if v.startswith("E")]
        fo["sweep"] = {"sheets": sorted(set(ms) | set(es)),
                       "no_air_devices_why": "air devices / duct openings in GWB are EXCLUDED by estimator standing order (no framed opening)"}
        fo["modules"]["ceiling_furring_oc_in"] = {"value": 16, "source": (c["ceilings"][0].get("source") or "A2.0")}
    json.dump(fo, open(os.path.join(C4, "fo_in.json"), "w"), indent=1, ensure_ascii=False)
    print("fo_in items", len(items), "sweep" if "sweep" in fo else "no GWB ceiling: no sweep needed")
else:
    so = json.load(open(os.path.join(C4, "out", "studs_out.json")))
    W = {w["id"]: w for w in c.get("walls") or []}
    rows = []
    for s in so["walls"]:
        sz = str(s.get("stud_size") or "")
        if re.search(r"hat channel|furring|\bzf\b", sz, re.I):
            w = W.get(s["id"], {})
            det = w.get("detail") or w.get("source") or "A2.0"
            rows.append({"id": s["id"], "family": "vertical furring (wall type " + str(w.get("tag") or "") + ")",
                         "description": f"{sz} - {w.get('stud_source') or ''}"[:300], "qty": s["lf"], "unit": "LF",
                         "source": det, "substrate_of": "drywall",
                         "substrate_source": f"{det} (gypsum board fastened to the furring over the existing back-up surface)"})
    for m in c.get("misc_items") or []:
        t = f"{m.get('familia')} {m.get('op')}"
        if re.search(r"hat channel|furring|girt|lath", t, re.I):
            rows.append({"id": m["ref"], "family": m["familia"], "description": str(m.get("op"))[:300], "qty": m["qty"],
                         "unit": m.get("unit", "LF"), "source": str(m["source"]).split(" ")[0],
                         "substrate_of": "drywall", "substrate_source": str(m["source"]).split(" ")[0]})
    json.dump({"rows": rows, **({} if rows else {"rows_none_reason": "no furring-like member in the set: the column furring of 5/A2.0 is 2 1/2\" metal studs (column_wrap CF-01 / CF-02, framing family), no hat / Z-furring / furring channel on walls (2/A2.0, 5/A2.0); no gypsum board ceiling system (A3.0)"})}, open(os.path.join(C4, "alcance_in.json"), "w"), indent=1, ensure_ascii=False)
    print("alcance_in rows", len(rows))
