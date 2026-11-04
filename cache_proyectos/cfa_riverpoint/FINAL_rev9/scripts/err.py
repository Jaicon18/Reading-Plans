import sys, pymupdf
pymupdf.TOOLS.mupdf_display_errors(False)
for f in sys.argv[1:]:
    d = pymupdf.open(f); out = {}
    for i, p in enumerate(d):
        pymupdf.TOOLS.reset_mupdf_warnings()
        p.get_pixmap(dpi=10, annots=False); p.get_text()
        w = pymupdf.TOOLS.mupdf_warnings()
        if "XObject" in w:
            out[i + 1] = sorted(set(x.split("'")[1] for x in w.splitlines() if "XObject resource" in x))
    print(f.split("/")[-1], {k: (len(v), v[:3]) for k, v in out.items()})
