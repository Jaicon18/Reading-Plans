#!/usr/bin/env python3
"""imagenes_hojas.py: una imagen por hoja con markups (U-158: '<HOJA> - IMAGE ONLY (not editable) - walls|ceilings|walls and ceilings revN.png'),
render del PDF de markups con sus anotaciones; hoja = Page Label impreso."""
import sys, os, glob
import pymupdf
pdf, out, rev = sys.argv[1:4]
for f in glob.glob(os.path.join(out, "* - IMAGE ONLY (not editable) - *.png")):
    os.remove(f)
d = pymupdf.open(pdf)
n = 0
for p in d:
    an = list(p.annots() or [])
    if not an:
        continue
    lab = p.get_label() or f"p{p.number + 1}"
    subs = " ".join(str(a.info.get("subject", "")) + " " + str(a.info.get("content", "")) for a in an).upper()
    kind = "walls and ceilings" if "CEILING" in subs and any(k in subs for k in ("LF", "WALL")) else ("ceilings" if "CEILING" in subs else "walls")
    if lab.upper().startswith("LEGEND") or "LEGEND" in lab.upper():
        continue
    p.get_pixmap(dpi=110, annots=True).save(os.path.join(out, f"{lab} - IMAGE ONLY (not editable) - {kind} {rev}.png"))
    n += 1
print("imagenes", n)
