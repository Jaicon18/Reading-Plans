"""Grand Kia: back-check report = the U-168 independent review (A1-A5, separate readers, before delivery) and how each finding was
closed (FIX_A4 / FIX_RCP integrated by program in build_canon / misc_gen / rcp_polys). Annotated with bitacora.py backcheck."""
import os, re
W = '/root/gk/work/revision_independiente'
L = ["# BACK-CHECK rev1 - Grand Kia (U-168 independent review A1-A5)", "",
     "Independent readers re-measured and re-read the take-off before delivery (A1 plan re-measure, A2 heights, A3 RCP, A4 scope, A5 PDF).",
     "Every finding was closed in the canon by program (no hand edits to the Excel); the open ones are RFIs or Review Items.", ""]
for d in ('A1_A3_planta', 'A2_A3_rcp', 'A4_alcance', 'A5_pdf'):
    f = os.path.join(W, d, 'HALLAZGOS.md')
    if not os.path.isfile(f):
        continue
    t = open(f).read()
    hs = re.findall(r"(?m)^###\s+(.+)$", t)
    L += [f"## {d}: {len(hs)} findings", ""] + [f"- {h}" for h in hs] + [""]
L += ["## Integration", "", "- FIX_A4 (revision_independiente/FIX_A4/fix_items.json): trims, wall / ceiling control joints, 13 openings, deflection track, Type X, Dens.",
      "- FIX_RCP (revision_independiente/FIX_RCP/geom.json): soffit lines, exclusions on rotated sheets, missing markups.",
      "- Heights: U-175 / U-176 protocol (alturas/FINAL), 3-side comparison and extreme-height checks in the gate.", ""]
open('/root/gk/work/etapas/BACKCHECK_rev1.md', 'w').write("\n".join(L) + "\n")
print(len(L), 'lines')
