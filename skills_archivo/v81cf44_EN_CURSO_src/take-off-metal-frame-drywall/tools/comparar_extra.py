#!/usr/bin/env python3
"""comparar_extra.py — v81cf (CFA #2284): comparar.py solo compara walls[]; esto compara A vs B en lo demás:
existing_walls[] (board only) por tag del inventario y por board, ceilings[], misc_items por familia y demo por keynote.
Uso: python3 comparar_extra.py canon_A.json canon_B.json inventario.json <out_dir>  -> revision_extra.md / .json
Un tag del inventario que está en tag_ids de existing_walls[] NO es "tag sin wall" (cierra la alerta de comparar.py)."""
import json, sys, os, re, collections

def sf(e):
    return float(e.get("length_ft") or 0) * float(e.get("height_ft") or 0) * int(e.get("faces") or 1) * int(e.get("layers") or 1)

def por_tag(c):
    d = collections.defaultdict(list)
    for e in c.get("existing_walls") or []:
        for t in e.get("tag_ids") or ["(no tag) " + str(e.get("id"))]:
            d[t].append(e)
    return d

def tot_board(c):
    d = collections.Counter()
    for e in c.get("existing_walls") or []:
        d["board-only " + str(e.get("board"))] += sf(e)
    for x in c.get("ceilings") or []:
        d["ceiling " + str(x.get("board") or x.get("system"))] += float(x.get("area_sf") or 0)
    return d

def misc(c):
    d = collections.Counter()
    for m in c.get("misc_items") or []:
        d[str(m.get("familia"))] += float(m.get("qty") or 0)
    return d

def main(a, b, inv, out):
    A, B, I = (json.load(open(x)) for x in (a, b, inv))
    os.makedirs(out, exist_ok=True)
    tags = [t["id"] for t in I["ocurrencias"]["partition_tag"]]
    ta, tb = por_tag(A), por_tag(B)
    filas, items = [], []
    for t in tags:
        ea, eb = ta.get(t, []), tb.get(t, [])
        if not ea and not eb:
            continue
        sa, sb_ = round(sum(sf(e) for e in ea), 1), round(sum(sf(e) for e in eb), 1)
        la = round(max([float(e.get("length_ft") or 0) for e in ea] or [0]), 2)
        lb = round(max([float(e.get("length_ft") or 0) for e in eb] or [0]), 2)
        ok = abs(sa - sb_) <= max(1.0, 0.02 * max(sa, sb_)) and abs(la - lb) <= max(0.1, 0.02 * max(la, lb))
        r = {"tag": t, "A_ids": [e["id"] for e in ea], "B_ids": [e["id"] for e in eb], "A_LF": la, "B_LF": lb, "A_SF": sa, "B_SF": sb_,
             "A": [(e["id"], e.get("board"), e.get("length_ft"), e.get("height_ft"), e.get("faces")) for e in ea],
             "B": [(e["id"], e.get("board"), e.get("length_ft"), e.get("height_ft"), e.get("faces")) for e in eb], "coincide": ok}
        filas.append(r)
        if not ok:
            items.append(r)
    sin = [t for t in tags if t not in ta and t not in tb]
    tba, tbb, ma, mb = tot_board(A), tot_board(B), misc(A), misc(B)
    res = {"por_tag": filas, "diferencias_tag": items,
           "board_totales": {k: [round(tba.get(k, 0), 1), round(tbb.get(k, 0), 1)] for k in sorted(set(tba) | set(tbb))},
           "misc_totales": {k: [round(ma.get(k, 0), 1), round(mb.get(k, 0), 1)] for k in sorted(set(ma) | set(mb))},
           "untagged_A": [e["id"] for e in A.get("existing_walls") or [] if not e.get("tag_ids")],
           "untagged_B": [e["id"] for e in B.get("existing_walls") or [] if not e.get("tag_ids")],
           "tags_sin_nada": sin}
    json.dump(res, open(os.path.join(out, "revision_extra.json"), "w"), indent=1)
    L = ["# Double reading — board-only, ceilings, misc / demo (comparar_extra.py)", "",
         f"Tags in board-only entries: {len(filas)} · match {len(filas) - len(items)} · differ {len(items)} · tags with nothing in A nor B: {sin}", "",
         "## Totals A vs B", ""] + [f"- {k}: A {v[0]} · B {v[1]}" for k, v in res["board_totales"].items()] + [""] + \
        [f"- misc {k}: A {v[0]} · B {v[1]}" for k, v in res["misc_totales"].items()] + ["", "## Tag differences", ""] + \
        [f"- {r['tag']}: A {r['A_LF']} LF / {r['A_SF']} SF {r['A_ids']} vs B {r['B_LF']} LF / {r['B_SF']} SF {r['B_ids']}" for r in items] + \
        ["", f"Untagged board-only entries: A {len(res['untagged_A'])} · B {len(res['untagged_B'])}"]
    open(os.path.join(out, "revision_extra.md"), "w").write("\n".join(L) + "\n")
    print(f"tags {len(filas)} · difieren {len(items)} · sin nada {len(sin)}")

if __name__ == "__main__":
    main(*sys.argv[1:5])
