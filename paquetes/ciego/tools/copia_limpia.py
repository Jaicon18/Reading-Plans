#!/usr/bin/env python3
"""copia_limpia.py (v77, R76.7 e) — la copia del bid set SIN /Annots que usan TODAS las tools que leen el PDF.

Por qué: arranque.py creaba la copia limpia, pero inventario_tags.py y alcances.py leían el PDF que se les pasara
(el original con los markups de otro estimador): tags, cotas y textos de las nubes de markup entraban al inventario.
Ahora las dos llaman copia_limpia(): si el PDF ya es la copia limpia se usa; si no, se usa (o se crea) la hermana
<nombre>_SIN_MARKUPS.pdf. Mismo nombre que arranque.limpiar().

Uso: python3 copia_limpia.py plano.pdf   -> imprime la ruta de la copia limpia
"""
import os
import sys

SUFIJO = "_SIN_MARKUPS.pdf"


def copia_limpia(pdf):
    """-> (ruta_limpia, n_anotaciones_quitadas | None si ya existía)."""
    if pdf.endswith(SUFIJO):
        return pdf, None
    dst = os.path.splitext(pdf)[0] + SUFIJO
    if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(pdf):
        return dst, None
    n = 0
    try:
        import pikepdf
        doc = pikepdf.open(pdf)
        for pg in doc.pages:
            if "/Annots" in pg:
                n += len(pg["/Annots"])
                del pg["/Annots"]
        doc.save(dst)
        doc.close()
    except ImportError:
        import pymupdf
        doc = pymupdf.open(pdf)
        for pg in doc:
            for a in list(pg.annots() or []):
                pg.delete_annot(a)
                n += 1
        doc.save(dst)
        doc.close()
    return dst, n


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    r, n = copia_limpia(sys.argv[1])
    print(r if n is None else f"{r}  ({n} anotaciones quitadas)")
