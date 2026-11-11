"""The markups PDF is built on the clean copy, which keeps the set's 1,589 'AutoCAD SHX Text' annotations (invisible Square
annots that carry the E / M / P drawing text; the visible glyphs are vector paths). In the MARKUPS PDF they are not our
markups: Bluebeam lists them in the Markups List with an empty Subject and they mix drawing text into the markup review.
Here they are removed from the markups PDF only (the clean bid set keeps them). No take-off markup is touched.
Use: python3 -I scripts/quitar_shx_markups.py <in.pdf> <out.pdf>"""
import sys
import pymupdf as fitz
d = fitz.open(sys.argv[1]); n = 0
for p in d:
    for a in list(p.annots() or []):
        if (a.info.get('title') or '').strip() == 'AutoCAD SHX Text':
            p.delete_annot(a); n += 1
d.save(sys.argv[2], garbage=3, deflate=True)
print('SHX drawing-text annotations removed from the markups PDF:', n)
