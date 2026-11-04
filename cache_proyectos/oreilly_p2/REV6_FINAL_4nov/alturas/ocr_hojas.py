#!/usr/bin/env python3
"""OCR con cajas (tesseract TSV, psm 11, 200 dpi) de las hojas de cortes que citan las alturas: A3.1 A3.2 A3.4 A4.2."""
import subprocess, sys, pymupdf
PDF = sys.argv[1]; OUT = sys.argv[2]
d = pymupdf.open(PDF)
lab = {d[i].get_label() or "": i for i in range(d.page_count)}
idx = {"A3.1": 39, "A3.2": 40, "A3.4": 42, "A4.2": 44}       # 0-based (SHEET_MAP: p.40 A3.1, p.41 A3.2, p.43 A3.4, p.45 A4.2)
for h, i in idx.items():
    png = f"{OUT}/{h}_200.png"
    d[i].get_pixmap(dpi=200, colorspace=pymupdf.csGRAY).save(png)
    subprocess.run(["tesseract", png, f"{OUT}/{h}_200", "--psm", "11", "tsv"], capture_output=True)
    print(h, "ok", flush=True)
