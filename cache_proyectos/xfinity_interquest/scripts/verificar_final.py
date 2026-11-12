"""markups_bluebeam.verificar on a markups PDF that already carries the RCP markups of markups_rcp.py, + U-167 /NM check.

Tool limit (etapas/TOOL_LIMITS_CALC.md): markups_rcp.py names the markup of a quantified misc soffit / ceiling 'TO-<id>' (here
TO-SOF-01-BOARD, the SOF-01 gyp header of the canon misc_items), and markups_bluebeam.verificar reads EVERY 'TO-' annot as a wall
-> 'annot TO-SOF-01-BOARD: wall que no está en el canon'. That one message is accepted ONLY for ids that are (a) a misc entry of
etapas/6_markups/rcp_polys.json and (b) a quantified canon misc_items row; every other failure of verificar stays a failure.
Also: markups_bluebeam.nm_fallas (unique /NM without '/' or '\\', U-167) and no /Sig field.
Use: python3 bitacora.py run scripts/verificar_final.py <tools_dir> <markups.pdf>"""
import json, os, re, sys
sys.path.insert(0, sys.argv[1])
import markups_bluebeam as mb
import pymupdf as fitz
K = os.environ.get("K") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pdf = sys.argv[2]
canon = os.path.join(K, "etapas/4_canon/takeoff_canon.json")
c = json.load(open(canon))
misc_q = {re.sub(r" board$", "", m["ref"]) for m in c.get("misc_items") or [] if float(m.get("qty") or 0) > 0}   # rev1c: 'SOF-01 board' -> TO-SOF-01
rcp = {e["id"] for e in json.load(open(os.path.join(K, "etapas/6_markups/rcp_polys.json"))) if e.get("misc")}
ok_ids = misc_q & rcp
det = {}
f = mb.verificar(pdf, canon, detalle=det)
acept = [x for x in f if (m := re.match(r"annot TO-(.+): wall que no está en el canon$", x)) and m.group(1) in ok_ids]
fallas = [x for x in f if x not in acept]
fallas += mb.nm_fallas(pdf)
d = fitz.open(pdf)
sig = [i + 1 for i in range(d.page_count) for w in (d[i].widgets() or []) if w.field_type == fitz.PDF_WIDGET_TYPE_SIGNATURE]
if sig:
    fallas.append(f"signature fields on pages {sig}")
print(f"wall markups: {det.get('annots')} annots, {det.get('con_geometria')} walls with geometry; "
      f"RCP misc markups accepted: {sorted(ok_ids)}; /NM unique without '/': {'yes' if not mb.nm_fallas(pdf) else 'NO'}")
for x in fallas:
    print("FAIL", x)
print("MARKUPS OK" if not fallas else f"MARKUPS NOT OK: {len(fallas)}")
sys.exit(1 if fallas else 0)
