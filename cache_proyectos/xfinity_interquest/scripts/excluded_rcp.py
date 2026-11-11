"""U-159 / U-160 EXCLUDED markups on the RCP for every room of etapas/6_markups/rcp_cuartos.json (disposition 'exclusion'):
grey hatched polygon of the room outline WITHOUT /Measure + red FreeText 'EXCLUDED - <printed reason> (<N/SHEET>)' INSIDE the room,
Subject EXCLUDED, no callout line (/CL), unique /NM without '/' (U-167, markups_bluebeam.nm_unicos).

Why this script and not `markups_rcp.py excluded` directly (tool limit, see etapas/TOOL_LIMITS_CALC.md): markups_rcp.aplicar works in
UNROTATED page space (polygon points not derotated, text blocks unrotated, FreeText with rotate 0). Every page of this set has
/Rotate 270, so the tool would put the polygon on the wrong place and write the text sideways. Here the same tool helpers are used
(markups_rcp.texto / caja_interior / _ajustar / frac_dentro, markups_bluebeam.nm_unicos / editable) but the geometry is computed in
the VISIBLE frame (rcp_cuartos polygons, page text blocks * rotation_matrix) and written with derotation_matrix, FreeText rotate =
page rotation. Both the gate (CE_RCP_CUARTOS) and Bluebeam read annot rect and vertices in the same PDF space, so >= 90 % of the text
box inside the polygon is preserved by the (orthogonal) rotation; it is re-checked here.
Use: python3 bitacora.py run scripts/excluded_rcp.py <tools_dir> <markups_in.pdf> <markups_out.pdf>"""
import json, os, sys, tempfile
sys.path.insert(0, sys.argv[1])
import pymupdf as fitz
import markups_rcp as MR
import markups_bluebeam as mb
K = os.environ.get("K") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pin, pout = sys.argv[2], sys.argv[3]
tab = json.load(open(os.path.join(K, "etapas/6_markups/rcp_cuartos.json")))


def hatch(doc, a, paso=9.0, ancho=0.45):
    """R2 M4 (U-160 'polígono gris con hatch'): the polygon appearance = translucent grey fill (ExtGState /H of the AP, opacity
    0.25) + 45-degree grey hatch lines (opaque, 'paso' pt apart, clipped to the polygon) + dashed grey outline. The annotation
    opacity /CA goes to 1 so the hatch stays visible; the fill keeps its 25 % through /H. No /Measure is added."""
    v = [float(t) for t in doc.xref_get_key(a.xref, "Vertices")[1].strip("[]").split()]
    pts = list(zip(v[0::2], v[1::2]))
    ap = doc.xref_get_key(a.xref, "AP/N")
    if ap[0] != "xref":
        raise SystemExit("EXCLUDED polygon without /AP /N")
    apx = int(ap[1].split()[0])
    path = f"{pts[0][0]:.2f} {pts[0][1]:.2f} m " + " ".join(f"{x:.2f} {y:.2f} l" for x, y in pts[1:]) + " h"
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    lin, k = [], (x0 - (y1 - y0))
    while k < x1:                                           # lines x - y = const, crossing the bbox
        lin.append(f"{k:.2f} {y0:.2f} m {k + (y1 - y0):.2f} {y1:.2f} l")
        k += paso * 1.41421356
    s = (f"q /H gs .45 .45 .45 rg {path} f Q\n"
         f"q {path} W n .45 .45 .45 RG {ancho} w 0 J\n" + "\n".join(lin) + " S Q\n"
         f"q [3 3] 0 d 1 w .45 .45 .45 RG {path} S Q\n")
    doc.update_stream(apx, s.encode())
    doc.xref_set_key(a.xref, "CA", "1")


