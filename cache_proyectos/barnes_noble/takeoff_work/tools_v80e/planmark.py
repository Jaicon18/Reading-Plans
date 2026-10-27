"""planmark.py — v73: marcado verificado sobre la hoja (contrato en referencias/herramientas.md).

Por qué viaja: bitacora.py exige `usa:planmark` y el zip v72b no lo traía; la prueba 21B lo reconstruyó desde el
contrato fuera de tools/ (P03). Esta es esa reconstrucción, con `sheet()` y tests sintéticos (test_planmark.py).

Contrato: factor pt->px DERIVADO (dpi/72) y VERIFICADO contra el PNG real (ScaleError); cache de render con la
identidad del PDF (sha256 path+mtime+size); ink() en espacio píxel, ventana ~14 pt, 7 sondas 0.08..0.92 por tramo;
verify() falla todo item con tinta < 0.04 (>= 30 % = "factor de escala mal"); overview() / sheet() NO escriben nada
si verify falla. Coordenadas en pt de la página ROTADA (como se ve), las mismas del canon (`band`).
Items: {id, band {ori H|V|D|BOX, ...}, lf, tagged}.
"""
import hashlib, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pymupdf as fitz
from PIL import Image, ImageDraw, ImageFont

CACHE = os.environ.get('PLANMARK_CACHE', os.path.join(tempfile.gettempdir(), 'planmark_cache'))
TINTA_MIN, OSCURO, VENTANA_PT, SONDAS = 0.04, 160, 14.0, (0.08, 0.22, 0.36, 0.5, 0.64, 0.78, 0.92)


class ScaleError(Exception):
    pass


class MarcaRechazada(Exception):
    pass


def _id_pdf(path):
    st = os.stat(path)
    return hashlib.sha256(f"{os.path.abspath(path)}|{st.st_mtime}|{st.st_size}".encode()).hexdigest()[:16]


