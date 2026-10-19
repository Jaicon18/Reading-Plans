# -*- coding: utf-8 -*-
"""Recorte de un detalle + banda de leyenda al pie.  Una imagen por detalle de la cadena."""
import os as _os_rutas  # rutas de trabajo: TAKEOFF_WORK / TAKEOFF_OUT (antes fijas en /home/claude/boa)
_TW = _os_rutas.environ.get("TAKEOFF_WORK", "/home/claude/boa")
_TO = _os_rutas.environ.get("TAKEOFF_OUT", "/mnt/user-data/outputs")
import sys, os
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f'{_TW}')
import zoom

F = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
NEGRO = (20, 20, 20)


def hoja(pg, box, out, titulo, lineas, dpi=600, maxw=1300, marcas=()):
    """marcas: lista de (color, x0,y0,x1,y1, 'rect'|'elip')  en pt de la hoja."""
    tmp = '/tmp/_det_%s.png' % os.path.basename(out)[:-4]
    zoom.zoom(pg, box[0], box[1], box[2], box[3], tmp, dpi=dpi, maxw=maxw)
    im = Image.open(tmp).convert('RGB')
    sx = im.width / (box[2] - box[0]); sy = im.height / (box[3] - box[1])
    X = lambda p: (p - box[0]) * sx
    Y = lambda p: (p - box[1]) * sy
    LEG = 62 + 26 * len(lineas)
    o = Image.new('RGB', (im.width, im.height + LEG), 'white')
    o.paste(im, (0, 0))
    d = ImageDraw.Draw(o)
    for col, a, b, c, e, k in marcas:
        f = d.ellipse if k == 'elip' else d.rectangle
        f([X(a), Y(b), X(c), Y(e)], outline=col, width=5)
    d.line([(0, im.height + 2), (o.width, im.height + 2)], fill=NEGRO, width=3)
    d.text((16, im.height + 14), titulo, fill=NEGRO, font=ImageFont.truetype(F, 21))
    f16 = ImageFont.truetype(FR, 17)
    y = im.height + 46
    for col, t in lineas:
        d.text((22, y), t, fill=col, font=f16); y += 26
    os.makedirs(os.path.dirname(out), exist_ok=True)
    o.save(out)
    os.remove(tmp)
    print('%s  %s' % (out, o.size))
    return out
