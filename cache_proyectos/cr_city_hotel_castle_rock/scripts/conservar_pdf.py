"""rev20a (COORDINACIÓN 12-nov: 'El PDF de markups (fe550b85…) NO cambia: el usuario está por exportar su CSV'). Paso de la cadena (no
edición a mano): el PDF de markups que deja armar_entrega se compara con el PDF ya entregado y validado (compuerta #4 de rev20, en la bitácora);
si TODAS las anotaciones (página, tipo, Subject, Contents, Title, rect redondeado a 0.1 pt, colores) y el texto / dibujo de las páginas son
iguales, se conservan los bytes del entregado (mismo sha256). Si hay UNA diferencia: FALLA y no copia nada (la diferencia se reporta).
Uso: conservar_pdf.py <pdf_entregado> <pdf_nuevo_en_la_entrega>"""
import hashlib
import shutil
import sys

import pymupdf as fitz

A, B = sys.argv[1], sys.argv[2]


def firma(p):
    d = fitz.open(p)
    out = []
    for i, pg in enumerate(d):
        for a in pg.annots() or []:
            inf = a.info
            r = a.rect
            out.append((i, a.type[1], inf.get('subject'), inf.get('content'), inf.get('title'),
                        tuple(round(v, 1) for v in (r.x0, r.y0, r.x1, r.y1)), str(a.colors)))
        out.append((i, 'TEXT', hashlib.sha256(pg.get_text('text').encode()).hexdigest()))
        out.append((i, 'DRAW', len(pg.get_drawings())))
    return d.page_count, out


fa, fb = firma(A), firma(B)
if fa != fb:
    na, nb = set(fa[1]), set(fb[1])
    print(f"CONSERVAR_PDF FALLA: páginas {fa[0]} vs {fb[0]}; solo en el entregado {len(na - nb)}, solo en el nuevo {len(nb - na)}")
    for x in list(na - nb)[:5] + list(nb - na)[:5]:
        print("   ", str(x)[:200])
    sys.exit(1)
shutil.copyfile(A, B)
print(f"CONSERVAR_PDF OK: {len(fa[1])} elementos iguales; se conserva el entregado sha256 {hashlib.sha256(open(B, 'rb').read()).hexdigest()[:16]}")