doc = fitz.open(pin)
pag ={(p.get_label() or "").strip(): p for p in doc}
hechos, faltan = [], []
for r in MR.exclusiones(tab):
    p = pag.get(str(r.get("draw_sheet") or r["sheet"]))
    if p is None:
        faltan.append(f"{r['sheet']} {r['room']}: no page labelled {r['sheet']}")
        continue
    M, Rm = p.derotation_matrix, p.rotation_matrix
    poly = r["polygon"]                                    # visible frame
    t = MR.texto(r)
    a = p.add_polygon_annot([fitz.Point(x, y) * M for x, y in poly])
    a.set_colors(stroke=MR.GRIS, fill=MR.GRIS)
    a.set_opacity(0.25)
    a.set_border(width=1.0, dashes=[3, 3])
    a.set_info(title="Take-off excluded", subject=MR.SUBJ, content=t)
    a.update()
    key = f"EXCL-{r['sheet']}-{str(r['room']).replace(' ', '_')}"           # U-167: unique /NM without '/'
    mb._nm(doc, a, key + "-outline")
    hatch(doc, a)
    blk = []
    for b in p.get_text("blocks"):
        if str(b[4]).strip():
            q = fitz.Rect(b[:4]) * Rm
            q.normalize()
            blk.append(tuple(q))
    x0, y0, x1, y1 = MR.caja_interior(poly, evitar=blk)
    fs, tt = MR._ajustar(t, x1 - x0, y1 - y0)
    if fs is None:
        faltan.append(f"{r['sheet']} {r['room']}: text does not fit inside the room at 1.6 pt")
        continue
    alto = len(tt.split("\n")) * fs * 1.22 + 2
    cy = (y0 + y1) / 2
    rv = fitz.Rect(x0, cy - alto / 2, x1, cy + alto / 2)
    fr = MR.frac_dentro(tuple(rv), poly)
    if fr < 0.9:
        faltan.append(f"{r['sheet']} {r['room']}: only {fr:.0%} of the text inside the room")
        continue
    ru = rv * M
    ru.normalize()
    a = p.add_freetext_annot(ru, tt, fontsize=fs, text_color=MR.ROJO, fill_color=None, align=1, rotate=p.rotation)
    a.set_border(width=0)
    a.set_info(title="Take-off excluded", subject=MR.SUBJ, content=t)
    a.update()
    mb._nm(doc, a, key + "-text")
    for k in ("CL", "LE", "IT"):
        if doc.xref_get_key(a.xref, k)[0] != "null":
            doc.xref_set_key(a.xref, k, "null")
    r["text_rect_visible"] = [round(v, 2) for v in rv]
    r["text_fontsize"] = fs
    hechos.append(f"{r['sheet']} {r['name']} {r['room']}")
labels = {i + 1: doc[i].get_label() for i in range(doc.page_count)}
mb.nm_unicos(doc, pref="EXCL")
tmp = tempfile.mktemp(suffix=".pdf", dir=os.path.dirname(os.path.abspath(pout)))
doc.save(tmp, garbage=3, deflate=True)
doc.close()
os.replace(tmp, pout)
mb.editable(pout, {k: v for k, v in labels.items() if v})          # page labels + /VP scale kept on the final PDF
# re-check in PDF space exactly as the delivery gate does (annot rect vs polygon vertices)
d = fitz.open(pout)
for r in MR.exclusiones(tab):
    p = next(pp for pp in d if (pp.get_label() or "").strip() == r["sheet"])
    t = MR.texto(r)
    bb = fitz.Rect(fitz.Point(*r["polygon"][0]) * p.derotation_matrix, fitz.Point(*r["polygon"][2]) * p.derotation_matrix)
    bb.normalize()
    pol = [a for a in p.annots() or [] if a.info.get("subject") == MR.SUBJ and a.type[1] == "Polygon" and a.info.get("content") == t
           and abs(min(q[0] for q in a.vertices) - bb.x0) < 0.5 and abs(min(q[1] for q in a.vertices) - bb.y0) < 0.5]
    ft = [a for a in p.annots() or [] if a.info.get("subject") == MR.SUBJ and a.type[1] == "FreeText" and a.info.get("content") == t]
    if len(pol) != 1 or not ft:
        faltan.append(f"{r['sheet']} {r['room']}: polygon / FreeText missing in the saved PDF")
        continue
    fr = max(MR.frac_dentro(tuple(f_.rect), [[q[0], q[1]] for q in pol[0].vertices]) for f_ in ft)
    r["text_inside_pdf_space"] = round(fr, 3)
    if fr < 0.9:
        faltan.append(f"{r['sheet']} {r['room']}: {fr:.0%} of the text inside (PDF space)")
json.dump(tab, open(os.path.join(K, "etapas/6_markups/rcp_cuartos.json"), "w"), indent=1, ensure_ascii=False)
mal = mb.nm_fallas(pout)
print(len(hechos), "EXCLUDED rooms:", "; ".join(hechos), "| /NM failures:", len(mal), "| missing:", faltan)
sys.exit(1 if faltan or mal else 0)