class Hoja:
    def __init__(self, pdf, page1, dpi=150, w_pt=None, h_pt=None):
        os.makedirs(CACHE, exist_ok=True)
        self.pdf, self.page1, self.dpi = pdf, page1, dpi
        self.F = dpi / 72.0
        p = fitz.open(pdf)[page1 - 1]
        self.w_pt = w_pt if w_pt is not None else p.rect.width       # rect = página ROTADA (como se ve)
        self.h_pt = h_pt if h_pt is not None else p.rect.height
        self.png = os.path.join(CACHE, f"{_id_pdf(pdf)}_p{page1}_{dpi}.png")
        if not os.path.exists(self.png):
            p.get_pixmap(matrix=fitz.Matrix(self.F, self.F)).save(self.png)
        self.img = Image.open(self.png).convert('L')
        fx, fy = self.img.size[0] / self.w_pt, self.img.size[1] / self.h_pt
        if abs(fx - self.F) > 0.01 or abs(fy - self.F) > 0.01:
            raise ScaleError(f"factor pt->px {round(fx,4)} x {round(fy,4)} != dpi/72 {round(self.F,4)} (¿página sin rotar?)")

    def ink(self, x, y):
        r = VENTANA_PT / 2 * self.F
        cx, cy = x * self.F, y * self.F
        box = (int(max(0, cx - r)), int(max(0, cy - r)), int(min(self.img.size[0], cx + r)), int(min(self.img.size[1], cy + r)))
        if box[2] <= box[0] or box[3] <= box[1]:
            return 0.0
        px = list(self.img.crop(box).getdata())
        return sum(1 for v in px if v < OSCURO) / len(px)

    def sondas(self, it):
        b = it['band']
        # v80 (R80.9): un wall grueso dibujado con dos líneas y núcleo blanco (parapet) no tiene tinta en el eje: se
        # sondea también cada cara (c0, c1) y vale si las DOS caras tienen tinta en la misma sonda.
        if b['ori'] in ('H', 'V'):
            eje = (b['c0'] + b['c1']) / 2
            def p(t, c):
                u = b['lo'] + t * (b['hi'] - b['lo'])
                return (u, c) if b['ori'] == 'H' else (c, u)
            best = 0.0
            for t in SONDAS:
                best = max(best, self.ink(*p(t, eje)), min(self.ink(*p(t, b['c0'])), self.ink(*p(t, b['c1']))))
            return best
        elif b['ori'] == 'D':
            (x0, y0), (x1, y1) = b['p0'], b['p1']
            pts = [(x0 + t * (x1 - x0), y0 + t * (y1 - y0)) for t in SONDAS]
        else:  # BOX: perímetro
            x0, y0, x1, y1 = b['x0'], b['y0'], b['x1'], b['y1']
            pts = [(x0, (y0 + y1) / 2), (x1, (y0 + y1) / 2), ((x0 + x1) / 2, y0), ((x0 + x1) / 2, y1)]
        return max(self.ink(x, y) for x, y in pts)

    def verify(self, items):
        res = [(it['id'], round(self.sondas(it), 3)) for it in items]
        malos = [r for r in res if r[1] < TINTA_MIN]
        if malos:
            diag = "factor de escala mal" if len(malos) >= 0.3 * len(res) else "tags puntuales sobre vacío"
            raise MarcaRechazada(f"{diag}: {len(malos)}/{len(res)} marcas sobre papel en blanco: {malos[:10]}")
        return res

    def _rect(self, it):
        b = it['band']
        if b['ori'] == 'H':
            return (b['lo'], b['c0'], b['hi'], b['c1'])
        if b['ori'] == 'V':
            return (b['c0'], b['lo'], b['c1'], b['hi'])
        if b['ori'] == 'D':
            (x0, y0), (x1, y1) = b['p0'], b['p1']
            return (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))
        return (b['x0'], b['y0'], b['x1'], b['y1'])

    def overview(self, items, titulo, out, leyenda=()):
        """Hoja COMPLETA, un solo type, rectángulo sobre la extensión real + etiqueta (id + LF); azul con tag, rojo
        sin tag. No escribe nada si verify falla."""
        res = self.verify(items)
        im = Image.open(self.png).convert('RGB')
        dr = ImageDraw.Draw(im)
        try:
            fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', int(9 * self.F))
            fT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', int(22 * self.F))
        except OSError:
            fnt = fT = ImageFont.load_default()
        import etiquetas   # v80f (R80e.21): etiquetas sin solapes, con leader line y fondo blanco
        labs, segs = [], []
        for it in items:
            col = (0, 70, 255) if it.get('tagged') else (230, 0, 0)
            x0, y0, x1, y1 = [v * self.F for v in self._rect(it)]
            pad = 3 * self.F
            dr.rectangle([x0 - pad, y0 - pad, x1 + pad, y1 + pad], outline=col, width=max(3, int(1.6 * self.F)))
            r = (x0 - pad, y0 - pad, x1 + pad, y1 + pad)
            own = [((r[0], r[1]), (r[2], r[1])), ((r[2], r[1]), (r[2], r[3])), ((r[2], r[3]), (r[0], r[3])),
                   ((r[0], r[3]), (r[0], r[1]))]
            segs += own
            labs.append({'text': f"{it['id']}  {it['lf']:.2f} LF", 'anchor': ((x0 + x1) / 2, (y0 + y1) / 2),
                         'color': col, 'own': own})
        etiquetas.colocar(dr, labs, fnt, im.size, obstaculos=segs, ancho_linea=max(2, int(self.F)))
        dr.rectangle([20, 20, 20 + 1700 * self.F / 2.083, 20 + 70 * self.F], fill=(255, 255, 255), outline=(0, 0, 0), width=3)
        dr.text((30, 26), titulo, fill=(0, 0, 0), font=fT)
        y = 26 + 30 * self.F
        for t in leyenda:
            dr.text((30, y), t, fill=(0, 0, 0), font=fnt); y += 12 * self.F
        im.save(out, quality=82)
        return {'out': out, 'tinta': res}

    def sheet(self, items, out, cols=4, pad_pt=36.0):
        """Contact sheet de recortes: un recorte por item (banda + pad_pt), rectángulo rojo / azul, 'id LF' debajo.
        No escribe nada si verify falla."""
        res = self.verify(items)
        im = Image.open(self.png).convert('RGB')
        tiles = []
        for it in items:
            x0, y0, x1, y1 = self._rect(it)
            box = [int(max(0, (x0 - pad_pt) * self.F)), int(max(0, (y0 - pad_pt) * self.F)),
                   int(min(im.size[0], (x1 + pad_pt) * self.F)), int(min(im.size[1], (y1 + pad_pt) * self.F))]
            t = im.crop(box).copy()
            dr = ImageDraw.Draw(t)
            col = (0, 70, 255) if it.get('tagged') else (230, 0, 0)
            dr.rectangle([x0 * self.F - box[0], y0 * self.F - box[1], x1 * self.F - box[0], y1 * self.F - box[1]],
                         outline=col, width=max(2, int(self.F)))
            tiles.append((t, f"{it['id']}  {it.get('lf', 0):.2f} LF"))
        w = max(t.size[0] for t, _ in tiles)
        h = max(t.size[1] for t, _ in tiles) + 18
        rows = (len(tiles) + cols - 1) // cols
        hoja = Image.new('RGB', (w * min(cols, len(tiles)), h * rows), (255, 255, 255))
        dr = ImageDraw.Draw(hoja)
        for k, (t, lab) in enumerate(tiles):
            cx, cy = (k % cols) * w, (k // cols) * h
            hoja.paste(t, (cx, cy))
            dr.text((cx + 4, cy + t.size[1] + 2), lab, fill=(0, 0, 0))
        hoja.save(out, quality=85)
        return {'out': out, 'tinta': res}
