# -*- coding: utf-8 -*-
"""ver_detalle.py -- recorta UN detalle del set para poder leerlo.

El dibujo de un detalle vive ARRIBA de su burbuja de rotulo. Se recorta desde la burbuja
hacia arriba y hacia los lados, con margen, y a 200 dpi para que el texto chico se lea.
"""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (antes fijas en /home/claude/boa)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", "/home/claude/boa")
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import os, sys, re, subprocess
from PIL import Image

NUM = re.compile(r'^\d{1,2}$')
PDF = f'{_TW}/BOA_SIN_MARKUPS.pdf'


def burbuja(idx, rot, n):
    import pdfplumber, warnings
    warnings.filterwarnings('ignore')
    with pdfplumber.open(PDF) as pdf:
        ws = pdf.pages[idx].extract_words() or []
    for h in [w for w in ws if w['text'].strip() == rot]:
        for x in [w for w in ws if w['text'].strip() == str(n)]:
            dy = h['top'] - x['top']
            dx = abs((h['x0'] + h['x1']) / 2 - (x['x0'] + x['x1']) / 2)
            if 4 < dy < 30 and dx < 22:
                return x['x0'], x['top']
    return None


def recorta(idx, rot, n, out=None, ancho=760, alto=640, dpi=200):
    pos = burbuja(idx, rot, n)
    if not pos:
        print('no encontre la burbuja %s/%s en la pagina %d' % (n, rot, idx)); return None
    x, y = pos
    png = '/tmp/claude-0/pg%d' % idx
    if not os.path.exists(png + '-%d.png' % (idx + 1)):
        subprocess.run(['pdftoppm', '-f', str(idx + 1), '-l', str(idx + 1), '-r', str(dpi),
                        '-png', PDF, png], capture_output=True)
    im = Image.open(png + '-%d.png' % (idx + 1))
    k = im.size[0] / 3024.0
    caja = (max(0, int((x - 60) * k)), max(0, int((y - alto) * k)),
            min(im.size[0], int((x + ancho) * k)), min(im.size[1], int((y + 34) * k)))
    c = im.crop(caja)
    c = c.resize((1400, max(1, int(c.height * 1400 / c.width))))
    out = out or '/tmp/claude-0/det_%s_%s.png' % (rot.replace('.', ''), n)
    c.save(out)
    print(out, c.size)
    return out


if __name__ == '__main__':
    recorta(int(sys.argv[1]), sys.argv[2], int(sys.argv[3]))
